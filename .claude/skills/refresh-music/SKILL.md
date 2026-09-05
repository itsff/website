---
name: refresh-music
description: Sync filipfracz.net's music page from Suno; avoids known pitfalls.
version: 1.0.0
author: Filip Fracz, Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [suno, music, sync, website, ffmpeg]
    related_skills: []
---

# Refresh Music Skill

Regenerates `js/songs.js` and downloads new tracks' mp3/cover art from
Filip's Suno "Best Of" playlist via `tools/sync-suno.py`. This skill exists
because the naive approach — running the script with plain `curl`/stdlib
`urllib` — silently produces broken, unplayable audio files that still look
fine (correct size, correct extension) until a listener actually hits play.

## When to Use

- User asks to "refresh the music page", "sync new songs from Suno", or
  add specific new tracks to the site.
- A visitor reports a song won't play — check the pitfalls below before
  assuming it's a front-end bug.
- Don't use for: editing blurbs/credits by hand in `js/songs.js` (that's a
  direct edit, not a sync) — see README.md's "Write-ups" section instead.

## Prerequisites

- Python 3, standard library only (no pip installs needed) for the script itself.
- `ffmpeg`/`ffprobe` on PATH — needed for the audio-recovery fallback below.
- A real browser session (this repo's agent has one via `browser_exec` /
  `browser-harness`) — needed because Suno's playlist page is Cloudflare-
  protected and returns no data to plain HTTP clients.

## Procedure

1. **Run the script first, plainly:**
   `terminal(command="python3 tools/sync-suno.py", workdir="<repo>")`
   If it prints `Could not find playlist data on the page. Is the playlist
   public?` — Cloudflare blocked the plain request. Go to step 2.

2. **Fetch playlist + song data through a real browser instead of curl.**
   Launch/attach headless Chromium with a **persistent, recognized profile
   directory** (`~/.config/chromium`, `~/.config/google-chrome`, etc — NOT
   an arbitrary `/tmp` dir), because `browser-harness`'s auto-discovery only
   scans the standard profile paths:
   ```
   terminal(command="chromium --headless=new --remote-debugging-port=9222 --no-sandbox --disable-gpu --user-data-dir=$HOME/.config/chromium", background=true)
   ```
   Wait for `curl -s http://localhost:9222/json/version` to respond, then
   `new_tab("https://suno.com/playlist/<id>")` and `new_tab("https://suno.com/song/<id>")`
   for each track. Read `document.scripts` for `self.__next_f.push(...)`
   chunks — that's the Next.js RSC payload containing the song JSON
   (`title`, `id`, `audio_url`, `image_large_url`, `caption`, `metadata.prompt`
   for lyrics). Same parsing logic as `parse_rows`/`fetch_playlist` in
   `tools/sync-suno.py`, just fed browser-rendered HTML instead of a raw fetch.

3. **Never trust the clip's `audio_url` field as-is.** It is frequently a
   dead placeholder: `https://studio-api.prod.suno.com/api/forbidden`.
   Prefer `media_urls[0].url` (a CloudFront-hosted `.m4a` link) as the
   download source in `sync-suno.py`'s `fetch_playlist()` — this repo's
   script already does this; if you're re-implementing the fetch manually,
   replicate it.

4. **Even the CloudFront `.m4a` link can return corrupted bytes** when
   fetched with a bare `curl`/`urllib` request lacking real session context
   (looked like valid HTTP 200 + correct Content-Length, but the payload
   doesn't parse as *any* known audio container — `ffprobe` reports
   "Header missing" / "moov atom not found"). If this happens:
   - Download the song's **video export** instead — `https://cdn1.suno.ai/<id>.mp4`
     — which plain `curl` CAN fetch correctly (confirmed empirically; unclear
     why the audio-only CDN path is flakier than the video one).
   - Extract just the audio track with ffmpeg, discarding video:
     `ffmpeg -y -i <id>.mp4 -vn -acodec libmp3lame -ab 192k <slug>.mp3`
   - This produces a real, valid MP3 that browsers can stream.

5. **Verify every downloaded/converted file before committing:**
   `ffprobe -hide_banner -v error -show_entries format=duration -of default=noprint_wrappers=1 <file>.mp3`
   A missing/absent duration means the file is corrupt — do not commit it.
   `file <file>.mp3` should say "Audio file with ID3 ... MPEG ADTS, layer III"
   — "data" as the file type means it's not actually an MP3.

6. **Update `js/songs.js`** — either let `sync-suno.py` regenerate it (fixes
   the `audio_url` fallback and preserves `blurb`/`credit` automatically), or
   hand-splice new entries in playlist order if you fetched data manually per
   step 2. Re-validate the file parses:
   ```
   python3 -c "import re,json; t=open('js/songs.js',encoding='utf-8').read(); m=re.search(r'const\s+SONGS\s*=\s*(\[.*\])\s*;', t, re.S); print(len(json.loads(m.group(1))), 'songs OK')"
   ```

7. **Sanity-check the live page before calling it done.** Serve locally
   (`python3 -m http.server`) or hit the deployed URL directly. Local
   `http.server` does NOT support HTTP range requests, so `<audio>` elements
   may appear stuck (`readyState=0`) even with a perfectly valid file — don't
   mistake that test-server limitation for a broken mp3. Confirm the file
   itself is valid with `ffprobe` (step 5); confirm production separately
   with a fresh `curl` (avoid re-using a locally cached copy of the same URL
   in `/tmp`, which will make a fixed file look unfixed).

8. **Commit + push to `master`.** GitHub Pages redeploys automatically.
   `git push` output showing the new commit hash is your deploy confirmation
   — there's no separate CI to wait on.

## Pitfalls

- **Cloudflare blocks plain HTTP fetches of `suno.com` pages** (`curl`,
  `urllib`, `requests` all get an empty/placeholder response) — always
  route playlist/song page reads through a real browser session.
- **`browser-harness` won't attach to a Chrome running with a `--user-data-dir`
  outside its scanned profile list** (`~/.config/chromium`, `~/.config/google-chrome`,
  etc. — see the harness's `_LINUX_PROFILES` list). Launching headless Chrome
  in `/tmp/whatever` silently fails to connect with `chrome-not-running`,
  which is misleading — Chrome IS running, it's just in an unrecognized dir.
- **`audio_url` on a Suno clip is not reliable** — always prefer `media_urls[0].url`.
- **A 200 response with the right Content-Length does not mean the audio is valid.**
  Corrupted CDN responses can pass every HTTP-level check and still be unplayable.
  `ffprobe` is the only trustworthy verification.
- **Filenames with non-ASCII characters slugify unpredictably** — `slugify()`
  in `sync-suno.py` transliterates Polish diacritics but drops other accents
  entirely (e.g. "Hé Samantha" → `h-samantha`, not `he-samantha`). Check the
  actual slug the script/you produced rather than guessing it from the title.
- **Local `python3 -m http.server` doesn't support range requests** — don't
  diagnose "song won't play" issues against it; test against the deployed
  GitHub Pages URL, or use a range-capable local server.

## Verification

- [ ] Every new/changed audio file passes `ffprobe` with a real, non-zero duration.
- [ ] `file <name>.mp3` reports it as an actual MPEG audio file, not `data`.
- [ ] `js/songs.js` parses as valid JSON after the `const SONGS = ` prefix.
- [ ] Song count in `js/songs.js` matches the playlist's track count.
- [ ] Fetched the live (not locally cached) production URL to confirm the
      fix is actually deployed, not just present in the git history.
