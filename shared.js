/* ============================================
   CREAM PAPER — shared runtime
   Loaded by both homepage and project pages.
   Owns: cream-tuned particles, cream page-transition
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

// Particles.js — cream paper config (dark dots low-opacity on cream).
// Deferred to idle so initial paint isn't fighting the canvas tick.
function initParticles() {
    if (typeof particlesJS !== 'function') {
        setTimeout(initParticles, 100);
        return;
    }
    particlesJS('particles-js', {
        particles: {
            number: { value: 70, density: { enable: true, value_area: 900 } },
            color: { value: '#1d1a16' },
            shape: { type: 'circle' },
            opacity: {
                value: 0.22,
                random: true,
                anim: { enable: true, speed: 0.6, opacity_min: 0.08, sync: false }
            },
            size: {
                value: 2.2,
                random: true,
                anim: { enable: true, speed: 1.2, size_min: 0.6, sync: false }
            },
            line_linked: {
                enable: true,
                distance: 150,
                color: '#1d1a16',
                opacity: 0.12,
                width: 1
            },
            move: {
                enable: true,
                speed: 0.6,
                direction: 'none',
                random: true,
                straight: false,
                out_mode: 'out'
            }
        },
        interactivity: {
            detect_on: 'canvas',
            events: {
                onhover: { enable: true, mode: 'grab' },
                onclick: { enable: false },
                resize: true
            },
            modes: {
                grab: { distance: 140, line_linked: { opacity: 0.25 } }
            }
        },
        retina_detect: true
    });
}

if ('requestIdleCallback' in window) {
    requestIdleCallback(initParticles, { timeout: 2000 });
} else {
    setTimeout(initParticles, 200);
}
