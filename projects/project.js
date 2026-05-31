/* ============================================
   CREAM PAPER — project page JS
   Owns: back-link click wiring.
   Shared runtime (particles, fade transition, bfcache)
   lives in /shared.js, loaded before this file.
   ============================================ */

const backLink = document.querySelector('.back-link');

if (backLink) {
    backLink.addEventListener('click', (e) => {
        e.preventDefault();
        window.navigateToProject(backLink.getAttribute('href'));
    });
}
