document.addEventListener("DOMContentLoaded", () => {
  const wallpaperEl = document.getElementById("wallpaper");
  const fullscreenBtn = document.getElementById("fullscreen-btn");

  if (!wallpaperEl) return;

  // Read from data attributes rather than window globals set by an inline
  // <script>, which would require 'unsafe-inline' in the CSP.
  let wallpapers = [];
  try {
    wallpapers = JSON.parse(wallpaperEl.dataset.wallpapers || "[]");
  } catch (e) {
    wallpapers = [];
  }

  let rotationSeconds = Number(wallpaperEl.dataset.rotationSeconds) || 15;
  let currentIndex = 0;

  function showWallpaper() {
    if (!wallpapers.length) return;
    wallpaperEl.style.backgroundImage = `url('/static/images/${wallpapers[currentIndex]}')`;
    currentIndex = (currentIndex + 1) % wallpapers.length;
  }

  showWallpaper();
  setInterval(showWallpaper, rotationSeconds * 1000);

  if (fullscreenBtn) {
    fullscreenBtn.addEventListener("click", () => {
      document.documentElement.requestFullscreen();
    });
  }
});
