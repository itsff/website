# filipfracz.net

Personal landing page. Plain static HTML/CSS + a touch of JS — **no build step**.
GitHub Pages serves the files as-is (the `.nojekyll` file disables Jekyll), with the
custom domain in `CNAME`.

## Files

| Path              | What it is                                              |
|-------------------|---------------------------------------------------------|
| `index.html`      | Landing page (profile + keycap links).                  |
| `projects.html`   | Projects list.                                          |
| `music.html`      | Music page — renders itself from `js/songs.js`.         |
| `css/style.css`   | The one and only stylesheet for every page.             |
| `js/songs.js`     | **Your song list.** The only file you edit for music.   |
| `js/music.js`     | Renders the song cards. You don't need to touch this.   |
| `music/audio/`    | Put your `.mp3` files here.                              |
| `images/`         | `cover.jpg` (hero), `profile.jpg`, favicons, song covers.|

## Music: sync from Suno (automatic)

The music page is driven by `js/songs.js`, which is **generated** from your Suno
"Best Of" playlist. To pull in new songs, just run:

```bash
python3 tools/sync-suno.py
```

It downloads any new mp3s (`music/audio/`) and cover art (`images/song-covers/`),
skips everything already downloaded, and rewrites `js/songs.js` in playlist order
with titles, dates, cover art, Suno links, and lyrics.

To sync a **different** playlist instead, pass its URL:
`python3 tools/sync-suno.py https://suno.com/playlist/<id>`
(or change `DEFAULT_PLAYLIST` at the top of the script).

**Write-ups:** add your note about a track in that song's `blurb` field in
`js/songs.js`. Blurbs are **preserved** every time you re-sync, so they won't be
overwritten. (Requires Python 3 — standard library only, no install.)

## Common edits

**Add a project** — copy an `<article class="project">` block in `projects.html`.

**Change your photo** — replace `images/profile.jpg` (square image works best).

## Preview locally

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploy

Push to `master`. GitHub Pages publishes automatically to https://filipfracz.net/.
