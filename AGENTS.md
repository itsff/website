# Agent notes — filipfracz.net

Static site, no build step, no dependencies. GitHub Pages serves the files
as-is (`.nojekyll` disables Jekyll; `CNAME` sets the custom domain).

## Music page

The music page (`music.html` + `js/songs.js`) is generated from Filip's Suno
"Best Of" playlist by `tools/sync-suno.py`. Do not hand-edit `js/songs.js` —
re-run the script instead (see README.md, "Music: sync from Suno").

**Before touching the music sync, load the skill at
`.claude/skills/refresh-music/SKILL.md`.** It documents non-obvious failure
modes (Cloudflare blocking plain `curl`, a dead `audio_url` field, corrupted
audio from the CDN clip endpoint, and how to verify a downloaded track is
actually playable before committing it). Skipping it is how broken mp3s
ended up committed and shipped to production once already.

## General conventions

- Plain HTML/CSS + a touch of vanilla JS. No frameworks, no npm, no build.
- `js/songs.js` is generated — see above.
- `js/music.js` renders song cards from `SONGS`; you shouldn't need to touch it.
- One stylesheet: `css/style.css`.
- Push to `master` deploys directly (GitHub Pages).
