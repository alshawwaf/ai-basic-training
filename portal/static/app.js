/* ── Theme toggle ───────────────────────────────────────────────────────── */

(function initTheme() {
    const saved = localStorage.getItem('portalTheme');
    if (saved === 'light') {
        document.documentElement.removeAttribute('data-theme');
    } else {
        document.documentElement.setAttribute('data-theme', 'dark');
    }
})();

function toggleTheme() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    if (isDark) {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('portalTheme', 'light');
    } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('portalTheme', 'dark');
    }
}

/* ── Command menu (logo click) ──────────────────────────────────────────── */

function toggleCommandMenu(e) {
    if (e) e.preventDefault();
    const menu = document.getElementById('cmdMenu');
    const overlay = document.getElementById('cmdOverlay');
    if (!menu) return;
    const opening = !menu.classList.contains('open');
    if (opening) {
        renderCommandMenu();
        // Position near click target
        if (e && e.currentTarget) {
            const rect = e.currentTarget.getBoundingClientRect();
            const isNavBrand = e.currentTarget.classList.contains('nav-brand');
            if (isNavBrand) {
                menu.style.top = '58px';
                menu.style.left = '16px';
                menu.style.right = 'auto';
            } else {
                // Position below the clicked element, centered
                const menuWidth = 320;
                let left = rect.left + rect.width / 2 - menuWidth / 2;
                left = Math.max(16, Math.min(left, window.innerWidth - menuWidth - 16));
                menu.style.top = (rect.bottom + 12) + 'px';
                menu.style.left = left + 'px';
                menu.style.right = 'auto';
            }
        }
        menu.classList.add('open');
        overlay.classList.add('open');
    } else {
        closeCommandMenu();
    }
}

function closeCommandMenu() {
    const menu = document.getElementById('cmdMenu');
    const overlay = document.getElementById('cmdOverlay');
    if (menu) menu.classList.remove('open');
    if (overlay) overlay.classList.remove('open');
    const confirm = document.getElementById('cmdConfirm');
    if (confirm) confirm.style.display = 'none';
}

/* Sidebar variant (lesson pages) */
function toggleSidebarMenu() {
    const panel = document.getElementById('cmdSidebarPanel');
    const chevron = document.getElementById('cmdChevron');
    if (!panel) return;
    const opening = !panel.classList.contains('open');
    if (opening) {
        renderCommandMenu();
        panel.classList.add('open');
        if (chevron) chevron.style.transform = 'rotate(180deg)';
    } else {
        panel.classList.remove('open');
        if (chevron) chevron.style.transform = '';
        const confirm = document.getElementById('cmdConfirm');
        if (confirm) confirm.style.display = 'none';
    }
}

