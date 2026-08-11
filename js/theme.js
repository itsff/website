/* Theme toggle: flip light/dark and remember the choice.
   The initial theme is set by a tiny inline script in each page's <head>
   (before paint) so there's no flash; this file only handles interaction. */
(function () {
  "use strict";
  var root = document.documentElement;

  function apply(theme) {
    root.dataset.theme = theme;
    try { localStorage.setItem("theme", theme); } catch (e) {}
  }

  document.addEventListener("click", function (e) {
    var btn = e.target.closest && e.target.closest(".theme-toggle");
    if (!btn) return;
    apply(root.dataset.theme === "light" ? "dark" : "light");
  });

  // Keep the copyright year current without any manual edits.
  var year = String(new Date().getFullYear());
  var yearEls = document.querySelectorAll(".year");
  for (var i = 0; i < yearEls.length; i++) yearEls[i].textContent = year;

  // If the user hasn't made an explicit choice, keep following the OS setting.
  try {
    window.matchMedia("(prefers-color-scheme: light)").addEventListener("change", function (ev) {
      if (!localStorage.getItem("theme")) {
        root.dataset.theme = ev.matches ? "light" : "dark";
      }
    });
  } catch (e) {}
})();
