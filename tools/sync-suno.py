#!/usr/bin/env python3
"""
Sync songs from a Suno playlist into this website.

What it does:
  * Reads a public Suno playlist (default: your "Best Of").
  * Downloads each track's cover art -> images/song-covers/<slug>.jpg
    (existing files are SKIPPED, so it is safe to run repeatedly).
  * mp3s are NOT downloadable from Suno any more: add them by hand to
    music/audio/<slug>.mp3 (the song shows without a player until you do).
  * Regenerates js/songs.js from the playlist, NEWEST FIRST,
    while PRESERVING any `blurb` (your write-up) you've added to a song.

Usage:
    python3 tools/sync-suno.py                 # sync the default playlist
    python3 tools/sync-suno.py <playlist-url>  # sync a different playlist

Requirements: Python 3 (standard library only). No build step, no pip.
"""

import hashlib
import json
import os
import re
import sys
import urllib.request

# The playlist to sync. Override by passing a playlist URL (or bare id) as arg 1.
DEFAULT_PLAYLIST = "82da2bd0-8c37-4485-b3ea-cce1e509a49f"  # "Best Of"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(ROOT, "music", "audio")
COVER_DIR = os.path.join(ROOT, "images", "song-covers")
SONGS_JS = os.path.join(ROOT, "js", "songs.js")

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"

# Transliterate Polish (and a couple of common) diacritics for tidy filenames.
TRANSLIT = str.maketrans({
    "ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n", "ó": "o",
    "ś": "s", "ź": "z", "ż": "z",
    "Ą": "a", "Ć": "c", "Ę": "e", "Ł": "l", "Ń": "n", "Ó": "o",
    "Ś": "s", "Ź": "z", "Ż": "z",
})


def slugify(title):
    t = title.strip().lower().translate(TRANSLIT)
    t = t.replace("c++", "c-plus-plus").replace("&", "and")
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t or "track"


def playlist_id_from(arg):
    m = re.search(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", arg)
    return m.group(0) if m else arg


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def fetch_playlist(pid):
    """Return (playlist_name, [song dicts]) from Suno's public playlist JSON API.

    (The playlist HTML page no longer embeds the data, so we use the API the
    web app itself calls. It needs no login for public playlists.)
    """
    name, songs, page, total = "playlist", [], 1, None
    while True:
        raw = get(f"https://studio-api.prod.suno.com/api/playlist/{pid}/?page={page}")
        obj = json.loads(raw)
        name = obj.get("name", name)
        total = obj.get("num_total_results", total)
        clips = obj.get("playlist_clips") or []
        if not clips:
            break
        for pc in clips:
            c = pc.get("clip") or {}
            md = c.get("metadata") or {}
            if not c.get("id"):
                continue
            songs.append({
                "title": (c.get("title") or "Untitled").strip(),
                "id": c.get("id"),
                "image_url": c.get("image_large_url") or c.get("image_url"),
                "created_at": c.get("created_at"),
                "lyrics": (md.get("prompt") or "").strip(),
                "description": (c.get("caption") or "").strip(),
            })
        if total is None or len(songs) >= total:
            break
        page += 1
    return name, songs


def download(url, dest):
    """Download url->dest unless it already exists. Returns 'skip' | 'ok' | 'err'."""
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return "skip"
    if not url:
        return "err"
    try:
        data = get(url)
    except Exception as e:  # noqa: BLE001
        print(f"    ! download failed: {e}")
        return "err"
    if not data:
        return "err"
    tmp = dest + ".part"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, dest)
    return "ok"


# Fields you hand-edit in songs.js that must survive a re-sync.
MANUAL_FIELDS = ("blurb", "credit", "lyrics_custom")


def load_existing():
    """Parse the current js/songs.js (valid JS: `const SONGS = [ ...json... ];`)
    into a list of song dicts, or [] if missing/unreadable."""
    if not os.path.exists(SONGS_JS):
        return []
    text = open(SONGS_JS, encoding="utf-8").read()
    m = re.search(r"const\s+SONGS\s*=\s*(\[.*\])\s*;", text, re.S)
    if not m:
        return []
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        print("  (note: couldn't parse existing songs.js; edits not preserved)")
        return []


def existing_manual(existing):
    """{song_id: {field: value}} for hand-edited fields, so write-ups and credits
    survive re-syncs."""
    return {s["id"]: {f: s[f] for f in MANUAL_FIELDS if s.get(f)}
            for s in existing if s.get("id")}


def month_year(iso):
    if not iso:
        return ""
    try:
        from datetime import datetime
        return datetime.strptime(iso[:10], "%Y-%m-%d").strftime("%b %Y")
    except ValueError:
        return ""


