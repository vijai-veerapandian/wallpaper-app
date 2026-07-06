document.addEventListener("DOMContentLoaded", () => {
  const wallpaperEl = document.getElementById("wallpaper");
  const fullscreenBtn = document.getElementById("fullscreen-btn");

  if (!wallpaperEl || !window.WALLPAPERS) return;

  let wallpapers = window.WALLPAPERS;
  let rotationSeconds = window.ROTATION_SECONDS || 15;
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