function renderCommandMenu() {
    const progress = JSON.parse(localStorage.getItem('portalProgress') || '{}');
    const bookmarks = JSON.parse(localStorage.getItem('portalBookmarks') || '[]');
    const last = JSON.parse(localStorage.getItem('portalLastVisited') || 'null');

    // ── Continue section
    const contEl = document.getElementById('cmdContinue');
    if (last) {
        contEl.innerHTML = `
            <div class="cmd-label">Continue</div>
            <a class="cmd-item cmd-continue" href="/lesson/${last.lessonId}/step/${last.step}">
                <span class="cmd-icon">&#9654;</span>
                <span class="cmd-item-info">
                    <strong>${last.title}</strong>
                    <span class="cmd-sub">Step ${last.step}</span>
                </span>
            </a>`;
    } else {
        contEl.innerHTML = `
            <div class="cmd-label">Continue</div>
            <div class="cmd-empty">No steps visited yet</div>`;
    }

    // ── Bookmarks section
    const bmEl = document.getElementById('cmdBookmarks');
    if (bookmarks.length > 0) {
        const items = bookmarks.map((bm, i) => `
            <div class="cmd-item cmd-bookmark-item">
                <a href="/lesson/${bm.lessonId}/step/${bm.step}" class="cmd-bookmark-link">
                    <span class="cmd-icon">&#9733;</span>
                    <span class="cmd-item-info">
                        <strong>${bm.title}</strong>
                        <span class="cmd-sub">Step ${bm.step}</span>
                    </span>
                </a>
                <button class="cmd-remove" onclick="removeBookmark(${i})" title="Remove">&times;</button>
            </div>`).join('');
        bmEl.innerHTML = `<div class="cmd-label">Bookmarks</div>${items}`;
    } else {
        bmEl.innerHTML = `<div class="cmd-label">Bookmarks</div><div class="cmd-empty">No bookmarks saved</div>`;
    }

    // ── Show "Bookmark this step" button only on lesson step pages
    const addBmBtn = document.getElementById('cmdAddBookmark');
    if (addBmBtn) {
        const onStepPage = /\/lesson\/([^/]+)\/step\/(\d+)/.exec(window.location.pathname);
        if (onStepPage) {
            addBmBtn.style.display = '';
            // Check if already bookmarked
            const lid = onStepPage[1], sn = parseInt(onStepPage[2]);
            const exists = bookmarks.some(b => b.lessonId === lid && b.step === sn);
            if (exists) {
                addBmBtn.innerHTML = '<span class="cmd-icon">&#9733;</span> Bookmarked';
                addBmBtn.disabled = true;
                addBmBtn.classList.add('cmd-btn-done');
            } else {
                addBmBtn.innerHTML = '<span class="cmd-icon">&#9734;</span> Bookmark this step';
                addBmBtn.disabled = false;
                addBmBtn.classList.remove('cmd-btn-done');
            }
        } else {
            addBmBtn.style.display = 'none';
        }
    }

    // ── Stats section
    const statsEl = document.getElementById('cmdStats');
    let totalSteps = 0, lessonsStarted = 0;
    Object.keys(progress).forEach(lid => {
        const steps = progress[lid] || [];
        if (steps.length > 0) lessonsStarted++;
        totalSteps += steps.length;
    });
    statsEl.innerHTML = `
        <div class="cmd-label">Progress</div>
        <div class="cmd-stats-grid">
            <div class="cmd-stat">
                <span class="cmd-stat-val">${totalSteps}</span>
                <span class="cmd-stat-label">Steps visited</span>
            </div>
            <div class="cmd-stat">
                <span class="cmd-stat-val">${lessonsStarted}</span>
                <span class="cmd-stat-label">/ 21 lessons</span>
            </div>
            <div class="cmd-stat">
                <span class="cmd-stat-val">${bookmarks.length}</span>
                <span class="cmd-stat-label">Bookmarks</span>
            </div>
        </div>`;
}

function addBookmark() {
    const match = /\/lesson\/([^/]+)\/step\/(\d+)/.exec(window.location.pathname);
    if (!match) return;
    const lessonId = match[1], step = parseInt(match[2]);
    const last = JSON.parse(localStorage.getItem('portalLastVisited') || 'null');
    const title = last && last.lessonId === lessonId ? last.title : lessonId;
    const bookmarks = JSON.parse(localStorage.getItem('portalBookmarks') || '[]');
    if (bookmarks.some(b => b.lessonId === lessonId && b.step === step)) return;
    bookmarks.push({ lessonId, step, title, ts: Date.now() });
    localStorage.setItem('portalBookmarks', JSON.stringify(bookmarks));
    renderCommandMenu();
}

function removeBookmark(index) {
    const bookmarks = JSON.parse(localStorage.getItem('portalBookmarks') || '[]');
    bookmarks.splice(index, 1);
    localStorage.setItem('portalBookmarks', JSON.stringify(bookmarks));
    renderCommandMenu();
}

function confirmResetAll() {
    document.getElementById('cmdConfirm').style.display = '';
}

function cancelReset() {
    document.getElementById('cmdConfirm').style.display = 'none';
}

function resetAllProgress() {
    localStorage.removeItem('portalProgress');
    localStorage.removeItem('portalLastVisited');
    localStorage.removeItem('portalBookmarks');
    localStorage.removeItem('visitedSteps');
    closeCommandMenu();
    window.location.reload();
}

/* ── Color maps ──────────────────────────────────────────────────────────── */

