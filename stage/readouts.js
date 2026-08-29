// ═══════════════════════════════════════════════════════════════════════════
// THE INSTRUMENT PANEL
//
// Metering that behaves like an instrument rather than a caption. Every
// readout carries an `interest` series computed at export time — how unlike
// its recent self the underlying measurement is right now — and the readout
// is only on stage while that is high. A steady verse leaves the frame almost
// bare; a tempo ramp, a key change or a section boundary brings things in.
// So the panel is itself a reading of how much is happening.
//
// Three rules keep it from becoming a HUD:
//
//   1. Everything is drawn in the same vector language as the music — the
//      same beam shader, the same additive bloom. Glyphs are strokes, not
//      textures pretending to be a user interface.
//   2. Readouts are children of the CAMERA, so they hold a stable position on
//      screen and stay legible, but they are still lit and bloomed in 3D and
//      they slide in from off-frame.
//   3. They earn their place. Nothing is pinned; nothing is permanent.
//
// The Laser class is passed in rather than imported, so this file has no
// opinion about how a beam is drawn.
// ═══════════════════════════════════════════════════════════════════════════

export function makePanel(THREE, Laser, D, camera, scene, opts = {}) {
  const clamp = (x, a, b) => x < a ? a : x > b ? b : x;
  const UI_LAYER = opts.uiLayer ?? 1;
  const RATE = D.rate;
  const P = D.panel;
  if (!P) return {update: () => {}, readouts: []};

  const at = (arr, t, dflt = 0) => {
    if (!arr || !arr.length) return dflt;
    const x = clamp(t * RATE, 0, arr.length - 1.001);
    const i = x | 0;
    return arr[i] + (arr[i + 1] - arr[i]) * (x - i);
  };
  const atI = (arr, t, dflt = 0) => {
    if (!arr || !arr.length) return dflt;
    return arr[clamp(Math.round(t * RATE), 0, arr.length - 1)];
  };

  // ── glyphs as strokes ────────────────────────────────────────────────────
  // A seven-segment-ish vector font, drawn with the beam shader so the type is
  // made of the same light as everything else. Only the characters the panel
  // can actually produce are defined; anything missing renders as a blank,
  // which is the correct failure — a gap, not a wrong glyph.
  //
  // Coordinates are in a 0..1 box (x right, y up). Each entry is a list of
  // polylines.
  const G = {};
  const seg = (...pts) => pts;
  const V = (x, y) => [x, y];
  // digits, built from the classic seven segments so they are consistent
  const S = {
    a: [V(0.1, 1.0), V(0.9, 1.0)], b: [V(0.9, 1.0), V(0.9, 0.55)],
    c: [V(0.9, 0.55), V(0.9, 0.1)], d: [V(0.1, 0.1), V(0.9, 0.1)],
    e: [V(0.1, 0.55), V(0.1, 0.1)], f: [V(0.1, 1.0), V(0.1, 0.55)],
    g: [V(0.1, 0.55), V(0.9, 0.55)],
  };
  const SEVEN = {
    '0': 'abcdef', '1': 'bc', '2': 'abged', '3': 'abgcd', '4': 'fgbc',
    '5': 'afgcd', '6': 'afgedc', '7': 'abc', '8': 'abcdefg', '9': 'afgbcd',
  };
  for (const [ch, segs] of Object.entries(SEVEN))
    G[ch] = [...segs].map(k => S[k]);
  G['.'] = [[V(0.45, 0.1), V(0.55, 0.1)]];
  G['-'] = [[V(0.15, 0.55), V(0.85, 0.55)]];
  G['+'] = [[V(0.15, 0.55), V(0.85, 0.55)], [V(0.5, 0.32), V(0.5, 0.78)]];
  G[':'] = [[V(0.45, 0.78), V(0.55, 0.78)], [V(0.45, 0.3), V(0.55, 0.3)]];
  G['/'] = [[V(0.15, 0.1), V(0.85, 1.0)]];
  G['#'] = [[V(0.3, 0.15), V(0.38, 0.95)], [V(0.62, 0.15), V(0.7, 0.95)],
            [V(0.12, 0.4), V(0.88, 0.48)], [V(0.12, 0.68), V(0.88, 0.76)]];
  G[' '] = [];
  // letters, stroked simply and legibly at small sizes
  Object.assign(G, {
    A: [[V(0.1, 0.1), V(0.5, 1), V(0.9, 0.1)], [V(0.25, 0.45), V(0.75, 0.45)]],
    B: [[V(0.1, 0.1), V(0.1, 1), V(0.72, 1), V(0.86, 0.86), V(0.72, 0.56),
         V(0.1, 0.56)], [V(0.72, 0.56), V(0.9, 0.36), V(0.74, 0.1), V(0.1, 0.1)]],
    C: [[V(0.9, 0.86), V(0.66, 1), V(0.24, 1), V(0.1, 0.72), V(0.1, 0.36),
         V(0.26, 0.1), V(0.66, 0.1), V(0.9, 0.24)]],
    D: [[V(0.1, 0.1), V(0.1, 1), V(0.62, 1), V(0.9, 0.72), V(0.9, 0.36),
         V(0.62, 0.1), V(0.1, 0.1)]],
    E: [[V(0.9, 1), V(0.1, 1), V(0.1, 0.1), V(0.9, 0.1)], [V(0.1, 0.55), V(0.7, 0.55)]],
    F: [[V(0.9, 1), V(0.1, 1), V(0.1, 0.1)], [V(0.1, 0.55), V(0.66, 0.55)]],
    G: [[V(0.9, 0.86), V(0.66, 1), V(0.24, 1), V(0.1, 0.72), V(0.1, 0.36),
         V(0.26, 0.1), V(0.7, 0.1), V(0.9, 0.28), V(0.9, 0.48), V(0.56, 0.48)]],
    H: [[V(0.1, 1), V(0.1, 0.1)], [V(0.9, 1), V(0.9, 0.1)], [V(0.1, 0.55), V(0.9, 0.55)]],
    I: [[V(0.5, 1), V(0.5, 0.1)], [V(0.25, 1), V(0.75, 1)], [V(0.25, 0.1), V(0.75, 0.1)]],
    J: [[V(0.8, 1), V(0.8, 0.3), V(0.6, 0.1), V(0.28, 0.1), V(0.12, 0.28)]],
    K: [[V(0.1, 1), V(0.1, 0.1)], [V(0.9, 1), V(0.1, 0.5)], [V(0.34, 0.62), V(0.9, 0.1)]],
    L: [[V(0.1, 1), V(0.1, 0.1), V(0.9, 0.1)]],
    M: [[V(0.1, 0.1), V(0.1, 1), V(0.5, 0.5), V(0.9, 1), V(0.9, 0.1)]],
    N: [[V(0.1, 0.1), V(0.1, 1), V(0.9, 0.1), V(0.9, 1)]],
    O: [[V(0.26, 1), V(0.74, 1), V(0.9, 0.74), V(0.9, 0.34), V(0.74, 0.1),
         V(0.26, 0.1), V(0.1, 0.34), V(0.1, 0.74), V(0.26, 1)]],
    P: [[V(0.1, 0.1), V(0.1, 1), V(0.72, 1), V(0.9, 0.8), V(0.72, 0.54), V(0.1, 0.54)]],
    Q: [[V(0.26, 1), V(0.74, 1), V(0.9, 0.74), V(0.9, 0.34), V(0.74, 0.1),
         V(0.26, 0.1), V(0.1, 0.34), V(0.1, 0.74), V(0.26, 1)], [V(0.62, 0.34), V(0.95, 0.0)]],
    R: [[V(0.1, 0.1), V(0.1, 1), V(0.72, 1), V(0.9, 0.8), V(0.72, 0.54), V(0.1, 0.54)],
        [V(0.46, 0.54), V(0.9, 0.1)]],
    S: [[V(0.9, 0.88), V(0.66, 1), V(0.26, 1), V(0.1, 0.8), V(0.26, 0.56),
         V(0.72, 0.52), V(0.9, 0.3), V(0.72, 0.1), V(0.26, 0.1), V(0.1, 0.22)]],
    T: [[V(0.1, 1), V(0.9, 1)], [V(0.5, 1), V(0.5, 0.1)]],
    U: [[V(0.1, 1), V(0.1, 0.32), V(0.3, 0.1), V(0.7, 0.1), V(0.9, 0.32), V(0.9, 1)]],
    V: [[V(0.1, 1), V(0.5, 0.1), V(0.9, 1)]],
    W: [[V(0.1, 1), V(0.28, 0.1), V(0.5, 0.66), V(0.72, 0.1), V(0.9, 1)]],
    X: [[V(0.1, 1), V(0.9, 0.1)], [V(0.9, 1), V(0.1, 0.1)]],
    Y: [[V(0.1, 1), V(0.5, 0.55), V(0.9, 1)], [V(0.5, 0.55), V(0.5, 0.1)]],
    Z: [[V(0.1, 1), V(0.9, 1), V(0.1, 0.1), V(0.9, 0.1)]],
  });

  const CH_W = 0.66;          // advance per character, in glyph boxes
  function measure(str) { return str.length * CH_W; }

  // ── a strip of text as one beam ─────────────────────────────────────────
  // The whole string becomes a single polyline: the beam jumps between strokes
  // with a zero-intensity segment, exactly the way a real galvo laser blanks
  // between figures. That means one draw call per label however long it is.
  class Label {
    constructor(maxChars = 24, width = 2.0) {
      this.maxChars = maxChars;
      this.cap = maxChars * 40;
      this.laser = new Laser(this.cap, width);
      this.pts = new Float32Array(this.cap * 3);
      this.cols = new Float32Array(this.cap * 3);
      this.ints = new Float32Array(this.cap);
      this.text = null;
      this.n = 0;
      this.obj = this.laser.mesh;
      // type has to blank cleanly between strokes, so no floor: a
      // zero-intensity segment must emit nothing at all
      this.laser.mat.uniforms.uFloor.value = 0.0;
    }
    set(str, size, colour, align = 0) {
      str = String(str).toUpperCase();
      const key = str + '|' + size + '|' + align;
      if (key !== this.text) {
        this.text = key;
        const w = measure(str) * size;
        const x0 = -w * align;
        let i = 0, px = 0, py = 0, first = true;
        for (let c = 0; c < str.length && i < this.cap - 2; c++) {
          const strokes = G[str[c]] ?? [];
          const ox = x0 + c * CH_W * size;
          for (const poly of strokes) {
            for (let k = 0; k < poly.length && i < this.cap; k++) {
              const X = ox + poly[k][0] * size, Y = poly[k][1] * size;
              if (k === 0 && !first) {
                // blank jump: repeat the last point, then the new one, dark
                this.pts[i * 3] = px; this.pts[i * 3 + 1] = py; this.pts[i * 3 + 2] = 0;
                this.ints[i] = 0; i++;
                if (i >= this.cap) break;
                this.pts[i * 3] = X; this.pts[i * 3 + 1] = Y; this.pts[i * 3 + 2] = 0;
                this.ints[i] = 0; i++;
                if (i >= this.cap) break;
              }
              this.pts[i * 3] = X; this.pts[i * 3 + 1] = Y; this.pts[i * 3 + 2] = 0;
              this.ints[i] = 0.80;
              px = X; py = Y; first = false; i++;
            }
          }
        }
        this.n = Math.max(2, i);
        this.dirty = true;
      }
      const [r, g, b] = colour;
      for (let k = 0; k < this.n; k++) {
        this.cols[k * 3] = r; this.cols[k * 3 + 1] = g; this.cols[k * 3 + 2] = b;
      }
      this.laser.set(this.pts, this.cols, this.ints, this.n, false);
    }
    get width() { return this.text ? 0 : 0; }
  }

  // ── a little vector graph, for the readouts that have a shape ───────────
  class Graph {
    constructor(pts = 64, width = 1.6) {
      this.m = pts;
      this.laser = new Laser(pts, width);
      this.pts = new Float32Array(pts * 3);
      this.cols = new Float32Array(pts * 3);
      this.ints = new Float32Array(pts);
      this.obj = this.laser.mesh;
      this.laser.mat.uniforms.uFloor.value = 0.0;
    }
    plot(fn, colour, w, h, gain = 1) {
      const [r, g, b] = colour;
      for (let i = 0; i < this.m; i++) {
        const u = i / (this.m - 1);
        this.pts[i * 3] = u * w;
        this.pts[i * 3 + 1] = clamp(fn(u), -1.2, 1.2) * h;
        this.pts[i * 3 + 2] = 0;
        this.cols[i * 3] = r; this.cols[i * 3 + 1] = g; this.cols[i * 3 + 2] = b;
        this.ints[i] = gain;
      }
      this.laser.set(this.pts, this.cols, this.ints, this.m, false);
    }
  }

  // ── one readout ─────────────────────────────────────────────────────────
  // Enters when interest crosses ON, dissolves when it falls below OFF and
  // stays there. Hysteresis on both the level and the timing, so a readout
  // never flickers on a marginal measurement.
  const ON = 0.34, OFF = 0.20, RISE = 0.30, FALL = 1.25, MIN_HOLD = 1.6;

  class Readout {
    constructor(spec, slot) {
      this.spec = spec;
      this.slot = slot;
      this.group = new THREE.Group();
      this.title = new Label(18, 1.1);
      this.value = new Label(12, 1.8);
      this.graph = new Graph(72, 1.2);
      this.group.add(this.title.obj, this.value.obj, this.graph.obj);
      // The panel is still made from the beam shader, but it bypasses the
      // scene bloom. Its own narrow skirt is enough glow for readable type.
      this.group.traverse(o => o.layers.set(UI_LAYER));
      this.title.obj.position.set(0, 0.205, 0);
      this.value.obj.position.set(0, 0.005, 0);
      this.graph.obj.position.set(0, -0.115, 0);
      this.e = 0;            // 0 hidden .. 1 fully on stage
      this.since = -1e9;
      this.live = false;
      this.rank = 0;         // slowly-followed interest, for stable ordering
      this.y = 1.02;         // eased slot position
      camera.add(this.group);
      this.group.visible = false;
    }

    // where a slot sits in camera space: a column down the right-hand side,
    // 3.4 units in front of the lens
    place(i, e, dt) {
      // a column down the right-hand edge, 3.4 units in front of the lens.
      // At 52 degrees and 16:9 the frame reaches x = +-2.95 there, so the
      // column sits at 1.92 and parks off-frame at 3.25.
      //
      // The slot is EASED rather than set. Ranking by interest means readouts
      // trade places, and a hard jump between two sub-frames of an
      // accumulated frame renders as two half-bright ghosts of the same
      // readout in different rows. Sliding also just looks better.
      const z = -3.4;
      const target = 1.02 - i * 0.54;
      this.y += (target - this.y) * (1 - Math.exp(-dt / 0.22));
      const xIn = 1.92, xOut = 3.25;
      const s = 1 - Math.pow(1 - e, 3);       // ease out
      this.group.position.set(xOut + (xIn - xOut) * s, this.y, z);
      this.group.scale.setScalar(0.90 + 0.10 * s);
    }

    update(t, dt, order) {
      const raw = at(this.spec.interest, t);
      const want = this.live ? raw > OFF : raw > ON;
      if (want && !this.live) { this.live = true; this.since = t; }
      if (!want && this.live && t - this.since > MIN_HOLD) this.live = false;
      const k = 1 - Math.exp(-dt / (this.live ? RISE : FALL));
      this.e += ((this.live ? 1 : 0) - this.e) * k;
      this.group.visible = this.e > 0.01;
      if (!this.group.visible) { this.y = 1.02 - order * 0.54; return; }
      this.place(order, this.e, dt);
      const dim = 0.30 + 0.70 * this.e;
      const hot = clamp(raw, 0, 1);
      this.draw(t, dim, hot);
      // additive strokes bloom hard, so the panel runs well under unity
      const al = this.e * 0.42 * (this.showE ?? 1);
      this.title.laser.mat.uniforms.uAlpha.value = al * 0.72;
      this.value.laser.mat.uniforms.uAlpha.value = al;
      this.graph.laser.mat.uniforms.uAlpha.value = al * 0.85;
    }
  }

  // ── the specific instruments ────────────────────────────────────────────
  const INK = [0.55, 0.62, 0.72];
  const HOT = [0.95, 0.78, 0.35];
  const COOL = [0.30, 0.72, 0.95];
  const mixc = (a, b, f) => [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f,
                             a[2] + (b[2] - a[2]) * f];

  const KIND = {
    tempo(t, dim, hot) {
      const v = at(P.tempo.bpm, t);
      this.title.set('TEMPO BPM', 0.052, INK);
      this.value.set(v.toFixed(1), 0.115, mixc(INK, HOT, hot), 0);
      // the last eight seconds of the written tempo, against its own range
      const lo = P.tempo.lo, hi = P.tempo.hi, sp = Math.max(1e-3, hi - lo);
      this.graph.plot(u => ((at(P.tempo.bpm, t - (1 - u) * 8) - lo) / sp) * 2 - 1,
                      mixc(COOL, HOT, hot), 0.62, 0.052, 0.55 + 0.6 * hot);
    },
    tonal(t, dim, hot) {
      this.title.set('TONAL BALANCE', 0.046, INK);
      const dv = at(P.mix.deviation, t);
      this.value.set(dv.toFixed(2), 0.098, mixc(INK, HOT, hot), 0);
      // the six bands now, against this song's own long-term average
      const nb = P.mix.bands.length;
      const row = [], tgt = P.mix.target;
      let tot = 1e-9;
      for (let b = 0; b < nb; b++) { row.push(at(P.mix.bands[b], t)); tot += row[b]; }
      this.graph.plot(u => {
        const x = u * (nb - 1), b = Math.min(nb - 2, x | 0), g = x - b;
        const cur = (row[b] / tot) * (1 - g) + (row[b + 1] / tot) * g;
        const tv = tgt[b] * (1 - g) + tgt[b + 1] * g;
        return (cur - tv) * 7.0;
      }, mixc(COOL, HOT, hot), 0.62, 0.055, 0.55 + 0.7 * hot);
    },
    loud(t, dim, hot) {
      const v = at(P.mix.loud, t);
      this.title.set('LOUDNESS REL', 0.046, INK);
      this.value.set((v >= 0 ? '+' : '') + v.toFixed(1), 0.100, mixc(INK, HOT, hot), 0);
      this.graph.plot(u => clamp((at(P.mix.loud, t - (1 - u) * 8) + 30) / 30, 0, 1) * 2 - 1,
                      mixc(COOL, HOT, hot), 0.62, 0.052, 0.5 + 0.6 * hot);
    },
    crest(t, dim, hot) {
      const v = at(P.mix.crest, t);
      this.title.set('CREST DB', 0.046, INK);
      this.value.set(v.toFixed(1), 0.100, mixc(INK, HOT, hot), 0);
      this.graph.plot(u => clamp(at(P.mix.crest, t - (1 - u) * 8) / 24, 0, 1) * 2 - 1,
                      mixc(COOL, HOT, hot), 0.62, 0.052, 0.5 + 0.6 * hot);
    },
    chord(t, dim, hot) {
      this.title.set('HARMONY', 0.046, INK);
      let nm = '';
      for (const c of P.chords) { if (c[0] <= t) nm = c[1]; else break; }
      this.value.set(nm || '-', 0.115, mixc(INK, HOT, hot), 0);
      this.graph.plot(() => 0, [0, 0, 0], 0.001, 0.001, 0);
    },
    bar(t, dim, hot) {
      const b = atI(P.grid.bar, t), be = atI(P.grid.beat, t);
      this.title.set('BAR BEAT', 0.046, INK);
      this.value.set(b + ':' + be, 0.108, mixc(INK, HOT, hot), 0);
      this.graph.plot(() => 0, [0, 0, 0], 0.001, 0.001, 0);
    },
    section(t, dim, hot) {
      let s = D.sections[0];
      for (const x of D.sections) if (t >= x.t0 - 0.001) s = x;
      this.title.set('SECTION', 0.046, INK);
      this.value.set(s.id.replace(/-/g, ' '), 0.062, mixc(INK, HOT, hot), 0);
      this.graph.plot(u => (u < (t - s.t0) / Math.max(0.1, s.t1 - s.t0) ? 0.6 : -0.6),
                      mixc(COOL, HOT, hot), 0.62, 0.036, 0.5);
    },
  };

  const PINNED = {tempo: 0, bar: 1};        // id -> fixed row, top left
  const readouts = [], pinned = [];
  for (const spec of P.readouts) {
    if (!KIND[spec.id]) continue;
    const r = new Readout(spec, spec.id);
    r.draw = KIND[spec.id];
    if (spec.id in PINNED) {
      r.pinRow = PINNED[spec.id];
      pinned.push(r);
    } else {
      readouts.push(r);
    }
  }
  // pinned readouts skip the whole entrance mechanism
  for (const r of pinned) {
    r.e = 1; r.live = true;
    r.group.visible = true;
    r.group.position.set(-2.72, 1.02 - r.pinRow * 0.54, -3.4);
    r.group.scale.setScalar(0.86);
  }

  // ── per frame ───────────────────────────────────────────────────────────
  // Readouts are ranked by how interesting they are right now and take slots
  // in that order, so the most newsworthy thing is always at the top and the
  // column closes up as things leave.
  const ranked = [];
  function update(t, dt, showE = 1) {
    for (const r of pinned) {
      const hot = clamp(at(r.spec.interest, t), 0, 1);
      r.draw(t, 1, hot);
      const al = (0.34 + 0.20 * hot) * showE;
      r.title.laser.mat.uniforms.uAlpha.value = al * 0.70;
      r.value.laser.mat.uniforms.uAlpha.value = al;
      r.graph.laser.mat.uniforms.uAlpha.value = al * 0.80;
    }
    // Rank on a slowly-followed version of interest, not the raw value: the
    // raw series is noisy enough that two readouts sitting close together
    // would trade places several times a second.
    const k = 1 - Math.exp(-dt / 1.5);
    ranked.length = 0;
    for (const r of readouts) {
      r.rank += (at(r.spec.interest, t) - r.rank) * k;
      ranked.push(r);
    }
    ranked.sort((a, b) => (b.rank - a.rank) || (a.slot < b.slot ? -1 : 1));
    let slot = 0;
    for (const r of ranked) {
      r.showE = showE;
      r.update(t, dt, slot);
      if (r.group.visible) slot++;
    }
  }

  function setRes(w, h) {
    for (const r of [...readouts, ...pinned])
      for (const l of [r.title.laser, r.value.laser, r.graph.laser])
        l.mat.uniforms.uRes.value.set(w, h);
  }

  return {update, setRes, readouts, Label, Graph};
}
