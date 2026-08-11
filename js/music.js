/* Renders the music page from the SONGS array in songs.js.
   You shouldn't need to touch this file — edit songs.js instead. */
(function () {
  "use strict";
  var list = document.getElementById("songs");
  if (!list) return;

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  if (typeof SONGS === "undefined" || !SONGS.length) {
    list.innerHTML = '<div class="empty">No songs published yet — check back soon.</div>';
    return;
  }

  var noteSVG =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
    '<circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/><path d="M9 18V5l12-2v13"/></svg>';

  list.innerHTML = SONGS.map(function (song) {
    var cover = song.cover
      ? '<img class="song__cover" src="' + esc(song.cover) + '" alt="' + esc(song.title) + ' cover">'
      : '<div class="song__cover placeholder" aria-hidden="true">' + noteSVG + "</div>";

    var date  = song.date  ? '<div class="song__date">' + esc(song.date) + "</div>" : "";
    // Your own write-up wins; otherwise fall back to the song's Suno description.
    var snippet = song.blurb || song.description || "";
    var blurb = snippet ? '<p class="song__blurb">' + esc(snippet) + "</p>" : "";

    var credit = "";
    if (song.credit && song.credit.length) {
      credit = '<p class="song__credit">&#8618; ' + song.credit.map(function (c) {
        return '<a href="' + esc(c.url) + '" target="_blank" rel="noopener">' + esc(c.label) + " &#8599;</a>";
      }).join(' <span class="sep">&middot;</span> ') + "</p>";
    }

    var audio = song.audio
      ? '<div class="song__audio"><audio controls preload="none" src="' + esc(song.audio) + '"></audio></div>'
      : "";

    var actions = [];
    if (song.audio) {
      actions.push('<a class="dl" href="' + esc(song.audio) + '" download>Download mp3 &#8595;</a>');
    }
    if (song.suno) {
      actions.push('<a href="' + esc(song.suno) + '" target="_blank" rel="noopener">Listen on Suno &#8599;</a>');
    }
    var ext = actions.length
      ? '<div class="song__ext">' + actions.join(' <span class="sep">&middot;</span> ') + "</div>"
      : "";

    var lyrics = song.lyrics
      ? '<details class="song__lyrics"><summary>Lyrics</summary><pre>' + esc(song.lyrics) + "</pre></details>"
      : "";

    return (
      '<article class="song">' +
        '<div class="song__head">' +
          cover +
          '<div class="song__meta">' +
            '<h2 class="song__title">' + esc(song.title) + "</h2>" +
            date +
            blurb +
            credit +
          "</div>" +
        "</div>" +
        audio +
        ext +
        lyrics +
      "</article>"
    );
  }).join("");
})();
