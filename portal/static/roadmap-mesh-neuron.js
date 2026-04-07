/* roadmap-mesh.js — neuron cluster layout + connector overlay
 *
 * Each .neuron-cluster on the home page is rendered as a glowing soma core
 * with N lesson satellites radiating outward as dendrite branches. This
 * script:
 *   1. Positions every satellite on an arc around its core (left clusters
 *      arc to the left, right clusters arc to the right).
 *   2. Draws the dendrite branches as bezier paths inside each cluster's
 *      .neuron-branches SVG.
 *   3. Draws the inter-cluster mesh — diagonal synapses connecting each
 *      core to the next core in the chain — into the page-level
 *      #roadmap-mesh SVG.
 *   4. Wires up hover highlighting: hovering a satellite lights up its
 *      branch; hovering a core lights up all branches in its cluster
 *      plus the inter-cluster paths attached to it.
 *
 * Desktop-only — the mobile media query collapses each cluster into a
 * vertical list and hides the SVG branch layer entirely.
 */
(function () {
    'use strict';

    const SVG_NS = 'http://www.w3.org/2000/svg';
    const MOBILE_QUERY = '(max-width: 960px)';

    /* Inter-cluster connector flow — the curriculum chain. */
    const INTER_CONNECTORS = [
        { source: 's1', target: 's2' },
        { source: 's2', target: 's3' },
        { source: 's3', target: 's4' },
        { source: 's4', target: 's5' },
    ];

    function svgEl(tag, attrs) {
        const node = document.createElementNS(SVG_NS, tag);
        if (attrs) for (const k in attrs) node.setAttribute(k, attrs[k]);
        return node;
    }

    /* ── Satellite layout ──────────────────────────────────────────────── */

    /* Place each satellite in the cluster's .neuron-stage area on an arc.
     * The arc fans outward from the cluster's outer side (left for `.left`,
     * right for `.right`). Returns an array of {sat, sx, sy, cx, cy} that
     * the branch drawer consumes — coordinates are stage-local. */
    function layoutCluster(cluster) {
        const stage = cluster.querySelector('.neuron-stage');
        const core  = cluster.querySelector('.neuron-core');
        const sats  = cluster.querySelectorAll('.neuron-satellite');
        if (!stage || !core || sats.length === 0) return [];

        const isLeft = cluster.classList.contains('left');
        const sRect  = stage.getBoundingClientRect();
        const coreR  = core.getBoundingClientRect();
        /* Half the satellite dot — used to align the branch endpoint with
         * the centre of the dot rather than the edge of the link element. */
        const DOT_HALF = 15;
        const cx = coreR.left + coreR.width  / 2 - sRect.left;
        const cy = coreR.top  + coreR.height / 2 - sRect.top;

        const N = sats.length;
        /* Arc parameters tuned for 4–6 satellites. A 120° arc keeps the
         * top and bottom satellites well clear of the title strip while
         * still giving each one breathing room. */
        const radius   = 180;
        const arcDeg   = 120;
        const halfArc  = arcDeg / 2;

        const placements = [];
        sats.forEach((sat, i) => {
            /* t goes 0..1 across the arc; with N=1 we centre it. */
            const t = N === 1 ? 0.5 : i / (N - 1);
            /* angleDeg is measured from the outward normal — positive
             * angles bend downward on screen, negative bend upward. */
            const angleDeg = -halfArc + t * arcDeg;
            const a = angleDeg * Math.PI / 180;

            /* Outward direction: -1 for left clusters, +1 for right. */
            const ox = isLeft ? -1 : 1;
            /* Rotated unit vector. ox * cos rotates the outward normal
             * by `a`; sin handles the vertical sweep. */
            const dx = ox * Math.cos(a);
            const dy = Math.sin(a);

            const sx = cx + dx * radius;
            const sy = cy + dy * radius;

            /* Position the satellite element relative to the stage. We use
             * top/left in pixels so click targets stay accurately
             * hit-tested. The translate() offset puts the centre of the
             * 30px dot on (sx, sy):
             *   - Left clusters use flex-direction: row-reverse, so the dot
             *     sits at the right edge; offset the right edge to sx by
             *     pulling the element 100% left then back right by DOT_HALF.
             *   - Right clusters have the dot at the left edge; pull right
             *     by DOT_HALF so the dot's centre lands on sx.
             */
            sat.style.position = 'absolute';
            sat.style.left = `${sx}px`;
            sat.style.top  = `${sy}px`;
            sat.style.transform = isLeft
                ? `translate(calc(-100% + ${DOT_HALF}px), -50%)`
                : `translate(${-DOT_HALF}px, -50%)`;

            placements.push({ sat, sx, sy, cx, cy, isLeft });
        });
        return placements;
    }

    /* Bezier from core to one satellite. The control point is offset
     * perpendicular to the chord so each branch curves organically. */
    function branchPath(cx, cy, sx, sy, curveSign) {
        const mx = (cx + sx) / 2;
        const my = (cy + sy) / 2;
        const dx = sx - cx;
        const dy = sy - cy;
        /* Perpendicular vector, scaled. curveSign alternates so adjacent
         * branches don't all bow the same way. */
        const px = -dy * 0.18 * curveSign;
        const py =  dx * 0.18 * curveSign;
        return `M ${cx} ${cy} Q ${mx + px} ${my + py} ${sx} ${sy}`;
    }

    function drawBranches(cluster, placements) {
        const svg   = cluster.querySelector('.neuron-branches');
        const stage = cluster.querySelector('.neuron-stage');
        if (!svg || !stage) return;
        const sRect = stage.getBoundingClientRect();
        svg.setAttribute('viewBox', `0 0 ${sRect.width} ${sRect.height}`);
        /* Clear previous paths. */
        Array.from(svg.querySelectorAll('.neuron-branch')).forEach(p => p.remove());

        placements.forEach((pl, i) => {
            const sign = i % 2 === 0 ? 1 : -1;
            const path = svgEl('path', {
                d: branchPath(pl.cx, pl.cy, pl.sx, pl.sy, sign),
                class: 'neuron-branch',
                'data-sat-idx': i,
            });
            svg.appendChild(path);
        });
    }

    /* ── Inter-cluster mesh ────────────────────────────────────────────── */

    /* Bezier from one core's outer edge to the next core's outer edge.
     * Cores in the chain alternate columns, so every hop is a diagonal
     * swoosh — exactly the synapse silhouette we want. */
    function interBezier(s, t) {
        const dx = t.x - s.x;
        const dy = t.y - s.y;
        const cx1 = s.x + dx * 0.55;
        const cy1 = s.y + dy * 0.05;
        const cx2 = t.x - dx * 0.55;
        const cy2 = t.y - dy * 0.05;
        return `M ${s.x} ${s.y} C ${cx1} ${cy1}, ${cx2} ${cy2}, ${t.x} ${t.y}`;
    }

    function coreEdgePoint(cluster, side) {
        const core = cluster.querySelector('.neuron-core');
        if (!core) return null;
        const r = core.getBoundingClientRect();
        const cx = r.left + r.width / 2;
        const cy = r.top  + r.height / 2;
        const radius = r.width / 2;
        /* Connect from the inner edge of the core (the side facing the
         * other cluster) so the synapse path doesn't cut through the
         * soma. */
        if (side === 'right') return { x: cx + radius, y: cy };
        if (side === 'left')  return { x: cx - radius, y: cy };
        return { x: cx, y: cy };
    }

    function drawInterMesh() {
        const roadmap = document.querySelector('.roadmap');
        const svg = document.getElementById('roadmap-mesh');
        if (!roadmap || !svg) return;

        Array.from(svg.querySelectorAll('.mesh-path')).forEach(p => p.remove());

        const rmRect = roadmap.getBoundingClientRect();
        svg.setAttribute('width',  rmRect.width);
        svg.setAttribute('height', rmRect.height);
        svg.setAttribute('viewBox', `0 0 ${rmRect.width} ${rmRect.height}`);

        INTER_CONNECTORS.forEach((cfg) => {
            const sourceCluster = document.querySelector(`.neuron-cluster.${cfg.source}`);
            const targetCluster = document.querySelector(`.neuron-cluster.${cfg.target}`);
            if (!sourceCluster || !targetCluster) return;

            /* Source core attaches on its inner edge — the side facing
             * the target column. */
            const sourceSide = sourceCluster.classList.contains('left')  ? 'right' : 'left';
            const targetSide = targetCluster.classList.contains('right') ? 'left'  : 'right';

            const sPt = coreEdgePoint(sourceCluster, sourceSide);
            const tPt = coreEdgePoint(targetCluster, targetSide);
            if (!sPt || !tPt) return;

            const s = { x: sPt.x - rmRect.left, y: sPt.y - rmRect.top };
            const t = { x: tPt.x - rmRect.left, y: tPt.y - rmRect.top };

            const path = svgEl('path', {
                d: interBezier(s, t),
                class: 'mesh-path',
                'data-pair': `${cfg.source}-${cfg.target}`,
            });
            svg.appendChild(path);
        });
    }

    /* ── Hover orchestration ───────────────────────────────────────────── */

    function bindClusterHover(cluster) {
        const sats = cluster.querySelectorAll('.neuron-satellite');
        const svg  = cluster.querySelector('.neuron-branches');
        if (!svg) return;
        sats.forEach((sat, i) => {
            sat.addEventListener('mouseenter', () => {
                cluster.classList.add('is-hovered');
                const branches = svg.querySelectorAll('.neuron-branch');
                branches.forEach((b) => {
                    if (Number(b.getAttribute('data-sat-idx')) === i) {
                        b.classList.add('is-active');
                    }
                });
            });
            sat.addEventListener('mouseleave', () => {
                cluster.classList.remove('is-hovered');
                svg.querySelectorAll('.neuron-branch.is-active')
                   .forEach(b => b.classList.remove('is-active'));
            });
        });
        const core = cluster.querySelector('.neuron-core');
        if (core) {
            core.addEventListener('mouseenter', () => {
                cluster.classList.add('is-hovered');
                /* Highlight every branch in the cluster. */
                svg.querySelectorAll('.neuron-branch').forEach(b => b.classList.add('is-active'));
                /* Also highlight inter-cluster mesh paths attached to this stage. */
                const stageId = cluster.dataset.stage;
                const mesh = document.getElementById('roadmap-mesh');
                if (mesh) {
                    mesh.querySelectorAll('.mesh-path').forEach(p => {
                        const pair = p.getAttribute('data-pair') || '';
                        if (pair.startsWith(stageId + '-') || pair.endsWith('-' + stageId)) {
                            p.classList.add('mesh-active');
                        }
                    });
                }
            });
            core.addEventListener('mouseleave', () => {
                cluster.classList.remove('is-hovered');
                svg.querySelectorAll('.neuron-branch.is-active')
                   .forEach(b => b.classList.remove('is-active'));
                const mesh = document.getElementById('roadmap-mesh');
                if (mesh) {
                    mesh.querySelectorAll('.mesh-path.mesh-active')
                        .forEach(p => p.classList.remove('mesh-active'));
                }
            });
        }
    }

    /* ── Inter-cluster mesh dropout (legacy "dropout" effect) ──────────── */
    /* A handful of inter-cluster paths fade briefly every ~1.6s, echoing
     * the dropout regularisation idea covered in the deep-learning stage. */
    function startDropout() {
        const svg = document.getElementById('roadmap-mesh');
        if (!svg) return;
        setInterval(() => {
            const paths = svg.querySelectorAll('.mesh-path');
            paths.forEach((p) => {
                if (Math.random() < 0.18) {
                    p.classList.add('mesh-dropped');
                    setTimeout(() => p.classList.remove('mesh-dropped'),
                               700 + Math.random() * 500);
                }
            });
        }, 1600);
    }

    /* ── Layout pipeline ───────────────────────────────────────────────── */

    function relayoutAll() {
        const clusters = document.querySelectorAll('.neuron-cluster');
        clusters.forEach((cluster) => {
            const placements = layoutCluster(cluster);
            drawBranches(cluster, placements);
        });
        /* Defer the inter-cluster mesh to the next frame so it sees the
         * post-layout core positions. */
        requestAnimationFrame(drawInterMesh);
    }

    function init() {
        if (window.matchMedia(MOBILE_QUERY).matches) return;
        relayoutAll();
        document.querySelectorAll('.neuron-cluster').forEach(bindClusterHover);
        startDropout();

        const roadmap = document.querySelector('.roadmap');
        if (roadmap && 'ResizeObserver' in window) {
            const ro = new ResizeObserver(() => relayoutAll());
            ro.observe(roadmap);
        }
        window.addEventListener('resize', relayoutAll);
        window.addEventListener('load', relayoutAll);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