/* Default teal theme: dark → bright teal (matches dark UI) */
function tealColor(value, max = 16) {
    const t = Math.max(0, Math.min(1, value / max));
    return `rgba(6, 182, 212, ${(t * 0.95 + 0.05 * (t > 0 ? 1 : 0)).toFixed(2)})`;
}
function tealText(value, max = 16) {
    return (value / max) > 0.45 ? '#0b0d17' : '#7b82a8';
}

/* Classic grayscale (available as option) */
function grayR(value, max = 16) {
    const t = Math.max(0, Math.min(1, value / max));
    const v = Math.round(255 * (1 - t));
    return `rgb(${v},${v},${v})`;
}
function grayRText(value, max = 16) {
    return (value / max) > 0.45 ? '#fff' : '#222';
}

/* Cool heat map: dark navy → indigo → violet → cyan → light cyan
   Replaces the previous black-red-yellow-white scheme — fits the brand
   palette and stays readable on a dark background. */
function hotColor(value, max = 16) {
    const t = Math.max(0, Math.min(1, value / max));
    // Stops: navy(0) -> indigo(0.33) -> violet(0.66) -> cyan(1)
    const stops = [
        [10,  12,  32],   // #0a0c20  near-black navy
        [55,  48,  140],  // #37308c  indigo
        [139, 92,  246],  // #8b5cf6  violet
        [92,  242, 251],  // #5cf2fb  bright cyan
    ];
    const seg = t * (stops.length - 1);
    const i = Math.min(stops.length - 2, Math.floor(seg));
    const f = seg - i;
    const r = Math.round(stops[i][0] + (stops[i + 1][0] - stops[i][0]) * f);
    const g = Math.round(stops[i][1] + (stops[i + 1][1] - stops[i][1]) * f);
    const b = Math.round(stops[i][2] + (stops[i + 1][2] - stops[i][2]) * f);
    return `rgb(${r},${g},${b})`;
}
function hotText(value, max = 16) {
    // Dark text on the bright cyan end, light text on the dark navy/violet end.
    return (value / max) > 0.7 ? '#04141a' : '#e6edff';
}

/* Green / red mask */
function maskColor(value) {
    return value > 0.5 ? 'var(--green)' : 'rgba(244, 63, 94, 0.2)';
}

/* Blue → Purple → Red correlation scale (readable on light & dark) */
function corrColor(value) {
    const t = Math.min(1, value / 0.7);
    let r, g, b;
    if (t < 0.5) {
        // Blue → Purple
        const s = t / 0.5;
        r = Math.round(60 + 130 * s);
        g = Math.round(130 * (1 - s));
        b = Math.round(220 - 40 * s);
    } else {
        // Purple → Red
        const s = (t - 0.5) / 0.5;
        r = Math.round(190 + 55 * s);
        g = Math.round(20 * (1 - s));
        b = Math.round(180 * (1 - s));
    }
    return `rgb(${r},${g},${b})`;
}

/* ── Grid rendering ──────────────────────────────────────────────────────── */

function renderGrid(containerId, data, options = {}) {
    const el = document.getElementById(containerId);
    if (!el) return;
    const colorFn  = options.colorFn  || tealColor;
    const textFn   = options.textFn   || null;
    const maxVal   = options.maxVal   || 16;
    const showVals = options.showVals || false;
    const animate  = options.animate  !== undefined ? options.animate : false;

    el.innerHTML = '';
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            const v = data[i][j];
            const cell = document.createElement('div');
            cell.className = 'cell' + (showVals ? ' show-val' : '');
            cell.style.backgroundColor = colorFn(v, maxVal);
            if (showVals) {
                cell.textContent = typeof v === 'number' ? (Number.isInteger(v) ? v : v.toFixed(1)) : v;
                cell.style.color = textFn ? textFn(v, maxVal) : tealText(v, maxVal);
            }
            cell.title = `[${i},${j}] = ${typeof v === 'number' ? Math.round(v * 100) / 100 : v}`;
            if (animate) {
                cell.style.opacity = '0';
                cell.style.transition = `opacity 0.3s ease ${(i * 8 + j) * 8}ms`;
                requestAnimationFrame(() => { cell.style.opacity = '1'; });
            }
            el.appendChild(cell);
        }
    }
}

/* ── Difference & similarity ─────────────────────────────────────────────── */