def write_songs_js(songs):
    header = (
        "/* ==========================================================================\n"
        "   js/songs.js  —  GENERATED by tools/sync-suno.py\n"
        "\n"
        "   Song data (titles, mp3s, covers, lyrics) is pulled from your Suno playlist.\n"
        "   Re-run the script any time to add new songs:  python3 tools/sync-suno.py\n"
        "\n"
        "   The snippet under each song is its Suno `description` (auto, refreshed every\n"
        "   sync). To override it with your own write-up, fill in that song's `blurb` —\n"
        "   a non-empty blurb always wins and is preserved across re-syncs.\n"
        "   (Keep the file valid: these are ordinary JSON strings in double quotes.)\n"
        "   ========================================================================== */\n\n"
    )
    body = json.dumps(songs, indent=2, ensure_ascii=False)
    text = header + "const SONGS = " + body + ";\n"
    with open(SONGS_JS, "w", encoding="utf-8") as f:
        f.write(text)
    stamp_page(hashlib.md5(text.encode("utf-8")).hexdigest()[:8])


def stamp_page(version):
    """Point music.html at js/songs.js?v=<hash of its content>. GitHub Pages lets
    browsers cache files for 10 minutes, so without this a visitor can keep an old
    songs.js (e.g. one with no mp3s yet) after we publish a new one."""
    page = os.path.join(ROOT, "music.html")
    html = open(page, encoding="utf-8").read()
    new = re.sub(r'/js/songs\.js(\?v=[0-9a-f]+)?"', f'/js/songs.js?v={version}"', html)
    if new != html:
        open(page, "w", encoding="utf-8").write(new)


def main():
    pid = playlist_id_from(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PLAYLIST
    os.makedirs(AUDIO_DIR, exist_ok=True)
    os.makedirs(COVER_DIR, exist_ok=True)

    print(f"Fetching playlist {pid} …")
    name, songs = fetch_playlist(pid)
    print(f'Playlist "{name}": {len(songs)} track(s)\n')

    existing = load_existing()
    manual = existing_manual(existing)
    by_id = {e["id"]: e for e in existing if e.get("id")}
    out, n_new_cover, n_no_audio = [], 0, 0

    # Newest first (by Suno creation time).
    songs.sort(key=lambda x: x.get("created_at") or "", reverse=True)

    for s in songs:
        old = by_id.get(s["id"], {})
        slug = slugify(s["title"])
        # Keep the paths the site already uses (stable deep links / filenames).
        audio_rel = old.get("audio") or f"music/audio/{slug}.mp3"
        cover_rel = old.get("cover") or f"images/song-covers/{slug}.jpg"

        # Covers are public on Suno's CDN. Audio is NOT downloadable (Suno's
        # mp3 CDN returns 403 and the m4a is encrypted), so mp3s must be added
        # by hand: drop <slug>.mp3 into music/audio/ and re-run.
        i = download(s["image_url"], os.path.join(ROOT, cover_rel))
        n_new_cover += (i == "ok")
        have_audio = os.path.exists(os.path.join(ROOT, audio_rel)) and \
            os.path.getsize(os.path.join(ROOT, audio_rel)) > 0
        if not have_audio:
            n_no_audio += 1
        flag = "· mp3 ok" if have_audio else f"· NO MP3 (add {audio_rel})"
        print(f"  {s['created_at'][:10]}  {s['title'][:46]:<46} {flag}")

        kept = manual.get(s["id"], {})
        entry = {
            "title": s["title"],
            "date": month_year(s["created_at"]),
            "created": s["created_at"],
            "cover": cover_rel if i in ("ok", "skip") else "",
            "audio": audio_rel if have_audio else "",
            "suno": f"https://suno.com/song/{s['id']}" if s["id"] else "",
            # blurb = your own write-up (manual, preserved). If empty, the music
            # page falls back to `description` (the song's Suno caption, below).
            "blurb": kept.get("blurb", ""),
        }
        if kept.get("credit"):           # keep credit right after blurb
            entry["credit"] = kept["credit"]
        entry["description"] = s.get("description", "")   # auto from Suno each sync
        # lyrics_custom (manual, preserved) replaces the lyrics Suno stores,
        # e.g. for standard spelling and only [Verse]/[Chorus] tags.
        if kept.get("lyrics_custom"):
            entry["lyrics_custom"] = kept["lyrics_custom"]
        entry["lyrics"] = kept.get("lyrics_custom") or s["lyrics"]
        entry["id"] = s["id"]
        out.append(entry)

    write_songs_js(out)
    print(f"\nDone. {n_new_cover} new cover(s); {n_no_audio} song(s) without an mp3.")
    print(f"Wrote {SONGS_JS} ({len(out)} songs).")


if __name__ == "__main__":
    main()
