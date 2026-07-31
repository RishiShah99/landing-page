# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Personal portfolio for Rishi Shah (Perception & ML Engineer), served from GitHub Pages at **shahrishi.com** (see `CNAME`). Pure static site — no build tools, no bundler, no package manager, no dependencies installed locally. All third-party code (particles.js, FontAwesome, Google Fonts) is pulled from CDNs at runtime.

## Local Dev & Deploy

- **Preview locally:** `python -m http.server 8000` from the repo root, then open `http://localhost:8000`. Opening `index.html` via `file://` mostly works but breaks relative paths to `projects/*.html` videos and the resume download — use the HTTP server.
- **Deploy:** push to `main`. GitHub Pages serves directly from the branch; there is no Actions workflow or build step. The `CNAME` file pins the custom domain.
- **No lint, no test, no typecheck.** Don't add tooling unless asked — the no-build constraint is intentional.

## Architecture

Two-tier static site: one homepage + N project detail pages sharing a single CSS/JS pair.

- `index.html` — landing page. Header, About, project grid (`.work-grid-2col`). Inline `<script>` block at the bottom owns: custom cursor, click-ripple, fade-overlay page transitions (`navigateToProject`), and particles.js init.
- `style.css` — homepage-only styles. Defines the "Neural Circuit Board" base: dark `#050a15` body, the `body::before` circuit-trace + neural-glow background pattern, header/about/portfolio sections, project grid, cursor styles.
- `projects/project.css` — shared stylesheet for **every** project detail page. Owns the full visual system used on project pages (back button, project-header, video-container, stats grid, tech grid, document-section typography, responsive breakpoints). Declares its own design tokens on `:root` (see below).
- `projects/project.js` — shared JS for every project detail page. Mirrors the cursor/particles setup from `index.html`, plus the back-button fade transition and scroll-hide behavior.
- `projects/*.html` — thin shells (~50 lines of boilerplate + content). Each links `project.css` + `project.js` and contains only its unique copy (title, meta, header block, overview, optional `.video-container`, `.tech-grid`, `.document-section`).
- `images/` — thumbnails (`project-1.png` … `project-9.png`), `user.jpg`, `Rishi_Shah_Resume.pdf`, and demo videos (`tool_segmentation.mp4`, `SurgicalToolAR.mp4`).

### Important: duplicated runtime logic

The custom cursor and particles.js init exist in **two places**: inline in `index.html` and in `projects/project.js`. They are intentionally separate because the configs differ (homepage uses denser particles with animated opacity/size + click ripple; project pages use a simpler config and add the back-button handler). When touching cursor or particles behavior, decide whether the change belongs on one side or both — they will drift if you only edit one.

### Page navigation

There is no router. Forward navigation: project cards in `index.html` carry `onclick="window.location.href='projects/<slug>.html'"`, which JS rewrites into a fade-overlay transition (`navigateToProject`). Back navigation: every project page has `<a class="back-button" href="../index.html">`, intercepted by `project.js` to apply the same fade overlay before navigating. If you add a new project page, the back button selector is required or `project.js` will throw.

### Cursor system

Native cursor is hidden globally via `cursor: none !important` (applied on `html`, `body`, `*`, and reasserted by inline `<style>` in each HTML head to prevent flash). Two divs (`.cursor`, `.cursor-glow`) are created in JS and follow `mousemove`. Interactive elements get a `.hover` class on mouseenter — the selector list lives in the JS file and must be updated when you introduce a new interactive element type.

## Design Tokens

Homepage uses literal hex values (`#050a15`, `#00b4d8`). Project pages use CSS variables on `:root` in `project.css`:

```
--primary: #00b4d8   /* cyan */
--secondary: #5EEAD4 /* teal */
--dark: #020510
--darker: #0a1628
--light: #e0f2fe
--accent: #38bdf8
```

The homepage's darker `#050a15` body and the project pages' `#020510` gradient are intentionally distinct — the fade-overlay transition lerps between them.

## Adding a New Project

1. Copy an existing `projects/*.html` as a template (they are interchangeable shells).
2. Update `<title>` and `<meta name="description">`.
3. Replace content inside `.container`: project-header (subtitle/title/subtitle/3 meta stats/optional `.project-link`), overview section (optionally with a `.video-container` containing `<video>` or `<iframe>`), `.tech-grid`, `.document-section`.
4. Add a thumbnail to `images/` (next sequential `project-N.png/jpg`).
5. Add a `.work` card to `.work-grid-2col` in `index.html` with `onclick="window.location.href='projects/<slug>.html'"`.

No CSS or JS edits needed — `project.css` / `project.js` cover everything.

## Analytics

Google Analytics (`gtag` with ID `G-0M7YNWC9WW`) is loaded only on `index.html`. Project pages are intentionally untracked. Don't propagate the gtag snippet to project pages without asking.
