/* roadmap-mesh.js — neural-network connector overlay for the AI Ninja home page.
 *
 * Replaces the four single-arrow connectors between stage cards with a fully
 * connected web of curved bezier paths (one per source-lesson × target-lesson
 * pair), styled per stage colour. Includes:
 *   - hover highlighting: hovering a lesson dims all paths except its own
 *   - dropout animation: a random subset of paths fades briefly every ~1.5s,
 *     visualising the dropout regularisation concept covered in lesson 3.2
 *
 * The mesh is desktop-only (matches the existing 960px breakpoint).
 */
(function () {
    'use strict';

    const SVG_NS = 'http://www.w3.org/2000/svg';
    const MOBILE_QUERY = '(max-width: 960px)';

    /* Connector definitions — zigzag column layout: every hop is a
     * diagonal swoosh between alternating left/right cards. */
    const CONNECTORS = [
        { source: 's1', target: 's2', dir: 'h-right' },
        { source: 's2', target: 's3', dir: 'h-left'  },
        { source: 's3', target: 's4', dir: 'h-right' },
        { source: 's4', target: 's5', dir: 'h-left'  },
    ];

    function svgEl(tag, attrs) {
        const node = document.createElementNS(SVG_NS, tag);
        if (attrs) {
            for (const key in attrs) node.setAttribute(key, attrs[key]);
        }
        return node;
    }

    /* Compute one attachment point per lesson card.
     * For horizontal connectors we attach to the per-lesson left/right edge.
     * For vertical connectors we spread N points along the stage card's
     * top/bottom edge — stacked lessons share an x range so per-lesson edges
     * would overlap into a blur. */
    function attachPoints(stageCard, side) {
        const lessons = stageCard.querySelectorAll('.lesson-card');
        const points = [];
        if (side === 'right' || side === 'left') {
            lessons.forEach((lesson) => {
                const r = lesson.getBoundingClientRect();
                points.push({
                    x: side === 'right' ? r.right : r.left,
                    y: r.top + r.height / 2,
                });
            });
        } else {
            const cardRect = stageCard.getBoundingClientRect();
            const y = side === 'bottom' ? cardRect.bottom : cardRect.top;
            const n = lessons.length;
            for (let i = 0; i < n; i++) {
                points.push({
                    x: cardRect.left + (cardRect.width * (i + 1)) / (n + 1),
                    y: y,
                });
            }
        }
        return points;
    }

    /* Bezier path string for one source→target line. Control points are
     * pulled toward the centre of the connector to give an organic synaptic
     * curve rather than a straight line. */
    function bezierPath(s, t, dir) {
        if (dir === 'v-down') {
            const dy = (t.y - s.y) * 0.5;
            return `M ${s.x} ${s.y} C ${s.x} ${s.y + dy}, ${t.x} ${t.y - dy}, ${t.x} ${t.y}`;
        }
        const dx = (t.x - s.x) * 0.5;
        return `M ${s.x} ${s.y} C ${s.x + dx} ${s.y}, ${t.x - dx} ${t.y}, ${t.x} ${t.y}`;
    }

    function sourceSideFor(dir) {
        if (dir === 'h-right') return 'right';
        if (dir === 'h-left')  return 'left';
        return 'bottom';
    }

    function targetSideFor(dir) {
        if (dir === 'h-right') return 'left';
        if (dir === 'h-left')  return 'right';
        return 'top';
    }

    /* Tag every lesson card with a stable mesh id so hover handlers can
     * cross-reference paths. Format: "<stage>-<index>" — same as data-source
     * and data-target on each path. */
    function tagLessons() {
        document.querySelectorAll('.stage-card').forEach((card) => {
            let stage = null;
            for (const cls of card.classList) {
                if (/^s\d$/.test(cls)) { stage = cls; break; }
            }
            if (!stage) return;
            card.querySelectorAll('.lesson-card').forEach((lesson, idx) => {
                lesson.dataset.meshId = `${stage}-${idx}`;
            });
        });
    }

    function drawMesh() {
        const roadmap = document.querySelector('.roadmap');
        const svg = document.getElementById('roadmap-mesh');
        if (!roadmap || !svg) return;

        /* Clear previous paths (preserves any <defs> if added later). */
        Array.from(svg.querySelectorAll('.mesh-path')).forEach((p) => p.remove());

        const rmRect = roadmap.getBoundingClientRect();
        svg.setAttribute('width',  rmRect.width);
        svg.setAttribute('height', rmRect.height);
        svg.setAttribute('viewBox', `0 0 ${rmRect.width} ${rmRect.height}`);

        CONNECTORS.forEach((cfg) => {
            const sourceCard = document.querySelector(`.stage-card.${cfg.source}`);
            const targetCard = document.querySelector(`.stage-card.${cfg.target}`);
            if (!sourceCard || !targetCard) return;

            const sourcePts = attachPoints(sourceCard, sourceSideFor(cfg.dir));
            const targetPts = attachPoints(targetCard, targetSideFor(cfg.dir));

            sourcePts.forEach((sPt, si) => {
                targetPts.forEach((tPt, ti) => {
                    const s = { x: sPt.x - rmRect.left, y: sPt.y - rmRect.top };
                    const t = { x: tPt.x - rmRect.left, y: tPt.y - rmRect.top };
                    const path = svgEl('path', {
                        d: bezierPath(s, t, cfg.dir),
                        class: 'mesh-path',
                        'data-pair':   `${cfg.source}-${cfg.target}`,
                        'data-source': `${cfg.source}-${si}`,
                        'data-target': `${cfg.target}-${ti}`,
                    });
                    svg.appendChild(path);
                });
            });
        });
    }

    /* Hover: highlight only paths attached to the hovered lesson, dim the rest. */
    function bindHover() {
        const svg = document.getElementById('roadmap-mesh');
        if (!svg) return;
        document.querySelectorAll('.lesson-card').forEach((card) => {
            card.addEventListener('mouseenter', () => {
                const meshId = card.dataset.meshId;
                if (!meshId) return;
                svg.classList.add('mesh-hover');
                svg.querySelectorAll('.mesh-path').forEach((p) => {
                    if (p.getAttribute('data-source') === meshId ||
                        p.getAttribute('data-target') === meshId) {
                        p.classList.add('mesh-active');
                    }
                });
            });
            card.addEventListener('mouseleave', () => {
                svg.classList.remove('mesh-hover');
                svg.querySelectorAll('.mesh-path.mesh-active')
                   .forEach((p) => p.classList.remove('mesh-active'));
            });
        });
    }

    /* Dropout: ~12% of paths fade out for ~1s every 1.6s. The animation runs
     * indefinitely; pauses while a lesson is hovered (mesh-hover state owns
     * the visuals). */
    function startDropout() {
        const svg = document.getElementById('roadmap-mesh');
        if (!svg) return;
        setInterval(() => {
            if (svg.classList.contains('mesh-hover')) return;
            const paths = svg.querySelectorAll('.mesh-path');
            paths.forEach((p) => {
                if (Math.random() < 0.12) {
                    p.classList.add('mesh-dropped');
                    setTimeout(() => p.classList.remove('mesh-dropped'),
                               700 + Math.random() * 500);
                }
            });
        }, 1600);
    }

    function init() {
        if (window.matchMedia(MOBILE_QUERY).matches) return;
        tagLessons();
        drawMesh();
        bindHover();
        startDropout();

        const roadmap = document.querySelector('.roadmap');
        if (roadmap && 'ResizeObserver' in window) {
            const ro = new ResizeObserver(() => drawMesh());
            ro.observe(roadmap);
        }
        window.addEventListener('resize', drawMesh);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