function diffGrid(a, b) {
    const result = [];
    for (let i = 0; i < 8; i++) {
        result.push([]);
        for (let j = 0; j < 8; j++) {
            result[i].push(Math.abs(a[i][j] - b[i][j]));
        }
    }
    return result;
}

function similarity(a, b) {
    let total = 0;
    for (let i = 0; i < 8; i++)
        for (let j = 0; j < 8; j++)
            total += Math.abs(a[i][j] - b[i][j]);
    return 1 - total / (64 * 16);
}

/* ── Animated value counter ──────────────────────────────────────────────── */

function animateValue(el, start, end, duration = 600, suffix = '') {
    const range = end - start;
    const startTime = performance.now();
    function step(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
        const current = Math.round(start + range * eased);
        el.textContent = current + suffix;
        if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
}

/* ── Learning path step activation ──────────────────────────────────────── */

function activateLpStep(el) {
    document.querySelectorAll('.lp-step').forEach(s => s.classList.remove('lp-active'));
    el.classList.add('lp-active');
}

/* ── Hint modal (challenge + security) ───────────────────────────────────── */

function openHintModal() {
    document.getElementById('hintModal').classList.add('open');
    document.getElementById('hintOverlay').classList.add('open');
}

function closeHintModal() {
    document.getElementById('hintModal').classList.remove('open');
    document.getElementById('hintOverlay').classList.remove('open');
    if (typeof activateExploreLp === 'function') activateExploreLp();
}

function showAnswer() {
    document.querySelector('.challenge-box .answer').classList.toggle('open');
}

/* ── Step completion tracking (localStorage) ─────────────────────────────── */

function markStepVisited(step) {
    try {
        const visited = JSON.parse(localStorage.getItem('visitedSteps') || '[]');
        if (!visited.includes(step)) {
            visited.push(step);
            localStorage.setItem('visitedSteps', JSON.stringify(visited));
        }
    } catch(e) {}
}

function getVisitedSteps() {
    try {
        return JSON.parse(localStorage.getItem('visitedSteps') || '[]');
    } catch(e) { return []; }
}

function applyVisitedSteps() {
    const visited = getVisitedSteps();
    const items = document.querySelectorAll('.sidebar li');
    items.forEach((li) => {
        const link = li.querySelector('a');
        if (!link) return;
        const href = link.getAttribute('href');
        const match = href.match(/\/step\/(\d+)/);
        if (match && visited.includes(parseInt(match[1]))) {
            li.classList.add('visited');
        }
    });
}

/* ── Mobile sidebar toggle ───────────────────────────────────────────────── */

function toggleSidebar() {
    document.querySelector('.sidebar').classList.toggle('open');
    const overlay = document.querySelector('.sidebar-overlay');
    if (overlay) overlay.classList.toggle('show');
}

/* ── Keyboard navigation ─────────────────────────────────────────────────── */

function setupKeyboardNav(currentStep) {
    document.addEventListener('keydown', (e) => {
        // Don't intercept when typing in inputs
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA') return;

        if (e.key === 'ArrowLeft' && currentStep > 0) {
            window.location.href = `/step/${currentStep - 1}`;
        } else if (e.key === 'ArrowRight' && currentStep < 9) {
            window.location.href = `/step/${currentStep + 1}`;
        }
    });
}

/* ── Utility ─────────────────────────────────────────────────────────────── */

async function fetchJSON(url) {
    const res = await fetch(url);
    return res.json();
}

/* ── Similarity meter helper ─────────────────────────────────────────────── */

function updateSimMeter(containerId, sim) {
    const el = document.getElementById(containerId);
    if (!el) return;
    const pct = (sim * 100).toFixed(0);
    const color = sim > 0.85 ? 'var(--red)' : sim > 0.7 ? 'var(--orange)' : 'var(--green)';
    el.innerHTML = `
        <span style="font-size:13px; color:var(--text-dim); min-width:70px;">Similarity</span>
        <div class="meter-track">
            <div class="meter-fill" style="width:${pct}%; background:${color};"></div>
        </div>
        <span class="meter-label" style="color:${color}">${pct}%</span>
    `;
}
