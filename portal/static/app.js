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

/* Hot color map: black → red → yellow → white */
function hotColor(value, max = 16) {
    const t = Math.max(0, Math.min(1, value / max));
    let r, g, b;
    if (t < 0.33)      { r = t / 0.33 * 255; g = 0; b = 0; }
    else if (t < 0.66)  { r = 255; g = (t - 0.33) / 0.33 * 255; b = 0; }
    else                 { r = 255; g = 255; b = (t - 0.66) / 0.34 * 255; }
    return `rgb(${Math.round(r)},${Math.round(g)},${Math.round(b)})`;
}
function hotText(value, max = 16) {
    return (value / max) < 0.4 ? '#ccc' : '#000';
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

/* ── Hint modal (challenge + security) ───────────────────────────────────── */

function openHintModal() {
    document.getElementById('hintModal').classList.add('open');
    document.getElementById('hintOverlay').classList.add('open');
}

function closeHintModal() {
    document.getElementById('hintModal').classList.remove('open');
    document.getElementById('hintOverlay').classList.remove('open');
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
