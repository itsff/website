#!/usr/bin/env python3
"""
Sync songs from a Suno playlist into this website.

What it does:
  * Reads a public Suno playlist (default: your "Best Of").
  * Downloads each track's mp3   -> music/audio/<slug>.mp3
    and its cover art           -> images/song-covers/<slug>.jpg
    Files that already exist are SKIPPED (safe to run repeatedly).
  * Regenerates js/songs.js from the playlist, in playlist order,
    while PRESERVING any `blurb` (your write-up) you've added to a song.

Usage:
    python3 tools/sync-suno.py                 # sync the default playlist
    python3 tools/sync-suno.py <playlist-url>  # sync a different playlist

Requirements: Python 3 (standard library only). No build step, no pip.
"""

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


def parse_rows(payload):
    """Parse the React-Flight stream into {row_id: raw_value}.

    Rows are either length-delimited text — `id:T<hexlen>,<bytes>` — or a
    newline-terminated JSON value — `id:<json>`. Long strings (like lyrics) live
    in their own text row and are referenced elsewhere as "$<id>".
    """
    b = payload.encode("utf-8")
    rows, i, n = {}, 0, len(b)
    while i < n:
        j = b.find(b":", i)
        if j == -1:
            break
        rid = b[i:j].decode("latin1")
        if not re.fullmatch(r"[0-9a-f]+", rid or ""):   # not a row header; resync
            nl = b.find(b"\n", i)
            if nl == -1:
                break
            i = nl + 1
            continue
        k = j + 1
        if b[k:k + 1] == b"T":                           # length-delimited text row
            c = b.find(b",", k)
            length = int(b[k + 1:c], 16)
            s = c + 1
            rows[rid] = b[s:s + length].decode("utf-8", "replace")
            i = s + length
            if b[i:i + 1] == b"\n":
                i += 1
        else:                                            # JSON row, newline terminated
            e = b.find(b"\n", k)
            if e == -1:
                e = n
            rows[rid] = b[k:e].decode("utf-8", "replace")
            i = e + 1
    return rows


def resolve(value, rows):
    """Resolve a "$<id>" reference to its row text; pass plain strings through."""
    if isinstance(value, str) and value.startswith("$"):
        return rows.get(value[1:], "")
    return value or ""


def fetch_playlist(pid):
    """Return (playlist_name, [song dicts]) parsed from the playlist page's RSC payload."""
    html = get(f"https://suno.com/playlist/{pid}").decode("utf-8", "replace")

    # The page is a Next.js app; song data streams as self.__next_f.push([1,"...json..."]).
    # Reassemble every chunk (JSON-decoding each so escapes resolve), then brace-match
    # the playlist object out of the concatenated payload.
    chunks = re.findall(r'self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)', html)
    payload = "".join(json.loads(c) for c in chunks)
    rows = parse_rows(payload)

    start = payload.find('"playlist":{"entity_type":"playlist_schema"')
    if start == -1:
        raise SystemExit("Could not find playlist data on the page. Is the playlist public?")
    start = payload.index("{", start)
    depth = 0
    for j in range(start, len(payload)):
        ch = payload[j]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = j + 1
                break
    obj = json.loads(payload[start:end])

    songs = []
    for pc in obj.get("playlist_clips", []):
        c = pc.get("clip") or {}
        md = c.get("metadata") or {}
        if not c.get("audio_url"):
            continue
        songs.append({
            "title": (c.get("title") or "Untitled").strip(),
            "id": c.get("id"),
            # audio_url on the clip is sometimes a dead "/api/forbidden" placeholder;
            # media_urls[].url (CloudFront-hosted m4a) is the reliable download link.
            "audio_url": (c.get("media_urls") or [{}])[0].get("url") or c.get("audio_url"),
            "image_url": c.get("image_large_url") or c.get("image_url"),
            "created_at": c.get("created_at"),
            "lyrics": resolve(md.get("prompt"), rows).strip(),
            "description": resolve(c.get("caption"), rows).strip(),
        })
    return obj.get("name", "playlist"), songs


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
MANUAL_FIELDS = ("blurb", "credit")


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


def existing_audio_owner(existing):
    """{audio_path: song_id} — lets us detect when a song was replaced under the
    same title (same filename, different id) so we can refresh its stale files."""
    return {s["audio"]: s["id"] for s in existing if s.get("audio") and s.get("id")}


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
    with open(SONGS_JS, "w", encoding="utf-8") as f:
        f.write(header + "const SONGS = " + body + ";\n")


def main():
    pid = playlist_id_from(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PLAYLIST
    os.makedirs(AUDIO_DIR, exist_ok=True)
    os.makedirs(COVER_DIR, exist_ok=True)

    print(f"Fetching playlist {pid} …")
    name, songs = fetch_playlist(pid)
    print(f'Playlist "{name}": {len(songs)} track(s)\n')

    existing = load_existing()
    manual = existing_manual(existing)
    audio_owner = existing_audio_owner(existing)
    out, n_new, n_skip, n_refresh = [], 0, 0, 0

    for s in songs:
        slug = slugify(s["title"])
        audio_rel = f"music/audio/{slug}.mp3"
        cover_rel = f"images/song-covers/{slug}.jpg"

        # If this filename was previously a DIFFERENT song id, the track was
        # replaced (e.g. re-generated with new lyrics) under the same title.
        # Delete the stale mp3/cover so they get re-downloaded fresh.
        replaced = audio_owner.get(audio_rel) not in (None, s["id"])
        if replaced:
            n_refresh += 1
            for rel in (audio_rel, cover_rel):
                fp = os.path.join(ROOT, rel)
                if os.path.exists(fp):
                    os.remove(fp)

        a = download(s["audio_url"], os.path.join(ROOT, audio_rel))
        i = download(s["image_url"], os.path.join(ROOT, cover_rel))
        n_new += (a == "ok")
        n_skip += (a == "skip")
        flag = ("· refreshed" if replaced and a == "ok"
                else "· new" if a == "ok"
                else "· have" if a == "skip" else "· ERR")
        print(f"  {s['title'][:46]:<46} {flag}")

        kept = manual.get(s["id"], {})
        entry = {
            "title": s["title"],
            "date": month_year(s["created_at"]),
            "cover": cover_rel if i in ("ok", "skip") else "",
            "audio": audio_rel if a in ("ok", "skip") else "",
            "suno": f"https://suno.com/song/{s['id']}" if s["id"] else "",
            # blurb = your own write-up (manual, preserved). If empty, the music
            # page falls back to `description` (the song's Suno caption, below).
            "blurb": kept.get("blurb", ""),
        }
        if kept.get("credit"):           # keep credit right after blurb
            entry["credit"] = kept["credit"]
        entry["description"] = s.get("description", "")   # auto from Suno each sync
        entry["lyrics"] = s["lyrics"]
        entry["id"] = s["id"]
        out.append(entry)

    write_songs_js(out)
    summary = f"\nDone. {n_new} new download(s), {n_skip} already present"
    summary += f", {n_refresh} refreshed (replaced)." if n_refresh else "."
    print(summary)
    print(f"Wrote {SONGS_JS} ({len(out)} songs).")


if __name__ == "__main__":
    main()
