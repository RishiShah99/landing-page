/* ============================================
   CREAM PAPER — shared runtime
   Loaded by both homepage and project pages.
   Owns: cream page-transition
   overlay (window.navigateToProject), bfcache cleanup.
   Page-specific JS layers click handlers on top.
   ============================================ */

// Cream fade transition — both surfaces use the same overlay
window.navigateToProject = function (url) {
    const overlay = document.createElement('div');
    overlay.className = 'page-transition-overlay';
    document.body.appendChild(overlay);
    requestAnimationFrame(() => { overlay.style.opacity = '1'; });
    setTimeout(() => { window.location.href = url; }, 200);
};

// bfcache restore: kill any leftover transition overlay so the page isn't covered
window.addEventListener('pageshow', (e) => {
    if (e.persisted) {
        document.querySelectorAll('.page-transition-overlay').forEach(el => el.remove());
    }
});
window.addEventListener('pagehide', () => {
    document.querySelectorAll('.page-transition-overlay').forEach(el => { el.style.opacity = '0'; });
});

