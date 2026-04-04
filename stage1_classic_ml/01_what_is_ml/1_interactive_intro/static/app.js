/* ── Color maps ──────────────────────────────────────────────────────────── */

function grayR(value, max = 16) {
    const t = Math.max(0, Math.min(1, value / max));
    const v = Math.round(255 * (1 - t));
    return `rgb(${v},${v},${v})`;
}

function grayRText(value, max = 16) {
    return (value / max) > 0.45 ? '#fff' : '#222';
}

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

function maskColor(value) {
    return value > 0.5 ? 'var(--green)' : 'var(--red)';
}

function corrColor(value) {
    // Yellow-Orange-Red scale
    const t = Math.min(1, value / 0.7);
    const r = 255;
    const g = Math.round(255 * (1 - t * 0.7));
    const b = Math.round(80 * (1 - t));
    return `rgb(${r},${g},${b})`;
}

/* ── Grid rendering ──────────────────────────────────────────────────────── */

function renderGrid(containerId, data, options = {}) {
    const el = document.getElementById(containerId);
    if (!el) return;
    const colorFn  = options.colorFn  || grayR;
    const textFn   = options.textFn   || null;
    const maxVal   = options.maxVal   || 16;
    const showVals = options.showVals || false;

    el.innerHTML = '';
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            const v = data[i][j];
            const cell = document.createElement('div');
            cell.className = 'cell' + (showVals ? ' show-val' : '');
            cell.style.backgroundColor = colorFn(v, maxVal);
            if (showVals) {
                cell.textContent = typeof v === 'number' ? (Number.isInteger(v) ? v : v.toFixed(1)) : v;
                cell.style.color = textFn ? textFn(v, maxVal) : grayRText(v, maxVal);
            }
            cell.title = `[${i},${j}] = ${typeof v === 'number' ? Math.round(v * 100) / 100 : v}`;
            el.appendChild(cell);
        }
    }
}

/* ── Challenge toggle ────────────────────────────────────────────────────── */

function toggleChallenge() {
    document.querySelector('.challenge-body').classList.toggle('open');
}

function showAnswer() {
    document.querySelector('.challenge-body .answer').classList.toggle('open');
}

/* ── Utility ─────────────────────────────────────────────────────────────── */

async function fetchJSON(url) {
    const res = await fetch(url);
    return res.json();
}

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
