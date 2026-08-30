const canvas = document.querySelector('#out');
const ctx = canvas.getContext('2d', {alpha: false, desynchronized: true});
const work = document.createElement('canvas');
const workCtx = work.getContext('2d', {alpha: false});
const semanticRiverLayer = document.createElement('canvas');
const semanticRiverCtx = semanticRiverLayer.getContext('2d', {alpha: false});
const receiverOpticalLayer = document.createElement('canvas');
const receiverOpticalCtx = receiverOpticalLayer.getContext('2d', {alpha: false});
const transport = document.querySelector('#transport');
const driversEl = document.querySelector('#drivers');
const captionEl = document.querySelector('#caption');
const playButton = document.querySelector('#play');
const scrub = document.querySelector('#scrub');
const clock = document.querySelector('#clock');
const sceneSelect = document.querySelector('#scene');
const loopToggle = document.querySelector('#loop');
const audio = document.querySelector('#audio');

const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, p) => a + (b - a) * p;
const smooth = x => { x = clamp(x); return x * x * (3 - 2 * x); };
const easeInOut = x => .5 - .5 * Math.cos(Math.PI * clamp(x));
const TAU = Math.PI * 2;
const hash = n => {
  const x = Math.sin(n * 127.1 + 311.7) * 43758.5453123;
  return x - Math.floor(x);
};

function graphicsBackend() {
  // Canvas2D does not expose its compositor directly. A tiny WebGL context in
  // the same Chromium GPU process does expose ANGLE's renderer, which is the
  // useful distinction here: RTX/D3D11 versus SwiftShader/software fallback.
  const probe = document.createElement('canvas');
  const gl = probe.getContext('webgl2') || probe.getContext('webgl');
  if (!gl) return 'Canvas2D · WebGL unavailable';
  const info = gl.getExtension('WEBGL_debug_renderer_info');
  const renderer = info
    ? gl.getParameter(info.UNMASKED_RENDERER_WEBGL)
    : gl.getParameter(gl.RENDERER);
  return `Canvas2D · ${renderer || 'renderer unavailable'}`;
}

const projectData = await (await fetch('/api/project', {cache: 'no-store'})).json();
const project = projectData.project;
const timeline = projectData.timeline;
const beatmap = projectData.beatmap;
const waveforms = projectData.waveforms;
const beatTimes = [...new Set((beatmap.bars || [])
  .flatMap(bar => bar.beats || [])
  .filter(Number.isFinite))].sort((a, b) => a - b);
const compiled = await (await fetch(`/projects/${project.slug}/generated/timeline.compiled.json`,
                                     {cache: 'no-store'})).json();
let performanceControls = {rate: 0, mouth: {}, signals: {}, notes: {}};
if (project.performance?.output) {
  try {
    const response = await fetch(`/projects/${project.slug}/${project.performance.output}`,
                                 {cache: 'no-store'});
    if (response.ok) performanceControls = await response.json();
  } catch (_) {
    // The scene still previews from envelopes before a project sync has built
    // the optional fine-grained performance controls.
  }
}
const motionClips = {};
for (const spec of project.motionClips || []) {
  try {
    const response = await fetch(`/projects/${project.slug}/${spec.output}`,
                                 {cache: 'no-store'});
    if (response.ok) {
      const clip = await response.json();
      clip.jointIndex = Object.fromEntries(clip.joints.map((name, index) => [name, index]));
      motionClips[spec.id] = clip;
    }
  } catch (_) {
    // Motion-driven scenes keep their environment visible if an optional clip
    // has not been generated yet.
  }
}
const tracks = Object.fromEntries(compiled.tracks.map(track => [track.id, track]));
const scenes = tracks.scenes.items;
const lyrics = tracks.lyrics.items;
const choreography = tracks.choreography?.items || [];
const transitionCues = tracks.transitions?.items || [];
const openingStartScene = scenes.find(scene => scene.id === 'scene-mteku12v');
const openingPuzzleScene = scenes.find(scene => scene.id === 'scene-mtejlbwp');
const gardenThresholdScene = scenes.find(scene => scene.id === 'scene-mtek08xn');
const gardenScene = scenes.find(scene => scene.id === 'scene-psychedelic-garden');
const patternScene = scenes.find(scene => scene.id === 'scene-pattern-aperture');
const midiNetworkScene = scenes.find(scene => scene.id === 'scene-mtejqrtr');
const receiverScene = scenes.find(scene => scene.id === 'scene-mtejt6in');
const riverScene = scenes.find(scene => scene.id === 'scene-rivers-of-mars');
const currentTurnsScene = scenes.find(scene => scene.id === 'scene-current-turns-home');
const lowLightOutroScene = scenes.find(scene => scene.id === 'scene-low-light-outro');
const signoffOutroScene = scenes.find(scene => scene.id === 'scene-mtekxa2z');
const productionCodaScene = scenes.find(scene => scene.id === 'scene-production-coda');
const marsUnmaskingScene = scenes.find(scene => scene.id === 'scene-mars-unmasking');
const semanticScene = scenes.find(scene => scene.id === 'scene-semantic-rocket-weather');
const openingSequence = openingStartScene && openingPuzzleScene ? {
  id: 'sequence-opening',
  start: openingStartScene.start,
  end: openingPuzzleScene.end,
  startSec: openingStartScene.startSec,
  endSec: openingPuzzleScene.endSec,
} : openingStartScene;
const gardenSequence = gardenThresholdScene && gardenScene ? {
  id: 'sequence-garden-intro',
  start: gardenThresholdScene.start,
  end: gardenScene.end,
  startSec: gardenThresholdScene.startSec,
  endSec: gardenScene.endSec,
} : gardenScene;
const gardenPatternSequence = gardenScene && patternScene ? {
  id: 'sequence-garden-pattern-contrast',
  start: gardenScene.start,
  end: patternScene.end,
  startSec: gardenScene.startSec,
  endSec: patternScene.endSec,
} : patternScene;
const middlePacingSequence = gardenThresholdScene && marsUnmaskingScene ? {
  id: 'sequence-garden-through-mars',
  start: gardenThresholdScene.start,
  end: marsUnmaskingScene.end,
  startSec: gardenThresholdScene.startSec,
  endSec: marsUnmaskingScene.endSec,
} : null;
const gardenPatternTransition = transitionCues.find(
  item => item.id === 'transition-garden-to-inspection');
const receiverGardenTransition = transitionCues.find(
  item => item.id === 'transition-error-lens-to-garden');
const inspectionWorldLyric = lyrics.find(item => item.id === 'lyr-030');
const riverPrototypeEnd = lyrics.find(item => item.id === 'lyr-060');
const riverWallStart = lyrics.find(item => item.id === 'lyr-058');
const chorusPlungeStart = lyrics.find(item => item.id === 'lyrics-mtejbyfp');
const riverPrototype = riverScene ? {
  id: 'sequence-river-biological-motion',
  start: riverScene.start,
  end: riverPrototypeEnd?.end || riverScene.end,
  startSec: riverScene.startSec,
  endSec: riverPrototypeEnd?.endSec || riverScene.endSec,
} : null;
const gardenRiverSequence = gardenThresholdScene && riverPrototype ? {
  id: 'sequence-garden-through-river',
  start: gardenThresholdScene.start,
  end: riverPrototype.end,
  startSec: gardenThresholdScene.startSec,
  endSec: riverPrototype.endSec,
} : null;
const riverWallSequence = riverScene && riverWallStart ? {
  id: 'sequence-spirograph-through-wall-chorus',
  start: riverWallStart.start,
  end: riverScene.end,
  startSec: riverWallStart.startSec,
  endSec: riverScene.endSec,
} : null;
const chorusAnswerSequence = currentTurnsScene && chorusPlungeStart ? {
  id: 'sequence-chorus-plunge-through-answer',
  start: chorusPlungeStart.start,
  end: currentTurnsScene.end,
  startSec: chorusPlungeStart.startSec,
  endSec: currentTurnsScene.endSec,
} : null;
const answerOutroSequence = currentTurnsScene && signoffOutroScene ? {
  id: 'sequence-answer-through-outro',
  start: '62.4.240',
  end: signoffOutroScene.end,
  startSec: choreography.find(item => item.id === 'choreo-current-03-answer-contact')?.startSec
         || currentTurnsScene.startSec,
  endSec: signoffOutroScene.endSec,
} : null;
const answerCreditsSequence = currentTurnsScene && productionCodaScene ? {
  id: 'sequence-answer-through-credits',
  start: '62.4.240',
  end: productionCodaScene.end,
  startSec: choreography.find(item => item.id === 'choreo-current-03-answer-contact')?.startSec
         || currentTurnsScene.startSec,
  endSec: productionCodaScene.endSec,
} : null;
const networkLossCue = choreography.find(item => item.id === 'choreo-midi-network-03-loss');
const networkGardenBridge = networkLossCue && gardenThresholdScene ? {
  id: 'sequence-network-loss-through-garden',
  start: networkLossCue.start,
  end: gardenThresholdScene.end,
  startSec: networkLossCue.startSec,
  endSec: gardenThresholdScene.endSec,
} : null;
const prototypeScenes = [openingSequence, midiNetworkScene, receiverScene, networkGardenBridge,
                         gardenSequence, gardenPatternSequence,
                         middlePacingSequence, gardenRiverSequence, patternScene,
                         marsUnmaskingScene, semanticScene, riverPrototype,
                         riverWallSequence, chorusAnswerSequence, answerOutroSequence,
                         answerCreditsSequence]
  .filter(Boolean);
const waveformById = Object.fromEntries(waveforms.tracks.map(track => [track.id, track]));
const duration = Math.max(compiled.timing.durationSec,
                          ...scenes.map(scene => scene.endSec || 0));
const query = new URLSearchParams(location.search);
const motionDebug = query.get('motionDebug') === '1';
let selectedScene = prototypeScenes.find(scene => scene.id === query.get('scene'))
                 || gardenSequence
                 || scenes[0];
let previewTime = selectedScene.startSec;
let offline = false;

for (const scene of prototypeScenes) {
  const option = document.createElement('option');
  option.value = scene.id;
  option.textContent = `${scene.start} · ${scene.id.replace(/^scene-/, '').replaceAll('-', ' ')}`;
  option.selected = scene.id === selectedScene.id;
  sceneSelect.append(option);
}
scrub.max = duration;
scrub.value = previewTime;

const driverRows = [
  ['lead-vocal', 'voice', '#f6c85f'],
  ['backing-vocals', 'echo', '#ffb6d6'],
  ['drums', 'drums', '#b993ff'],
  ['guitar', 'guitar', '#69e6c2'],
  ['bass', 'bass', '#ff7e67'],
  ['master', 'master', '#dbe5ff'],
];
driversEl.innerHTML = '<div class="driver-title">DAW → picture</div>' + driverRows.map(([id, label, color]) =>
  `<div class="driver" data-id="${id}"><span>${label}</span><div class="meter"><i style="--c:${color}"></i></div><b>0.00</b></div>`
).join('');

function sample(id, t, field = 'rms') {
  const track = waveformById[id];
  if (!track) return 0;
  const f = (t - track.offsetSec) * track.rate;
  if (f <= 0) return track[field]?.[0] || 0;
  const values = track[field] || track.rms;
  const a = Math.floor(f);
  if (a >= values.length - 1) return values.at(-1) || 0;
  return lerp(values[a], values[a + 1], f - a);
}

function sampleSeries(values, position) {
  if (!values?.length) return 0;
  if (position <= 0) return values[0] || 0;
  const index = Math.floor(position);
  if (index >= values.length - 1) return values.at(-1) || 0;
  return lerp(values[index], values[index + 1], position - index);
}

function mouthAt(t) {
  const position = t * (performanceControls.rate || 60);
  const rest = {open: .06, wide: .5, round: .2, teeth: 0, tongue: 0, tongue_pos: 0};
  for (const key of Object.keys(rest)) {
    const values = performanceControls.mouth?.[key];
    if (values?.length) rest[key] = sampleSeries(values, position);
  }
  return rest;
}

function signalAt(id, t) {
  const signal = performanceControls.signals?.[id];
  if (!signal) return 0;
  return sampleSeries(signal.samples, (t - signal.offsetSec) * signal.rate) / 127;
}

function rawVoiceAt(t) {
  return clamp(sample('lead-vocal', t, 'peak') * .68
             + sample('lead-vocal', t, 'rms') * .72);
}

function vocalistDynamicsAt(t) {
  const raw = rawVoiceAt(t);
  const step = .06;
  const hold = .22;
  const release = 1.18;
  let held = raw;
  let connected = true;
  let silence = 0;
  let voicedDuration = 0;
  let voicedEnergy = 0;
  for (let age = 0; age <= 2.6; age += step) {
    const value = rawVoiceAt(t - age);
    const decay = age <= hold ? 1 : Math.exp(-(age - hold) / release);
    held = Math.max(held, value * decay);
    if (!connected) continue;
    if (value > .045) {
      silence = 0;
      voicedDuration += step;
      voicedEnergy += value * step;
    } else {
      silence += step;
      if (silence > .24) connected = false;
    }
  }
  const average = voicedDuration ? voicedEnergy / voicedDuration : 0;
  const sustain = clamp(voicedDuration / 2.35) * clamp(average * 1.7);
  return {
    raw,
    held,
    sustain,
    level: clamp(held * 1.18 + sustain * .28),
  };
}

function noteEventsBetween(id, start, end) {
  const events = performanceControls.notes?.[id] || [];
  let low = 0, high = events.length;
  while (low < high) {
    const middle = (low + high) >> 1;
    if (events[middle].on < start) low = middle + 1;
    else high = middle;
  }
  const visible = [];
  for (let index = low; index < events.length && events[index].on <= end; index++) {
    visible.push({...events[index], index});
  }
  return visible;
}

function slowSample(id, t, field = 'rms', radius = .32) {
  let total = 0, weight = 0;
  for (let i = -4; i <= 4; i++) {
    const q = i / 4;
    const w = 1 - Math.abs(q) * .58;
    total += sample(id, t + q * radius, field) * w;
    weight += w;
  }
  return weight ? total / weight : 0;
}

function drumPulse(t) {
  const track = waveformById.drums;
  if (!track) return {value: 0, eventTime: t, index: 0};
  const end = Math.floor((t - track.offsetSec) * track.rate);
  let best = {value: 0, eventTime: t, index: end};
  const window = Math.round(track.rate * .72);
  for (let i = Math.max(1, end - window); i <= end; i++) {
    const peak = track.peak[i] || 0;
    const prior = track.peak[i - 1] || 0;
    const attack = clamp((peak - prior * .82) * 2.6 + peak * .28);
    const age = t - (track.offsetSec + i / track.rate);
    const value = attack * Math.exp(-age * 5.2);
    if (value > best.value) best = {value, eventTime: t - age, index: i};
  }
  return best;
}

function driversAt(t) {
  const drum = drumPulse(t);
  const vocalist = vocalistDynamicsAt(t);
  return {
    voice: clamp(sample('lead-vocal', t, 'peak') * .74 + sample('lead-vocal', t, 'rms') * .55),
    echo: clamp(sample('backing-vocals', t, 'rms') * 1.35),
    drums: clamp(drum.value * 1.6),
    drumEvent: drum,
    guitar: clamp(sample('guitar', t, 'rms') * 1.45
                  + sample('guitar', t, 'peak') * .3),
    bass: clamp(sample('bass', t, 'rms') * 1.25 + sample('bass', t, 'peak') * .22),
    master: clamp(sample('master', t, 'rms') * 1.05 + sample('master', t, 'peak') * .18),
    voiceBody: clamp(slowSample('lead-vocal', t, 'rms', .38) * 1.75),
    echoBody: clamp(slowSample('backing-vocals', t, 'rms', .46) * 1.65),
    drumBody: clamp(slowSample('drums', t, 'rms', .34) * 1.7),
    bassBody: clamp(slowSample('bass', t, 'rms', .58) * 1.55),
    masterBody: clamp(slowSample('master', t, 'rms', .72) * 1.35),
    voiceFeature: vocalist.level,
    voiceSustain: vocalist.sustain,
  };
}

function activeLyric(t) {
  return lyrics.find(item => t >= item.startSec && t < item.endSec) || null;
}

function sceneAt(t) {
  return scenes.find(item => t >= item.startSec && t < item.endSec) || scenes.at(-1);
}

function pathStroke(g, path, color, width, alpha = 1, glow = 12) {
  g.save();
  g.globalCompositeOperation = 'screen';
  g.lineCap = 'round';
  g.lineJoin = 'round';
  if (glow > 0) {
    g.strokeStyle = color;
    g.globalAlpha = alpha * .24;
    g.lineWidth = width * 4.2;
    g.filter = `blur(${glow}px)`;
    g.stroke(path);
  }
  g.filter = 'none';
  g.globalAlpha = alpha;
  g.lineWidth = width;
  g.strokeStyle = color;
  g.stroke(path);
  g.globalAlpha = alpha * .78;
  // Keep the white laser core proportional to the path. A fixed pixel floor
  // explodes when a character is drawn in its small local coordinate system
  // and the context is scaled up to the frame.
  g.lineWidth = width * .28;
  g.strokeStyle = '#fff';
  g.stroke(path);
  g.restore();
}

function depthKnockout(g, path, width, alpha) {
  if (alpha <= .001) return;
  g.save();
  g.globalCompositeOperation = 'source-over';
  g.lineCap = 'round';
  g.lineJoin = 'round';
  g.strokeStyle = '#01040a';
  g.globalAlpha = alpha;
  g.lineWidth = width;
  g.stroke(path);
  g.restore();
}

function glowDot(g, x, y, r, color, alpha = 1) {
  const gradient = g.createRadialGradient(x, y, 0, x, y, r * 5);
  gradient.addColorStop(0, color);
  gradient.addColorStop(.14, color);
  gradient.addColorStop(1, '#0000');
  g.save();
  g.globalCompositeOperation = 'screen';
  g.globalAlpha = alpha;
  g.fillStyle = gradient;
  g.beginPath();
  g.arc(x, y, r * 5, 0, TAU);
  g.fill();
  g.restore();
}

function drawAtmosphere(g, w, h, t, d, p) {
  const gradient = g.createRadialGradient(w * .5, h * .48, 1, w * .5, h * .5, w * .74);
  gradient.addColorStop(0, `rgba(${Math.round(18 + d.master * 25)},8,22,1)`);
  gradient.addColorStop(.5, '#070714');
  gradient.addColorStop(1, '#020207');
  g.fillStyle = gradient;
  g.fillRect(0, 0, w, h);

  g.save();
  g.globalCompositeOperation = 'screen';
  for (let i = 0; i < 54; i++) {
    const x = hash(i * 3.1) * w;
    const y = hash(i * 7.7 + 8) * h;
    const drift = Math.sin(t * (.06 + hash(i) * .08) + i) * h * .009;
    const r = (.35 + hash(i + 19) * 1.2) * (1 + d.master * .7);
    g.globalAlpha = .08 + hash(i + 2) * .2;
    g.fillStyle = i % 5 ? '#c7dfff' : '#ff876f';
    g.beginPath(); g.arc(x, y + drift, r, 0, TAU); g.fill();
  }
  g.restore();
}

function drawPerson(g, x, y, size, facing, color, t, voice, speaking, intent) {
  const s = size;
  const sway = Math.sin(t * 1.1 + facing) * .035 + (intent - .5) * .04;
  const wave = Math.sin(t * 3.1 + facing * 2.4) * (.16 + voice * .2);
  g.save();
  g.translate(x, y);
  g.scale(facing * s, s);
  g.rotate(sway * facing);

  const body = new Path2D();
  body.moveTo(-.01, -.18);
  body.bezierCurveTo(.09, .02, -.13, .27, .01, .56);
  pathStroke(g, body, color, 2.35 / s, .9, 13 / s);

  const head = new Path2D();
  head.moveTo(-.17, -.44);
  head.bezierCurveTo(-.21, -.65, .06, -.73, .2, -.54);
  head.bezierCurveTo(.31, -.39, .18, -.19, -.03, -.2);
  head.bezierCurveTo(-.2, -.2, -.27, -.31, -.17, -.44);
  pathStroke(g, head, color, 2.2 / s, .96, 14 / s);

  const nearArm = new Path2D();
  nearArm.moveTo(.01, -.08);
  nearArm.bezierCurveTo(.21, -.12, .33, -.35 + wave, .48, -.47 + wave * .45);
  nearArm.bezierCurveTo(.57, -.55 + wave * .2, .56, -.68 + wave * .24, .5, -.73 + wave * .18);
  pathStroke(g, nearArm, color, 2 / s, speaking ? 1 : .7, 12 / s);

  const farArm = new Path2D();
  farArm.moveTo(-.02, -.05);
  farArm.bezierCurveTo(-.19, .02, -.25, .19 - intent * .17, -.43, .11 - intent * .23);
  farArm.bezierCurveTo(-.5, .08 - intent * .2, -.53, .01 - intent * .19, -.49, -.05 - intent * .2);
  pathStroke(g, farArm, color, 1.65 / s, .6, 9 / s);

  for (const [offset, bend] of [[-.025, -.07], [.008, 0], [.038, .07]]) {
    const finger = new Path2D();
    finger.moveTo(.5, -.73 + wave * .18 + offset);
    finger.bezierCurveTo(.58, -.78 + wave * .18 + bend, .61, -.73 + bend, .64, -.67 + bend);
    pathStroke(g, finger, color, 1.05 / s, .82, 7 / s);
  }

  const leftLeg = new Path2D();
  leftLeg.moveTo(.01, .55);
  leftLeg.bezierCurveTo(-.03, .72, -.23, .82, -.28, 1.03);
  pathStroke(g, leftLeg, color, 2 / s, .82, 11 / s);
  const rightLeg = new Path2D();
  rightLeg.moveTo(.01, .55);
  rightLeg.bezierCurveTo(.14, .72, .07, .92, .24, 1.04);
  pathStroke(g, rightLeg, color, 2 / s, .82, 11 / s);

  g.fillStyle = '#f7fbff';
  g.globalAlpha = .9;
  g.beginPath(); g.arc(.055, -.49, .014, 0, TAU); g.fill();
  g.beginPath(); g.arc(.165, -.475, .012, 0, TAU); g.fill();
  const mouth = new Path2D();
  const open = speaking ? .012 + voice * .075 : .008;
  mouth.moveTo(.06, -.38);
  mouth.bezierCurveTo(.105, -.35 + open, .17, -.35 + open, .205, -.395);
  pathStroke(g, mouth, '#fff5d1', 1.3 / s, .95, 5 / s);

  if (speaking && voice > .08) {
    for (let i = 0; i < 3; i++) {
      const r = .15 + i * .1 + voice * .08;
      const phrase = new Path2D();
      phrase.moveTo(.25, -.41);
      phrase.bezierCurveTo(.32 + r * .2, -.52 - r * .15,
                           .42 + r * .42, -.28 + r * .12,
                           .51 + r, -.4 + Math.sin(t * 2 + i) * .03);
      pathStroke(g, phrase, color, (1.1 - i * .18) / s, .23 + voice * .18, 7 / s);
    }
  }
  g.restore();
}

function drawMars(g, w, h, t, d, p) {
  const cx = w * .5 + Math.sin(t * .23) * w * .006;
  const cy = h * .47 + Math.sin(t * .31) * h * .008;
  const base = Math.min(w, h) * (.235 + d.bassBody * .035);
  const reveal = smooth(p / .16);
  const innerReveal = smooth((p - .28) / .34);
  const turn = t * (.075 + d.bassBody * .018);
  const colors = ['#ff5f6f', '#ff9b68', '#ffd16b', '#59dfcc', '#7b92ff'];

  glowDot(g, cx, cy, base * .56, '#ff435f',
          reveal * (.11 + d.masterBody * .18));

  // Broad curved masses imply a planet through overlap and occlusion rather
  // than outlining a circle and decorating its centre.
  g.save();
  g.globalCompositeOperation = 'screen';
  g.lineCap = 'round';
  g.filter = `blur(${Math.round(10 + d.masterBody * 9)}px)`;
  for (let band = 0; band < 5; band++) {
    const path = new Path2D();
    const rotation = turn * (band % 2 ? -1 : 1) + band * .58;
    path.ellipse(cx, cy, base * (1.02 + band * .055),
                 base * (.18 + band * .095), rotation, 0, TAU);
    g.strokeStyle = colors[band];
    g.globalAlpha = reveal * (.035 + d.masterBody * .022);
    g.lineWidth = base * (.19 - band * .018);
    g.stroke(path);
  }
  g.restore();

  const mass = new Path2D();
  mass.moveTo(cx - base * .91, cy + base * .06);
  mass.bezierCurveTo(cx - base * .76, cy - base * .68,
                     cx - base * .19, cy - base * .93,
                     cx + base * .28, cy - base * .73);
  mass.bezierCurveTo(cx + base * .83, cy - base * .52,
                     cx + base * .94, cy + base * .02,
                     cx + base * .67, cy + base * .53);
  mass.bezierCurveTo(cx + base * .31, cy + base * .89,
                     cx - base * .42, cy + base * .77,
                     cx - base * .91, cy + base * .06);
  const gradient = g.createRadialGradient(cx - base * .18, cy - base * .2,
                                          base * .05, cx, cy, base * 1.1);
  gradient.addColorStop(0, '#7c263e');
  gradient.addColorStop(.48, '#3a102b');
  gradient.addColorStop(1, '#080618');
  g.save();
  g.globalCompositeOperation = 'source-over';
  g.globalAlpha = reveal * (.72 + d.bassBody * .12);
  g.fillStyle = gradient;
  g.fill(mass);
  g.restore();

  g.save();
  g.clip(mass);
  g.globalCompositeOperation = 'screen';
  g.lineCap = 'round';
  for (let band = 0; band < 5; band++) {
    const y = cy + (band - 2) * base * .24;
    const drift = Math.sin(turn * 1.7 + band * 1.3) * base * .12;
    const river = new Path2D();
    river.moveTo(cx - base * 1.2, y + drift);
    river.bezierCurveTo(cx - base * .58, y - base * (.24 - band * .018),
                        cx + base * .22, y + base * (.27 + band * .012),
                        cx + base * 1.2, y - drift * .7);
    g.strokeStyle = colors[(band + 1) % colors.length];
    g.globalAlpha = reveal * (.075 + innerReveal * .045);
    g.lineWidth = base * (.19 - band * .018);
    g.stroke(river);
  }
  g.restore();

  // Great-circle ribbons rotate at different inclinations. Back halves are
  // quiet; front halves carry the bright line weight and make the mass turn.
  for (let orbit = 0; orbit < 8; orbit++) {
    const family = orbit % 5;
    const rotation = turn * (orbit % 2 ? -.72 : .56) + orbit * .47;
    const rx = base * (.74 + family * .075);
    const ry = base * (.1 + (orbit % 4) * .075 + d.bassBody * .025);
    const back = new Path2D();
    back.ellipse(cx, cy, rx, ry, rotation, Math.PI, TAU);
    pathStroke(g, back, colors[family], .72 + family * .08,
               reveal * (.1 + innerReveal * .08), 5 + family * 2);
    const front = new Path2D();
    front.ellipse(cx, cy, rx, ry, rotation, 0, Math.PI);
    pathStroke(g, front, colors[family], 1.05 + family * .13 + d.drums * .48,
               reveal * (.34 + innerReveal * .28), 9 + family * 3);
  }

  // A few long S-bands provide an organic surface rhythm without reading as
  // arbitrary little marks inside a perimeter.
  for (let band = -2; band <= 2; band++) {
    const y = cy + band * base * .19;
    const span = base * (1 - Math.abs(band) * .08);
    const path = new Path2D();
    path.moveTo(cx - span, y);
    path.bezierCurveTo(cx - span * .54, y - base * (.14 + band * .018),
                       cx + span * .28, y + base * (.17 - band * .012),
                       cx + span, y - base * .025);
    pathStroke(g, path, band % 2 ? '#ff8c72' : '#ffd06a',
               1.05 + d.bassBody * .6,
               reveal * (.19 + innerReveal * .23), 8);
  }

  if (innerReveal > .01) {
    for (let arm = 0; arm < 3; arm++) {
      const a = arm / 3 * TAU + turn * .8;
      const curl = new Path2D();
      curl.moveTo(cx + Math.cos(a) * base * .38,
                  cy + Math.sin(a) * base * .3);
      curl.bezierCurveTo(cx + Math.cos(a + .62) * base * .25,
                         cy + Math.sin(a + .62) * base * .2,
                         cx + Math.cos(a + 1.45) * base * .13,
                         cy + Math.sin(a + 1.45) * base * .11,
                         cx + Math.cos(a + 2.1) * base * .055,
                         cy + Math.sin(a + 2.1) * base * .045);
      pathStroke(g, curl, colors[(arm + 3) % colors.length],
                 1.25 + d.voiceFeature,
                 innerReveal * (.38 + d.voiceFeature * .26), 11);
    }
  }
}

let marsNoteEventsCache = null;

function marsNoteEvents() {
  if (marsNoteEventsCache) return marsNoteEventsCache;
  marsNoteEventsCache = (performanceControls.notes?.['diva-notes'] || [])
    .filter(event => event.on >= marsUnmaskingScene.startSec
                  && event.on < marsUnmaskingScene.endSec)
    .map((event, index) => ({...event, index}));
  return marsNoteEventsCache;
}

function marsNoteLayout(event) {
  const pitchHeight = clamp((event.pitch - 37) / 52);
  const depth = hash(event.index * 4.19 + event.pitch * .73);
  return {pitchHeight, depth};
}

function marsNoteTrailPoint(w, h, event, u, t, shot, d) {
  const {pitchHeight, depth} = marsNoteLayout(event);
  const fromLeft = event.pitch % 2 === 0;
  const travel = fromLeft ? u : 1 - u;
  const x = lerp(-w * .14, w * 1.14, travel);
  const laneY = lerp(h * .77, h * .17, pitchHeight);
  const embrace = Math.sin(clamp(u) * Math.PI);
  const angle = (pitchHeight - .5) * 2.2 + u * (1.15 + depth * .85)
              + shot.index * .19 + t * .035;
  return {
    x: x + Math.cos(angle) * w * (.075 + depth * .105) * embrace,
    y: laneY + Math.sin(angle) * h * (.11 + depth * .16) * embrace
       + Math.sin(u * Math.PI * 2 + event.index) * h * .018 * d.bassBody,
  };
}

function drawMarsNoteTrails(g, w, h, t, d, shot, foreground = false) {
  const leadIn = 1.05;
  const tailOut = 1.55;
  const visible = marsNoteEvents().map(event => {
    const end = event.off + tailOut;
    const start = event.on - leadIn;
    return {event, start, end, progress: clamp((t - start) / (end - start)),
            ...marsNoteLayout(event)};
  }).filter(note => t >= note.start && t <= note.end
                  && (foreground ? note.depth > .54 : note.depth <= .54))
    .sort((a, b) => a.depth - b.depth);
  for (const note of visible) {
    const duration = Math.max(.08, note.event.off - note.event.on);
    const trailLength = .07 + Math.min(.9, duration) * .17;
    const points = [];
    for (let index = 0; index <= 30; index++) {
      const u = note.progress - trailLength * (1 - index / 30);
      points.push(marsNoteTrailPoint(w, h, note.event, u, t, shot, d));
    }
    const path = motionCurve(points);
    const color = NOTE_COLORS[note.event.pitch % 12];
    const onset = Math.exp(-Math.abs(t - note.event.on) * 5.2);
    const edgeFade = smooth(clamp(note.progress / .12))
                   * smooth(clamp((1 - note.progress) / .14));
    pathStroke(g, path, color, 1 + note.depth * 2.4,
               edgeFade * (.42 + note.event.velocity * .38),
               8 + note.depth * 17);
    const head = points.at(-1);
    glowDot(g, head.x, head.y, 1.4 + note.depth * 4 + onset * 2.1,
            color, edgeFade * (.38 + onset * .48));
  }
}

function drawPackets(g, w, h, t, d, p) {
  const count = 7;
  for (let i = 0; i < count; i++) {
    const phase = i / count * TAU + t * (.12 + d.bass * .09);
    const rx = w * (.25 + d.bass * .025);
    const ry = h * (.27 + d.master * .018);
    const x = w * .5 + Math.cos(phase) * rx;
    const y = h * .47 + Math.sin(phase) * ry;
    const r = (1.1 + d.drums * 1.7 + hash(i) * 1.15) * w / 1280;
    glowDot(g, x, y, r, i % 2 ? '#60e7ca' : '#ffbd63', .16 + d.echo * .19);
    const tail = new Path2D();
    tail.moveTo(x, y);
    tail.bezierCurveTo(x - Math.sin(phase) * w * .035,
                       y + Math.cos(phase) * h * .05,
                       x - Math.sin(phase) * w * .065,
                       y + Math.cos(phase) * h * .08,
                       x - Math.sin(phase) * w * .09,
                       y + Math.cos(phase) * h * .095);
    pathStroke(g, tail, i % 2 ? '#52cdbb' : '#d98c5b', .75, .23 + d.echo * .28, 6);
  }
}

const OPENING_SHOT_KINDS = ['opening-oscilloscope', 'opening-bifurcation',
                            'opening-assembly', 'opening-warm-call',
                            'opening-important-fan', 'opening-listener-crossing',
                            'opening-solid-contour', 'opening-piece-tableau',
                            'opening-fit-tests', 'opening-network-fold'];
const GARDEN_SHOT_KINDS = ['garden-threshold', 'garden-light-dolly',
                           'garden-branching-canopy', 'garden-drum-awakening'];
const MIDI_NETWORK_SHOT_KINDS = ['midi-network-pack', 'midi-network-flight',
                                 'midi-network-loss'];
const RECEIVER_SHOT_KINDS = ['receiver-empty-starfield', 'receiver-phase-demand',
                             'receiver-raw-scan', 'receiver-constructive-interference',
                             'receiver-garden-phaseplate'];
const PATTERN_SHOT_KINDS = ['inspection-delivery', 'inspection-pattern-test',
                            'inspection-world-plus', 'inspection-pre-mars'];
const RIVER_SHOT_KINDS = ['river-moon-descent', 'river-chrome-entry',
                          'river-current-macro', 'river-tail-notation',
                          'river-spirograph-bend', 'river-mouth-microcosm',
                          'river-heaven-drumwall', 'river-guitar-vault',
                          'river-chorus-plunge'];
const MARS_SHOT_KINDS = ['crane-reveal', 'overhead-rings', 'plunging-spiral',
                     'diagonal-refusal', 'counterfeit-line',
                     'overhead-excavation', 'rising-kaleidoscope'];
const SEMANTIC_SHOT_KINDS = ['semantic-call-response', 'semantic-filament-weather',
                             'semantic-rocket-overhead', 'semantic-rain-to-river'];
const CURRENT_SHOT_KINDS = ['current-switchyard-turn', 'current-following-wake',
                            'current-answer-contact'];
const OUTRO_SHOT_KINDS = ['outro-left-call', 'outro-right-response',
                          'outro-time-tunnel', 'outro-crosscut-reprise',
                          'outro-goodnight-cascade', 'outro-final-iris'];
const CODA_SHOT_KINDS = ['production-coda-title'];
const SHOT_KINDS = [...OPENING_SHOT_KINDS,
                    ...GARDEN_SHOT_KINDS, ...MIDI_NETWORK_SHOT_KINDS,
                    ...RECEIVER_SHOT_KINDS,
                    ...PATTERN_SHOT_KINDS,
                    ...MARS_SHOT_KINDS, ...SEMANTIC_SHOT_KINDS,
                    ...RIVER_SHOT_KINDS, ...CURRENT_SHOT_KINDS,
                    ...OUTRO_SHOT_KINDS, ...CODA_SHOT_KINDS];
const FALLBACK_SHOT_EDGES = [94.616667, 96.033333, 98.516667, 99.95,
                             101.55, 103.483333, 106.85, 109.15];
const productionCues = choreography
  .filter(item => item.blocking?.rendererShot && SHOT_KINDS.includes(item.blocking.rendererShot))
  .sort((a, b) => a.startSec - b.startSec);

function shotAt(t) {
  const cue = productionCues.find(item => t >= item.startSec && t < item.endSec);
  if (cue) {
    const kind = cue.blocking.rendererShot;
    const family = [OPENING_SHOT_KINDS,
                    GARDEN_SHOT_KINDS, MIDI_NETWORK_SHOT_KINDS,
                    RECEIVER_SHOT_KINDS,
                    PATTERN_SHOT_KINDS, MARS_SHOT_KINDS,
                    SEMANTIC_SHOT_KINDS, RIVER_SHOT_KINDS,
                    CURRENT_SHOT_KINDS, OUTRO_SHOT_KINDS, CODA_SHOT_KINDS]
      .find(kinds => kinds.includes(kind));
    const index = family?.indexOf(kind) ?? -1;
    return {index, kind, name: kind.replaceAll('-', ' '), cue,
            start: cue.startSec, end: cue.endSec,
            p: clamp((t - cue.startSec) / (cue.endSec - cue.startSec))};
  }
  let index = FALLBACK_SHOT_EDGES.length - 2;
  for (let i = 0; i < FALLBACK_SHOT_EDGES.length - 1; i++) {
    if (t < FALLBACK_SHOT_EDGES[i + 1]) { index = i; break; }
  }
  const start = FALLBACK_SHOT_EDGES[index], end = FALLBACK_SHOT_EDGES[index + 1];
  return {index, kind: MARS_SHOT_KINDS[index], name: MARS_SHOT_KINDS[index].replaceAll('-', ' '), start, end,
          p: clamp((t - start) / (end - start))};
}

function interactionState(shot, id) {
  const interaction = shot.cue?.blocking?.interactions?.find(item => item.id === id);
  if (!interaction) return {active: false, reach: 0, contact: 0, recoil: 0};
  const [start, end] = interaction.window || [0, 1];
  const q = clamp((shot.p - start) / Math.max(.001, end - start));
  const approach = smooth(clamp(q / .46));
  const recoil = smooth(clamp((q - .66) / .34));
  const contact = smooth(clamp((q - .38) / .16)) * (1 - smooth(clamp((q - .67) / .12)));
  return {active: shot.p >= start && shot.p <= end,
          reach: approach * (1 - recoil), contact, recoil, q, interaction};
}

function blockingPathPoint(points, progress) {
  if (!points?.length) return [50, 50];
  if (points.length === 1) return points[0];
  const scaled = clamp(progress, 0, .999999) * (points.length - 1);
  const index = Math.floor(scaled), q = scaled - index;
  return [lerp(points[index][0], points[index + 1][0], q),
          lerp(points[index][1], points[index + 1][1], q)];
}

function drawMarsFaceActor(g, x, y, size, color, t, d, phase = 0,
                           alpha = 1, cant = 0, featured = false) {
  const energy = featured ? d.voiceFeature
               : clamp(d.echoBody * .72 + d.voiceSustain * .18
                       + d.drumBody * .1);
  const billing = featured
    ? 1 + d.voiceSustain * .48 + d.voiceFeature * .16
    : 1 + d.echoBody * .16 + d.drums * .05;
  const rock = Math.sin(t * (featured ? 1.22 : .58) + phase)
             * (featured ? .12 : .045);
  const bob = Math.sin(t * (featured ? 2.04 : .83) + phase * 1.7)
            * size * (featured ? .045 : .018);
  const performanceTime = featured ? t : t + phase * .026;
  const formationWave = featured ? 1
    : 1 + Math.sin(t * 2.35 + phase * 1.6)
          * (.035 + d.drumBody * .09 + d.echoBody * .055);
  drawFrontFeatures(g, x, y + bob, size * billing * formationWave,
                    performanceTime, d, energy, color,
                    phase, alpha, cant + rock);
}

function drawChorusGlyph(g, x, y, size, rotation, color, t, d, pose = 0) {
  // Berkeley geometry comes from the ensemble positions, not from making each
  // performer a tiny anatomical doodle. Faces remain camera-addressing while
  // their paths form rings, fans, spirals, and processions.
  const cant = Math.sin(rotation) * .22
             + Math.sin(t * .31 + pose * 1.17) * .035;
  drawMarsFaceActor(g, x, y, size * 2.35, color, t, d, pose * .71,
                    .58 + d.echoBody * .38, cant, false);
}

function drawMarsFormationRibbon(g, points, color, d, alpha = .22) {
  if (!points.length) return;
  const path = motionCurve([...points, points[0], points[1] || points[0]]);
  pathStroke(g, path, color, .72 + d.bassBody * .55,
             alpha + d.masterBody * .08, 7 + d.masterBody * 7);
}

function drawExpressiveProfile(g, s, t, d, voice, color) {
  // Reuse the earlier vector vocalist's grammar: lips and upper lashes are
  // independent performance marks. Their spacing, cant, closure and mouth
  // aperture carry the expression; no dots, pupils, nose or full facial mask.
  const open = .008 + voice * .052 + d.drums * .012;
  const wide = .075 + voice * .035;
  const blink = clamp((d.drums - .62) * 2.1);
  const gaze = (d.echo - .35) * .055;
  const cant = (d.voice - .35) * .08;

  const lid = new Path2D();
  lid.moveTo(.015 + gaze, -.585);
  lid.bezierCurveTo(.065 + gaze, -.625 + blink * .025,
                    .125 + gaze, -.615 + blink * .035,
                    .17 + gaze, -.578 + blink * .008);
  lid.moveTo(.145 + gaze, -.586); lid.bezierCurveTo(.18, -.61, .19, -.62, .205, -.63);
  lid.moveTo(.153 + gaze, -.579); lid.bezierCurveTo(.19, -.585, .205, -.59, .22, -.598);
  g.save(); g.rotate(cant); pathStroke(g, lid, '#f8f1dd', 1.05 / s, .92, 4 / s); g.restore();

  const upper = new Path2D();
  upper.moveTo(.12 - wide, -.475);
  upper.bezierCurveTo(.145, -.494, .162, -.488, .177, -.477);
  upper.bezierCurveTo(.19, -.492, .214, -.488, .225 + wide * .28, -.468);
  pathStroke(g, upper, color, 1.2 / s, .96, 5 / s);
  const lower = new Path2D();
  lower.moveTo(.12 - wide, -.467);
  lower.bezierCurveTo(.15, -.45 + open, .195, -.438 + open,
                      .225 + wide * .28, -.468);
  pathStroke(g, lower, '#ffb18e', (1.15 + voice * .65) / s, .9, 5 / s);

  if (open > .035) {
    const tongue = new Path2D();
    tongue.moveTo(.148, -.454 + open * .55);
    tongue.bezierCurveTo(.17, -.444 + open, .195, -.445 + open, .211, -.458 + open * .52);
    pathStroke(g, tongue, '#ff657e', .78 / s, clamp((open - .025) * 12), 3 / s);
  }
}

function drawContourFigure(g, x, y, size, facing, color, t, d, pose = {}) {
  const s = size;
  const lean = pose.lean || 0;
  const voice = pose.speaking ? d.voice : d.echo * .45;
  const phrase = pose.speaking ? voice : d.echo;
  const reach = (pose.reach || 0) + phrase * .11 + d.drums * .055;
  const sweep = (pose.sweep || 0) + Math.sin(t * 2.1 + facing) * phrase * .075;
  const turn = pose.turn || 0;
  const kick = pose.kick || 0;
  const nod = Math.sin(t * 3.05 + facing) * phrase * .025 - d.drums * .035;
  const breath = Math.sin(t * 1.4 + facing * .6) * (.004 + phrase * .012);
  g.save();
  g.translate(x, y - breath * s);
  g.rotate(lean + nod);
  g.scale(facing * s, s);

  if (pose.detached) {
    // A performance does not require a diagram of a complete body. Keep the
    // face and hand as independent actors, with no arm segment connecting the
    // gesture back to an anatomical torso.
    const faceArc = new Path2D();
    faceArc.moveTo(-.12, -.48);
    faceArc.bezierCurveTo(-.2, -.65, -.03, -.78, .13, -.7);
    faceArc.bezierCurveTo(.23, -.65, .25, -.57, .215, -.53);
    faceArc.bezierCurveTo(.27, -.5, .255, -.445, .19, -.42);
    pathStroke(g, faceArc, color, 2.1 / s, .9, 10 / s);
    drawExpressiveProfile(g, s, t, d, voice, color);

    const hx = .53 + reach * .26 + Math.sin(t * 1.7) * phrase * .025;
    const hy = -.42 - sweep * .22 - d.drums * .035;
    g.save();
    g.translate(hx, hy);
    g.rotate(-.25 + sweep * .22 + Math.sin(t * 2.4) * phrase * .08);
    const palm = new Path2D();
    palm.moveTo(-.07, .03);
    palm.bezierCurveTo(-.04, -.055, .045, -.08, .105, -.015);
    palm.bezierCurveTo(.14, .045, .09, .11, .018, .105);
    palm.bezierCurveTo(-.045, .1, -.085, .065, -.07, .03);
    pathStroke(g, palm, color, 1.45 / s, .88, 7 / s);
    for (let i = 0; i < 4; i++) {
      const finger = new Path2D();
      const fy = -.03 + i * .028;
      finger.moveTo(.07, fy);
      finger.bezierCurveTo(.145 + i * .012, fy - .045 - phrase * .025,
                           .19 + i * .008, fy - .015,
                           .205 + i * .006, fy + .025 + d.drums * .018);
      pathStroke(g, finger, color, .8 / s, .78, 4 / s);
    }
    g.restore();

    if (voice > .05) {
      const phraseMark = new Path2D();
      phraseMark.moveTo(.22, -.45);
      phraseMark.bezierCurveTo(.35, -.54 - voice * .06, .42, -.31,
                               .58 + voice * .18, -.4 + Math.sin(t * 3) * .025);
      pathStroke(g, phraseMark, color, (1 + voice) / s, .22 + voice * .35, 6 / s);
    }
    g.restore();
    return;
  }

  const torso = new Path2D();
  torso.moveTo(-.15, -.15);
  torso.bezierCurveTo(-.24, .02, -.13 + sweep * .05, .25, -.04, .43);
  torso.bezierCurveTo(.04, .5, .19, .43, .16, .31);
  torso.bezierCurveTo(.08, .14, .23, -.02, .13, -.18);
  torso.bezierCurveTo(.04, -.26, -.08, -.24, -.15, -.15);
  g.fillStyle = '#030713d8';
  g.fill(torso);
  pathStroke(g, torso, color, 2.35 / s, .93, 11 / s);

  const head = new Path2D();
  head.moveTo(-.11, -.48);
  head.bezierCurveTo(-.2, -.64, -.04, -.79, .13, -.71);
  head.bezierCurveTo(.23, -.67, .24, -.6, .21 + turn * .025, -.56);
  head.bezierCurveTo(.255, -.545, .265, -.515, .22, -.495);
  head.bezierCurveTo(.25, -.475, .24, -.445, .195, -.43);
  head.bezierCurveTo(.18, -.35, .1, -.31, .01, -.33);
  head.bezierCurveTo(-.08, -.35, -.14, -.4, -.11, -.48);
  g.fillStyle = '#020611ed';
  g.fill(head);
  pathStroke(g, head, color, 2.15 / s, .96, 10 / s);
  drawExpressiveProfile(g, s, t, d, voice, color);

  const neck = new Path2D();
  neck.moveTo(.015, -.32);
  neck.bezierCurveTo(.01, -.25, -.02, -.2, -.05, -.16);
  pathStroke(g, neck, color, 1.15 / s, .58, 5 / s);

  const nearArm = new Path2D();
  nearArm.moveTo(.11, -.13);
  nearArm.bezierCurveTo(.29, -.08, .39 + reach * .14, -.28 - sweep * .24,
                        .58 + reach * .28, -.43 - sweep * .25);
  nearArm.bezierCurveTo(.66 + reach * .31, -.5 - sweep * .2,
                        .7 + reach * .3, -.55 - sweep * .14,
                        .76 + reach * .27, -.54 - sweep * .11);
  pathStroke(g, nearArm, color, (2.25 + voice * 1.2) / s, .96, 11 / s);

  const farArm = new Path2D();
  farArm.moveTo(-.11, -.11);
  farArm.bezierCurveTo(-.3, -.02, -.35 - sweep * .12, .15 + reach * .08,
                       -.55 - sweep * .2, .08 - reach * .12);
  pathStroke(g, farArm, color, 1.45 / s, .58, 7 / s);

  if (!pose.bust) {
    const nearLeg = new Path2D();
    nearLeg.moveTo(.06, .4);
    nearLeg.bezierCurveTo(.17, .57, .08 + kick * .18, .77,
                          .28 + kick * .36, .96 - kick * .12);
    pathStroke(g, nearLeg, color, 2.15 / s, .9, 10 / s);
    const farLeg = new Path2D();
    farLeg.moveTo(-.035, .4);
    farLeg.bezierCurveTo(-.11, .57, -.28 - kick * .06, .72,
                         -.34 - kick * .18, .94);
    pathStroke(g, farLeg, color, 1.5 / s, .65, 8 / s);
  }

  if (voice > .05) {
    const phrase = new Path2D();
    phrase.moveTo(.22, -.43);
    phrase.bezierCurveTo(.39, -.5 - voice * .08, .5, -.31 + voice * .05,
                         .72 + voice * .24, -.41 + Math.sin(t * 3) * .025);
    pathStroke(g, phrase, color, (1.05 + voice) / s, .25 + voice * .38, 7 / s);
  }
  g.restore();
}

function withCamera(g, w, h, camera, draw) {
  g.save();
  g.translate(w * .5 + (camera.x || 0), h * .5 + (camera.y || 0));
  g.rotate(camera.roll || 0);
  g.scale(camera.zoom || 1, (camera.zoom || 1) * (camera.pitch || 1));
  g.translate(-w * .5, -h * .5);
  draw();
  g.restore();
}

function drawCurvedProscenium(g, w, h, t, d, count = 12, turn = 0) {
  for (let i = 0; i < count; i++) {
    const q = (i + .5) / count;
    const x = q * w;
    const bend = Math.sin(t * .65 + i * .73 + turn) * w * (.018 + d.drums * .016);
    const path = new Path2D();
    path.moveTo(x, -h * .08);
    path.bezierCurveTo(x + bend, h * .2,
                       x - bend * 1.6, h * .7,
                       x + bend * .7, h * 1.08);
    pathStroke(g, path, i % 3 ? '#342761' : '#74558e', .65 + d.drums * .7,
               .1 + d.master * .13, 5);
  }
}

function drawPeripheralActivity(g, w, h, t, d, foreground = false) {
  // These actors spend most of their lives outside the central stage. Each
  // cycle enters from an edge, performs a parameter-specific curve in the
  // periphery, and clears the frame again. Scale and speed vary with depth so
  // the border reads as active offstage space rather than a flat decoration.
  const count = foreground ? 4 : 10;
  for (let i = 0; i < count; i++) {
    const seed = i + (foreground ? 40 : 0);
    const depth = .18 + hash(seed * 2.7) * .82;
    const speed = .028 + hash(seed * 5.1) * .035 + d.drums * .012;
    const cycle = (t * speed + hash(seed * 8.3)) % 1;
    const visit = Math.sin(cycle * Math.PI);
    const fromLeft = seed % 2 === 0;
    const penetration = w * (foreground ? .2 : .12) * visit;
    const x = fromLeft ? -w * .055 + penetration : w * 1.055 - penetration;
    const y = h * (.12 + hash(seed * 11.9) * .75)
            + Math.sin(t * (.35 + depth * .3) + seed) * h * .025;
    const size = Math.min(w, h) * (foreground ? .055 : .018 + depth * .025)
               * (1 + d.bass * .18);
    const alpha = visit * (foreground ? .18 + d.master * .18 : .12 + d.echo * .22);
    const color = seed % 3 ? '#64dfcb' : '#f0a16f';
    drawMarsFaceActor(g, x, y, size * (foreground ? 2.2 : 1.75),
                      color, t, d, seed * .83, alpha,
                      (fromLeft ? 1 : -1) * (.12 + depth * .08), false);
  }
}

function openingCamera(shot, w, h) {
  // Adjacent cues share these boundaries. Each move has a destination:
  // signal aperture, paired identities, formation, speaker, listener, pieces,
  // fit seam, and finally the existing MIDI package camera.
  const boundaries = [
    {x: 0, y: h * .035, zoom: 1.18, roll: -.055, pitch: .96},
    {x: -w * .025, y: -h * .015, zoom: 1.3, roll: .018, pitch: .92},
    {x: w * .025, y: -h * .025, zoom: 1.06, roll: -.035, pitch: .94},
    {x: 0, y: -h * .075, zoom: .84, roll: .075, pitch: .87},
    {x: w * .065, y: h * .005, zoom: 1.03, roll: .025, pitch: .94},
    {x: w * .025, y: -h * .08, zoom: .82, roll: -.085, pitch: .86},
    {x: -w * .075, y: h * .008, zoom: 1.06, roll: -.035, pitch: .93},
    {x: w * .06, y: h * .015, zoom: 1.15, roll: .06, pitch: .91},
    {x: 0, y: -h * .075, zoom: .79, roll: .115, pitch: .83},
    {x: -w * .045, y: h * .025, zoom: 1.13, roll: .018, pitch: .91},
    {x: w * .105, y: h * .022, zoom: .9, roll: -.05, pitch: .955},
  ];
  const index = Math.max(0, OPENING_SHOT_KINDS.indexOf(shot.kind));
  return mixCamera(boundaries[index], boundaries[index + 1], shot.p);
}

function fillOpeningBackground(g, w, h, t, d, shot) {
  const index = Math.max(0, OPENING_SHOT_KINDS.indexOf(shot.kind));
  const focusRight = ['opening-listener-crossing'].includes(shot.kind);
  const focusLeft = ['opening-warm-call', 'opening-important-fan',
                     'opening-solid-contour'].includes(shot.kind);
  const cx = focusRight ? w * .74 : focusLeft ? w * .25 : w * .5;
  const cy = focusRight ? h * .39 : focusLeft ? h * .53 : h * .49;
  const gradient = g.createRadialGradient(cx, cy, 1, cx, cy, w * .92);
  gradient.addColorStop(0, focusRight
    ? `rgba(10,48,62,${.72 + d.masterBody * .16})`
    : focusLeft ? `rgba(47,31,45,${.76 + d.masterBody * .15})`
                : `rgba(28,19,63,${.77 + d.masterBody * .16})`);
  gradient.addColorStop(.48, index > 6 ? '#0b0a1e' : '#080b20');
  gradient.addColorStop(1, '#010207');
  g.fillStyle = gradient;
  g.fillRect(0, 0, w, h);
}

function drawOpeningDust(g, w, h, t, d, shot, foreground = false) {
  const layers = foreground ? [{depth: 1, count: 12, speed: .026}]
                            : [{depth: .2, count: 34, speed: .0045},
                               {depth: .52, count: 24, speed: .011},
                               {depth: .78, count: 17, speed: .018}];
  const shotIndex = Math.max(0, OPENING_SHOT_KINDS.indexOf(shot.kind));
  g.save();
  g.globalCompositeOperation = 'screen';
  for (const [layerIndex, layer] of layers.entries()) {
    for (let i = 0; i < layer.count; i++) {
      const seed = i + layerIndex * 97 + (foreground ? 401 : 0);
      const direction = seed % 3 ? 1 : -1;
      const drift = t * layer.speed * direction
                  + shotIndex * layer.depth * .008;
      const x = (((hash(seed * 4.31 + 2) + drift) % 1 + 1) % 1)
              * w * 1.24 - w * .12;
      const y = h * (.05 + hash(seed * 7.11 + 8) * .88)
              + Math.sin(t * (.07 + layer.depth * .09) + seed)
                * h * (.004 + layer.depth * .012);
      const pulse = .72 + Math.sin(t * (.35 + hash(seed) * .6) + seed) * .23;
      const size = (.34 + hash(seed + 13) * 1.15)
                 * lerp(.65, foreground ? 3.1 : 2.05, layer.depth);
      const color = seed % 13 === 0 ? '#f3b46f'
                  : seed % 7 === 0 ? '#9b8cff' : '#8debe1';
      g.globalAlpha = (.055 + layer.depth * .12 + d.masterBody * .055) * pulse;
      g.fillStyle = color;
      g.beginPath();
      g.ellipse(x, y, size * (1 + layer.depth * .45), size * .58,
                hash(seed + 22) * TAU + t * .018 * direction, 0, TAU);
      g.fill();
      if (foreground && i % 4 === 0) {
        const trail = new Path2D();
        trail.moveTo(x - direction * size * 5, y + size * .35);
        trail.bezierCurveTo(x - direction * size * 2.4, y - size * .4,
                            x - direction * size, y + size * .3, x, y);
        pathStroke(g, trail, color, .55 + layer.depth,
                   (.09 + d.masterBody * .11) * pulse, 5);
      }
    }
  }
  g.restore();
}

function drawOpeningBassCurrents(g, w, h, t, d, shot) {
  const right = shot.kind === 'opening-listener-crossing';
  for (let lane = 0; lane < 5; lane++) {
    const depth = (lane + 1) / 5;
    const phase = t * (.08 + depth * .055) * (lane % 2 ? -1 : 1) + lane;
    const y = h * (.2 + lane * .15);
    const path = new Path2D();
    path.moveTo(-w * .18, y + Math.sin(phase) * h * .05);
    path.bezierCurveTo(w * .15, y - h * (.09 + depth * .045)
                               + Math.sin(phase + 1.1) * h * .04,
                        w * .62, y + h * (.1 + depth * .035)
                                + Math.cos(phase + 2.2) * h * .035,
                        w * 1.18, y - h * .035 + Math.sin(phase + 3) * h * .045);
    const color = right
      ? ['#6ce7dc', '#8498ff', '#ef9bd1'][lane % 3]
      : ['#f0be70', '#66dfd3', '#a28cff'][lane % 3];
    pathStroke(g, path, color, .55 + depth * .65 + d.bassBody * 1.1,
               .055 + depth * .045 + d.bassBody * .065, 5 + depth * 6);
  }
}

function drawOpeningDrumApertures(g, w, h, t, d, shot) {
  const low = signalMagnitude('drum-low', t, .07);
  const mid = signalMagnitude('drum-mid', t, .05);
  const high = signalMagnitude('drum-high', t, .03);
  const centres = [[-.08, .18], [1.06, .8], [.53, 1.1]];
  for (let ring = 0; ring < 10; ring++) {
    const centre = centres[ring % centres.length];
    const family = ring % 3;
    const q = (ring + 2) / 11;
    const rx = w * (.14 + q * .54 + low * .025);
    const ry = h * (.06 + q * .26 + mid * .02);
    const path = new Path2D();
    path.ellipse(w * centre[0] + Math.sin(t * .08 + ring) * w * .012,
                 h * centre[1] + Math.cos(t * .07 + ring) * h * .012,
                 rx, ry, -.28 + t * .008 * (family - 1) + ring * .025,
                 0, TAU);
    const color = ['#ffb36e', '#6ce4d8', '#9b8aff'][family];
    pathStroke(g, path, color, .6 + low * 1.6 + q * .55,
               .055 + q * .05 + high * .11, 5 + q * 7 + high * 5);
    if (high > .08 && ring % 3 === 0) {
      const angle = t * (1.2 + high) + ring;
      glowDot(g, w * centre[0] + Math.cos(angle) * rx,
              h * centre[1] + Math.sin(angle) * ry,
              1 + high * 3.2, color, .12 + high * .3);
    }
  }
}

function drawOpeningPeripheralOmens(g, w, h, t, d, shot) {
  const index = Math.max(0, OPENING_SHOT_KINDS.indexOf(shot.kind));
  const marsAlpha = index === 0 ? .06 : .1 + Math.min(.1, index * .012);
  const mars = new Path2D();
  mars.ellipse(w * (.69 + Math.sin(t * .045) * .035), h * .86,
               w * .71, h * (.17 + d.bassBody * .018),
               -.28 + t * .012, Math.PI * 1.04, Math.PI * 1.93);
  pathStroke(g, mars, '#f08f68', 2 + d.bassBody * 2.2,
             marsAlpha + d.bassBody * .04, 12);
  const inner = new Path2D();
  inner.ellipse(w * .69, h * .86, w * .56, h * .11,
                -.24 + t * .009, Math.PI * 1.06, Math.PI * 1.9);
  pathStroke(g, inner, '#ffd071', .8 + d.bassBody,
             marsAlpha * .62, 7);

  if (index < 6) return;
  const root = new Path2D();
  root.moveTo(-w * .12, h * .78);
  root.bezierCurveTo(w * .02, h * (.69 + Math.sin(t * .14) * .035),
                      w * .08, h * .57, w * .17, h * .52);
  pathStroke(g, root, '#68e2b8', 1 + d.bassBody * 1.2,
             .12 + d.masterBody * .08, 8);
  for (let branch = 0; branch < 4; branch++) {
    const startX = w * (.025 + branch * .035);
    const startY = h * (.7 - branch * .045);
    const sway = Math.sin(t * .22 + branch) * w * .012;
    const leaf = new Path2D();
    leaf.moveTo(startX, startY);
    leaf.bezierCurveTo(startX + w * .025, startY - h * .045,
                       startX + w * .06 + sway, startY - h * .065,
                       startX + w * .085 + sway, startY - h * .11);
    pathStroke(g, leaf, branch % 2 ? '#72e5cf' : '#e18fc4',
               .65 + d.drumBody * .55,
               .08 + d.drumBody * .08, 5);
  }
}

function openingSignalPoint(w, h, q, t, d) {
  const phase = q * TAU * 1.04 + t * .11;
  const delay = (q - .5) * .026;
  const guitar = signalAt('guitar', t - delay);
  const bass = signalAt('bass', t - delay * .72);
  const low = signalAt('drum-low', t - delay * .45);
  const mid = signalAt('drum-mid', t - delay * .34);
  const high = signalAt('drum-high', t - delay * .22);
  const instrumental = guitar * .044 + bass * .026
                     + low * .013 + mid * .011 + high * .009;
  return {
    x: lerp(-w * .16, w * 1.16, q),
    y: h * (.49 + Math.sin(phase) * .135
             + Math.sin(q * Math.PI * 3 - t * .07) * .035
             + instrumental * (.78 + d.masterBody * .38)),
  };
}

function openingOscilloscopeReveal(shot) {
  if (shot.kind !== 'opening-oscilloscope') return 1;
  return smooth(clamp((shot.p - .24) / .6));
}

function drawOpeningChromaticIgnition(g, w, h, t, d, shot) {
  if (shot.kind !== 'opening-oscilloscope') return;
  const p = clamp(shot.p);
  const collapse = smooth(clamp(p / .36));
  const unfurl = openingOscilloscopeReveal(shot);
  const exposure = Math.pow(1 - collapse, 1.45);
  const cx = w * .5;
  const cy = h * .49;
  const radius = lerp(Math.max(w, h) * 1.28, h * .018, collapse);
  const blooms = [
    {x: -.08, y: .18, color: [255, 196, 143]},
    {x: 1.06, y: .24, color: [151, 240, 231]},
    {x: .46, y: 1.03, color: [181, 157, 255]},
  ];

  g.save();
  g.globalCompositeOperation = 'screen';
  g.fillStyle = `rgba(216,226,255,${.72 * exposure})`;
  g.fillRect(-w, -h, w * 3, h * 3);
  for (const [index, bloom] of blooms.entries()) {
    const x = lerp(w * bloom.x, cx, collapse);
    const y = lerp(h * bloom.y, cy, collapse);
    const gradient = g.createRadialGradient(x, y, 0, x, y,
                                            radius * (1 + index * .08));
    const [r, green, b] = bloom.color;
    gradient.addColorStop(0, `rgba(${r},${green},${b},${.95 - collapse * .24})`);
    gradient.addColorStop(.28, `rgba(${r},${green},${b},${.54 * (1 - unfurl * .45)})`);
    gradient.addColorStop(1, `rgba(${r},${green},${b},0)`);
    g.fillStyle = gradient;
    g.fillRect(-w, -h, w * 3, h * 3);
  }

  // Edge light is pulled into the point along unequal curves, so the exposure
  // feels gathered rather than simply faded down.
  for (let ray = 0; ray < 16; ray++) {
    const angle = ray / 16 * TAU + .17;
    const start = {x: cx + Math.cos(angle) * w * .82,
                   y: cy + Math.sin(angle) * h * .82};
    const path = new Path2D();
    path.moveTo(start.x, start.y);
    path.bezierCurveTo(lerp(start.x, cx, .38) + Math.sin(ray) * w * .04,
                       lerp(start.y, cy, .38) + Math.cos(ray) * h * .06,
                       lerp(start.x, cx, .76) - Math.cos(ray * 1.7) * w * .025,
                       lerp(start.y, cy, .76) + Math.sin(ray * 1.4) * h * .035,
                       cx, cy);
    pathStroke(g, path, ['#ffd095', '#95f1e8', '#b29aff'][ray % 3],
               1 + (ray % 4) * .32, exposure * (.16 + collapse * .28), 12);
  }

  const pointStrength = Math.sin(clamp(collapse) * Math.PI * .82)
                      * (1 - unfurl * .52);
  glowDot(g, cx, cy, lerp(h * .34, h * .018, collapse), '#f4f3d4',
          .42 + pointStrength * .68 + d.masterBody * .14);
  glowDot(g, cx, cy, h * (.009 + pointStrength * .013), '#fff2b9',
          .84 - unfurl * .46);

  // The first outward wave is the same material that becomes the trace.
  if (unfurl > .001) {
    const ring = new Path2D();
    ring.ellipse(cx, cy, w * .47 * unfurl, h * .19 * unfurl,
                 -.08 + unfurl * .12, 0, TAU);
    pathStroke(g, ring, '#9ff4e9', 1.2 + d.guitar * 1.8,
               (1 - unfurl) * .56, 14);
  }
  g.restore();
}

function drawOpeningOscilloscope(g, w, h, t, d, shot, alpha = 1) {
  drawOpeningChromaticIgnition(g, w, h, t, d, shot);
  const reveal = openingOscilloscopeReveal(shot);
  if (reveal < .001) return;
  const origin = {x: w * .5, y: h * .49};
  const upper = [], lower = [];
  for (let index = 0; index <= 90; index++) {
    const q = index / 90;
    const signal = openingSignalPoint(w, h, q, t, d);
    const point = {x: lerp(origin.x, signal.x, reveal),
                   y: lerp(origin.y, signal.y, reveal)};
    const width = h * (.11 + d.masterBody * .035)
                * (.78 + Math.sin(q * Math.PI) * .36) * reveal;
    upper.push({x: point.x, y: point.y - width});
    lower.push({x: point.x, y: point.y + width});
  }
  const body = new Path2D();
  body.moveTo(upper[0].x, upper[0].y);
  upper.slice(1).forEach(point => body.lineTo(point.x, point.y));
  [...lower].reverse().forEach(point => body.lineTo(point.x, point.y));
  body.closePath();
  fillMembrane(g, body, '#5fcfc7', alpha * reveal * (.025 + d.masterBody * .035), 24);
  pathStroke(g, motionCurve(upper), '#f2bf70', 1.6 + d.masterBody * 2.2,
             alpha * reveal * (.58 + d.masterBody * .22), 15);
  pathStroke(g, motionCurve(lower), '#68e4d7', 1.6 + d.masterBody * 2.2,
             alpha * reveal * (.58 + d.masterBody * .22), 15);
  const core = [];
  for (let index = 0; index <= 80; index++) {
    const point = openingSignalPoint(w, h, index / 80, t + .009, d);
    core.push({x: lerp(origin.x, point.x, reveal),
               y: lerp(origin.y, point.y, reveal)});
  }
  pathStroke(g, motionCurve(core), '#aa92ff', .8 + d.guitar * 1.3,
             alpha * reveal * (.34 + d.guitar * .28), 8);
}

function drawOpeningSignalToFirstThem(g, w, h, t, d, shot, alpha = 1) {
  if (shot.kind !== 'opening-bifurcation') return;
  const morph = smooth(clamp((shot.p - .04) / .78));
  const centre = {x: w * .17, y: h * .49};
  const size = h * lerp(.24, .31, morph);
  const groups = [
    {q0: .06, q1: .37, kind: 'left-eye'},
    {q0: .63, q1: .94, kind: 'right-eye'},
    {q0: .34, q1: .67, kind: 'mouth'},
  ];
  for (const [groupIndex, group] of groups.entries()) {
    const points = [];
    for (let index = 0; index <= 22; index++) {
      const u = index / 22;
      const source = openingSignalPoint(w, h, lerp(group.q0, group.q1, u), t, d);
      let tx;
      let ty;
      if (group.kind === 'left-eye') {
        tx = centre.x + lerp(-.31, -.035, u) * size;
        ty = centre.y - (.135 + Math.sin(u * Math.PI) * .052) * size;
      } else if (group.kind === 'right-eye') {
        tx = centre.x + lerp(.035, .31, u) * size;
        ty = centre.y - (.135 + Math.sin(u * Math.PI) * .047) * size;
      } else {
        tx = centre.x + lerp(-.19, .2, u) * size;
        ty = centre.y + (.14 + Math.sin(u * TAU) * .035
                         + Math.sin(u * Math.PI) * .018) * size;
      }
      points.push({x: lerp(source.x, tx, morph),
                   y: lerp(source.y, ty, morph)});
    }
    const color = ['#f6ca7a', '#ffe0a0', '#f1b77e'][groupIndex];
    pathStroke(g, motionCurve(points), color,
               1.25 + d.guitar * 1.55 + morph * .65,
               alpha * (.46 + morph * .36), 13);
    const pulseQ = ((t * (.24 + groupIndex * .025) + groupIndex * .23) % 1 + 1) % 1;
    const pulse = points[Math.min(points.length - 1,
                                  Math.floor(pulseQ * points.length))];
    glowDot(g, pulse.x, pulse.y, 1.6 + d.drums * 2.2,
            NOTE_COLORS[(groupIndex * 4 + 2) % 12], alpha * (.22 + d.drums * .24));
  }
}

function drawOpeningSplitSignal(g, w, h, t, d, shot, alpha = 1) {
  const fork = {x: w * .5, y: h * (.49 + Math.sin(t * .16) * .018)};
  const ends = [
    {x: w * .17, y: h * .48, color: '#f2c174', side: -1},
    {x: w * .83, y: h * .37, color: '#70e7d8', side: 1},
  ];
  for (const end of ends) {
    const reveal = shot.kind === 'opening-bifurcation'
      ? end.side < 0
        ? smooth(clamp((shot.p - .4) / .48))
        : smooth(clamp((shot.p - .3) / .52))
      : 1;
    if (reveal < .001) continue;
    const path = new Path2D();
    path.moveTo(fork.x, fork.y);
    path.bezierCurveTo(w * (.5 + end.side * .11),
                       h * (.31 + end.side * .08 + Math.sin(t * .2) * .025),
                       w * (.5 + end.side * .23),
                       h * (.61 - end.side * .1 + Math.cos(t * .17) * .02),
                       end.x, end.y);
    pathStroke(g, path, end.color, 1.3 + d.bassBody * 1.5,
               alpha * reveal * (.46 + d.masterBody * .22), 12);
    for (let pulse = 0; pulse < 3; pulse++) {
      const q = ((t * (.1 + pulse * .008) + pulse / 3) % 1 + 1) % 1;
      const point = curvedPoint(fork,
        {x: w * (.5 + end.side * .11), y: h * (.31 + end.side * .08)},
        {x: w * (.5 + end.side * .23), y: h * (.61 - end.side * .1)}, end, q);
      glowDot(g, point.x, point.y, 1.5 + d.drums * 2.5,
              NOTE_COLORS[(pulse * 4 + (end.side > 0 ? 2 : 7)) % 12],
              alpha * reveal * (.2 + d.drums * .28));
    }
  }
}

function drawOpeningListenerFace(g, x, y, size, color, t, d, alpha, gaze, cant = 0) {
  // Sample the mouth from the silent beginning so the listening Them never
  // lip-syncs Them 1. Current time still drives gaze, blink, and moving hold.
  const quietTime = .25 + (t % 1) * .025;
  drawFrontFeatures(g, x, y + Math.sin(t * .63) * size * .012,
                    size, quietTime, d, d.echoBody * .22, color,
                    4.6, alpha, cant + Math.sin(t * .41) * .018, gaze);
}

function drawOpeningFaces(g, w, h, t, d, shot, alpha = 1) {
  const p = smooth(shot.p);
  let left = {x: .17, y: .49, size: .33, a: 1};
  let right = {x: .84, y: .37, size: .25, a: 1};
  let featured = false;
  if (shot.kind === 'opening-bifurcation') {
    const firstReveal = smooth(clamp((shot.p - .38) / .4));
    const secondReveal = smooth(clamp((shot.p - .58) / .34));
    left = {x: .17, y: .49, size: lerp(.24, .31, p), a: firstReveal};
    right = {x: lerp(.62, .84, secondReveal), y: lerp(.48, .37, secondReveal),
             size: lerp(.08, .24, secondReveal), a: secondReveal};
  } else if (shot.kind === 'opening-assembly') {
    left = {x: .17, y: .49, size: .34, a: 1};
    right = {x: .84, y: .37, size: .28, a: 1};
  } else if (shot.kind === 'opening-warm-call') {
    left = {x: .14, y: .49, size: .7, a: 1};
    right = {x: .86, y: .35, size: .24, a: .84};
    featured = true;
  } else if (shot.kind === 'opening-important-fan') {
    left = {x: .14, y: .48, size: .48, a: .9};
    right = {x: .89, y: .36, size: .18, a: .56};
    featured = true;
  } else if (shot.kind === 'opening-listener-crossing') {
    left = {x: lerp(.12, -.03, p), y: .52, size: lerp(.3, .18, p), a: 1 - p * .72};
    right = {x: lerp(.84, .72, p), y: lerp(.37, .42, p), size: lerp(.26, .56, p), a: 1};
  } else if (shot.kind === 'opening-solid-contour') {
    left = {x: .18, y: .48, size: .67, a: 1};
    right = {x: .93, y: .35, size: .17, a: .42};
    featured = true;
  } else if (['opening-piece-tableau', 'opening-fit-tests'].includes(shot.kind)) {
    left = {x: -.015, y: .54, size: .28, a: .66};
    right = {x: 1.015, y: .36, size: .25, a: .6};
    featured = shot.kind === 'opening-piece-tableau';
  } else if (shot.kind === 'opening-network-fold') {
    left = {x: -.04, y: .55, size: .23, a: 1 - p};
    right = {x: .91, y: .38, size: .16, a: .35 + p * .2};
  }
  drawMarsFaceActor(g, w * left.x, h * left.y, h * left.size,
                    '#f4ce83', t, d, 6.4, alpha * left.a, -.075, featured);
  const parcelGaze = shot.kind === 'opening-listener-crossing'
    ? lerp(-.08, .09, smooth(clamp((shot.p - .08) / .8))) : -.035;
  drawOpeningListenerFace(g, w * right.x, h * right.y, h * right.size,
                          '#74e8da', t, d, alpha * right.a,
                          parcelGaze, .065);
}

function openingFormationPose(index, count, w, h, t, shot, mode) {
  const angle = index / count * TAU - Math.PI * .5;
  if (mode === 'important') {
    return {x: w * .5 + Math.cos(angle + t * .025) * w * (.25 + (index % 2) * .035),
            y: h * .49 + Math.sin(angle + t * .025) * h * (.25 + (index % 3) * .02),
            rotation: angle + Math.PI * .5,
            scale: .82 + (Math.sin(angle) + 1) * .18};
  }
  if (mode === 'tableau') {
    const ring = index % 2;
    const a = angle + t * (ring ? -.045 : .035);
    return {x: w * .5 + Math.cos(a) * w * (ring ? .34 : .2),
            y: h * .5 + Math.sin(a) * h * (ring ? .29 : .18),
            rotation: a + Math.PI * .5,
            scale: ring ? .9 : 1.22};
  }
  const fanQ = index / Math.max(1, count - 1);
  const fanA = lerp(Math.PI * 1.05, Math.PI * 1.95, fanQ);
  const fan = {x: w * .5 + Math.cos(fanA) * w * .36,
               y: h * .63 + Math.sin(fanA) * h * .31,
               rotation: fanA + Math.PI * .5};
  const ringA = angle + t * .035;
  const ring = {x: w * .5 + Math.cos(ringA) * w * .29,
                y: h * .49 + Math.sin(ringA) * h * .23,
                rotation: ringA + Math.PI * .5};
  const q = smooth(shot.p);
  return {x: lerp(fan.x, ring.x, q), y: lerp(fan.y, ring.y, q),
          rotation: lerp(fan.rotation, ring.rotation, q),
          scale: .78 + (index % 3) * .13};
}

function drawOpeningFragmentFormation(g, w, h, t, d, shot, mode = 'assembly', alpha = 1) {
  const count = mode === 'tableau' ? 16 : 12;
  const points = [];
  for (let index = 0; index < count; index++) {
    points.push(openingFormationPose(index, count, w, h, t, shot, mode));
  }
  for (const parity of [0, 1]) {
    const ribbonPoints = points.filter((_, index) => index % 2 === parity)
      .map(point => ({x: point.x, y: point.y}));
    pathStroke(g, motionCurve([...ribbonPoints, ribbonPoints[0], ribbonPoints[1]]),
               parity ? '#72e0d4' : '#e7a46f', .7 + d.bassBody * .65,
               alpha * (.1 + d.masterBody * .08), 7);
  }
  points.forEach((point, index) => {
    const color = NOTE_COLORS[(index * 5 + (mode === 'important' ? 2 : 0)) % 12];
    const pulse = .45 + .55 * Math.max(0, Math.sin(t * 1.25 + index * .83));
    drawInspectionFragment(g, point.x, point.y,
                           h * .027 * point.scale * (1 + d.bassBody * .12),
                           point.rotation, color,
                           clamp(d.masterBody * .55 + d.drums * .35 + pulse * .2),
                           index, alpha * (.65 + pulse * .24));
  });
}

function openingNoteEvents(t) {
  return noteEventsBetween('diva-notes', t - 1.05, t + .72)
    .filter(event => event.off - event.on > .16 || event.velocity > .58)
    .sort((a, b) => Math.abs(a.on - t) - Math.abs(b.on - t))
    .slice(0, 7);
}

function drawOpeningNoteActors(g, w, h, t, d, shot, mode = 'speaker', alpha = 1) {
  for (const event of openingNoteEvents(t)) {
    const start = event.on - .72;
    const end = event.off + .78;
    if (t < start || t > end) continue;
    const p = clamp((t - start) / Math.max(.1, end - start));
    const pitch = clamp((event.pitch - 30) / 55);
    const depth = hash(event.index * 3.71 + event.pitch * .63);
    const side = event.pitch % 2 ? 1 : -1;
    const a = mode === 'tableau'
      ? {x: side < 0 ? -w * .1 : w * 1.1, y: h * lerp(.84, .16, pitch)}
      : {x: w * .2, y: h * (.55 + (pitch - .5) * .22)};
    const dPoint = mode === 'tableau'
      ? {x: w * (.5 + Math.cos(event.index * 1.7) * .27),
         y: h * (.5 + Math.sin(event.index * 1.7) * .22)}
      : {x: w * .82, y: h * (.37 + (pitch - .5) * .18)};
    const b = {x: lerp(a.x, dPoint.x, .32),
               y: h * (.18 + depth * .63)};
    const c = {x: lerp(a.x, dPoint.x, .73),
               y: h * (.78 - depth * .52)};
    const points = [];
    const duration = Math.max(.08, event.off - event.on);
    const trail = .05 + Math.min(1.8, duration) * .055;
    for (let index = 0; index <= 22; index++) {
      points.push(curvedPoint(a, b, c, dPoint,
        clamp(p - trail * (1 - index / 22))));
    }
    const color = NOTE_COLORS[event.pitch % 12];
    const edge = smooth(clamp(p / .12)) * smooth(clamp((1 - p) / .14));
    const onset = Math.exp(-Math.abs(t - event.on) * 5.5);
    pathStroke(g, motionCurve(points), color,
               .7 + depth * 1.4 + event.velocity,
               alpha * edge * (.27 + event.velocity * .34), 7 + depth * 9);
    const head = points.at(-1);
    glowDot(g, head.x, head.y, 1.3 + depth * 2.5 + onset * 2.4,
            color, alpha * edge * (.26 + onset * .52));
  }
}

function drawOpeningVoiceMaterial(g, w, h, t, d, shot, alpha = 1) {
  const solid = smooth(clamp((shot.p - .42) / .5));
  const points = [];
  for (let index = 0; index <= 64; index++) {
    const q = index / 64;
    const carrier = signalAt('lead-vocal', t - q * .014);
    points.push({
      x: lerp(w * .26, w * .69, q),
      y: h * (.52 - Math.sin(q * Math.PI) * .17
               + Math.sin(q * TAU * 1.3 + t * .35) * .025
               + carrier * (.006 + d.voiceFeature * .014)),
    });
  }
  const path = motionCurve(points);
  pathStroke(g, path, '#f2c377', 1 + d.voiceFeature * 2.6,
             alpha * (.38 + d.voiceSustain * .38), 11 + d.voiceFeature * 10);
  if (solid > .01) {
    const end = points.at(-1);
    drawInspectionFragment(g, end.x, end.y, h * (.038 + solid * .038),
                           -.22 + shot.p * .3, '#f2c377',
                           clamp(d.voiceFeature + solid * .35), 2,
                           alpha * solid);
  }
}

function drawOpeningParcelOmen(g, w, h, t, d, shot, alpha = 1) {
  const p = smooth(shot.p);
  const routeA = {x: w * .12, y: h * .66};
  const routeB = {x: w * .36, y: h * .35};
  const routeC = {x: w * .68, y: h * .31};
  const routeD = {x: w * 1.08, y: h * .57};
  const point = curvedPoint(routeA, routeB, routeC, routeD, p);
  const tangent = curvedTangent(routeA, routeB, routeC, routeD, p);
  const angle = Math.atan2(tangent.y, tangent.x);
  const size = h * (.055 + Math.sin(p * Math.PI) * .035);
  const route = new Path2D();
  route.moveTo(routeA.x, routeA.y);
  route.bezierCurveTo(routeB.x, routeB.y, routeC.x, routeC.y, routeD.x, routeD.y);
  pathStroke(g, route, '#78ded5', .7 + d.bassBody,
             alpha * .18, 6);
  g.save();
  g.translate(point.x, point.y);
  g.rotate(angle);
  for (let layer = 0; layer < 2; layer++) {
    const shell = new Path2D();
    shell.moveTo(-size * .8, 0);
    shell.bezierCurveTo(-size * .45, -size * (.42 + layer * .08),
                        size * .4, -size * (.32 + layer * .07), size * .75, 0);
    shell.bezierCurveTo(size * .38, size * (.32 + layer * .06),
                       -size * .42, size * (.4 + layer * .07), -size * .8, 0);
    pathStroke(g, shell, layer ? '#efb870' : '#72e4d7', 1 + d.drums,
               alpha * (.52 - layer * .12), 9);
  }
  glowDot(g, 0, 0, size * .075 * (1 + d.drums), '#a695ff', alpha * .72);
  g.restore();
}

function drawOpeningFitTests(g, w, h, t, d, shot, alpha = 1) {
  const centres = [[.25, .63], [.53, .35], [.76, .59]];
  for (let pair = 0; pair < 3; pair++) {
    const q = clamp(shot.p * 3 - pair);
    const contact = smooth(clamp(q / .62));
    const recoil = smooth(clamp((q - .72) / .28));
    const centre = centres[pair];
    const separation = w * (.13 * (1 - contact) + .018 + recoil * .065);
    const y = h * centre[1] + Math.sin(t * .3 + pair) * h * .018;
    const scale = h * (.035 + pair * .007) * (1 + d.bassBody * .12);
    const colors = [['#ef9a70', '#ffd06f'], ['#68dfb9', '#72cfe8'],
                    ['#a58fff', '#ef91c9']][pair];
    drawInspectionFragment(g, w * centre[0] - separation, y, scale,
                           .15 + pair * .28 - contact * .22, colors[0],
                           d.masterBody + contact * .2, pair, alpha * (.45 + contact * .5));
    drawInspectionFragment(g, w * centre[0] + separation, y, scale,
                           Math.PI + .2 - pair * .18 + contact * .2, colors[1],
                           d.masterBody + contact * .2, pair + 3,
                           alpha * (.45 + contact * .5));
    if (contact > .72 && recoil < .45) {
      const seam = new Path2D();
      seam.moveTo(w * centre[0], y - scale * 1.25);
      seam.bezierCurveTo(w * centre[0] - scale * .16, y - scale * .38,
                         w * centre[0] + scale * .15, y + scale * .42,
                         w * centre[0], y + scale * 1.2);
      pathStroke(g, seam, '#fff2c1', .7 + d.drums * 1.2,
                 alpha * (1 - recoil) * .52, 8);
    }
  }
  const orbitShot = {...shot, p: (shot.p + .36) % 1};
  drawOpeningFragmentFormation(g, w, h, t, d, orbitShot, 'assembly', alpha * .22);
}

function drawOpeningNetworkFold(g, w, h, t, d, shot, alpha = 1) {
  const p = smooth(shot.p);
  const fold = smooth(clamp((shot.p - .38) / .62));
  const cx = lerp(w * .54, w * .13, fold);
  const cy = lerp(h * .49, h * .55, fold);
  const radius = h * lerp(.26, .075, fold);
  const colors = ['#f0926e', '#ffd06e', '#6de1bc', '#78d4e7', '#a58dff'];
  for (let arc = 0; arc < 5; arc++) {
    const start = arc / 5 * TAU + t * (.015 + arc * .002) + fold * arc * .38;
    const path = new Path2D();
    path.ellipse(cx, cy, radius * (1.05 + arc * .045),
                 radius * (.66 + arc * .035), -.2 + fold * .16,
                 start, start + TAU * (.62 - fold * .12));
    pathStroke(g, path, colors[arc], 1 + d.bassBody * 1.3,
               alpha * (.35 + d.masterBody * .18) * (1 - fold * .42), 10);
  }
  const river = new Path2D();
  river.moveTo(cx - radius * .9, cy + radius * .1);
  river.bezierCurveTo(cx - radius * .4, cy - radius * .38,
                       cx + radius * .24, cy + radius * .43,
                       cx + radius * .88, cy - radius * .08);
  pathStroke(g, river, '#70dcd5', .9 + d.guitar * 1.2,
             alpha * (1 - fold * .5) * .48, 8);

  if (fold > .08) {
    g.save();
    g.globalAlpha = alpha * fold;
    drawMidiPackageSource(g, w, h, t, d, 0);
    g.restore();
  }
}

function drawOpeningSequence(g, w, h, t, d, shot) {
  const start = openingSequence?.startSec || 0;
  const end = openingSequence?.endSec || 29.95;
  const overall = clamp((t - start) / Math.max(.001, end - start));
  const handoff = shot.kind === 'opening-network-fold'
    ? smooth(clamp((shot.p - .58) / .42)) : 0;
  fillOpeningBackground(g, w, h, t, d, shot);
  drawOpeningDust(g, w, h, t, d, shot, false);

  if (handoff > .001) {
    g.save();
    g.globalAlpha = handoff;
    drawMidiNetworkAtmosphere(g, w, h, t, d, handoff * .04);
    g.restore();
  }

  const camera = openingCamera(shot, w, h);
  withCamera(g, w, h, camera, () => {
    drawOpeningDrumApertures(g, w, h, t, d, shot);
    drawOpeningBassCurrents(g, w, h, t, d, shot);
    drawOpeningPeripheralOmens(g, w, h, t, d, shot);

    if (shot.kind === 'opening-oscilloscope') {
      drawOpeningOscilloscope(g, w, h, t, d, shot, 1);
      drawOpeningNoteActors(g, w, h, t, d, shot, 'speaker',
                            .35 * openingOscilloscopeReveal(shot));
    } else if (shot.kind === 'opening-bifurcation') {
      drawOpeningOscilloscope(g, w, h, t, d, shot,
                              1 - smooth(clamp((shot.p - .12) / .68)));
      drawOpeningSignalToFirstThem(g, w, h, t, d, shot, 1);
      drawOpeningSplitSignal(g, w, h, t, d, shot, 1);
      drawOpeningFaces(g, w, h, t, d, shot);
      drawOpeningNoteActors(g, w, h, t, d, shot, 'speaker', .52);
    } else if (shot.kind === 'opening-assembly') {
      drawOpeningSplitSignal(g, w, h, t, d, shot, 1 - shot.p * .45);
      drawOpeningFragmentFormation(g, w, h, t, d, shot, 'assembly', 1);
      drawOpeningFaces(g, w, h, t, d, shot);
      drawOpeningNoteActors(g, w, h, t, d, shot, 'tableau', .72);
    } else if (shot.kind === 'opening-warm-call') {
      drawOpeningFaces(g, w, h, t, d, shot);
      drawOpeningSplitSignal(g, w, h, t, d, shot, .42);
      drawOpeningNoteActors(g, w, h, t, d, shot, 'speaker', .78);
    } else if (shot.kind === 'opening-important-fan') {
      drawOpeningFragmentFormation(g, w, h, t, d, shot, 'important', 1);
      drawOpeningFaces(g, w, h, t, d, shot);
      drawOpeningNoteActors(g, w, h, t, d, shot, 'tableau', .7);
    } else if (shot.kind === 'opening-listener-crossing') {
      drawOpeningParcelOmen(g, w, h, t, d, shot, 1);
      drawOpeningFaces(g, w, h, t, d, shot);
      drawOpeningNoteActors(g, w, h, t, d, shot, 'speaker', .38);
    } else if (shot.kind === 'opening-solid-contour') {
      drawOpeningFaces(g, w, h, t, d, shot);
      drawOpeningVoiceMaterial(g, w, h, t, d, shot, 1);
      drawOpeningNoteActors(g, w, h, t, d, shot, 'speaker', .58);
    } else if (shot.kind === 'opening-piece-tableau') {
      drawOpeningFragmentFormation(g, w, h, t, d, shot, 'tableau', 1);
      drawOpeningFaces(g, w, h, t, d, shot, .72);
      drawOpeningNoteActors(g, w, h, t, d, shot, 'tableau', 1);
    } else if (shot.kind === 'opening-fit-tests') {
      drawOpeningFitTests(g, w, h, t, d, shot, 1);
      drawOpeningFaces(g, w, h, t, d, shot, .55);
      drawOpeningNoteActors(g, w, h, t, d, shot, 'tableau', .45);
    } else {
      if (handoff > .05) {
        const networkShot = {kind: 'midi-network-pack', p: 0};
        const actors = midiNetworkActorsAt(midiNetworkScene?.startSec || 29.95, w, h, d);
        g.save();
        g.globalAlpha = handoff * .62;
        drawMidiRoutingNetwork(g, w, h, t, d, networkShot, actors);
        g.restore();
      }
      drawOpeningNetworkFold(g, w, h, t, d, shot, 1);
      drawOpeningFaces(g, w, h, t, d, shot, .5);
      drawOpeningNoteActors(g, w, h, t, d, shot, 'tableau', 1 - handoff * .55);
    }
  });
  drawOpeningDust(g, w, h, t, d, shot, true);
  return overall;
}

function drawOpeningFormation(g, w, h, t, d, overall, q) {
  withCamera(g, w, h, {
    x: lerp(w * .09, 0, easeInOut(q)), y: lerp(h * .08, 0, q),
    zoom: lerp(1.34, .86, easeInOut(q)), roll: lerp(-.12, .04, q), pitch: .98,
  }, () => {
    drawCurvedProscenium(g, w, h, t, d, 10, q);
    const reveal = easeInOut(q);
    drawMars(g, w, h, t, d, overall);
    const ringPoints = [];
    for (let i = 0; i < 14; i++) {
      const a = i / 14 * TAU - Math.PI * .52 + t * .13;
      const r = Math.min(w, h) * lerp(.05, .39 + (i % 2) * .06, reveal);
      const x = w * .5 + Math.cos(a) * r;
      const y = h * .48 + Math.sin(a) * r * .74;
      ringPoints.push({x, y});
      drawChorusGlyph(g, x, y,
                      Math.min(w, h) * .055, a + Math.PI * .5,
                      i % 2 ? '#ef9f67' : '#65d9c5', t, d, i);
    }
    drawMarsFormationRibbon(g, ringPoints, '#ffd06a', d, .2);
    drawMarsFaceActor(g, w * .83, h * .7, Math.min(w, h) * .42,
                      '#f1a060', t, d, .3, .96, -.08 + q * .14, true);
    drawMarsFaceActor(g, w * .15, h * .73, Math.min(w, h) * .3,
                      '#63dfca', t, d, 2.1, .78, .08, false);
  });
}

function drawOverheadFormation(g, w, h, t, d, overall, q) {
  const spin = t * (.28 + d.bass * .12) + q * .9;
  withCamera(g, w, h, {
    zoom: .86 + q * .09 + d.drums * .035, roll: spin * .12,
    pitch: .82 + Math.sin(q * Math.PI) * .08,
  }, () => {
    drawCurvedProscenium(g, w, h, t, d, 14, 2.4);
    drawMars(g, w, h, t, d, overall);
    for (let ring = 0; ring < 2; ring++) {
      const count = ring ? 18 : 10;
      const radius = Math.min(w, h) * (ring ? .42 : .29) * (1 + d.drums * .045);
      const ringPoints = [];
      for (let i = 0; i < count; i++) {
        const a = i / count * TAU + spin * (ring ? -1 : 1);
        const x = w * .5 + Math.cos(a) * radius;
        const y = h * .48 + Math.sin(a) * radius * .79;
        ringPoints.push({x, y});
        drawChorusGlyph(g, x, y,
                        Math.min(w, h) * (ring ? .043 : .052),
                        a + (ring ? -Math.PI * .5 : Math.PI * .5),
                        (i + ring) % 2 ? '#f0a169' : '#64dbc8',
                        t, d, i + ring * 20);
      }
      drawMarsFormationRibbon(g, ringPoints,
                              ring ? '#65dfcb' : '#ffab6e', d,
                              ring ? .16 : .23);
    }
  });
}

function drawSpinningFormation(g, w, h, t, d, overall, q) {
  withCamera(g, w, h, {
    zoom: lerp(.8, 1.5, easeInOut(q)), roll: lerp(-.24, .64, easeInOut(q)),
    pitch: lerp(.78, 1.02, q),
  }, () => {
    drawMars(g, w, h, t, d, overall);
    const spiralPoints = [];
    for (let i = 0; i < 26; i++) {
      const a = i / 26 * TAU + t * .48;
      const wave = .55 + .45 * Math.sin(i * 2.17 + t * 2.1);
      const r = Math.min(w, h) * (.23 + .26 * wave + q * .12);
      const x = w * .5 + Math.cos(a) * r;
      const y = h * .48 + Math.sin(a) * r * .7;
      spiralPoints.push({x, y});
      drawChorusGlyph(g, x, y,
                      Math.min(w, h) * (.035 + wave * .022),
                      a + Math.PI * .5 + q * .7,
                      i % 2 ? '#ffad69' : '#56dfc5', t, d, i);
    }
    drawMarsFormationRibbon(g, spiralPoints, '#ff77b5', d, .19);
  });
}

function drawBreakFormation(g, w, h, t, d, overall, q) {
  withCamera(g, w, h, {
    x: lerp(w * .1, -w * .08, easeInOut(q)), y: -h * .02,
    zoom: 1.05 + q * .12, roll: lerp(.18, -.22, q), pitch: .94,
  }, () => {
    drawCurvedProscenium(g, w, h, t, d, 9, 4.2);
    drawMars(g, w, h, t, d, overall);
    const diagonal = [];
    for (let i = 0; i < 12; i++) {
      const u = (i + .5) / 12;
      const x = lerp(w * .18, w * .88, u) + Math.sin(u * Math.PI) * w * .08 * q;
      const y = h * (.22 + u * .52) + Math.sin(t * 2 + i) * h * .018 * d.drums;
      diagonal.push({x, y});
      drawChorusGlyph(g, x, y, Math.min(w, h) * .05,
                      -.8 + u * 1.5, i % 2 ? '#ef9b68' : '#5cd7c2', t, d, i);
    }
    drawMarsFormationRibbon(g, diagonal, '#72ead5', d, .24);
    drawMarsFaceActor(g, lerp(-w * .04, w * .28, easeInOut(q)), h * .72,
                      Math.min(w, h) * .47, '#63dfca', t, d,
                      1.2, .98, -.2, true);
    drawMarsFaceActor(g, lerp(w * .82, w * 1.04, q), h * .7,
                      Math.min(w, h) * .32, '#f1a060', t, d,
                      2.8, .7, .16, false);
  });
}

function drawCounterfeitLine(g, w, h, t, d, overall, q) {
  withCamera(g, w, h, {
    x: lerp(w * .13, -w * .16, q), zoom: 1.08, roll: -.08 + q * .14, pitch: .9,
  }, () => {
    drawMars(g, w, h, t, d, overall);
    const procession = [];
    for (let i = 0; i < 16; i++) {
      const u = (i + q * 1.5) / 15;
      const x = u * w;
      const y = h * (.5 + Math.sin(u * TAU + t * .35) * .19);
      const flip = i % 2 ? 1 : -1;
      procession.push({x, y});
      drawChorusGlyph(g, x, y, Math.min(w, h) * (.055 + d.drums * .012),
                      flip * (.45 + q * .35),
                      i % 3 ? '#e8946a' : '#65dfca', t, d, i);
    }
    drawMarsFormationRibbon(g, procession, '#ff9b6d', d, .21);
    drawMarsFaceActor(g, w * .29, h * .72, Math.min(w, h) * .44,
                      '#62ddc6', t, d, .8, .96, -.08, true);
  });
}

function drawDigFormation(g, w, h, t, d, overall, q) {
  const spin = t * .37;
  withCamera(g, w, h, {
    zoom: lerp(1.16, .83, easeInOut(q)), roll: lerp(.22, -.18, q), pitch: .76,
  }, () => {
    drawMars(g, w, h, t, d, overall);
    for (let ring = 0; ring < 3; ring++) {
      const count = 10 + ring * 6;
      const radius = Math.min(w, h) * (.28 + ring * .115) * (1 + d.drums * .035);
      const ringPoints = [];
      for (let i = 0; i < count; i++) {
        const a = i / count * TAU + spin * (ring % 2 ? -1 : 1);
        const x = w * .5 + Math.cos(a) * radius;
        const y = h * .48 + Math.sin(a) * radius * .76;
        ringPoints.push({x, y});
        drawChorusGlyph(g, x, y,
                        Math.min(w, h) * (.05 - ring * .006), a - Math.PI * .5,
                        (i + ring) % 3 ? '#5adcc4' : '#f5a464',
                        t, d, i + ring * 30);
      }
      drawMarsFormationRibbon(g, ringPoints,
                              ring % 2 ? '#ff9d6d' : '#64e5cf', d,
                              .19 - ring * .025);
    }
    const burst = d.drumEvent;
    for (let i = 0; i < 12; i++) {
      const a = i / 12 * TAU + hash(burst.index + i) * .18;
      const r0 = Math.min(w, h) * .19;
      const r1 = r0 + Math.min(w, h) * (.08 + burst.value * .19) * (1 + i % 3 * .2);
      const path = new Path2D();
      path.moveTo(w * .5 + Math.cos(a) * r0, h * .48 + Math.sin(a) * r0 * .76);
      path.bezierCurveTo(w * .5 + Math.cos(a - .18) * lerp(r0, r1, .35),
                         h * .48 + Math.sin(a - .18) * lerp(r0, r1, .35) * .76,
                         w * .5 + Math.cos(a + .15) * lerp(r0, r1, .72),
                         h * .48 + Math.sin(a + .15) * lerp(r0, r1, .72) * .76,
                         w * .5 + Math.cos(a) * r1,
                         h * .48 + Math.sin(a) * r1 * .76);
      pathStroke(g, path, i % 2 ? '#ffd06e' : '#66efd3', 1.2 + d.drums,
                 .22 + burst.value * .38, 8);
    }
  });
}

function drawFinalKaleidoscope(g, w, h, t, d, overall, q) {
  withCamera(g, w, h, {
    zoom: lerp(1.08, .63, easeInOut(q)), roll: lerp(-.12, .48, q), pitch: .88,
  }, () => {
    drawMars(g, w, h, t, d, overall);
    for (let ring = 0; ring < 3; ring++) {
      const count = 12 + ring * 8;
      const radius = Math.min(w, h) * (.25 + ring * .14) * (1 + d.drums * .04);
      const ringPoints = [];
      for (let i = 0; i < count; i++) {
        const a = i / count * TAU + t * (.24 + ring * .05) * (ring % 2 ? -1 : 1);
        const bloom = Math.sin(q * Math.PI) * .14;
        const x = w * .5 + Math.cos(a) * radius;
        const y = h * .48 + Math.sin(a) * radius * (.72 + bloom);
        ringPoints.push({x, y});
        drawChorusGlyph(g, x, y,
                        Math.min(w, h) * (.052 - ring * .007),
                        a + (i % 2 ? Math.PI * .5 : -Math.PI * .5),
                        (i + ring) % 2 ? '#f4a267' : '#5be0c7',
                        t, d, i + ring * 40);
      }
      drawMarsFormationRibbon(g, ringPoints,
                              ring % 2 ? '#ff8e72' : '#6fe9d0', d,
                              .21 - ring * .025);
    }
  });
}

function drawGardenAtmosphere(g, w, h, t, d, overall) {
  const cx = w * (.5 + Math.sin(overall * Math.PI * 2.2) * .025);
  const cy = h * (.42 + Math.sin(overall * Math.PI * 1.4) * .018);
  const gradient = g.createRadialGradient(cx, cy, 1, cx, cy, w * .72);
  gradient.addColorStop(0, `rgba(12,${Math.round(31 + d.masterBody * 34)},38,1)`);
  gradient.addColorStop(.42, '#071518');
  gradient.addColorStop(.78, '#080815');
  gradient.addColorStop(1, '#020307');
  g.fillStyle = gradient;
  g.fillRect(0, 0, w, h);

  g.save();
  g.globalCompositeOperation = 'screen';
  for (let i = 0; i < 42; i++) {
    const z = (hash(i * 8.3) + overall * (.42 + hash(i) * .7)) % 1;
    const spread = Math.pow(z, .72);
    const x = cx + (hash(i * 4.7 + 3) - .5) * w * spread * 1.22;
    const y = cy + (hash(i * 6.1 + 9) - .35) * h * spread * .9;
    const r = (.45 + z * 1.8) * (1 + d.masterBody * .45);
    g.globalAlpha = .08 + z * .2;
    g.fillStyle = i % 4 ? '#7ce8ad' : '#ff7fb2';
    g.beginPath(); g.arc(x, y, r, 0, TAU); g.fill();
  }
  g.restore();
}

function drawGardenColorStage(g, w, h, t, d, shot, overall) {
  const cx = w * (.5 + Math.sin(t * .21) * .025);
  const cy = h * (.47 + Math.cos(t * .17) * .02);
  const bank = Math.abs(d.drumEvent.index) % 4;
  const colors = ['#ff366f', '#22d9ab', '#f4bc38', '#4d5eff'];
  const stageMass = .45 + d.drumBody * .42 + d.masterBody * .18;

  g.save();
  g.globalCompositeOperation = 'screen';
  const wash = g.createRadialGradient(cx, cy, w * .025, cx, cy, w * .78);
  wash.addColorStop(0, `${colors[bank]}32`);
  wash.addColorStop(.3, `${colors[(bank + 1) % 4]}1d`);
  wash.addColorStop(.72, `${colors[(bank + 3) % 4]}12`);
  wash.addColorStop(1, '#00000000');
  g.globalAlpha = .5 + d.drums * .24;
  g.fillStyle = wash;
  g.fillRect(0, 0, w, h);

  // A colored architectural tunnel: the drum field is the stage itself.
  for (let ring = 0; ring < 11; ring++) {
    const z = (ring / 11 + overall * .94 + t * .018) % 1;
    const depth = Math.pow(z, 1.72);
    const rx = lerp(w * .055, w * .79, depth);
    const ry = lerp(h * .035, h * .57, depth);
    const band = lerp(3, w * .075, depth) * stageMass;
    g.beginPath();
    g.ellipse(cx, cy, rx, ry, Math.sin(t * .11 + ring) * .035, 0, TAU);
    g.strokeStyle = colors[(ring + bank) % colors.length];
    g.lineWidth = band * (1 + d.drums * .17);
    g.globalAlpha = lerp(.045, .12, depth) * (1 + d.drums * .5);
    g.stroke();
  }

  // Broad rays turn drum attacks into changes of spatial illumination rather
  // than another small central pulse.
  for (let ray = 0; ray < 18; ray++) {
    const a = ray / 18 * TAU + t * .045;
    const spread = .018 + d.drums * .014;
    const reach = Math.hypot(w, h) * .86;
    const wedge = new Path2D();
    wedge.moveTo(cx, cy);
    wedge.quadraticCurveTo(cx + Math.cos(a - spread) * reach * .42,
                           cy + Math.sin(a - spread) * reach * .26,
                           cx + Math.cos(a - spread) * reach,
                           cy + Math.sin(a - spread) * reach);
    wedge.quadraticCurveTo(cx + Math.cos(a + spread) * reach * .48,
                           cy + Math.sin(a + spread) * reach * .34, cx, cy);
    g.fillStyle = colors[(ray + bank) % colors.length];
    g.globalAlpha = (ray % 3 === bank % 3 ? .026 : .011) * (1 + d.drums * 1.8);
    g.fill(wedge);
  }
  g.restore();
}

function gardenProjection(w, h, wx, wy, wz, travel, sway = 0) {
  const rel = wz - travel;
  if (rel <= .14) return null;
  const scale = 1.42 / (rel + .28);
  return {
    x: w * .5 + (wx - sway) * w * .27 * scale,
    y: h * .43 + wy * h * .24 * scale,
    scale,
    rel,
  };
}

function drawGardenLeaf(g, x, y, size, angle, color, open, alpha = .75, glow = 0) {
  if (open <= .02 || size < .35) return;
  const reach = size * smooth(open);
  const nx = Math.cos(angle), ny = Math.sin(angle);
  const tx = -ny, ty = nx;
  const tipX = x + nx * reach, tipY = y + ny * reach;
  const leaf = new Path2D();
  leaf.moveTo(x, y);
  leaf.bezierCurveTo(x + nx * reach * .38 + tx * reach * .32,
                     y + ny * reach * .38 + ty * reach * .32,
                     tipX - nx * reach * .16 + tx * reach * .18,
                     tipY - ny * reach * .16 + ty * reach * .18,
                     tipX, tipY);
  leaf.bezierCurveTo(tipX - nx * reach * .12 - tx * reach * .16,
                     tipY - ny * reach * .12 - ty * reach * .16,
                     x + nx * reach * .34 - tx * reach * .24,
                     y + ny * reach * .34 - ty * reach * .24,
                     x, y);
  if (glow > 2) {
    g.save();
    g.globalCompositeOperation = 'source-over';
    g.fillStyle = '#01040a';
    // A near leaf should interrupt the tunnel, not become an opaque cutout.
    // Keep this as a shallow local-value change; the contour supplies the
    // stronger foreground cue.
    g.globalAlpha = alpha * clamp(glow / 18) * .12;
    g.fill(leaf);
    g.restore();
  }
  g.save();
  g.globalCompositeOperation = 'screen';
  g.globalAlpha = alpha * .16;
  g.fillStyle = color;
  g.fill(leaf);
  g.restore();
  pathStroke(g, leaf, color, Math.max(.55, size * .025), alpha, glow);
}

function drawGardenBranch(g, x, y, length, angle, depth, growth, seed, color,
                          width, alpha = 1, glow = 0) {
  const stage = smooth(growth);
  if (stage <= .008 || length < 1.2) return;
  const reach = length * stage;
  const bend = (hash(seed * 2.37) - .5) * length * .38;
  const nx = Math.cos(angle), ny = Math.sin(angle);
  const tx = -ny, ty = nx;
  const ex = x + nx * reach + tx * bend * stage;
  const ey = y + ny * reach + ty * bend * stage;
  const stem = new Path2D();
  stem.moveTo(x, y);
  stem.bezierCurveTo(x + nx * reach * .28 + tx * bend * .12,
                     y + ny * reach * .28 + ty * bend * .12,
                     x + nx * reach * .72 + tx * bend * .8,
                     y + ny * reach * .72 + ty * bend * .8,
                     ex, ey);
  depthKnockout(g, stem, Math.max(.8, width * 4.2),
                alpha * clamp(glow / 15) * .48);
  pathStroke(g, stem, color, Math.max(.55, width), alpha * (.48 + depth * .1), glow);

  const leafOpen = clamp((growth - .42) * 2.2);
  if (depth <= 1 || leafOpen > .25) {
    drawGardenLeaf(g, ex, ey, length * (.2 + depth * .02),
                   angle + (hash(seed + 5) > .5 ? .62 : -.62), color, leafOpen,
                   alpha * (.46 + depth * .09), glow);
  }
  if (depth <= 0) return;
  const childGrowth = clamp((growth - .16) * 1.28);
  const split = .42 + hash(seed + 13) * .26;
  drawGardenBranch(g, ex, ey, length * (.62 + hash(seed + 2) * .08),
                   angle - split, depth - 1, childGrowth, seed + 11.7,
                   color, width * .78, alpha, glow);
  drawGardenBranch(g, ex, ey, length * (.59 + hash(seed + 7) * .1),
                   angle + split * .86, depth - 1,
                   clamp(childGrowth - .05 + hash(seed + 8) * .12), seed + 23.4,
                   color, width * .75, alpha, glow);
}

function drawGardenStemTail(g, h, x, y, length, angle, side, seed, color,
                            width, alpha, glow, projectedScale) {
  const towardCamera = hash(seed + 91.3) > .58;
  const reach = Math.max(h * (projectedScale > .62 ? .38 : .22),
                         length * (towardCamera ? 1.72 : 1.28));
  const tailAngle = angle + Math.PI;
  const normalX = -Math.sin(tailAngle), normalY = Math.cos(tailAngle);
  const position = q => {
    const along = reach * (q * .3 + q * q * .7);
    const curl = side * reach * (.12 + (towardCamera ? .19 : .08))
               * Math.sin(q * Math.PI * .82);
    const edgeward = side * reach * q * q * (towardCamera ? .42 : .21);
    return [x + Math.cos(tailAngle) * along + normalX * curl + edgeward,
            y + Math.sin(tailAngle) * along + normalY * curl
              + reach * q * q * (towardCamera ? .12 : -.055)];
  };
  // Taper with a handful of cheap direct strokes. Avoid shadowBlur here: this
  // runs for every visible plant, and dozens of filtered sub-strokes overwhelm
  // Canvas2D even on a fast GPU.
  const segments = 7;
  const strokes = [];
  for (let segment = 0; segment < segments; segment++) {
    const q0 = segment / segments, q1 = (segment + 1) / segments;
    const p0 = position(q0), p1 = position(q1);
    // Reach zero before the geometric endpoint. The invisible remaining curve
    // lets the eye complete the stem instead of reading a clipped terminal cap.
    const fade = 1 - smooth(clamp((q0 - .08) / .78));
    if (fade <= .002) continue;
    const depthScale = towardCamera ? lerp(1, 1.7, q0) : lerp(1, .18, q0);
    const path = new Path2D();
    path.moveTo(p0[0], p0[1]);
    path.quadraticCurveTo(lerp(p0[0], p1[0], .48) + normalX * reach * .006,
                          lerp(p0[1], p1[1], .48) + normalY * reach * .006,
                          p1[0], p1[1]);
    strokes.push({path, fade, depthScale});
  }
  g.save();
  g.lineCap = 'round';
  g.lineJoin = 'round';
  g.globalCompositeOperation = 'source-over';
  g.strokeStyle = '#080412';
  for (const stroke of strokes) {
    g.globalAlpha = alpha * stroke.fade * clamp(glow / 15) * .34;
    g.lineWidth = Math.max(1, width * stroke.depthScale * 3.8);
    g.stroke(stroke.path);
  }
  g.globalCompositeOperation = 'screen';
  g.strokeStyle = color;
  for (const stroke of strokes) {
    const localWidth = Math.max(.45, width * stroke.depthScale);
    g.globalAlpha = alpha * stroke.fade * clamp(glow / 15) * .12;
    g.lineWidth = localWidth * 3.2;
    g.stroke(stroke.path);
    g.globalAlpha = alpha * stroke.fade * (.45 + projectedScale * .18);
    g.lineWidth = localWidth;
    g.stroke(stroke.path);
  }
  g.restore();
}

function gardenPlant(i) {
  const side = i % 2 ? 1 : -1;
  return {
    wz: .85 + i * .63 + hash(i * 3.4) * .22,
    wx: side * (.73 + hash(i * 8.1 + 4) * 1.38),
    side,
    seed: i * 17.3 + 4,
    color: ['#69e7a7', '#3cc9b7', '#e38bb7', '#e8c56b'][i % 4],
  };
}

function drawGardenPlants(g, w, h, t, d, shot, overall, travel, group) {
  const sway = Math.sin(overall * TAU * 1.12) * .18;
  const plants = [];
  for (let i = 0; i < 25; i++) {
    const plant = gardenPlant(i);
    const projected = gardenProjection(w, h, plant.wx, .82, plant.wz, travel, sway);
    if (!projected || projected.x < -w * .7 || projected.x > w * 1.7) continue;
    const band = projected.rel > 4.2 ? 'far' : projected.rel > 1.55 ? 'mid' : 'near';
    if (band !== group) continue;
    plants.push({...plant, projected});
  }
  plants.sort((a, b) => b.projected.rel - a.projected.rel);
  for (const plant of plants) {
    const p = plant.projected;
    const spatialGrowth = clamp((7.2 - p.rel) / 3.7 + d.drumBody * .2);
    const length = h * (.3 + hash(plant.seed) * .13) * p.scale;
    const leadOpening = interactionState(shot, 'lead-opens-canopy').reach;
    const lightCoax = interactionState(shot, 'green-light-coaxes-growth').reach;
    const fanLaunch = interactionState(shot, 'drums-launch-branch-fans').reach;
    const reaction = leadOpening * .3 + lightCoax * .18 + fanLaunch * .22;
    const angle = -Math.PI * .5 - plant.side * (.12 + hash(plant.seed + 2) * .16 + reaction);
    const cycle = t * (.44 + d.drumBody * .06) + plant.seed * .071;
    const generation = Math.floor(cycle);
    const phase = cycle - generation;
    const oldAlpha = 1 - smooth(clamp((phase - .18) / .78));
    const newAlpha = smooth(clamp(phase / .62));
    const depth = clamp((p.scale - .18) / 1.05);
    const width = Math.max(.55, h * .0032 * p.scale * (1 + d.bassBody * .24));
    const glow = lerp(0, 14, depth) * (.6 + d.masterBody * .55);
    drawGardenStemTail(g, h, p.x, p.y, length, angle, plant.side,
                       plant.seed + generation * 31.7, plant.color, width,
                       .68 + newAlpha * .24, glow, p.scale);
    // The mature generation is pressed down and out of the composition while
    // a new, slightly different recursive generation grows through it.
    drawGardenBranch(g, p.x + plant.side * length * phase * .018,
                     p.y + length * phase * .11, length, angle,
                     p.rel < 1.25 ? 3 : 2, spatialGrowth,
                     plant.seed + generation * 31.7, plant.color, width,
                     oldAlpha * .72, glow);
    drawGardenBranch(g, p.x, p.y, length, angle,
                     p.rel < 1.25 ? 3 : 2, spatialGrowth * smooth(phase),
                     plant.seed + (generation + 1) * 31.7, plant.color, width,
                     newAlpha, glow);
  }
}

function drawFrontFeatures(g, x, y, size, t, d, energy, color,
                           phase = 0, alpha = 1, rotation = 0,
                           gazeOverride = null) {
  const s = Math.max(4, size);
  const mouth = mouthAt(t);
  const blink = clamp((d.drums - .7) * 2.8 + Math.sin(t * .83 + phase) > .985 ? .8 : 0);
  const gaze = gazeOverride ?? (Math.sin(t * .47 + phase) * .025
                              + (d.echo - .35) * .035);
  const eyeLift = (energy - .25) * .035;
  g.save();
  g.translate(x, y);
  g.rotate(rotation);
  g.scale(s, s);

  for (const side of [-1, 1]) {
    const cx = side * .18 + gaze;
    const lid = new Path2D();
    lid.moveTo(cx - .105, -.09 + eyeLift);
    lid.bezierCurveTo(cx - .045, -.15 + blink * .055,
                      cx + .055, -.15 + blink * .055,
                      cx + .112, -.085 + eyeLift);
    lid.moveTo(cx - .1, -.082 + eyeLift);
    lid.bezierCurveTo(cx - .02, -.025 - blink * .018,
                      cx + .06, -.025 - blink * .018,
                      cx + .108, -.08 + eyeLift);
    lid.moveTo(cx + side * .085, -.105 + eyeLift);
    lid.bezierCurveTo(cx + side * .125, -.155,
                      cx + side * .145, -.16,
                      cx + side * .17, -.145);
    pathStroke(g, lid, '#f8f2df', 1.22 / s, alpha * .92, 4 / s);
  }

  const open = .006 + mouth.open * .13 + energy * .024;
  const wide = .12 + mouth.wide * .115 - mouth.round * .035;
  const upper = new Path2D();
  const lower = new Path2D();
  const points = 64;
  for (let index = 0; index <= points; index++) {
    const q = index / points * 2 - 1;
    const arch = 1 - q * q;
    const carrier = signalAt('lead-vocal', t - q * .0065);
    const ripple = carrier * (.0018 + energy * .0072) * Math.sin(Math.PI * (index / points));
    const px = q * wide;
    const upperY = .15 - arch * (.022 + mouth.wide * .024) + ripple;
    const lowerY = .15 + arch * open - ripple * .72;
    if (!index) { upper.moveTo(px, upperY); lower.moveTo(px, lowerY); }
    else { upper.lineTo(px, upperY); lower.lineTo(px, lowerY); }
  }
  pathStroke(g, upper, color, 1.45 / s, alpha, 5 / s);
  pathStroke(g, lower, '#ff9cae', (1.25 + energy * .55) / s, alpha * .95, 5 / s);
  if (mouth.teeth > .16 && open > .025) {
    const teeth = new Path2D();
    teeth.moveTo(-wide * .72, .151 + open * .18);
    teeth.bezierCurveTo(-wide * .2, .164 + open * .12,
                         wide * .2, .164 + open * .12, wide * .72, .151 + open * .18);
    pathStroke(g, teeth, '#fff9e9', .62 / s, alpha * mouth.teeth, 2 / s);
  }
  if (mouth.tongue > .08 && open > .035) {
    const tongue = new Path2D();
    const tongueX = mouth.tongue_pos * wide * .2;
    tongue.moveTo(-wide * .48 + tongueX, .15 + open * .66);
    tongue.bezierCurveTo(-wide * .12 + tongueX, .15 + open * .82,
                         wide * .2 + tongueX, .15 + open * .78,
                         wide * .48 + tongueX, .15 + open * .61);
    pathStroke(g, tongue, '#ff5f8b', .8 / s, alpha * mouth.tongue, 3 / s);
  }
  g.restore();
}

const NOTE_COLORS = [
  '#7cf0cf', '#8de5ff', '#aab8ff', '#c9a4ff', '#ef9cdc', '#ff9cae',
  '#ffb889', '#f4d873', '#bfe878', '#82ef9f', '#72edcf', '#7edff3',
];

function drawGardenMidiNotes(g, w, h, t, d, shot, front = false) {
  // Notes are occasional scene actors, not a permanent piano roll. The green
  // light and waking sections get exact DAW-note seeds; the denser canopy is
  // left free for the vocalist and foliage.
  if (!['garden-light-dolly', 'garden-drum-awakening'].includes(shot.kind)) return;
  const leadIn = .86;
  const trail = .72;
  const candidates = noteEventsBetween('diva-notes', t - 1.55, t + leadIn)
    .filter(event => {
      const duration = event.off - event.on;
      return duration > .52 || event.velocity > .76
          || (event.index + event.pitch * 3) % 4 === 0;
    })
    .sort((a, b) => Math.abs(t - a.on) - Math.abs(t - b.on))
    .slice(0, 9);
  for (const event of candidates) {
    const start = event.on - leadIn;
    const end = event.off + trail;
    if (t < start || t > end) continue;
    const duration = Math.max(.04, event.off - event.on);
    const arrival = smooth(clamp((t - start) / leadIn));
    const departure = smooth(clamp((t - event.off) / trail));
    const depth = clamp(arrival * (1 - departure * .22));
    if ((depth > .57) !== front) continue;
    const pitch = clamp((event.pitch - 45) / 42);
    const side = (event.pitch + event.index) % 2 ? 1 : -1;
    const sourceX = w * (.5 + Math.sin(event.index * 1.73) * .035);
    const sourceY = h * (.43 + Math.cos(event.pitch * .81) * .025);
    const targetX = w * (.5 + side * (.16 + pitch * .2));
    const targetY = h * (.61 - pitch * .36);
    const bow = Math.sin(arrival * Math.PI) * side;
    const x = lerp(sourceX, targetX, arrival) + bow * w * .105
            + side * departure * w * .36;
    const y = lerp(sourceY, targetY, arrival)
            - Math.sin(arrival * Math.PI * 1.4) * h * .07
            - departure * h * (.11 + pitch * .09);
    const velocity = clamp(event.velocity);
    const scale = lerp(.24, 1.08, depth) * (1 - departure * .42);
    const size = Math.min(w, h) * (.017 + velocity * .022) * scale;
    const elongation = 1 + Math.min(1.4, duration) * .48;
    const onset = Math.exp(-Math.abs(t - event.on) * 7.5);
    const color = NOTE_COLORS[event.pitch % 12];
    const rotation = side * (.35 + arrival * .9) + departure * side * 1.2;

    g.save();
    g.translate(x, y);
    g.rotate(rotation);
    const seed = new Path2D();
    seed.moveTo(-size * elongation, 0);
    seed.bezierCurveTo(-size * .45, -size * (.72 + velocity * .25),
                        size * .52, -size * .62, size * elongation, 0);
    seed.bezierCurveTo(size * .48, size * (.54 + duration * .16),
                       -size * .5, size * .7, -size * elongation, 0);
    g.globalCompositeOperation = 'screen';
    g.globalAlpha = .055 + velocity * .09 + onset * .1;
    g.fillStyle = color;
    g.fill(seed);
    pathStroke(g, seed, color, .7 + scale * 1.45,
               .28 + velocity * .47 + onset * .2, 5 + depth * 12);
    const wake = new Path2D();
    wake.moveTo(-size * elongation * 1.15, 0);
    wake.bezierCurveTo(-size * (2.4 + duration), side * size * .8,
                       -size * (3.2 + duration), -side * size * .55,
                       -size * (4.1 + duration), side * size * .2);
    pathStroke(g, wake, color, .55 + velocity, .12 + velocity * .23, 4 + depth * 6);
    g.restore();
    if (onset > .08) glowDot(g, x, y, size * (1.2 + onset * 1.8), color,
                             onset * (.28 + velocity * .45));
  }
}

function drawFeaturedGardenVocalist(g, w, h, t, d, shot, reveal) {
  const level = d.voiceFeature;
  const sustain = d.voiceSustain;
  const lyric = activeLyric(t);
  const lyricIndex = lyric ? lyrics.indexOf(lyric) : -1;
  let spin = 0;
  if (lyric && lyricIndex >= 0 && lyricIndex % 4 === 0) {
    const spinProgress = clamp((t - lyric.startSec - .08) / .7);
    const anticipation = spinProgress < .16
      ? -Math.sin(spinProgress / .16 * Math.PI) * .13 : 0;
    spin = smooth(spinProgress) * TAU + anticipation;
  }
  const rock = Math.sin(t * 2.15) * (.065 + sustain * .055)
             + Math.sin(t * 4.3 + .8) * .025
             + (d.drumEvent.index % 2 ? 1 : -1) * d.drums * .055;
  const x = w * (.5 + Math.sin(t * .79) * .17
            + Math.sin(t * 1.63) * .025
            + (shot.kind === 'garden-drum-awakening' ? .09 : 0));
  const y = h * (.325 + Math.sin(t * 1.08) * .065
            + Math.sin(t * 3.15) * .018 - level * .032 - d.drums * .025);
  const size = Math.min(w, h)
             * (.22 + level * .38 + sustain * .09 + d.drums * .025);
  const alpha = reveal * (.48 + level * .46 + sustain * .08);

  g.save();
  g.globalCompositeOperation = 'screen';
  g.translate(x, y);
  g.scale(1.45, .72);
  const bloom = g.createRadialGradient(0, 0, size * .04, 0, 0, size * .88);
  bloom.addColorStop(0, `rgba(255,213,137,${.2 + level * .2})`);
  bloom.addColorStop(.34, `rgba(255,137,182,${.08 + sustain * .1})`);
  bloom.addColorStop(1, '#0000');
  g.fillStyle = bloom;
  g.beginPath();
  g.arc(0, 0, size * .92, 0, TAU);
  g.fill();
  g.restore();
  drawFrontFeatures(g, x, y, size, t, d, level, '#ffd786', 0,
                    alpha, rock + spin);
}

function drawGardenSwirlField(g, w, h, t, d, front = false) {
  const count = front ? 3 : 5;
  for (let ribbon = 0; ribbon < count; ribbon++) {
    const side = ribbon % 2 ? 1 : -1;
    const phase = t * (.46 + ribbon * .035) * side + ribbon * 1.37;
    const cx = side < 0 ? -w * (.08 + ribbon * .035) : w * (1.08 + ribbon * .025);
    const cy = h * (.18 + ribbon * .17) + Math.sin(phase * .71) * h * .12;
    const rx = w * (.46 + ribbon * .055) * (1 + d.bassBody * .11);
    const ry = h * (.24 + ribbon * .025);
    const path = new Path2D();
    const points = 130;
    for (let index = 0; index <= points; index++) {
      const u = index / points;
      const a = u * TAU * (1.12 + ribbon * .08) + phase;
      const bassWave = signalAt('bass', t - u * .085 - ribbon * .011);
      const ripple = bassWave * h * (.004 + d.bassBody * .012) * Math.sin(u * Math.PI);
      const x = cx + Math.cos(a) * rx + Math.sin(a * 2.03) * rx * .18;
      const y = cy + Math.sin(a * (1.43 + ribbon * .03)) * ry
              + Math.cos(a) * ripple;
      if (!index) path.moveTo(x, y); else path.lineTo(x, y);
    }
    const colors = ['#ff6cae', '#62efc7', '#edc857', '#846cff', '#5ea7ff'];
    const alpha = (front ? .18 : .11) + d.bassBody * (front ? .34 : .24);
    pathStroke(g, path, colors[ribbon % colors.length],
               (front ? 1.25 : .8) + d.bassBody * 1.8, alpha, front ? 14 : 5);
  }
}

function drawGardenSwirlActors(g, w, h, t, d, shot, front = false) {
  const colors = ['#ff96c8', '#75f2d0', '#ffd166', '#8e86ff', '#65b9ff', '#f77b63'];
  const voidPull = interactionState(shot, 'void-draws-counterorbit').reach;
  for (let i = 0; i < 7; i++) {
    const life = (shot.p * 1.36 + i / 7 + (front ? .13 : 0)) % 1;
    const depth = Math.sin(life * Math.PI);
    if ((depth > .56) !== front) continue;
    const spin = i / 7 * TAU + life * TAU * (i % 2 ? 1.05 : -.92);
    const radius = lerp(w * .72, w * (.2 - voidPull * .045), depth);
    const x = w * .5 + Math.cos(spin) * radius;
    const y = h * .47 + Math.sin(spin) * radius * .47;
    const size = Math.min(w, h) * lerp(.055, .16, depth);
    const path = new Path2D();
    for (let j = 0; j <= 32; j++) {
      const q = j / 32;
      const curl = q * Math.PI * 1.45 + spin;
      const response = Math.sin(q * Math.PI) * (.16 + d.echoBody * .12);
      const px = x + Math.cos(curl) * size * (q - .4) + Math.sin(curl * 1.7) * size * response;
      const py = y + Math.sin(curl) * size * .72 * (q - .4)
               + Math.cos(curl * 1.31) * size * response;
      if (!j) path.moveTo(px, py); else path.lineTo(px, py);
    }
    pathStroke(g, path, colors[i % colors.length],
               .8 + depth * 2.1 + d.echoBody * .8,
               .18 + depth * .5, front ? 15 : 4);
    if (front && i % 3 === 0) {
      drawFrontFeatures(g, x, y, size * .82, t, d, d.echoBody,
                        colors[i % colors.length], i, .18 + depth * .38,
                        spin + Math.PI * .5);
    }
  }
}

function drawGardenFeatureOrbit(g, w, h, t, d, shot, front = false) {
  const count = 8;
  const voidPull = interactionState(shot, 'void-draws-counterorbit').reach;
  for (let i = 0; i < count; i++) {
    const direction = i % 2 ? 1 : -1;
    const a = i / count * TAU + direction * t * (.24 + d.echo * .12);
    const depth = .5 + .5 * Math.sin(a);
    if ((depth > .52) !== front) continue;
    const recoil = voidPull * (i % 2 ? 1 : -.42);
    const x = w * .5 + Math.cos(a) * w * (.55 + (i % 3) * .018 + recoil * .11);
    const y = h * .46 + Math.sin(a) * h * (.36 + recoil * .07);
    const size = Math.min(w, h) * (.07 + depth * .045);
    drawFrontFeatures(g, x, y, size, t, d, d.echoBody * .72,
                      i % 2 ? '#ffc0df' : '#7cf0cf', i * .91,
                      .25 + d.echoBody * .5, recoil * .18);
  }
}

function drawInteractionScore(g, w, h, t, d, shot) {
  const blocking = shot.cue?.blocking;
  if (!blocking?.interactions?.length) return;
  const elements = Object.fromEntries((blocking.elements || []).map(item => [item.id, item]));
  const colors = ['#ffd166', '#69efc8', '#ff7fb4', '#8c87ff'];
  for (let index = 0; index < blocking.interactions.length; index++) {
    const interaction = blocking.interactions[index];
    const state = interactionState(shot, interaction.id);
    if (!state.active || state.reach < .015) continue;
    const initiator = elements[interaction.initiator], responder = elements[interaction.responder];
    if (!initiator || !responder) continue;
    const a0 = blockingPathPoint(initiator.path, shot.p);
    const b0 = blockingPathPoint(responder.path, shot.p);
    const a = [w * a0[0] / 100, h * a0[1] / 100];
    const b = [w * b0[0] / 100, h * b0[1] / 100];
    const dx = b[0] - a[0], dy = b[1] - a[1], distance = Math.hypot(dx, dy) || 1;
    const normal = [-dy / distance, dx / distance];
    const bow = normal.map(value => value * distance * (.12 + index * .025));
    const control = [(a[0] + b[0]) * .5 + bow[0], (a[1] + b[1]) * .5 + bow[1]];
    const color = colors[index % colors.length];
    for (const [from, reverse] of [[a, false], [b, true]]) {
      const reach = clamp(state.reach * (reverse ? .94 : 1.08));
      const path = new Path2D();
      for (let step = 0; step <= 28; step++) {
        let q = step / 28 * reach * .54;
        if (reverse) q = 1 - q;
        const iq = 1 - q;
        const x = iq * iq * a[0] + 2 * iq * q * control[0] + q * q * b[0];
        const y = iq * iq * a[1] + 2 * iq * q * control[1] + q * q * b[1];
        if (!step) path.moveTo(x, y); else path.lineTo(x, y);
      }
      pathStroke(g, path, color, 1 + d.masterBody * 1.5,
                 .25 + state.contact * .55, 8 + state.contact * 12);
    }
    if (state.contact > .02) {
      const q = .5, iq = .5;
      glowDot(g, iq * iq * a[0] + 2 * iq * q * control[0] + q * q * b[0],
              iq * iq * a[1] + 2 * iq * q * control[1] + q * q * b[1],
              2.5 + state.contact * 7, color, state.contact);
    }
  }
}

function drawGardenDrumStage(g, w, h, t, d, overall, travel, awakening) {
  const p = gardenProjection(w, h, 0, .68, travel + 2.35, travel,
                             Math.sin(overall * TAU * 1.12) * .18);
  if (!p) return;
  const r = w * .28 * p.scale;
  const hit = d.drums;
  const bank = d.drumEvent.index % 4;
  g.save();
  g.globalCompositeOperation = 'screen';
  const stageFill = g.createRadialGradient(p.x, p.y, r * .04, p.x, p.y, r * 1.75);
  stageFill.addColorStop(0, `rgba(255,220,110,${.1 + d.drumBody * .14})`);
  stageFill.addColorStop(.38, `rgba(58,226,177,${.07 + d.drumBody * .09})`);
  stageFill.addColorStop(1, '#0000');
  g.fillStyle = stageFill;
  g.beginPath(); g.ellipse(p.x, p.y, r * 1.78, r * .72, 0, 0, TAU); g.fill();
  g.restore();
  glowDot(g, p.x, p.y, Math.max(2, r * (.08 + hit * .08)), '#86ffb7', .26 + hit * .5);
  for (let ring = 0; ring < 4; ring++) {
    const pulse = 1 + hit * (.18 + ring * .11);
    const root = new Path2D();
    root.ellipse(p.x, p.y, r * pulse * (1 + ring * .28),
                 r * (.24 + d.bass * .07) * pulse * (1 + ring * .17),
                 Math.sin(t * .17) * .08, 0, TAU);
    pathStroke(g, root, ring === bank ? '#f4dd73' : '#4ee0b0',
               1.5 + d.drumBody * 5 + hit * 2.1,
               .24 + d.drumBody * .14 + hit * (.36 - ring * .04), ring ? 7 : 15);
  }
  for (let i = 0; i < 12; i++) {
    const a = i / 12 * TAU;
    const open = .25 + (i % 4 === bank ? hit * .92 : hit * .18);
    const x = p.x + Math.cos(a) * r * 1.15;
    const y = p.y + Math.sin(a) * r * .34;
    drawGardenLeaf(g, x, y, r * (.45 + open * .35), a - Math.PI * .5,
                   i % 2 ? '#e98db9' : '#f2ce72', .45 + open, .5 + open * .3);
  }
  const membrane = new Path2D();
  membrane.moveTo(p.x - r * .65, p.y);
  membrane.bezierCurveTo(p.x - r * .3, p.y - r * (.22 + hit * .12),
                          p.x + r * .28, p.y + r * (.16 + hit * .1),
                          p.x + r * .68, p.y);
  pathStroke(g, membrane, '#fff3b0', 1 + hit * 2.5, .45 + hit * .46, 8);

  if (awakening > 0) {
    const wakeY = p.y - r * (1.05 + awakening * .42);
    const wake = new Path2D();
    wake.moveTo(p.x - r * .2, wakeY + r * .38);
    wake.bezierCurveTo(p.x - r * (.42 + awakening * .1), wakeY,
                        p.x - r * .1, wakeY - r * .58,
                        p.x + r * .12, wakeY - r * .44);
    wake.bezierCurveTo(p.x + r * .38, wakeY - r * .27,
                        p.x + r * .34, wakeY + r * .25,
                        p.x + r * .08, wakeY + r * .42);
    wake.bezierCurveTo(p.x - r * .02, wakeY + r * .58,
                        p.x - r * .12, wakeY + r * .5,
                        p.x - r * .2, wakeY + r * .38);
    g.save(); g.fillStyle = '#010307e8'; g.fill(wake); g.restore();
    pathStroke(g, wake, '#78e8bd', .8 + d.master * .8, awakening * .4, 5);
  }
}

function drawGardenLight(g, w, h, t, d, shot, overall, travel) {
  const sway = Math.sin(overall * TAU * 1.12) * .18;
  const wz = Math.max(6.35, travel + 2.1);
  const coax = interactionState(shot, 'green-light-coaxes-growth');
  const voidPull = interactionState(shot, 'void-draws-counterorbit');
  const wx = Math.sin(t * .73) * .48 + Math.sin(t * .19) * .16
           + coax.reach * .65 - voidPull.reach * .32;
  const p = gardenProjection(w, h, wx, .22 + Math.sin(t * .51) * .12, wz, travel, sway);
  if (!p) return;
  const r = Math.max(2, Math.min(w, h) * (.014 + d.voice * .009) * clamp(p.scale, .4, 1.2));
  const trail = new Path2D();
  trail.moveTo(p.x, p.y);
  trail.bezierCurveTo(p.x - w * .035, p.y + h * .02,
                      p.x + w * .025, p.y + h * .07,
                      p.x - w * (.05 + d.echo * .04), p.y + h * .095);
  pathStroke(g, trail, '#62ff92', 1 + d.voiceBody * 1.2,
             .35 + d.voiceBody * .35, 8 + coax.contact * 9);
  glowDot(g, p.x, p.y, r * (1 + coax.contact * .8), '#66ff99',
          .72 + d.voiceBody * .25);
}

function drawGardenFrame(g, w, h, t, d, shot) {
  const start = gardenSequence?.startSec ?? gardenScene?.startSec ?? t;
  const end = gardenSequence?.endSec ?? gardenScene?.endSec ?? (t + 1);
  const overall = clamp((t - start) / Math.max(.001, end - start));
  const travel = overall * 6.55;
  drawGardenAtmosphere(g, w, h, t, d, overall);
  drawGardenColorStage(g, w, h, t, d, shot, overall);
  drawGardenSwirlField(g, w, h, t, d, false);
  drawGardenPlants(g, w, h, t, d, shot, overall, travel, 'far');
  drawGardenMidiNotes(g, w, h, t, d, shot, false);
  drawGardenSwirlActors(g, w, h, t, d, shot, false);
  drawGardenFeatureOrbit(g, w, h, t, d, shot, false);
  const awakening = shot.kind === 'garden-drum-awakening'
    ? smooth((shot.p - .08) / .72) : 0;
  drawGardenDrumStage(g, w, h, t, d, overall, travel, awakening);
  drawGardenPlants(g, w, h, t, d, shot, overall, travel, 'mid');
  drawGardenLight(g, w, h, t, d, shot, overall, travel);
  drawInteractionScore(g, w, h, t, d, shot);

  const featureReveal = smooth((overall - .3) / .16);
  if (featureReveal > 0) {
    drawFeaturedGardenVocalist(g, w, h, t, d, shot, featureReveal);
  }
  drawGardenSwirlActors(g, w, h, t, d, shot, true);
  drawGardenFeatureOrbit(g, w, h, t, d, shot, true);
  drawGardenMidiNotes(g, w, h, t, d, shot, true);
  drawGardenSwirlField(g, w, h, t, d, true);
  drawGardenPlants(g, w, h, t, d, shot, overall, travel, 'near');
  return overall;
}

let midiNetworkMetaCache = null;

function midiNetworkMeta() {
  if (midiNetworkMetaCache) return midiNetworkMetaCache;
  const all = performanceControls.notes?.['diva-notes'] || [];
  const groups = new Map();
  all.forEach((event, index) => {
    if (!midiNetworkScene || event.on < midiNetworkScene.startSec
        || event.on >= midiNetworkScene.endSec) return;
    const key = event.on.toFixed(4);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push({event, index});
  });
  const byIndex = new Map();
  [...groups.values()].forEach((group, groupIndex) => {
    group.sort((a, b) => a.event.pitch - b.event.pitch);
    group.forEach((entry, ordinal) => byIndex.set(entry.index, {
      groupIndex, ordinal, count: group.length,
    }));
  });
  midiNetworkMetaCache = {byIndex, groups: [...groups.values()]};
  return midiNetworkMetaCache;
}

function curvedPoint(a, b, c, d, p) {
  const q = 1 - p;
  return {
    x: q * q * q * a.x + 3 * q * q * p * b.x + 3 * q * p * p * c.x + p * p * p * d.x,
    y: q * q * q * a.y + 3 * q * q * p * b.y + 3 * q * p * p * c.y + p * p * p * d.y,
  };
}

function curvedTangent(a, b, c, d, p) {
  const q = 1 - p;
  return {
    x: 3 * q * q * (b.x - a.x) + 6 * q * p * (c.x - b.x)
       + 3 * p * p * (d.x - c.x),
    y: 3 * q * q * (b.y - a.y) + 6 * q * p * (c.y - b.y)
       + 3 * p * p * (d.y - c.y),
  };
}

function midiNetworkRoute(event, meta, w, h, d) {
  const pitch = clamp((event.pitch - 37) / 41);
  const chordOffset = meta.count > 1
    ? (meta.ordinal / Math.max(1, meta.count - 1) - .5) : 0;
  const lane = (event.pitch + meta.groupIndex) % 5;
  const lateEcho = event.on >= 36.4;
  if (lateEcho) {
    const side = lane % 2 ? 1 : -1;
    return {
      preA: {x: side > 0 ? w * 1.09 : w * .66, y: side > 0 ? h * .18 : h * 1.08},
      source: {x: side > 0 ? w * .9 : w * .58, y: side > 0 ? h * .22 : h * .88},
      b: {x: w * (.72 + side * .05), y: h * (.18 + pitch * .58)},
      c: {x: w * (.46 - side * .04), y: h * (.78 - pitch * .5)},
      junction: {x: w * .33, y: h * (.26 + lane * .11)},
      exitB: {x: w * .16, y: h * (.18 + pitch * .46)},
      exitC: {x: -w * .02, y: h * (.42 + chordOffset * .22)},
      exit: {x: -w * .13, y: h * (.24 + lane * .13)},
      lateEcho,
    };
  }
  const targetY = h * lerp(.75, .2, pitch) + chordOffset * h * .055;
  const direction = lane % 2 ? 1 : -1;
  return {
    preA: {x: -w * .13, y: h * (.57 + chordOffset * .08)},
    source: {x: w * .14, y: h * (.55 + chordOffset * .08)},
    b: {x: w * .31, y: targetY + direction * h * (.11 + d.bassBody * .035)},
    c: {x: w * .52, y: targetY - direction * h * (.13 + d.bassBody * .045)},
    junction: {x: w * .68, y: targetY + Math.sin(meta.groupIndex * 1.7) * h * .075},
    exitB: {x: w * .78, y: targetY - direction * h * .18},
    exitC: {x: lane === 0 || lane === 3 ? w * .72 : w * .98,
            y: lane < 2 ? -h * .08 : h * 1.08},
    exit: {x: lane === 0 || lane === 3 ? w * .57 : w * 1.13,
           y: lane < 2 ? -h * .18 : h * 1.18},
    lateEcho,
  };
}

function midiNetworkActorsAt(t, w, h, d) {
  const metaCache = midiNetworkMeta();
  const leadIn = .55;
  const release = .68;
  const events = noteEventsBetween('diva-notes', t - 2.35, t + leadIn)
    .filter(event => midiNetworkScene
      && event.on >= midiNetworkScene.startSec
      && event.on < midiNetworkScene.endSec)
    .slice(-28);
  const actors = [];
  for (const event of events) {
    const meta = metaCache.byIndex.get(event.index);
    if (!meta) continue;
    const start = event.on - leadIn;
    const end = event.off + release;
    if (t < start || t > end) continue;
    const route = midiNetworkRoute(event, meta, w, h, d);
    let point, tangent, stage;
    if (t < event.on) {
      const p = smooth((t - start) / leadIn);
      const b = {x: lerp(route.preA.x, route.source.x, .42),
                 y: route.preA.y - h * .08};
      const c = {x: lerp(route.preA.x, route.source.x, .76),
                 y: route.source.y + h * .05};
      point = curvedPoint(route.preA, b, c, route.source, p);
      tangent = curvedTangent(route.preA, b, c, route.source, p);
      stage = 'approach';
    } else if (t <= event.off) {
      const duration = Math.max(.08, event.off - event.on);
      const p = smooth((t - event.on) / duration);
      point = curvedPoint(route.source, route.b, route.c, route.junction, p);
      tangent = curvedTangent(route.source, route.b, route.c, route.junction, p);
      stage = 'sustain';
    } else {
      const p = smooth((t - event.off) / release);
      point = curvedPoint(route.junction, route.exitB, route.exitC, route.exit, p);
      tangent = curvedTangent(route.junction, route.exitB, route.exitC, route.exit, p);
      stage = 'release';
    }
    const normalLength = Math.hypot(tangent.x, tangent.y) || 1;
    const chordSpread = Math.min(w, h) * (.012 + meta.count * .0018);
    const chordOffset = (meta.ordinal - (meta.count - 1) * .5) * chordSpread;
    point.x += -tangent.y / normalLength * chordOffset;
    point.y += tangent.x / normalLength * chordOffset;
    actors.push({event, meta, route, point, tangent, stage});
  }
  return actors;
}

function drawMidiNetworkAtmosphere(g, w, h, t, d, local) {
  const gradient = g.createRadialGradient(w * .36, h * .48, 0,
                                           w * .36, h * .48, w * .86);
  gradient.addColorStop(0, `rgba(34,25,73,${.78 + d.masterBody * .18})`);
  gradient.addColorStop(.42, '#090c28');
  gradient.addColorStop(.78, '#030712');
  gradient.addColorStop(1, '#010207');
  g.fillStyle = gradient;
  g.fillRect(0, 0, w, h);

  g.save();
  g.globalCompositeOperation = 'screen';
  for (let index = 0; index < 36; index++) {
    const depth = .2 + hash(index * 2.7) * .8;
    const x = w * ((hash(index * 4.3 + 9) + local * depth * .08) % 1);
    const y = h * (.08 + hash(index * 5.1 + 3) * .78);
    g.globalAlpha = .025 + depth * .08;
    g.fillStyle = index % 3 ? '#8a9cff' : '#f58fc9';
    g.beginPath();
    g.ellipse(x, y, .5 + depth * 1.2, .35 + depth * .55,
              hash(index) * TAU, 0, TAU);
    g.fill();
  }
  g.restore();
}

function drawMidiRoutingNetwork(g, w, h, t, d, shot, actors) {
  const loss = shot.kind === 'midi-network-loss';
  const laneColors = ['#76f2d1', '#8edfff', '#aaa4ff', '#ee91d1', '#ff9b9d'];
  for (let lane = 0; lane < 7; lane++) {
    const f = lane / 6;
    const path = new Path2D();
    path.moveTo(-w * .08, h * (.23 + f * .56));
    path.bezierCurveTo(w * (.2 + Math.sin(lane) * .06),
                        h * (.08 + (1 - f) * .72 + d.bassBody * .04),
                        w * (.52 + Math.cos(lane * 1.4) * .08),
                        h * (.17 + f * .58 - d.bassBody * .045),
                        w * .69, h * (.18 + ((lane * 3) % 7) / 6 * .62));
    path.bezierCurveTo(w * .82, h * (lane % 2 ? -.08 : 1.08),
                        w * (lane % 3 ? 1.02 : .62),
                        h * (lane < 3 ? -.12 : 1.12),
                        lane % 3 ? w * 1.12 : w * .54,
                        lane < 3 ? -h * .18 : h * 1.18);
    pathStroke(g, path, laneColors[lane % laneColors.length],
               .55 + d.bassBody * .8,
               (loss ? .055 : .1) + d.masterBody * .08, 4 + d.bassBody * 5);
  }

  const nodes = [
    [.14, .55], [.32, .27], [.37, .72], [.53, .43], [.68, .25], [.69, .64], [.89, .53],
  ];
  const eventAge = t - d.drumEvent.eventTime;
  const pulse = eventAge >= 0 && eventAge < .65 ? 1 - smooth(eventAge / .65) : 0;
  nodes.forEach(([nx, ny], index) => {
    const actorNear = actors.some(actor => Math.hypot(actor.point.x - nx * w,
                                                       actor.point.y - ny * h) < w * .07);
    const r = Math.min(w, h) * (.018 + (actorNear ? .018 : 0) + pulse * .008);
    const gate = new Path2D();
    gate.ellipse(nx * w, ny * h, r * (1.4 + d.bassBody * .22),
                 r * (.55 + (actorNear ? .28 : 0)),
                 -.35 + index * .21, 0, TAU);
    pathStroke(g, gate, laneColors[index % laneColors.length],
               .7 + (actorNear ? 1.2 : 0),
               .18 + (actorNear ? .42 : 0) + pulse * .18, 7 + actorNear * 7);
  });

  const receptorEnergy = actors.reduce((best, actor) =>
    Math.max(best, clamp(1 - Math.hypot(actor.point.x - w * .9,
                                        actor.point.y - h * .53) / (w * .18))), 0);
  const receptor = new Path2D();
  receptor.ellipse(w * .91, h * .53, w * (.055 + receptorEnergy * .018),
                   h * (.13 - receptorEnergy * .035), .12, 0, TAU);
  pathStroke(g, receptor, '#ffd286', 1 + receptorEnergy * 1.5,
             .12 + receptorEnergy * .34, 9);
  const empty = new Path2D();
  empty.moveTo(w * .865, h * .53);
  empty.bezierCurveTo(w * .885, h * (.49 - receptorEnergy * .02),
                       w * .93, h * (.57 + receptorEnergy * .02),
                       w * .952, h * .53);
  pathStroke(g, empty, '#ffd286', .7, loss ? .22 : .09, 4);
}

function drawMidiChordHarnesses(g, actors, w, h) {
  const groups = new Map();
  for (const actor of actors) {
    if (actor.meta.count < 3) continue;
    const key = actor.event.on.toFixed(4);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(actor);
  }
  for (const group of groups.values()) {
    group.sort((a, b) => a.event.pitch - b.event.pitch);
    if (group.length < 2) continue;
    const path = new Path2D();
    group.forEach((actor, index) => {
      const {x, y} = actor.point;
      if (!index) path.moveTo(x, y);
      else {
        const prior = group[index - 1].point;
        path.bezierCurveTo(lerp(prior.x, x, .36), prior.y - h * .018,
                           lerp(prior.x, x, .68), y + h * .018, x, y);
      }
    });
    const force = Math.min(1, group.length / 10);
    pathStroke(g, path, '#eef5ff', .55 + force * 1.2,
               .08 + force * .28, 6 + force * 9);
  }
}

function drawMidiNoteActor(g, actor, w, h, t) {
  const {event, meta, point, tangent, stage} = actor;
  const duration = Math.max(.01, event.off - event.on);
  const velocity = clamp((event.velocity - .22) / .58);
  const pitch = clamp((event.pitch - 37) / 41);
  const color = NOTE_COLORS[event.pitch % 12];
  const onset = Math.exp(-Math.abs(t - event.on) * 9);
  const release = stage === 'release' ? clamp((t - event.off) / .68) : 0;
  const chordAttenuation = 1 / (1 + Math.max(0, meta.count - 1) * .075);
  const colorBody = lerp(.92, .68, clamp(meta.count / 10));
  const size = Math.min(w, h) * (.024 + velocity * .028)
             * (1 + Math.min(10, meta.count) * .018);
  const length = size * (1.5 + Math.min(1.62, duration) * 2.4);
  const angle = Math.atan2(tangent.y, tangent.x);
  g.save();
  g.translate(point.x, point.y);
  g.rotate(angle);
  const body = new Path2D();
  body.moveTo(-length, 0);
  body.bezierCurveTo(-length * .65, -size * (.72 + pitch * .2),
                      size * .12, -size * (.58 + velocity * .32), size, 0);
  body.bezierCurveTo(size * .1, size * (.48 + duration * .14),
                     -length * .55, size * (.62 + velocity * .2), -length, 0);
  g.globalCompositeOperation = 'screen';
  g.globalAlpha = colorBody * (.1 + velocity * .18 + onset * .06)
                * (1 - release * .58);
  g.fillStyle = color;
  g.fill(body);
  pathStroke(g, body, color, 1.05 + velocity * 2.1,
             chordAttenuation * (.34 + velocity * .31 + onset * .11)
               * (1 - release * .5),
             5 + velocity * 8);
  const sustainLine = new Path2D();
  sustainLine.moveTo(-length * .9, 0);
  sustainLine.bezierCurveTo(-length * .48, Math.sin(t * 13 + event.pitch) * size * .12,
                            -length * .1, -Math.sin(t * 11 + event.pitch) * size * .1,
                            size * .72, 0);
  pathStroke(g, sustainLine, '#fff9ea', .55 + velocity * .55,
             chordAttenuation * (.14 + velocity * .24) * (1 - release), 3);
  g.restore();
  if (onset > .06) glowDot(g, point.x, point.y,
                           size * (1.2 + onset * 1.9), color,
                           chordAttenuation * onset * (.24 + velocity * .38));
}

function drawMidiPackageSource(g, w, h, t, d, local) {
  const open = smooth(local / .22);
  const x = w * .13, y = h * .55;
  for (let layer = 0; layer < 4; layer++) {
    const path = new Path2D();
    const r = Math.min(w, h) * (.065 + layer * .019);
    path.moveTo(x - r, y + r * .12);
    path.bezierCurveTo(x - r * .55, y - r * (1 + open * .25),
                        x + r * .52, y - r * (.8 + open * .34),
                        x + r, y - r * .08);
    path.bezierCurveTo(x + r * .45, y + r * (.64 + open * .28),
                        x - r * .5, y + r * (.78 + open * .2),
                        x - r, y + r * .12);
    pathStroke(g, path, layer % 2 ? '#ff91cf' : '#79e9d3',
               .75 + d.masterBody, (.15 + d.voiceBody * .16) * (1 - layer * .12), 7);
  }
}

function mixCamera(a, b, p) {
  const q = easeInOut(p);
  return {
    x: lerp(a.x, b.x, q),
    y: lerp(a.y, b.y, q),
    zoom: lerp(a.zoom, b.zoom, q),
    roll: lerp(a.roll, b.roll, q),
    pitch: lerp(a.pitch, b.pitch, q),
  };
}

function mixCameraLinear(a, b, p) {
  const q = clamp(p);
  return {
    x: lerp(a.x, b.x, q),
    y: lerp(a.y, b.y, q),
    zoom: lerp(a.zoom, b.zoom, q),
    roll: lerp(a.roll, b.roll, q),
    pitch: lerp(a.pitch, b.pitch, q),
  };
}

function midiNetworkCamera(shot, w, h) {
  // These boundary keyframes are intentionally shared between adjacent shots.
  // The sustained move transfers attention from the package gate, through the
  // chord procession, to the empty receptor and finally the wrong branch.
  const packageStart = {
    x: w * .105, y: h * .022, zoom: .9, roll: -.05, pitch: .955,
  };
  const packageRelease = {
    x: w * .035, y: 0, zoom: 1.02, roll: -.012, pitch: .93,
  };
  const receptorApproach = {
    x: -w * .095, y: -h * .026, zoom: 1.16, roll: .05, pitch: .9,
  };
  const emptyReceptor = {
    x: -w * .13, y: h * .008, zoom: .93, roll: -.018, pitch: .95,
  };
  const wrongBranch = {
    x: w * .04, y: -h * .026, zoom: .82, roll: -.075, pitch: .985,
  };
  const knotFull = {
    x: -w * .025, y: h * .012, zoom: 1.02, roll: -.018, pitch: .95,
  };
  const knotOrbit = {
    x: w * .018, y: -h * .018, zoom: 1.1, roll: .045, pitch: .92,
  };
  const p = clamp(shot.p || 0);

  if (shot.kind === 'midi-network-pack') {
    return mixCamera(packageStart, packageRelease, p);
  }
  if (shot.kind === 'midi-network-flight') {
    return mixCamera(packageRelease, receptorApproach, p);
  }
  if (p < .34) {
    return mixCameraLinear(receptorApproach, knotFull, smooth(p / .34));
  }
  return mixCameraLinear(knotFull, knotOrbit, smooth((p - .34) / .66));
}

let midiLossGuitarEventsCache = null;

function midiLossGuitarEvents() {
  if (midiLossGuitarEventsCache) return midiLossGuitarEventsCache;
  midiLossGuitarEventsCache = (performanceControls.notes?.['guitar-notes'] || [])
    .filter(event => event.on >= 33.1 && event.on < 34.9)
    .map((event, index) => ({...event, index}));
  return midiLossGuitarEventsCache;
}

function midiLossSpiroPoint(w, h, event, u, t, strand, scale = 1) {
  const innerOptions = [2, 3, 4, 3];
  const outer = 7;
  const inner = innerOptions[strand % innerOptions.length];
  const pen = inner * (.78 + event.velocity * .22);
  const turn = strand % 2 ? -1 : 1;
  const rotation = (t - 34.433333) * (.055 + strand * .009) * turn
                 + strand * .41;
  const theta = u * TAU * inner + rotation;
  const ratio = (outer - inner) / inner;
  const normalizer = outer - inner + pen;
  const x = ((outer - inner) * Math.cos(theta)
           + pen * Math.cos(ratio * theta)) / normalizer;
  const y = ((outer - inner) * Math.sin(theta)
           - pen * Math.sin(ratio * theta)) / normalizer;
  const radius = Math.min(w, h) * (.69 + strand * .018) * scale;
  const guitarRipple = signalAt('guitar', t - u * .018)
                     * Math.min(w, h) * .006 * Math.sin(u * Math.PI);
  const roll = -.1 + strand * .035;
  const cosine = Math.cos(roll), sine = Math.sin(roll);
  return {
    x: w * .545 + x * radius * cosine - y * radius * .76 * sine,
    y: h * .48 + x * radius * sine + y * radius * .76 * cosine
       + guitarRipple,
  };
}

function midiLossSpiroPath(w, h, event, t, strand, scale = 1) {
  const points = [];
  for (let index = 0; index <= 150; index++) {
    points.push(midiLossSpiroPoint(w, h, event, index / 150,
                                   t, strand, scale));
  }
  return motionCurve(points);
}

function drawMidiLossNotePacket(g, w, h, t, d, event, strand, scale,
                                head, direction, alpha, secondary = false) {
  const duration = Math.max(.08, event.off - event.on);
  const trailLength = (.035 + Math.min(1.8, duration) * .052)
                    * (secondary ? .68 : 1);
  const points = [];
  for (let index = 0; index <= 34; index++) {
    const q = index / 34;
    const u = head - direction * trailLength * q;
    points.push(midiLossSpiroPoint(w, h, event, u, t, strand, scale));
  }
  const path = motionCurve(points);
  const color = NOTE_COLORS[event.pitch % 12];
  const signal = Math.abs(signalAt('guitar', t - strand * .008));
  const pulse = .56 + .44 * Math.max(0, Math.sin((t - event.on) * TAU * .72
                                                + strand * .8));
  const velocity = clamp(event.velocity);
  pathStroke(g, path, color,
             (secondary ? .7 : 1.15) + velocity * (secondary ? .8 : 1.65),
             alpha * pulse * (secondary ? .26 : .68),
             8 + velocity * 12);
  const tip = points[0];
  glowDot(g, tip.x, tip.y,
          Math.min(w, h) * (secondary ? .006 : .009)
            * (1 + velocity * .8 + signal * .45),
          color, alpha * pulse * (secondary ? .42 : .92));
}

function drawMidiLossSpirographKnot(g, w, h, t, d, shot, reveal,
                                    options = {}) {
  if (reveal <= .001) return;
  const events = midiLossGuitarEvents();
  if (!events.length) return;
  const exitFlight = options.holdScale ? 0
    : smooth(clamp((shot.p - .55) / .17));
  const scale = lerp(.48, 1.08, smooth(clamp(shot.p / .34)))
              * lerp(1, .42, exitFlight);
  const breath = 1 + d.bassBody * .045 + Math.sin(t * .73) * .012;
  const knotScale = scale * breath;

  if (!options.noHalo) {
    g.save();
    g.globalCompositeOperation = 'screen';
    const halo = g.createRadialGradient(w * .545, h * .48, 1,
                                        w * .545, h * .48,
                                        Math.min(w, h) * .58 * knotScale);
    halo.addColorStop(0, `rgba(44,17,68,${.08 + d.masterBody * .08})`);
    halo.addColorStop(.52, `rgba(14,42,58,${.045 + d.bassBody * .06})`);
    halo.addColorStop(1, '#0000');
    g.globalAlpha = reveal;
    g.fillStyle = halo;
    g.fillRect(0, 0, w, h);
    g.restore();
  }

  for (const [strand, event] of events.entries()) {
    const path = midiLossSpiroPath(w, h, event, t, strand, knotScale);
    const color = NOTE_COLORS[event.pitch % 12];
    const velocity = clamp(event.velocity);
    pathStroke(g, path, color, 8 + velocity * 6,
               reveal * (.018 + d.masterBody * .025), 22);
    pathStroke(g, path, color, .85 + velocity * 1.2,
               reveal * (.42 + velocity * .3), 9 + velocity * 7);

    const travel = ((t - event.on) * (.115 + strand * .011)
                  + strand / events.length + 10) % 1;
    drawMidiLossNotePacket(g, w, h, t, d, event, strand, knotScale,
                           travel, 1, reveal, false);
    drawMidiLossNotePacket(g, w, h, t, d, event, strand, knotScale,
                           (travel + .47) % 1, 1, reveal * .72, true);
  }

  const lateEvents = noteEventsBetween('diva-notes', 36.4, 38.7)
    .filter(event => t >= event.on - .08 && t <= event.off + .72);
  for (const event of lateEvents) {
    const strand = Math.abs(event.pitch) % events.length;
    const source = events[strand];
    const progress = clamp((t - event.on + .08)
                         / Math.max(.2, event.off - event.on + .8));
    const head = (1 - progress + event.pitch * .013 + 10) % 1;
    drawMidiLossNotePacket(g, w, h, t, d,
                           {...source, pitch: event.pitch,
                            velocity: event.velocity,
                            on: event.on, off: event.off},
                           strand, knotScale, head, -1,
                           reveal * smooth(clamp(progress / .18))
                             * (1 - smooth(clamp((progress - .7) / .3))), true);
  }

  if (!options.noAperture) {
    const aperture = new Path2D();
    const cx = w * .585, cy = h * .49;
    aperture.ellipse(cx, cy,
                     w * (.035 + d.bassBody * .007),
                     h * (.075 + d.masterBody * .012),
                     -.18 + Math.sin(t * .19) * .025, 0, TAU);
    pathStroke(g, aperture, '#7ef1e2', 1 + d.drumBody * 1.2,
               reveal * (.34 + d.masterBody * .24), 11);
  }
}

function midiLossPacketRoutePoint(w, h, u) {
  const junction = {x: w * .7, y: h * .47};
  if (u <= .69) {
    const p = smooth(u / .69);
    return curvedPoint({x: -w * .08, y: h * .63},
                       {x: w * .24, y: h * .25},
                       {x: w * .51, y: h * .68}, junction, p);
  }
  const p = smooth((u - .69) / .31);
  return curvedPoint(junction,
                     {x: w * .77, y: h * .56},
                     {x: w * .96, y: h * .7},
                     {x: w * 1.18, y: h * .61}, p);
}

function midiLossPacketRouteTangent(w, h, u) {
  const prior = midiLossPacketRoutePoint(w, h, clamp(u - .003));
  const next = midiLossPacketRoutePoint(w, h, clamp(u + .003));
  return Math.atan2(next.y - prior.y, next.x - prior.x);
}

function drawMidiLossTimingNetwork(g, w, h, t, d, shot, alpha) {
  const incoming = new Path2D();
  for (let index = 0; index <= 62; index++) {
    const point = midiLossPacketRoutePoint(w, h, .69 * index / 62);
    if (!index) incoming.moveTo(point.x, point.y);
    else incoming.lineTo(point.x, point.y);
  }
  pathStroke(g, incoming, '#70ead9', 1.1 + d.bassBody * .9,
             alpha * (.42 + d.masterBody * .22), 10);

  const wrongBranch = new Path2D();
  for (let index = 0; index <= 32; index++) {
    const point = midiLossPacketRoutePoint(w, h, .69 + .31 * index / 32);
    if (!index) wrongBranch.moveTo(point.x, point.y);
    else wrongBranch.lineTo(point.x, point.y);
  }
  pathStroke(g, wrongBranch, '#e8b96f', 1.2 + d.drumBody * .9,
             alpha * (.48 + d.drums * .22), 11);

  const intended = new Path2D();
  intended.moveTo(w * .7, h * .47);
  intended.bezierCurveTo(w * .76, h * .35,
                         w * .83, h * .35,
                         w * .885, h * .38);
  pathStroke(g, intended, '#8ef2e5', .85 + d.masterBody * .55,
             alpha * .42, 8);

  const sideBranches = [
    [.18, -.16, .31, -.05], [.34, .15, .43, .26],
    [.5, -.17, .59, -.28], [.7, .13, .79, .22],
  ];
  for (const [u, dy, endU, endDy] of sideBranches) {
    const point = midiLossPacketRoutePoint(w, h, u);
    const branch = new Path2D();
    branch.moveTo(point.x, point.y);
    branch.bezierCurveTo(point.x + w * .035, point.y + h * dy * .38,
                         w * endU, point.y + h * endDy * .72,
                         w * (endU + .08), point.y + h * endDy);
    pathStroke(g, branch, u % .3 > .1 ? '#8d93e8' : '#dd83bd',
               .55 + d.drumBody * .45, alpha * .13, 5);
  }

  const start = shot.start || 34.433333;
  const end = shot.end || 38.333333;
  const beats = beatTimes.filter(beat => beat >= start - .05 && beat <= end + .05);
  beats.forEach((beat, index) => {
    const timing = clamp((beat - start) / Math.max(.001, end - start));
    const u = .08 + timing * .61;
    const point = midiLossPacketRoutePoint(w, h, u);
    const pulse = Math.exp(-Math.abs(t - beat) * 6.2);
    const radius = Math.min(w, h) * (.016 + index * .00135 + pulse * .012);
    const color = index % 2 ? '#72ead9' : '#e5b86c';
    const gate = new Path2D();
    gate.ellipse(point.x, point.y, radius * (1.4 + pulse * .28),
                 radius * (.58 + pulse * .18),
                 midiLossPacketRouteTangent(w, h, u), 0, TAU);
    pathStroke(g, gate, color, .85 + pulse * 1.5,
               alpha * (.38 + pulse * .6), 8 + pulse * 9);
    for (let tick = 0; tick < 4; tick++) {
      const angle = tick / 4 * TAU + index * .22;
      const tickPath = new Path2D();
      tickPath.moveTo(point.x + Math.cos(angle) * radius * 1.65,
                      point.y + Math.sin(angle) * radius * .8);
      tickPath.lineTo(point.x + Math.cos(angle) * radius * (1.92 + pulse * .22),
                      point.y + Math.sin(angle) * radius * (1.02 + pulse * .12));
      pathStroke(g, tickPath, color, .55 + pulse * .55,
                 alpha * (.28 + pulse * .34), 4);
    }

    const nextBeat = beats[index + 1];
    if (nextBeat !== undefined) {
      for (let subdivision = 1; subdivision < 4; subdivision++) {
        const subTime = lerp(beat, nextBeat, subdivision / 4);
        const subTiming = clamp((subTime - start) / Math.max(.001, end - start));
        const subU = .08 + subTiming * .61;
        const subPoint = midiLossPacketRoutePoint(w, h, subU);
        const subAngle = midiLossPacketRouteTangent(w, h, subU);
        const subPulse = Math.exp(-Math.abs(t - subTime) * 9);
        const tick = new Path2D();
        tick.ellipse(subPoint.x, subPoint.y,
                     radius * (.16 + subPulse * .08),
                     radius * (.34 + subPulse * .12),
                     subAngle, 0, TAU);
        pathStroke(g, tick, subdivision === 2 ? '#f0d397' : '#74dcd4',
                   .55 + subPulse * .8,
                   alpha * (.22 + subPulse * .42), 4 + subPulse * 5);
      }
    }
  });

  const junctionPulse = Math.exp(-Math.abs(shot.p - .69) * 22);
  glowDot(g, w * .7, h * .47,
          Math.min(w, h) * (.018 + junctionPulse * .034), '#ffcf70',
          alpha * (.34 + junctionPulse * .72));
}

function drawMidiDeliveryPacket(g, x, y, size, rotation, t, d, alpha) {
  const events = midiLossGuitarEvents();
  const beat = musicalBeatAt(t);
  const pulse = .5 + .5 * Math.sin(beat * Math.PI);
  g.save();
  g.translate(x, y);
  g.rotate(rotation);
  g.scale(size, size);

  for (let layer = 0; layer < 3; layer++) {
    const shell = new Path2D();
    const inset = layer * .055;
    shell.moveTo(-.62 + inset, .08);
    shell.bezierCurveTo(-.5, -.43 + inset,
                         .27, -.52 + inset * .4,
                         .62 - inset, -.06);
    shell.bezierCurveTo(.4, .42 - inset * .3,
                        -.33, .48 - inset,
                        -.62 + inset, .08);
    pathStroke(g, shell, layer % 2 ? '#f19ac8' : '#72ead8',
               (1.4 - layer * .22) / size,
               alpha * (.72 - layer * .14), (10 - layer * 2) / size);
  }

  const contents = new Path2D();
  events.forEach((event, index) => {
    const pitch = clamp((event.pitch - 52) / 14);
    const nx = -.35 + index * .23;
    const ny = lerp(.22, -.24, pitch);
    if (!index) contents.moveTo(nx, ny);
    else contents.bezierCurveTo(nx - .09, ny + (index % 2 ? .08 : -.08),
                                nx - .035, ny, nx, ny);
  });
  pathStroke(g, contents, '#f6f3df', .75 / size, alpha * .5, 4 / size);

  events.forEach((event, index) => {
    const pitch = clamp((event.pitch - 52) / 14);
    const duration = Math.max(.08, event.off - event.on);
    const nx = -.35 + index * .23;
    const ny = lerp(.22, -.24, pitch);
    const color = NOTE_COLORS[event.pitch % 12];
    const nodePulse = .58 + .42 * Math.max(0,
      Math.sin(beat * TAU + index * .9));
    const tail = new Path2D();
    tail.moveTo(nx, ny);
    tail.bezierCurveTo(nx - .07 - duration * .035, ny - .055,
                       nx - .14 - duration * .06, ny + .05,
                       nx - .2 - duration * .08, ny);
    pathStroke(g, tail, color, (.85 + event.velocity) / size,
               alpha * nodePulse * .72, 6 / size);
    const durationHalo = new Path2D();
    durationHalo.ellipse(nx, ny,
                         .026 + Math.min(.065, duration * .018),
                         .019 + event.velocity * .012,
                         -.12 + index * .09, 0, TAU);
    pathStroke(g, durationHalo, color, .7 / size,
               alpha * (.4 + nodePulse * .35), 4 / size);
    glowDot(g, nx, ny, .018 + event.velocity * .012 + pulse * .006,
            color, alpha * nodePulse);
  });

  const scanX = lerp(-.48, .48, (beat % 1 + 1) % 1);
  const scan = new Path2D();
  scan.moveTo(scanX, -.28);
  scan.bezierCurveTo(scanX + .035, -.08, scanX - .025, .12, scanX, .3);
  pathStroke(g, scan, '#fff4c8', .65 / size,
             alpha * (.18 + d.drums * .32), 5 / size);
  g.restore();
}

function drawDistantReceiverFace(g, w, h, t, d, alpha, scale = 1) {
  const size = h * .18 * scale;
  drawFrontFeatures(g, w * .885, h * .36, size, t, d,
                    d.voiceFeature * .6, '#74f1e2', 4.7,
                    alpha, -.025, -.035);
}

function drawMidiLossPacketChase(g, w, h, t, d, shot, actors, local) {
  const reveal = smooth(clamp(shot.p / .1));
  if (reveal < .999) {
    g.save();
    g.globalAlpha = 1 - reveal;
    drawMidiRoutingNetwork(g, w, h, t, d, shot, actors);
    drawMidiPackageSource(g, w, h, t, d, local);
    drawMidiChordHarnesses(g, actors, w, h);
    actors.forEach(actor => drawMidiNoteActor(g, actor, w, h, t));
    g.restore();
  }

  const starReveal = smooth(clamp((shot.p - .62) / .34));
  if (starReveal > .001) {
    g.save();
    g.globalAlpha = starReveal;
    drawReceiverMusicalStarfield(g, w, h, t, d,
                                 {kind: 'receiver-empty-starfield', p: shot.p});
    g.restore();
  }

  const camera = {x: -w * shot.p * .035, y: h * shot.p * .012,
                  zoom: 1 + shot.p * .14, roll: -.018 + shot.p * .025,
                  pitch: .96};
  withCamera(g, w, h, camera, () => {
    drawMidiLossTimingNetwork(g, w, h, t, d, shot,
                              reveal * (1 - starReveal * .62));
    drawDistantReceiverFace(g, w, h, t, d,
                            reveal * (1 - starReveal), 1 + shot.p * .18);
    const u = lerp(.04, 1, smooth(shot.p));
    const point = midiLossPacketRoutePoint(w, h, u);
    const angle = midiLossPacketRouteTangent(w, h, u);
    const approach = Math.sin(clamp(shot.p) * Math.PI);
    const size = h * (.16 + approach * .085)
               * (1 - smooth(clamp((shot.p - .86) / .14)) * .38);
    const packetAlpha = reveal
      * (1 - smooth(clamp((shot.p - .93) / .07)));
    drawMidiDeliveryPacket(g, point.x, point.y, size, angle, t, d, packetAlpha);
  });

  if (starReveal > .001) {
    const closeShot = {kind: 'receiver-empty-starfield',
                       p: .58 + starReveal * .08};
    drawReceiverSearchingFigure(g, w, h, t, d, closeShot, starReveal);
  }
}

function drawMidiNetworkScene(g, w, h, t, d, shot) {
  const local = clamp((t - midiNetworkScene.startSec)
                    / Math.max(.001, midiNetworkScene.endSec - midiNetworkScene.startSec));
  drawMidiNetworkAtmosphere(g, w, h, t, d, local);
  const actors = midiNetworkActorsAt(t, w, h, d);
  if (shot.kind === 'midi-network-loss') {
    drawMidiLossPacketChase(g, w, h, t, d, shot, actors, local);
    return local;
  }
  const camera = midiNetworkCamera(shot, w, h);
  withCamera(g, w, h, camera, () => {
    const knotReveal = shot.kind === 'midi-network-loss'
      ? smooth(clamp(shot.p / .24)) : 0;
    if (knotReveal < .999) {
      g.save();
      g.globalAlpha = 1 - knotReveal;
      drawMidiRoutingNetwork(g, w, h, t, d, shot, actors);
      drawMidiPackageSource(g, w, h, t, d, local);
      drawMidiChordHarnesses(g, actors, w, h);
      actors.sort((a, b) => a.event.pitch - b.event.pitch)
        .forEach(actor => drawMidiNoteActor(g, actor, w, h, t));
      g.restore();
    }
    if (shot.kind === 'midi-network-loss') {
      const routeExit = smooth(clamp((shot.p - .72) / .28));
      drawMidiLossSpirographKnot(g, w, h, t, d, shot,
                                 knotReveal * (1 - routeExit));
    }
  });
  return local;
}

let receiverDivaEventsCache = null;
let receiverGuitarEventsCache = null;

function receiverNoteEvents(id) {
  if (id === 'diva-notes' && receiverDivaEventsCache) return receiverDivaEventsCache;
  if (id === 'guitar-notes' && receiverGuitarEventsCache) return receiverGuitarEventsCache;
  const events = (performanceControls.notes?.[id] || [])
    .filter(event => !receiverScene
      || (event.on >= receiverScene.startSec - .55
          && event.on < receiverScene.endSec + .55))
    .map((event, index) => ({...event, index}));
  if (id === 'diva-notes') receiverDivaEventsCache = events;
  if (id === 'guitar-notes') receiverGuitarEventsCache = events;
  return events;
}

function rotatedLensPoint(cx, cy, rx, ry, turn, x, y) {
  const px = x * rx, py = y * ry;
  const cosine = Math.cos(turn), sine = Math.sin(turn);
  return {x: cx + px * cosine - py * sine,
          y: cy + px * sine + py * cosine};
}

function receiverLensPath(cx, cy, rx, ry, turn = 0) {
  const p = (x, y) => rotatedLensPoint(cx, cy, rx, ry, turn, x, y);
  const path = new Path2D();
  let a = p(-.16, -1.02);
  path.moveTo(a.x, a.y);
  let b = p(-.82, -.94), c = p(-1.12, -.28), d = p(-.7, .72);
  path.bezierCurveTo(b.x, b.y, c.x, c.y, d.x, d.y);
  b = p(-.38, 1.12); c = p(.52, 1.04); d = p(.91, .36);
  path.bezierCurveTo(b.x, b.y, c.x, c.y, d.x, d.y);
  b = p(1.17, -.16); c = p(.57, -1.12); d = p(-.16, -1.02);
  path.bezierCurveTo(b.x, b.y, c.x, c.y, d.x, d.y);
  path.closePath();
  return path;
}

function receiverLensGeometry(w, h, shot, t) {
  const pulse = .5 + .5 * Math.sin(t * .42);
  if (shot.kind === 'receiver-empty-starfield') {
    return {cx: w * lerp(.585, .44, smooth(shot.p)), cy: h * .5,
            rx: w * lerp(.075, .19, smooth(shot.p)), ry: h * lerp(.18, .34, smooth(shot.p)),
            turn: lerp(.03, -.16, shot.p)};
  }
  if (shot.kind === 'receiver-phase-demand') {
    return {cx: w * lerp(.44, .49, shot.p), cy: h * lerp(.5, .52, shot.p),
            rx: w * (.2 + shot.p * .08), ry: h * (.36 + shot.p * .08),
            turn: -.16 + shot.p * .25};
  }
  if (shot.kind === 'receiver-raw-scan') {
    return {cx: w * .5, cy: h * .5, rx: w * .82, ry: h * .92,
            turn: .19 + Math.sin(shot.p * Math.PI) * .05};
  }
  if (shot.kind === 'receiver-constructive-interference') {
    return {cx: w * (.48 + Math.sin(shot.p * Math.PI) * .025), cy: h * .51,
            rx: w * (.31 + pulse * .015), ry: h * (.46 + pulse * .018),
            turn: lerp(.22, -.08, smooth(shot.p))};
  }
  const expansion = smooth(clamp((shot.p - .06) / .94));
  return {cx: w * .5, cy: h * .5,
          rx: w * lerp(.33, 1.08, expansion),
          ry: h * lerp(.47, 1.34, expansion),
          turn: lerp(-.08, .025, expansion)};
}

function drawReceiverAtmosphere(g, w, h, t, d, amount = 1) {
  const gradient = g.createRadialGradient(w * .43, h * .49, 1,
                                           w * .43, h * .49, w * .78);
  gradient.addColorStop(0, `rgba(${Math.round(9 + d.masterBody * 19)},20,29,1)`);
  gradient.addColorStop(.48, '#070813');
  gradient.addColorStop(1, '#010205');
  g.save();
  g.globalAlpha = amount;
  g.fillStyle = gradient;
  g.fillRect(0, 0, w, h);
  g.globalCompositeOperation = 'screen';
  for (let index = 0; index < 32; index++) {
    const x = hash(index * 4.1 + 30) * w;
    const y = hash(index * 7.7 + 14) * h;
    const drift = Math.sin(t * (.055 + hash(index) * .07) + index) * h * .012;
    g.globalAlpha = amount * (.035 + hash(index + 8) * .12);
    g.fillStyle = index % 3 ? '#65ebdb' : '#e7b66f';
    g.beginPath();
    g.arc(x, y + drift, .5 + hash(index + 2) * 1.2, 0, TAU);
    g.fill();
  }
  g.restore();
}

function drawReceiverMusicalStarfield(g, w, h, t, d, shot) {
  const gradient = g.createRadialGradient(w * .72, h * .48, 1,
                                           w * .72, h * .48, w * .88);
  gradient.addColorStop(0, '#081629');
  gradient.addColorStop(.43, '#060a18');
  gradient.addColorStop(1, '#010205');
  g.fillStyle = gradient;
  g.fillRect(0, 0, w, h);

  const bands = [
    {id: 'drum-high', color: '#a99aff', count: 54, depth: .2,
     energy: Math.abs(signalAt('drum-high', t)), speed: .004},
    {id: 'drum-mid', color: '#62e8df', count: 36, depth: .52,
     energy: Math.abs(signalAt('drum-mid', t)), speed: .011},
    {id: 'drum-low', color: '#ff7d83', count: 22, depth: .82,
     energy: Math.abs(signalAt('drum-low', t)), speed: .021},
    {id: 'bass', color: '#f0c66d', count: 14, depth: 1,
     energy: Math.abs(signalAt('bass', t)), speed: .03},
  ];
  const localTime = t - (receiverScene?.startSec || 0);
  for (const [bandIndex, band] of bands.entries()) {
    for (let index = 0; index < band.count; index++) {
      const seed = index + bandIndex * 113;
      const baseX = hash(seed * 4.17 + 9);
      const drift = localTime * band.speed * (1 + hash(seed * 2.3) * .7)
                  + shot.p * band.depth * .025;
      const x = (((baseX + drift) % 1 + 1) % 1) * w * 1.18 - w * .09;
      const y = hash(seed * 8.31 + 17) * h
              + Math.sin(t * (.045 + band.depth * .055) + seed) * h
                * (.004 + band.depth * .008);
      const localPulse = .45 + .55 * Math.max(0,
        Math.sin(t * (1.15 + bandIndex * .73) + seed * 1.91));
      const energy = clamp(band.energy * (1.15 + bandIndex * .12)
                         + (band.id === 'bass' ? d.bassBody * .25 : 0));
      const radius = (.45 + hash(seed * 5.6) * 1.25)
                   * lerp(.65, 2.55, band.depth)
                   * (1 + energy * (.55 + band.depth * .7));
      const alpha = (.12 + band.depth * .14 + energy * .32)
                  * (.68 + localPulse * .32);
      glowDot(g, x, y, radius, band.color, alpha);
      g.save();
      g.globalCompositeOperation = 'screen';
      g.globalAlpha = alpha * (.45 + energy * .4);
      g.fillStyle = band.color;
      g.beginPath();
      g.arc(x, y, Math.max(.45, radius * .18), 0, TAU);
      g.fill();
      g.restore();
      if (band.depth > .7 && energy > .08) {
        const wake = new Path2D();
        wake.moveTo(x, y);
        wake.bezierCurveTo(x - w * .012 * band.depth,
                           y + h * .004 * Math.sin(seed),
                           x - w * .028 * band.depth,
                           y - h * .006 * Math.cos(seed),
                           x - w * .045 * band.depth, y);
        pathStroke(g, wake, band.color, .45 + energy,
                   alpha * energy * .22, 4);
      }
    }
  }

  const pitchStars = receiverActiveNotes('diva-notes', t, .18, .86).slice(0, 16);
  for (const event of pitchStars) {
    const pitch = clamp((event.pitch - 36) / 60);
    const x = w * (.08 + hash(event.index * 7.13 + event.pitch) * .84);
    const y = h * lerp(.82, .13, pitch);
    const onset = Math.exp(-Math.abs(t - event.on) * 7);
    const release = 1 - smooth(clamp((t - event.off) / .86));
    const color = NOTE_COLORS[event.pitch % 12];
    const depth = .28 + event.velocity * .72;
    glowDot(g, x, y, Math.min(w, h) * (.004 + depth * .008 + onset * .006),
            color, release * (.28 + event.velocity * .4 + onset * .48));
    const orbit = new Path2D();
    orbit.ellipse(x, y, w * (.006 + depth * .012),
                  h * (.003 + depth * .008),
                  event.pitch * .13 + t * .035, 0, TAU);
    pathStroke(g, orbit, color, .55 + event.velocity,
               release * (.12 + onset * .38), 5);
  }
}

function receiverDeliveryRoutePoint(w, h, q) {
  const junction = {x: w * .675, y: h * .49};
  if (q <= .48) {
    const p = smooth(q / .48);
    return curvedPoint({x: w * .545, y: h * .48},
                       {x: w * .585, y: h * .39},
                       {x: w * .64, y: h * .58}, junction, p);
  }
  const p = smooth((q - .48) / .52);
  return curvedPoint(junction,
                     {x: w * .73, y: h * .35},
                     {x: w * .9, y: -h * .02},
                     {x: w * 1.14, y: -h * .18}, p);
}

function drawReceiverDeliveryRoute(g, w, h, t, d, shot, alpha) {
  const q = clamp(shot.p / .58);
  const intended = new Path2D();
  intended.moveTo(w * .545, h * .48);
  intended.bezierCurveTo(w * .61, h * .37,
                         w * .69, h * .59,
                         w * .765, h * .64);
  pathStroke(g, intended, '#6ce9d8', .75 + d.masterBody,
             alpha * (1 - smooth(clamp((shot.p - .36) / .5))) * .28, 7);

  const wrong = new Path2D();
  for (let index = 0; index <= 58; index++) {
    const point = receiverDeliveryRoutePoint(w, h, index / 58);
    if (!index) wrong.moveTo(point.x, point.y); else wrong.lineTo(point.x, point.y);
  }
  pathStroke(g, wrong, '#e2b673', .8 + d.drumBody * .7,
             alpha * .32, 7);

  const point = receiverDeliveryRoutePoint(w, h, q);
  const fade = 1 - smooth(clamp((shot.p - .48) / .18));
  const scale = lerp(.42, .2, smooth(q));
  g.save();
  g.translate(point.x, point.y);
  g.rotate(shot.p * TAU * 1.28 + q * .7);
  g.scale(scale, scale);
  g.translate(-w * .545, -h * .48);
  drawMidiLossSpirographKnot(g, w, h, t, d,
                             {kind: 'midi-network-loss', p: .7},
                             alpha * fade,
                             {holdScale: true, noHalo: true, noAperture: true});
  g.restore();

  const contact = Math.exp(-Math.pow((q - .48) / .075, 2));
  glowDot(g, w * .675, h * .49,
          Math.min(w, h) * (.012 + contact * .025), '#f4d36e',
          alpha * (.16 + contact * .82));
  if (contact > .03) {
    const recoil = new Path2D();
    recoil.moveTo(w * .675, h * .49);
    recoil.bezierCurveTo(w * (.65 - contact * .03), h * (.46 + contact * .04),
                         w * (.7 + contact * .025), h * (.43 - contact * .06),
                         w * (.72 + contact * .04), h * (.37 - contact * .09));
    pathStroke(g, recoil, '#ff8e9c', .8 + contact * 1.4,
               alpha * contact * .54, 9);
  }
}

function drawOpenReceivingPalm(g, x, y, size, mirror, t, d, alpha, lift) {
  g.save();
  g.translate(x, y - lift * size * .08);
  g.scale(mirror * size, size);
  g.rotate(mirror * (.06 + lift * .1));
  const palm = new Path2D();
  palm.moveTo(-.18, .12);
  palm.bezierCurveTo(-.23, -.01, -.15, -.15, -.03, -.17);
  palm.bezierCurveTo(.1, -.19, .22, -.1, .21, .05);
  palm.bezierCurveTo(.19, .2, .04, .28, -.1, .23);
  palm.bezierCurveTo(-.15, .21, -.18, .17, -.18, .12);
  pathStroke(g, palm, '#79eee0', 1.85 / size, alpha * .9, 8 / size);
  for (let finger = 0; finger < 4; finger++) {
    const fx = -.12 + finger * .082;
    const spread = (finger - 1.5) * .055;
    const length = .24 + Math.sin((finger + 1) / 5 * Math.PI) * .12;
    const path = new Path2D();
    path.moveTo(fx, -.12);
    path.bezierCurveTo(fx + spread * .25, -.21,
                       fx + spread * .72, -length + lift * .015,
                       fx + spread, -length - .08 + lift * .018);
    pathStroke(g, path, finger % 2 ? '#f5c279' : '#78e9df',
               1.02 / size, alpha * (.7 + finger * .055), 5 / size);
  }
  const thumb = new Path2D();
  thumb.moveTo(-.13, -.05);
  thumb.bezierCurveTo(-.25, -.14, -.34, -.09, -.36, .04);
  pathStroke(g, thumb, '#f0bc76', 1.05 / size, alpha * .74, 5 / size);
  g.restore();
}

function drawReceiverSearchingFigure(g, w, h, t, d, shot, alpha) {
  const search = smooth(clamp((shot.p - .24) / .7));
  const routeGaze = lerp(-.055, .065, smooth(clamp(shot.p / .42)));
  const scan = Math.sin((shot.p - .42) * Math.PI * 3.2) * .055;
  const gaze = shot.p < .44 ? routeGaze : scan;
  const x = w * (.79 - search * .025);
  const y = h * (.43 + Math.sin(t * .54) * .012);
  const size = h * (.54 + d.voiceSustain * .08);
  const rotation = -.025 + Math.sin(t * .68) * .018
                 + (shot.p < .44 ? shot.p * .08 : scan * .32);
  g.save();
  g.globalCompositeOperation = 'screen';
  const bloom = g.createRadialGradient(x, y, 1, x, y, size * .62);
  bloom.addColorStop(0, `rgba(72,222,213,${.07 + d.voiceBody * .07})`);
  bloom.addColorStop(1, '#0000');
  g.globalAlpha = alpha;
  g.fillStyle = bloom;
  g.beginPath(); g.arc(x, y, size * .62, 0, TAU); g.fill();
  g.restore();
  drawFrontFeatures(g, x, y, size, t, d, d.voiceFeature,
                    '#74f1e2', 4.7, alpha, rotation, gaze);
}

function drawReceiverEmptyStarfieldScene(g, w, h, t, d, shot) {
  drawReceiverMusicalStarfield(g, w, h, t, d, shot);
  const searchingShot = {...shot, p: .62 + shot.p * .38};
  drawReceiverSearchingFigure(g, w, h, t, d, searchingShot, 1);
}

function drawReceiverRouteAfterimages(g, w, h, t, d, alpha = 1) {
  const colors = ['#58d9d0', '#db9f6a', '#7f88d9'];
  for (let route = 0; route < 6; route++) {
    const side = route % 2 ? 1 : -1;
    const path = new Path2D();
    path.moveTo(w * (1.08 - route * .025), h * (.12 + route * .14));
    path.bezierCurveTo(w * (.82 + side * .05), h * (.08 + route * .13),
                       w * (.67 - side * .08), h * (.68 - route * .07),
                       w * (.43 + side * .04), h * (.43 + route * .035));
    path.bezierCurveTo(w * (.25 - side * .09), h * (.24 + route * .08),
                       w * (.16 + side * .05), h * (.82 - route * .055),
                       -w * .12, h * (.29 + route * .1));
    const flicker = .62 + .38 * Math.sin(t * .71 + route * 1.37);
    pathStroke(g, path, colors[route % colors.length],
               .55 + d.drumBody * .65,
               alpha * flicker * (.08 + d.masterBody * .08), 5);
  }
}

function drawReceiverOpticalDistortion(g, w, h, lens, t, d, alpha) {
  if (alpha <= .002) return;
  if (receiverOpticalLayer.width !== g.canvas.width
      || receiverOpticalLayer.height !== g.canvas.height) {
    receiverOpticalLayer.width = g.canvas.width;
    receiverOpticalLayer.height = g.canvas.height;
  }
  receiverOpticalCtx.setTransform(1, 0, 0, 1, 0, 0);
  receiverOpticalCtx.globalAlpha = 1;
  receiverOpticalCtx.globalCompositeOperation = 'source-over';
  receiverOpticalCtx.drawImage(g.canvas, 0, 0);
  const path = receiverLensPath(lens.cx, lens.cy, lens.rx, lens.ry, lens.turn);
  const mid = signalAt('drum-mid', t);
  const high = signalAt('drum-high', t);
  const separation = Math.min(w, h) * (.0035 + d.drumBody * .0065);
  g.save();
  g.clip(path);
  g.globalCompositeOperation = 'screen';
  g.globalAlpha = alpha * (.18 + Math.abs(mid) * .12);
  g.filter = 'saturate(1.32) hue-rotate(18deg)';
  g.drawImage(receiverOpticalLayer, separation * (1 + mid), -separation * high,
              w, h);
  g.globalAlpha = alpha * (.12 + Math.abs(high) * .1);
  g.filter = 'saturate(1.25) hue-rotate(-28deg)';
  g.drawImage(receiverOpticalLayer, -separation * (1 - high), separation * mid,
              w, h);
  g.filter = 'none';
  const glaze = g.createLinearGradient(lens.cx - lens.rx, lens.cy - lens.ry,
                                        lens.cx + lens.rx, lens.cy + lens.ry);
  glaze.addColorStop(0, 'rgba(70,243,224,.07)');
  glaze.addColorStop(.48, 'rgba(0,0,0,0)');
  glaze.addColorStop(1, 'rgba(255,187,102,.08)');
  g.globalAlpha = alpha;
  g.fillStyle = glaze;
  g.fillRect(0, 0, w, h);
  g.restore();
}

function drawReceiverContours(g, w, h, lens, t, d, shot, alpha = 1) {
  const plate = receiverLensPath(lens.cx, lens.cy, lens.rx, lens.ry, lens.turn);
  const mid = signalAt('drum-mid', t);
  const high = signalAt('drum-high', t);
  const raw = shot.kind === 'receiver-raw-scan';
  const growing = shot.kind === 'receiver-constructive-interference'
               || shot.kind === 'receiver-garden-phaseplate';
  g.save();
  g.clip(plate);
  const families = [
    {color: '#65eee0', phase: mid * 1.4, offset: -1},
    {color: '#efb965', phase: .35 + high * 1.6, offset: 1},
  ];
  for (const [familyIndex, family] of families.entries()) {
    const count = raw ? 18 : 13;
    for (let line = 0; line < count; line++) {
      const path = new Path2D();
      for (let step = 0; step <= 52; step++) {
        const u = step / 52;
        const across = u * 2 - 1;
        const band = (line / Math.max(1, count - 1) * 2 - 1);
        const phase = across * TAU * (raw ? 1.34 : 1.05)
                    + line * .43 + t * (.13 + familyIndex * .035) + family.phase;
        const shear = (mid * Math.sin(u * Math.PI)
                     + high * Math.sin(u * TAU * 1.7 + line)) * lens.ry * .055;
        const x0 = across * lens.rx * 1.16
                 + Math.sin(phase * .72) * lens.rx * (.025 + d.bassBody * .025)
                 + family.offset * lens.rx * .006;
        const y0 = band * lens.ry * .88
                 + Math.sin(phase) * lens.ry * (raw ? .105 : .075)
                 + shear + family.offset * lens.ry * .008;
        const point = rotatedLensPoint(lens.cx, lens.cy, 1, 1, lens.turn, x0, y0);
        if (!step) path.moveTo(point.x, point.y); else path.lineTo(point.x, point.y);
      }
      const irregular = raw ? (.36 + hash(line * 2.7 + familyIndex) * .54) : .72;
      pathStroke(g, path, family.color,
                 .55 + d.drumBody * .7 + (growing ? .35 : 0),
                 alpha * irregular * (.11 + d.masterBody * .13), raw ? 4 : 7);
    }
  }
  g.restore();
  pathStroke(g, plate, '#75f3df', 1 + d.drumBody * 1.8,
             alpha * (.24 + d.masterBody * .22), 11);
  const echo = receiverLensPath(lens.cx + lens.rx * .018, lens.cy - lens.ry * .012,
                                lens.rx * 1.012, lens.ry * .99, lens.turn + .012);
  pathStroke(g, echo, '#efb56b', .7 + d.drumBody,
             alpha * (.15 + d.masterBody * .16), 7);
}

function receiverActiveNotes(id, t, lead = .3, release = 1.05) {
  return receiverNoteEvents(id).filter(event =>
    t >= event.on - lead && t <= event.off + release)
    .sort((a, b) => Math.abs(t - a.on) - Math.abs(t - b.on));
}

function receiverNotePoint(event, lens) {
  const pitch = clamp((event.pitch - 36) / 60);
  const angle = lerp(2.45, -1.0, pitch) + (hash(event.index * 2.17) - .5) * .4;
  const radius = .24 + hash(event.index * 5.3 + event.pitch) * .53;
  const localX = Math.cos(angle) * lens.rx * radius;
  const localY = Math.sin(angle) * lens.ry * radius;
  return {...rotatedLensPoint(lens.cx, lens.cy, 1, 1, lens.turn, localX, localY),
          pitch, angle, radius};
}

function drawReceiverDivaCaustics(g, w, h, t, d, lens, alpha = 1) {
  const events = receiverActiveNotes('diva-notes', t, .48, .9).slice(0, 12);
  g.save();
  g.clip(receiverLensPath(lens.cx, lens.cy, lens.rx, lens.ry, lens.turn));
  for (const event of events) {
    const point = receiverNotePoint(event, lens);
    const onset = Math.exp(-Math.abs(t - event.on) * 4.4);
    const sustain = 1 - smooth(clamp((t - event.off) / .9));
    const duration = Math.min(2.2, Math.max(.05, event.off - event.on));
    const path = new Path2D();
    path.moveTo(point.x - lens.rx * 1.2, point.y + lens.ry * .24);
    path.bezierCurveTo(point.x - lens.rx * .42, point.y - lens.ry * (.16 + point.pitch * .16),
                       point.x + lens.rx * (.35 + duration * .08), point.y + lens.ry * .13,
                       point.x + lens.rx * 1.2, point.y - lens.ry * .22);
    const color = NOTE_COLORS[event.pitch % 12];
    pathStroke(g, path, color, 2.5 + duration * 3.2,
               alpha * sustain * (.025 + onset * .07 + event.velocity * .035), 18);
    pathStroke(g, path, color, .65 + event.velocity * 1.1,
               alpha * sustain * (.13 + onset * .2), 6);
  }
  g.restore();
}

function drawReceiverGuitarSeeds(g, w, h, t, d, lens, shot, alpha = 1) {
  const events = receiverActiveNotes('guitar-notes', t, .28, 1.35)
    .slice(0, shot.kind === 'receiver-garden-phaseplate' ? 42 : 22);
  const growing = shot.kind === 'receiver-constructive-interference'
               || shot.kind === 'receiver-garden-phaseplate';
  for (const event of events) {
    const point = receiverNotePoint(event, lens);
    const onset = Math.exp(-Math.abs(t - event.on) * 7.2);
    const release = 1 - smooth(clamp((t - event.off) / 1.35));
    const duration = Math.max(.05, event.off - event.on);
    const color = NOTE_COLORS[event.pitch % 12];
    const edge = rotatedLensPoint(lens.cx, lens.cy, lens.rx, lens.ry, lens.turn,
                                  -1.05, .72 - point.pitch * 1.4);
    const probe = new Path2D();
    probe.moveTo(edge.x, edge.y);
    probe.bezierCurveTo(lerp(edge.x, point.x, .31), edge.y - lens.ry * .12,
                        lerp(edge.x, point.x, .72), point.y + lens.ry * .09,
                        point.x, point.y);
    pathStroke(g, probe, color, .65 + event.velocity * .95,
               alpha * release * (.1 + onset * .32 + (growing ? .12 : 0)), 6);
    const nodeRadius = Math.min(w, h) * (.003 + event.velocity * .0045 + onset * .006);
    glowDot(g, point.x, point.y, nodeRadius, color,
            alpha * release * (.28 + onset * .7));
    if (!growing) continue;
    const branchAmount = smooth(clamp((t - event.on) / Math.max(.18, duration * .7)));
    for (const side of [-1, 1]) {
      const length = Math.min(w, h) * (.035 + Math.min(1.4, duration) * .045)
                   * branchAmount;
      const branch = new Path2D();
      branch.moveTo(point.x, point.y);
      branch.bezierCurveTo(point.x + Math.cos(point.angle + side * .8) * length * .35,
                           point.y + Math.sin(point.angle + side * .8) * length * .22,
                           point.x + Math.cos(point.angle + side * 1.18) * length * .72,
                           point.y + Math.sin(point.angle + side * 1.18) * length * .64,
                           point.x + Math.cos(point.angle + side * 1.42) * length,
                           point.y + Math.sin(point.angle + side * 1.42) * length);
      pathStroke(g, branch, side > 0 ? '#6df0d9' : '#e9ba6e',
                 .7 + event.velocity * .75,
                 alpha * release * branchAmount * (.18 + event.velocity * .25), 7);
    }
  }
}

function receiverCamera(shot, w, h) {
  if (shot.kind === 'receiver-empty-starfield') {
    return mixCameraLinear({x: w * .03, y: 0, zoom: .84, roll: -.06, pitch: .96},
                           {x: -w * .025, y: h * .01, zoom: 1, roll: -.015, pitch: .94},
                           smooth(shot.p));
  }
  if (shot.kind === 'receiver-phase-demand') {
    return mixCameraLinear({x: -w * .02, y: h * .02, zoom: 1, roll: -.015, pitch: .94},
                           {x: -w * .08, y: h * .065, zoom: 1.16, roll: .045, pitch: .9},
                           smooth(shot.p));
  }
  if (shot.kind === 'receiver-raw-scan') {
    return mixCameraLinear({x: w * .04, y: -h * .04, zoom: 1.22, roll: .08, pitch: .91},
                           {x: -w * .07, y: h * .035, zoom: 1.45, roll: -.08, pitch: .88},
                           smooth(shot.p));
  }
  if (shot.kind === 'receiver-constructive-interference') {
    const arc = Math.sin(shot.p * Math.PI);
    return {x: w * (.045 - shot.p * .08), y: -h * .025 * arc,
            zoom: lerp(1.24, .94, smooth(shot.p)), roll: lerp(-.07, .05, shot.p),
            pitch: lerp(.9, .96, shot.p)};
  }
  return mixCameraLinear({x: -w * .025, y: 0, zoom: .96, roll: .04, pitch: .96},
                         {x: 0, y: 0, zoom: 1.05, roll: 0, pitch: 1},
                         smooth(shot.p));
}

function drawReceiverFace(g, w, h, t, d, shot, alpha = 1) {
  let x = w * .84, y = h * .49, size = h * .48, localAlpha = alpha;
  if (shot.kind === 'receiver-empty-starfield') {
    x = w * lerp(1.05, .83, smooth(shot.p));
    y = h * (.49 + Math.sin(shot.p * Math.PI) * .02);
    size = h * .45;
  } else if (shot.kind === 'receiver-phase-demand') {
    x = w * lerp(.83, .72, smooth(shot.p));
    y = h * lerp(.5, .46, smooth(shot.p));
    size = h * lerp(.48, .67, smooth(shot.p));
  } else if (shot.kind === 'receiver-raw-scan') {
    x = w * 1.035; y = h * .16; size = h * .32; localAlpha *= .48;
  } else if (shot.kind === 'receiver-constructive-interference') {
    x = w * lerp(.91, 1.02, smooth(shot.p));
    y = h * lerp(.47, .38, shot.p); size = h * .31; localAlpha *= .64;
  } else {
    x = w * lerp(.93, 1.18, smooth(shot.p));
    y = h * lerp(.43, .27, shot.p); size = h * lerp(.3, .2, shot.p);
    localAlpha *= 1 - smooth(clamp((shot.p - .55) / .4));
  }
  if (localAlpha <= .005) return;
  drawMarsFaceActor(g, x, y, size, '#74f1e2', t, d, 4.7,
                    localAlpha, -.05, true);
}

function drawReceiverScene(g, w, h, t, d, shot) {
  const local = clamp((t - receiverScene.startSec)
                    / Math.max(.001, receiverScene.endSec - receiverScene.startSec));
  const resolvedShot = RECEIVER_SHOT_KINDS.includes(shot.kind) ? shot : {
    ...shot, kind: 'receiver-empty-starfield', p: local,
  };
  const opening = resolvedShot.kind === 'receiver-empty-starfield';
  if (opening) {
    drawReceiverEmptyStarfieldScene(g, w, h, t, d, resolvedShot);
    return local;
  }
  const sourceFade = 1;
  if (resolvedShot.kind === 'receiver-phase-demand') {
    drawReceiverMusicalStarfield(g, w, h, t, d, resolvedShot);
    g.save();
    g.globalAlpha = smooth(clamp(resolvedShot.p / .7));
    drawReceiverAtmosphere(g, w, h, t, d, 1);
    g.restore();
  } else {
    drawReceiverAtmosphere(g, w, h, t, d, 1);
  }
  drawReceiverRouteAfterimages(g, w, h, t, d,
    resolvedShot.kind === 'receiver-phase-demand' ? .06 : .22);
  const camera = receiverCamera(resolvedShot, w, h);
  withCamera(g, w, h, camera, () => {
    const lens = receiverLensGeometry(w, h, resolvedShot, t);
    const gardenReveal = resolvedShot.kind === 'receiver-garden-phaseplate'
      ? smooth(clamp((resolvedShot.p - .3) / .62)) : 0;
    if (gardenReveal > 0 && gardenThresholdScene) {
      const gardenCue = choreography.find(item => item.id === 'choreo-garden-01-threshold');
      const gardenShot = {kind: 'garden-threshold', p: 0, cue: gardenCue,
                          start: gardenThresholdScene.startSec,
                          end: gardenThresholdScene.endSec};
      g.save();
      g.clip(receiverLensPath(lens.cx, lens.cy, lens.rx, lens.ry, lens.turn));
      g.globalAlpha = gardenReveal;
      drawGardenFrame(g, w, h, gardenThresholdScene.startSec + .001, d, gardenShot);
      g.restore();
    }
    const fieldReveal = resolvedShot.kind === 'receiver-phase-demand'
      ? smooth(clamp(resolvedShot.p / .3)) : 1;
    drawReceiverOpticalDistortion(g, w, h, lens, t, d,
                                  fieldReveal * (.56 + d.drumBody * .2));
    drawReceiverDivaCaustics(g, w, h, t, d, lens, fieldReveal);
    drawReceiverContours(g, w, h, lens, t, d, resolvedShot, fieldReveal);
    drawReceiverGuitarSeeds(g, w, h, t, d, lens, resolvedShot, fieldReveal);
    drawReceiverFace(g, w, h, t, d, resolvedShot, sourceFade);
  });
  drawInteractionScore(g, w, h, t, d, resolvedShot);
  return local;
}

function drawReceiverGardenOpticalOverlay(g, w, h, t, d) {
  if (!receiverGardenTransition || t < receiverGardenTransition.startSec
      || t >= receiverGardenTransition.endSec) return;
  const q = clamp((t - receiverGardenTransition.startSec)
                / Math.max(.001, receiverGardenTransition.endSec
                                  - receiverGardenTransition.startSec));
  const boundary = gardenThresholdScene?.startSec ?? receiverScene?.endSec ?? t;
  const beforeGarden = t < boundary;
  const outward = beforeGarden
    ? smooth(clamp((t - receiverGardenTransition.startSec)
                 / Math.max(.001, boundary - receiverGardenTransition.startSec)))
    : 1;
  const decay = beforeGarden ? 1
    : 1 - smooth(clamp((t - boundary)
                     / Math.max(.001, receiverGardenTransition.endSec - boundary)));
  const lens = {cx: w * .5, cy: h * .5,
                rx: w * lerp(.42, 1.18, outward),
                ry: h * lerp(.56, 1.42, outward), turn: lerp(-.05, .02, outward)};
  const overlayShot = {kind: 'receiver-garden-phaseplate', p: outward, cue: null};
  drawReceiverOpticalDistortion(g, w, h, lens, t, d, decay * .3);
  drawReceiverContours(g, w, h, lens, t, d, overlayShot, decay * .34);
}

const BIOLOGICAL_SWIMMER_CLIP = 'cmu-125-06-freestyle';

function motionPoseAt(id, seconds, phase = 0, speed = 1) {
  const clip = motionClips[id];
  if (!clip?.frames?.length) return null;
  const framePosition = (((seconds * speed + phase) % clip.durationSec + clip.durationSec)
                        % clip.durationSec) * clip.sampleRate;
  const firstIndex = Math.floor(framePosition) % clip.frames.length;
  const secondIndex = (firstIndex + 1) % clip.frames.length;
  const q = framePosition - Math.floor(framePosition);
  const first = clip.frames[firstIndex], second = clip.frames[secondIndex];
  const pose = {};
  for (const [name, jointIndex] of Object.entries(clip.jointIndex)) {
    const offset = jointIndex * 3;
    pose[name] = [
      lerp(first[offset], second[offset], q),
      lerp(first[offset + 1], second[offset + 1], q),
      lerp(first[offset + 2], second[offset + 2], q),
    ];
  }
  return pose;
}

function musicalBeatAt(seconds) {
  if (beatTimes.length < 2) return seconds * 1.4;
  let lower = 0, upper = beatTimes.length - 1;
  while (lower + 1 < upper) {
    const middle = (lower + upper) >> 1;
    if (beatTimes[middle] <= seconds) lower = middle;
    else upper = middle;
  }
  if (seconds < beatTimes[0]) {
    const span = Math.max(.001, beatTimes[1] - beatTimes[0]);
    return (seconds - beatTimes[0]) / span;
  }
  if (seconds >= beatTimes.at(-1)) {
    const span = Math.max(.001, beatTimes.at(-1) - beatTimes.at(-2));
    return beatTimes.length - 1 + (seconds - beatTimes.at(-1)) / span;
  }
  const span = Math.max(.001, beatTimes[upper] - beatTimes[lower]);
  return lower + (seconds - beatTimes[lower]) / span;
}

function midpoint(a, b) {
  return [(a.x + b.x) * .5, (a.y + b.y) * .5, (a.depth + b.depth) * .5];
}

function motionCurve(points) {
  const path = new Path2D();
  if (!points.length) return path;
  path.moveTo(points[0].x, points[0].y);
  for (let index = 1; index < points.length - 1; index++) {
    const next = midpoint(points[index], points[index + 1]);
    path.quadraticCurveTo(points[index].x, points[index].y, next[0], next[1]);
  }
  const last = points.at(-1);
  if (points.length > 1) {
    const previous = points.at(-2);
    path.quadraticCurveTo(previous.x, previous.y, last.x, last.y);
  }
  return path;
}

function projectSwimmerPose(pose, cx, cy, size, roll = 0, direction = 1,
                            crossScale = 1) {
  const projected = {};
  const cosine = Math.cos(roll), sine = Math.sin(roll);
  for (const [name, point] of Object.entries(pose)) {
    const along = point[2] * size * direction;
    const across = (point[0] * .76 - point[1] * .14) * size * crossScale;
    projected[name] = {
      x: cx + along * cosine - across * sine,
      y: cy + along * sine + across * cosine,
      depth: point[1],
    };
  }
  return projected;
}

function drawMotionRig(g, points, size, alpha) {
  const chains = [
    ['root', 'head'],
    ['root', 'lclavicle', 'lhumerus', 'lradius', 'lhand'],
    ['root', 'rclavicle', 'rhumerus', 'rradius', 'rhand'],
  ];
  for (const chain of chains) {
    pathStroke(g, motionCurve(chain.map(name => points[name]).filter(Boolean)), '#ffdf82',
               Math.max(.7, size * .006), alpha * .26, 3);
  }
  for (const [index, point] of Object.values(points).entries()) {
    glowDot(g, point.x, point.y, Math.max(1.2, size * .012),
            index % 2 ? '#ff80c8' : '#74f6e6', alpha * .8);
  }
}

function flagellumPoints(root, head, size, t, d, options = {}, phaseOffset = 0) {
  let forwardX = head.x - root.x;
  let forwardY = head.y - root.y;
  const forwardLength = Math.hypot(forwardX, forwardY);
  if (forwardLength < .001) {
    const fallback = options.roll || 0;
    forwardX = Math.cos(fallback) * (options.direction || 1);
    forwardY = Math.sin(fallback) * (options.direction || 1);
  } else {
    forwardX /= forwardLength;
    forwardY /= forwardLength;
  }
  const backX = -forwardX;
  const backY = -forwardY;
  const normalX = -backY;
  const normalY = backX;
  const beat = musicalBeatAt(t);
  const actorPhase = (options.phase || 0) * .73 + phaseOffset;
  const broadPhase = beat * Math.PI * .82 + actorPhase;
  const pulseCenter = ((beat * .82 + actorPhase * .19) % 1 + 1) % 1;
  const tailLength = size * (.9 + d.bassBody * .16 + phaseOffset * .025);
  const points = [];
  for (let index = 0; index <= 12; index++) {
    const s = index / 12;
    const rootEase = smooth(clamp(s / .2));
    const broadAmplitude = size * (.026 + d.bassBody * .048)
                         * rootEase * (.28 + s * .82);
    const broadWave = Math.sin(broadPhase - s * TAU * 1.18) * broadAmplitude;
    const packetDistance = (s - pulseCenter) / .115;
    const packet = Math.exp(-packetDistance * packetDistance)
                 * Math.sin((s - pulseCenter) * TAU * 2.2)
                 * size * (.018 + d.drums * .085) * rootEase;
    const filament = Math.sin(broadPhase * 1.37 - s * TAU * 1.72 + phaseOffset * 2.4)
                   * size * phaseOffset * .012 * rootEase * s;
    const reach = tailLength * s;
    const curl = Math.sin(broadPhase * .43 - s * Math.PI) * size * .018 * s;
    points.push({
      x: root.x + backX * (reach + curl) + normalX * (broadWave + packet + filament),
      y: root.y + backY * (reach + curl) + normalY * (broadWave + packet + filament),
      depth: root.depth,
    });
  }
  return points;
}

function drawMusicalFlagellum(g, root, head, size, t, d, alpha, options) {
  const mainPoints = flagellumPoints(root, head, size, t, d, options, 0);
  const upperPoints = flagellumPoints(root, head, size * .98, t, d, options, .46);
  const lowerPoints = flagellumPoints(root, head, size * .94, t, d, options, -.38);
  const main = motionCurve(mainPoints);
  const upper = motionCurve(upperPoints);
  const lower = motionCurve(lowerPoints);
  pathStroke(g, main, '#62e4d2', size * .105, alpha * .1, size * .12);
  pathStroke(g, main, '#b9fff0', size * .037 * (1 + d.bassBody * .2),
             alpha * .78, size * .052);
  pathStroke(g, main, '#fff0bd', size * .008, alpha * .7, size * .024);
  pathStroke(g, upper, '#ff8fc8', size * .012, alpha * .48, size * .033);
  pathStroke(g, lower, '#72eedb', size * .009, alpha * .43, size * .03);
  const tip = mainPoints.at(-1);
  const beforeTip = mainPoints.at(-2);
  glowDot(g, tip.x, tip.y, size * (.012 + d.drums * .009),
          '#fff0bd', alpha * (.48 + d.drums * .3));
  return {
    points: mainPoints,
    tip,
    energy: clamp(d.bassBody * .58 + d.drumBody * .3 + d.drums * .48),
    notationRoll: Math.atan2(root.y - beforeTip.y, root.x - beforeTip.x),
  };
}

function drawTailNotation(g, x, y, size, roll, energy, alpha, phase) {
  const cosine = Math.cos(roll), sine = Math.sin(roll);
  for (let ring = 0; ring < 5; ring++) {
    const travel = ((phase * .4 + ring / 5) % 1);
    const length = size * (.1 + travel * (.56 + energy * .28));
    const spread = size * (.035 + travel * .13);
    const path = new Path2D();
    const startX = x - cosine * length * .08;
    const startY = y - sine * length * .08;
    path.moveTo(startX - sine * spread, startY + cosine * spread);
    path.bezierCurveTo(x - cosine * length * .28 - sine * spread * .7,
                       y - sine * length * .28 + cosine * spread * .7,
                       x - cosine * length * .72 + sine * spread * .62,
                       y - sine * length * .72 - cosine * spread * .62,
                       x - cosine * length + sine * spread * .15,
                       y - sine * length - cosine * spread * .15);
    pathStroke(g, path, ring % 2 ? '#75f0dc' : '#ff86c8',
               .7 + energy * 1.8, alpha * (1 - travel) * .4, 8);
  }
}

function drawChromeSwimmer(g, w, h, t, d, options = {}) {
  const pose = motionPoseAt(BIOLOGICAL_SWIMMER_CLIP,
                            t - riverScene.startSec,
                            options.phase || 0, options.speed || 1);
  if (!pose) return null;
  const size = options.size || w * .22;
  const alpha = options.alpha ?? 1;
  const points = projectSwimmerPose(pose, options.x, options.y, size,
                                    options.roll || 0, options.direction || 1,
                                    options.crossScale || 1);
  const shoulder = {
    x: (points.lclavicle.x + points.rclavicle.x) * .5,
    y: (points.lclavicle.y + points.rclavicle.y) * .5,
    depth: (points.lclavicle.depth + points.rclavicle.depth) * .5,
  };
  const body = motionCurve([points.root, shoulder, points.head]);
  const leftFin = motionCurve([points.lhumerus, points.lradius, points.lhand]);
  const rightFin = motionCurve([points.rhumerus, points.rradius, points.rhand]);

  g.save();
  g.globalCompositeOperation = 'screen';
  const flagellum = drawMusicalFlagellum(g, points.root, points.head, size,
                                         t, d, alpha, options);
  if (options.ripples) {
    drawTailNotation(g, flagellum.tip.x, flagellum.tip.y, size,
                     flagellum.notationRoll, flagellum.energy, alpha,
                     musicalBeatAt(t) + (options.phase || 0));
  }
  const normalX = -Math.sin(options.roll || 0);
  const normalY = Math.cos(options.roll || 0);
  const shell = new Path2D();
  shell.moveTo(points.root.x + normalX * size * .022,
               points.root.y + normalY * size * .022);
  shell.bezierCurveTo(points.root.x + normalX * size * .072,
                      points.root.y + normalY * size * .072,
                      shoulder.x + normalX * size * .058,
                      shoulder.y + normalY * size * .058,
                      shoulder.x + normalX * size * .058,
                      shoulder.y + normalY * size * .058);
  shell.bezierCurveTo(points.head.x + normalX * size * .048,
                      points.head.y + normalY * size * .048,
                      points.head.x - normalX * size * .038,
                      points.head.y - normalY * size * .038,
                      shoulder.x - normalX * size * .052,
                      shoulder.y - normalY * size * .052);
  shell.bezierCurveTo(points.root.x - normalX * size * .064,
                      points.root.y - normalY * size * .064,
                      points.root.x - normalX * size * .022,
                      points.root.y - normalY * size * .022,
                      points.root.x + normalX * size * .022,
                      points.root.y + normalY * size * .022);
  shell.closePath();
  const chrome = g.createLinearGradient(points.root.x, points.root.y,
                                        points.head.x, points.head.y);
  chrome.addColorStop(0, '#238d91');
  chrome.addColorStop(.34, '#bdfef0');
  chrome.addColorStop(.58, '#486ea5');
  chrome.addColorStop(.78, '#f8e3bd');
  chrome.addColorStop(1, '#4bc7c1');
  g.fillStyle = chrome;
  g.globalAlpha = alpha * .16;
  g.shadowColor = '#84f1e4';
  g.shadowBlur = size * .085;
  g.fill(shell);
  pathStroke(g, shell, '#bffcf1', size * .008, alpha * .34, size * .035);
  for (const [elbow, wrist, hand, color, side] of [
    [points.lhumerus, points.lradius, points.lhand, '#8ff4df', 1],
    [points.rhumerus, points.rradius, points.rhand, '#ff91c9', -1],
  ]) {
    const finShell = new Path2D();
    const offsetX = normalX * size * .028 * side;
    const offsetY = normalY * size * .028 * side;
    finShell.moveTo(elbow.x, elbow.y);
    finShell.quadraticCurveTo(wrist.x, wrist.y, hand.x, hand.y);
    finShell.bezierCurveTo(hand.x + offsetX * 1.7, hand.y + offsetY * 1.7,
                           wrist.x + offsetX, wrist.y + offsetY,
                           elbow.x, elbow.y);
    finShell.closePath();
    g.fillStyle = color;
    g.globalAlpha = alpha * .12;
    g.shadowColor = color;
    g.shadowBlur = size * .04;
    g.fill(finShell);
  }
  pathStroke(g, body, '#78dcd6', size * .12, alpha * .11, size * .13);
  pathStroke(g, body, '#c8fff6', size * .047 * (1 + d.master * .18),
             alpha * .86, size * .055);
  pathStroke(g, body, '#fff2c5', size * .009, alpha * .72, size * .025);
  pathStroke(g, leftFin, '#9ff9e3', size * .025, alpha * .72, size * .04);
  pathStroke(g, rightFin, '#ff9fd2', size * .022, alpha * .66, size * .04);

  for (const [hand, color] of [[points.lhand, '#9ff9e3'], [points.rhand, '#ff9fd2']]) {
    g.save();
    g.translate(hand.x, hand.y);
    g.rotate((options.roll || 0) + hand.depth * .5);
    g.beginPath();
    g.ellipse(0, 0, size * .052, size * (.012 + Math.abs(hand.depth) * .018),
              0, 0, TAU);
    g.fillStyle = color;
    g.globalAlpha = alpha * .2;
    g.shadowColor = color;
    g.shadowBlur = size * .045;
    g.fill();
    g.restore();
  }

  const direction = options.direction || 1;
  const headAngle = options.roll || 0;
  const eyeX = points.head.x + Math.cos(headAngle) * size * .018 * direction;
  const eyeY = points.head.y + Math.sin(headAngle) * size * .018 * direction - size * .018;
  const eye = new Path2D();
  eye.moveTo(eyeX - size * .032, eyeY);
  eye.bezierCurveTo(eyeX - size * .008, eyeY - size * .021,
                    eyeX + size * .021, eyeY - size * .018,
                    eyeX + size * .036, eyeY + size * .002);
  pathStroke(g, eye, '#fff5d7', size * .012, alpha * .92, size * .035);
  glowDot(g, eyeX + size * .008, eyeY - size * .005, size * .011,
          '#63f3e4', alpha * .75);
  const mouth = new Path2D();
  const mouthOpen = .012 + d.voice * .025;
  mouth.moveTo(points.head.x - size * .006, points.head.y + size * .025);
  mouth.bezierCurveTo(points.head.x + size * .018 * direction,
                      points.head.y + size * (mouthOpen + .017),
                      points.head.x + size * .055 * direction,
                      points.head.y + size * (mouthOpen * .2 + .018),
                      points.head.x + size * .071 * direction,
                      points.head.y + size * .004);
  pathStroke(g, mouth, '#ff9acb', size * (.009 + d.voice * .006),
             alpha * .85, size * .035);
  if (motionDebug) drawMotionRig(g, points, size, alpha);
  g.restore();
  return {points, tail: flagellum.tip, head: points.head, tailEnergy: flagellum.energy};
}

let semanticNoteEventsCache = null;

function semanticNoteEvents() {
  if (semanticNoteEventsCache) return semanticNoteEventsCache;
  semanticNoteEventsCache = (performanceControls.notes?.['diva-notes'] || [])
    .filter(event => event.on >= semanticScene.startSec - .05
                  && event.on < semanticScene.endSec)
    .map((event, index) => ({...event, index}));
  return semanticNoteEventsCache;
}

function semanticNoteLayout(event) {
  return {
    pitchHeight: clamp((event.pitch - 37) / 42),
    depth: hash(event.index * 5.17 + event.pitch * .81),
  };
}

function semanticNoteTrailPoint(w, h, event, u, t, shot, d) {
  const {pitchHeight, depth} = semanticNoteLayout(event);
  const travel = event.index % 2 ? u : 1 - u;
  if (shot.kind === 'semantic-call-response') {
    const angle = travel * TAU * 1.12 + event.index * .21 + t * .04;
    const radius = w * (.14 + depth * .23 + Math.sin(u * Math.PI) * .045);
    return {
      x: w * .5 + Math.cos(angle) * radius,
      y: h * .48 + Math.sin(angle) * h * (.17 + depth * .18)
         + (pitchHeight - .5) * h * .2,
    };
  }
  if (shot.kind === 'semantic-filament-weather') {
    const x = lerp(-w * .18, w * 1.18, u);
    const laneY = lerp(h * .78, h * .16, pitchHeight);
    const phrase = Math.sin(u * TAU * (1.05 + depth * .3)
                          - t * .35 + event.index * .38);
    return {
      x: x + phrase * w * (.035 + depth * .04),
      y: laneY + phrase * h * (.08 + depth * .11)
         + Math.sin(u * Math.PI) * (event.index % 2 ? 1 : -1) * h * .08,
    };
  }
  if (shot.kind === 'semantic-rocket-overhead') {
    const direction = event.index % 2 ? 1 : -1;
    const x = direction > 0 ? lerp(-w * .22, w * 1.25, u)
                            : lerp(w * 1.22, -w * .25, u);
    const arch = Math.sin(clamp(u) * Math.PI);
    return {
      x,
      y: h * (.14 + (1 - pitchHeight) * .28)
         + arch * h * (.2 + depth * .27)
         + Math.sin(u * TAU * 1.6 + event.index) * h * .018 * d.bassBody,
    };
  }
  const x = lerp(-w * .25, w * 1.25, u);
  const riverY = h * (.5
    + Math.sin(u * TAU * 1.08 - (t - semanticScene.startSec) * .22) * .112
    + Math.sin(u * TAU * .48 + t * .135 + .8) * .048
    + (pitchHeight - .5) * .22);
  const skyY = h * (.03 + pitchHeight * .18)
             + Math.sin(u * TAU + event.index) * h * .07;
  const condense = smooth(clamp(u * 1.16 - .1));
  return {
    x,
    y: lerp(skyY, riverY, condense)
       + Math.sin(u * TAU * 2 + event.index) * h * .012 * (1 - condense),
  };
}

function drawSemanticNoteTrails(g, w, h, t, d, shot, foreground = false) {
  const leadIn = .78;
  const tailOut = 1.28;
  const visible = semanticNoteEvents().map(event => {
    const start = event.on - leadIn;
    const end = event.off + tailOut;
    return {event, start, end, progress: clamp((t - start) / (end - start)),
            ...semanticNoteLayout(event)};
  }).filter(note => t >= note.start && t <= note.end
                  && (foreground ? note.depth > .56 : note.depth <= .56))
    .sort((a, b) => a.depth - b.depth);
  for (const note of visible) {
    const duration = Math.max(.05, note.event.off - note.event.on);
    const trailLength = .08 + Math.min(2.1, duration) * .18;
    const points = [];
    for (let index = 0; index <= 28; index++) {
      const u = note.progress - trailLength * (1 - index / 28);
      points.push(semanticNoteTrailPoint(w, h, note.event, u, t, shot, d));
    }
    const path = motionCurve(points);
    const color = NOTE_COLORS[note.event.pitch % 12];
    const onset = Math.exp(-Math.abs(t - note.event.on) * 5.4);
    const edgeFade = smooth(clamp(note.progress / .1))
                   * smooth(clamp((1 - note.progress) / .14));
    pathStroke(g, path, color, .85 + note.depth * 2.8,
               edgeFade * (.38 + note.event.velocity * .46),
               8 + note.depth * 18);
    const head = points.at(-1);
    glowDot(g, head.x, head.y, 1.4 + note.depth * 4.4 + onset * 2.5,
            color, edgeFade * (.42 + onset * .5));
  }
}

function semanticCamera(shot, w, h) {
  const p = smooth(shot.p);
  if (shot.kind === 'semantic-call-response') {
    return mixCamera({x: w * .035, y: h * .03, zoom: .88, roll: -.035, pitch: .93},
                     {x: -w * .025, y: -h * .015, zoom: 1.04, roll: .018, pitch: .96}, p);
  }
  if (shot.kind === 'semantic-filament-weather') {
    return mixCamera({x: -w * .06, y: h * .01, zoom: 1.02, roll: .03, pitch: .94},
                     {x: w * .15, y: -h * .04, zoom: 1.3, roll: -.075, pitch: .87}, p);
  }
  if (shot.kind === 'semantic-rocket-overhead') {
    return mixCamera({x: w * .08, y: h * .09, zoom: 1.22, roll: -.11, pitch: .85},
                     {x: -w * .12, y: -h * .07, zoom: .83, roll: .12, pitch: .9}, p);
  }
  return mixCamera({x: w * .07, y: -h * .12, zoom: .82, roll: .12, pitch: .88},
                   {x: w * .015, y: h * .015, zoom: 1.03, roll: -.045, pitch: .94}, p);
}

function drawSemanticBackdrop(g, w, h, t, d, shot) {
  const field = g.createRadialGradient(w * .52, h * .42, 0,
                                      w * .52, h * .42, Math.max(w, h));
  const warm = shot.kind === 'semantic-rocket-overhead';
  field.addColorStop(0, warm ? '#261536' : '#10203c');
  field.addColorStop(.54, warm ? '#140c2b' : '#071329');
  field.addColorStop(1, '#020512');
  g.fillStyle = field;
  g.fillRect(-w, -h, w * 3, h * 3);
  g.save();
  g.globalCompositeOperation = 'screen';
  for (let index = 0; index < 62; index++) {
    const depth = .18 + hash(index * 2.73) * .82;
    const drift = (t - semanticScene.startSec) * (.0008 + depth * .0032);
    const x = ((((hash(index * 7.31) + drift) % 1.22) + 1.22) % 1.22 - .11) * w;
    const y = (hash(index * 11.9 + 3) + Math.sin(t * .09 + index) * .012) * h;
    glowDot(g, x, y, .25 + depth * 1.45,
            index % 5 ? '#7691cc' : '#ffc88c', .045 + depth * .11);
  }
  g.restore();
}

function drawSemanticWeather(g, w, h, t, d, shot) {
  if (shot.kind === 'semantic-call-response') {
    for (let ring = 0; ring < 9; ring++) {
      const q = ring / 8;
      const path = new Path2D();
      path.ellipse(w * .5, h * .48, w * (.12 + q * .43), h * (.09 + q * .28),
                   t * (.018 + q * .007) + q * .28, 0, TAU);
      pathStroke(g, path, ring % 2 ? '#65e2cf' : '#ff9a72',
                 .7 + q * 1.1 + d.bassBody * .6,
                 .12 + (1 - q) * .18 + d.masterBody * .08, 7 + q * 8);
    }
    return;
  }
  if (shot.kind === 'semantic-filament-weather') {
    for (let line = 0; line < 13; line++) {
      const q = line / 12;
      const y = h * lerp(.14, .82, q);
      const path = new Path2D();
      path.moveTo(-w * .25, y + Math.sin(t * .25 + line) * h * .04);
      path.bezierCurveTo(w * .13, y - h * (.18 - q * .08),
                         w * .54, y + h * (.17 - q * .06),
                         w * 1.25, y + Math.sin(t * .31 + line * .8) * h * .09);
      const color = line % 3 === 0 ? '#ff936e' : line % 3 === 1 ? '#73ead4' : '#9aa8ff';
      pathStroke(g, path, color, 1 + (line % 4) * .55 + d.bassBody,
                 .12 + (line % 4) * .035 + d.masterBody * .08, 9 + (line % 3) * 5);
    }
    return;
  }
  if (shot.kind === 'semantic-rocket-overhead') {
    const clap = d.drums + d.drumBody * .45;
    for (let front = 0; front < 8; front++) {
      const q = front / 7;
      const path = new Path2D();
      path.moveTo(-w * .28, h * (.04 + q * .11));
      path.bezierCurveTo(w * .18, h * (.02 + q * .03),
                         w * .52, h * (.58 - q * .12),
                         w * 1.3, h * (.1 + q * .28));
      pathStroke(g, path, front % 2 ? '#ff7a86' : '#f4c86b',
                 4 + q * 11 + clap * 8,
                 .035 + q * .035 + clap * .04, 18 + q * 22);
    }
    for (let echo = 0; echo < 5; echo++) {
      const radius = w * (.1 + echo * .09 + d.drums * .035);
      const arc = new Path2D();
      arc.ellipse(w * .52, -h * .04, radius, radius * .52,
                  .03 + echo * .08, .08, Math.PI - .08);
      pathStroke(g, arc, '#c6b5ff', 1 + echo * .4,
                 .13 + clap * .1, 8 + echo * 5);
    }
    return;
  }
  const morph = smooth(shot.p);
  for (let line = 0; line < 18; line++) {
    const q = line / 17;
    const points = [];
    for (let index = 0; index <= 30; index++) {
      const u = index / 30;
      const sky = {
        x: lerp(-w * .38, w * 1.38, u),
        y: h * (.05 + q * .32 + Math.sin(u * TAU + line * .37 - t * .22) * .1),
      };
      const river = riverFlowFieldPoint(w, h, u, lerp(-.128, .128, q),
                                        line, riverScene.startSec, d);
      points.push({x: lerp(sky.x, river.x, morph),
                   y: lerp(sky.y, river.y, morph)});
    }
    const color = ['#ff9879', '#88e4d7', '#829bc8', '#d5fff2'][line % 4];
    pathStroke(g, motionCurve(points), color,
               .8 + (line % 4) * .5 + d.masterBody * .5,
               .12 + morph * .12 + (line % 5 === 1 ? .07 : 0),
               6 + morph * 5);
  }
}

function drawSemanticWitnesses(g, w, h, t, d, shot) {
  if (shot.kind === 'semantic-call-response') {
    const answer = smooth(shot.p);
    drawMarsFaceActor(g, w * (.23 + answer * .025), h * .54, h * .48,
                      '#81f0d7', t, d, .3, .96, -.08, true);
    drawMarsFaceActor(g, w * (.77 - answer * .025), h * .49, h * .44,
                      '#ffae83', t, d, 2.1, .9, .09, false);
  } else if (shot.kind === 'semantic-filament-weather') {
    drawMarsFaceActor(g, -w * .015, h * .57, h * .55,
                      '#81f0d7', t, d, .7, .7, -.12, true);
    drawMarsFaceActor(g, w * 1.015, h * .42, h * .43,
                      '#ffae83', t, d, 2.7, .58, .1, false);
  } else if (shot.kind === 'semantic-rocket-overhead') {
    drawMarsFaceActor(g, w * .2, h * .73, h * .32,
                      '#81f0d7', t, d, 1.2, .64, -.08, true);
    drawMarsFaceActor(g, w * .82, h * .74, h * .29,
                      '#ffae83', t, d, 3.2, .55, .1, false);
  } else {
    const fade = 1 - smooth(clamp((shot.p - .22) / .45));
    drawMarsFaceActor(g, w * .14, h * .33, h * .32,
                      '#81f0d7', t, d, 1.6, fade * .5, -.08, true);
    drawMarsFaceActor(g, w * .87, h * .27, h * .27,
                      '#ffae83', t, d, 3.8, fade * .42, .1, false);
  }
}

function drawSemanticRiverReveal(g, w, h, t, d, shot) {
  const reveal = smooth(clamp((shot.p - .58) / .42));
  if (reveal <= 0) return;
  if (semanticRiverLayer.width !== w || semanticRiverLayer.height !== h) {
    semanticRiverLayer.width = w;
    semanticRiverLayer.height = h;
  }
  semanticRiverCtx.setTransform(1, 0, 0, 1, 0, 0);
  semanticRiverCtx.clearRect(0, 0, w, h);
  const riverShot = {kind: 'river-moon-descent', p: 0, start: riverScene.startSec,
                     end: riverScene.startSec + 2.68};
  drawRiverScene(semanticRiverCtx, w, h,
                 lerp(t, riverScene.startSec, reveal), d, riverShot);
  g.save();
  g.globalAlpha = reveal;
  g.drawImage(semanticRiverLayer, 0, 0);
  g.restore();
}

function drawSemanticScene(g, w, h, t, d, shot) {
  const local = clamp((t - semanticScene.startSec)
                    / Math.max(.001, semanticScene.endSec - semanticScene.startSec));
  withCamera(g, w, h, semanticCamera(shot, w, h), () => {
    drawSemanticBackdrop(g, w, h, t, d, shot);
    drawSemanticNoteTrails(g, w, h, t, d, shot, false);
    drawSemanticWeather(g, w, h, t, d, shot);
    drawSemanticWitnesses(g, w, h, t, d, shot);
    drawSemanticNoteTrails(g, w, h, t, d, shot, true);
  });
  if (shot.kind === 'semantic-rain-to-river') {
    drawSemanticRiverReveal(g, w, h, t, d, shot);
  }
  return local;
}

function riverFlowFieldPoint(w, h, u, laneOffset, strand, t, d) {
  const elapsed = t - riverScene.startSec;
  const strandNoise = hash(strand * 4.73 + 1.9);
  const broadPhase = u * TAU * 1.08 - elapsed * .22;
  const longPhase = u * TAU * .48 + elapsed * .135 + .8;
  const broad = Math.sin(broadPhase) * (.112 + d.bassBody * .03);
  const longSwell = Math.sin(longPhase) * (.048 + d.masterBody * .014);
  const laneBreath = laneOffset * (1 + Math.sin(u * TAU * .62
                          - elapsed * .19 + strand * .31) * .5);
  const exchange = Math.sin(u * TAU * (1.17 + strandNoise * .08)
                         - elapsed * (.25 + strandNoise * .08)
                         + strand * .73
                         + Math.sin(longPhase) * 1.08) * .022;
  const surface = Math.sin(u * TAU * 2.08 + elapsed * .3
                        + strand * .49 + Math.sin(broadPhase) * 1.4) * .007;
  return {
    x: lerp(-w * .58, w * 1.58, u)
     + Math.cos(longPhase + strand * .17) * w * .005
     + laneOffset * elapsed * w * .018,
    y: h * (.5 + broad + longSwell + laneBreath + exchange + surface),
    depth: 0,
  };
}

function riverFlowPath(w, h, laneOffset, strand, t, d) {
  const points = [];
  for (let index = 0; index <= 28; index++) {
    points.push(riverFlowFieldPoint(w, h, index / 28,
                                   laneOffset, strand, t, d));
  }
  return motionCurve(points);
}

function drawRiverWorld(g, w, h, t, d, local, shot) {
  const field = g.createRadialGradient(w * .52, h * .45, 0,
                                      w * .52, h * .45, Math.max(w, h));
  field.addColorStop(0, '#14213f');
  field.addColorStop(.48, '#08132f');
  field.addColorStop(1, '#020716');
  g.fillStyle = field;
  g.fillRect(-w, -h, w * 3, h * 3);

  g.save();
  g.globalCompositeOperation = 'screen';
  const starTravel = t - riverScene.startSec;
  for (let index = 0; index < 54; index++) {
    const travel = starTravel * (.0007 + hash(index * 3.17) * .0018);
    const x = ((((hash(index * 8.11) + travel) % 1.16) + 1.16) % 1.16 - .08) * w;
    const y = hash(index * 11.27 + 2) * h * .8;
    const pulse = .45 + Math.sin(t * (.4 + hash(index) * .7) + index) * .22;
    glowDot(g, x, y, .35 + hash(index + 9) * 1.35,
            index % 7 ? '#8da7df' : '#ffca91', .08 + pulse * .12);
  }
  g.restore();

  const moonX = w * (.77 - local * .035);
  const moonY = h * (.17 + Math.sin(t * .16) * .018);
  const moonR = Math.min(w, h) * (.095 + d.bass * .012);
  const moon = g.createRadialGradient(moonX - moonR * .3, moonY - moonR * .35,
                                     moonR * .08, moonX, moonY, moonR);
  moon.addColorStop(0, '#fff0b9');
  moon.addColorStop(.35, '#db9e76');
  moon.addColorStop(1, '#9d3d4d');
  g.save();
  g.globalAlpha = .78;
  g.shadowColor = '#f27e8d';
  g.shadowBlur = moonR * .38;
  g.fillStyle = moon;
  g.beginPath();
  g.arc(moonX, moonY, moonR, 0, TAU);
  g.fill();
  g.restore();

  const terrainTop = new Path2D();
  terrainTop.moveTo(-w * .85, h * .17);
  terrainTop.bezierCurveTo(-w * .34, h * (.04 + d.bass * .025),
                           w * .05, h * .28, w * .43, h * .12);
  terrainTop.bezierCurveTo(w * .83, h * .01, w * 1.27, h * .34, w * 1.85, h * .17);
  terrainTop.lineTo(w * 1.85, -h * .85);
  terrainTop.lineTo(-w * .85, -h * .85);
  terrainTop.closePath();
  g.fillStyle = '#40142d';
  g.globalAlpha = .82;
  g.fill(terrainTop);

  const terrainBottom = new Path2D();
  terrainBottom.moveTo(-w * .85, h * .76);
  terrainBottom.bezierCurveTo(-w * .34, h * .91, w * .05, h * .58,
                              w * .46, h * .77);
  terrainBottom.bezierCurveTo(w * .86, h * .92, w * 1.31, h * .58,
                              w * 1.85, h * .76);
  terrainBottom.lineTo(w * 1.85, h * 1.85);
  terrainBottom.lineTo(-w * .85, h * 1.85);
  terrainBottom.closePath();
  g.fillStyle = '#6e2633';
  g.globalAlpha = .72;
  g.fill(terrainBottom);

  for (let layer = 0; layer < 5; layer++) {
    const laneOffset = lerp(.108, -.108, layer / 4);
    const river = riverFlowPath(w, h, laneOffset, 40 + layer, t, d);
    const colors = ['#081f3f', '#0d4764', '#126f7c', '#4a9e9c', '#a0e7d3'];
    pathStroke(g, river, colors[layer], h * (.17 - layer * .027),
               .2 + layer * .075, h * (.045 + layer * .008));
  }

  g.save();
  g.globalCompositeOperation = 'screen';
  const currentColors = ['#7edfd6', '#b9fff0', '#69b7c4', '#d2fff3', '#7fa9c9'];
  for (let line = 0; line < 18; line++) {
    const laneOffset = lerp(-.128, .128, line / 17);
    const current = riverFlowPath(w, h, laneOffset, line, t, d);
    const centerBias = 1 - Math.abs(line / 17 - .5) * 2;
    pathStroke(g, current, currentColors[line % currentColors.length],
               .65 + (line % 4) * .28 + d.masterBody * .45,
               .13 + centerBias * .18 + (line % 5 === 1 ? .08 : 0),
               4 + centerBias * 5);
  }
  g.restore();

}

function riverCamera(shot, w, h) {
  const p = clamp(shot.p);
  const moonStart = {x: w * .12, y: h * .09, zoom: .78, roll: -.055, pitch: .94};
  const moonReveal = {x: -w * .035, y: -h * .025, zoom: 1.06, roll: .012, pitch: .94};
  const swimmerClose = {x: -w * .145, y: h * .018, zoom: 1.2, roll: -.025, pitch: .91};
  const schoolWide = {x: w * .075, y: -h * .065, zoom: .78, roll: .19, pitch: .8};
  const waterline = {x: -w * .105, y: h * .02, zoom: 1.24, roll: -.045, pitch: .93};
  const macroStart = {x: w * .34, y: h * .16, zoom: 2.35, roll: -.43, pitch: .7};
  const macroEnd = {x: -w * .28, y: -h * .12, zoom: 3.15, roll: .14, pitch: .86};
  // The first two shots are one sustained move with a shared boundary. Linear
  // interpolation keeps both camera velocity and the swimmers' apparent
  // travel alive; the previous double easing produced a perceptible pause at
  // their introduction even though their own river clock never stopped.
  if (shot.kind === 'river-moon-descent') return mixCameraLinear(moonStart, moonReveal, p);
  if (shot.kind === 'river-chrome-entry') return mixCameraLinear(moonReveal, swimmerClose, p);
  if (shot.kind === 'river-current-macro') return mixCamera(macroStart, macroEnd, p);
  return mixCamera(schoolWide, waterline, p);
}

function riverActorFlowPoint(w, h, u, laneOffset, strand, t, d) {
  const point = riverFlowFieldPoint(w, h, u, laneOffset, strand, t, d);
  return {x: point.x / w, y: point.y / h};
}

function drawPathSwimmer(g, w, h, t, d, pathAt, u, options = {}) {
  const point = pathAt(u);
  const before = pathAt(u - .003);
  const after = pathAt(u + .003);
  const heading = Math.atan2((after.y - before.y) * h,
                             (after.x - before.x) * w);
  return drawChromeSwimmer(g, w, h, t, d, {
    ...options,
    x: point.x * w,
    y: point.y * h,
    roll: heading + (options.headingOffset || 0),
    direction: 1,
  });
}

const RIVER_CONTINUOUS_SCHOOL = [
  {lane: -.068, offset: .03, travel: .024, depth: .08, depthTravel: .08,
   size: .067, phase: .4, stroke: .76},
  {lane: -.034, offset: .2, travel: .029, depth: .22, depthTravel: .12,
   size: .074, phase: 1.7, stroke: .91},
  {lane: .012, offset: .37, travel: .026, depth: .36, depthTravel: .2,
   size: .088, phase: 2.9, stroke: .82},
  {lane: .058, offset: .55, travel: .034, depth: .51, depthTravel: .14,
   size: .083, phase: 4.2, stroke: .98, ripples: true},
  {lane: -.052, offset: .71, travel: .038, depth: .66, depthTravel: .18,
   size: .094, phase: 5.45, stroke: .86},
  {lane: .076, offset: .84, travel: .022, depth: .8, depthTravel: .15,
   size: .109, phase: 3.7, stroke: .73, ripples: true},
  {lane: .025, offset: .94, travel: .043, depth: .92, depthTravel: .05,
   size: .118, phase: 6.2, stroke: 1.02, alpha: .82},
  {lane: -.006, offset: .12, travel: .033, depth: .56, depthTravel: .52,
   size: .178, phase: .25, stroke: .9, ripples: true, featured: true},
];

function drawRiverSchool(g, w, h, t, d) {
  const elapsed = t - riverScene.startSec;
  const active = RIVER_CONTINUOUS_SCHOOL.map((actor, index) => {
    const raw = actor.offset + elapsed * actor.travel;
    const u = ((raw % 1) + 1) % 1;
    const depth = clamp(actor.depth + (u - .5) * (actor.depthTravel || 0)
                      + Math.sin(elapsed * .07 + actor.phase) * .035);
    return {...actor, index, u, depth};
  }).sort((a, b) => a.depth - b.depth);
  for (const actor of active) {
    const depthScale = .5 + actor.depth * .92;
    drawPathSwimmer(g, w, h, t, d,
      u => riverActorFlowPoint(w, h, u, actor.lane, 70 + actor.index, t, d),
      actor.u, {
        size: w * actor.size * depthScale,
        phase: actor.phase,
        speed: actor.stroke,
        alpha: (.17 + actor.depth * .7) * (actor.alpha || 1),
        crossScale: .7 + actor.depth * .34,
        ripples: Boolean(actor.ripples && actor.depth > .45),
      });
  }
}

let riverNoteEventsCache = null;

function riverNoteEvents() {
  if (riverNoteEventsCache) return riverNoteEventsCache;
  riverNoteEventsCache = (performanceControls.notes?.['diva-notes'] || [])
    .filter(event => event.on >= riverScene.startSec && event.on < riverScene.endSec)
    .map((event, index) => ({...event, index}));
  return riverNoteEventsCache;
}

function riverNoteLayout(event) {
  const pitchHeight = clamp((event.pitch - 36) / 30);
  const stableDepth = hash(event.index * 3.17 + event.pitch * .71);
  return {
    pitchHeight,
    laneOffset: lerp(.135, -.135, pitchHeight),
    depth: clamp(.16 + stableDepth * .58 + pitchHeight * .2),
  };
}

function riverNoteRibbonPath(w, h, t, d, event, headU, lengthU, laneOffset) {
  const points = [];
  for (let index = 0; index <= 18; index++) {
    const u = headU + lengthU * index / 18;
    points.push(riverFlowFieldPoint(w, h, u, laneOffset,
                                   120 + event.index, t, d));
  }
  return {path: motionCurve(points), head: points[0], tail: points.at(-1)};
}

function drawRiverNoteRibbon(g, w, h, t, d, event, progress, depth,
                             laneOffset) {
  const headU = lerp(.96, .04, progress);
  const duration = Math.max(.12, event.off - event.on);
  const velocity = clamp(event.velocity);
  const lengthU = .072 + Math.min(2.5, duration) * .078;
  const ribbon = riverNoteRibbonPath(w, h, t, d, event,
                                     headU, lengthU, laneOffset);
  const onset = Math.exp(-Math.abs(t - event.on) * 6.5);
  const edgeFade = smooth(clamp(progress / .13))
                 * smooth(clamp((1 - progress) / .16));
  const color = NOTE_COLORS[event.pitch % 12];
  const width = .75 + depth * 1.8 + velocity * .7;
  pathStroke(g, ribbon.path, color, width * 5.4,
             edgeFade * (.075 + depth * .07), 13 + depth * 19);
  pathStroke(g, ribbon.path, color, width * 1.35,
             edgeFade * (.64 + velocity * .3 + onset * .08), 5 + depth * 11);
  pathStroke(g, ribbon.path, '#fff7dc', Math.max(.32, width * .12),
             edgeFade * (.055 + onset * .18), 2 + onset * 5);
  glowDot(g, ribbon.head.x, ribbon.head.y,
          1.4 + depth * 3.4 + onset * 2.2,
          color, edgeFade * (.52 + onset * .4));
}

function drawRiverFlowMotes(g, w, h, t, d) {
  const elapsed = t - riverScene.startSec;
  const motes = [];
  for (let index = 0; index < 82; index++) {
    const depth = hash(index * 2.91 + 4.2);
    const speed = .128 + depth * .026;
    const phase = hash(index * 7.13 + 1.8);
    const u = 1 - (((phase + elapsed * speed) % 1 + 1) % 1);
    const laneOffset = lerp(-.16, .16, hash(index * 5.37 + 8.4));
    const point = riverFlowFieldPoint(w, h, u, laneOffset,
                                      220 + index, t, d);
    motes.push({index, depth, point});
  }
  motes.sort((a, b) => a.depth - b.depth);
  g.save();
  g.globalCompositeOperation = 'screen';
  for (const mote of motes) {
    const pulse = .72 + Math.sin(t * (.38 + mote.depth * .22)
                                + mote.index * 1.7) * .18;
    const radius = .28 + mote.depth * 2.15;
    const color = mote.index % 11 === 0 ? '#ffabd1'
                : mote.index % 5 === 0 ? '#fff0b2' : '#a4eee5';
    glowDot(g, mote.point.x, mote.point.y, radius, color,
            (.035 + mote.depth * .2) * pulse);
  }
  g.restore();
}

function riverVisibleNotesAt(t) {
  const leadIn = 1.2;
  const travelDuration = 6.2;
  return riverNoteEvents().filter(event => {
    const start = event.on - leadIn;
    return t >= start && t <= start + travelDuration;
  }).map(event => {
    const start = event.on - leadIn;
    const progress = clamp((t - start) / travelDuration);
    return {event, progress, ...riverNoteLayout(event)};
  });
}

function drawRiverNoteRibbons(g, w, h, t, d) {
  const visible = riverVisibleNotesAt(t).sort((a, b) => a.depth - b.depth);
  for (const note of visible) {
    drawRiverNoteRibbon(g, w, h, t, d, note.event,
                        smooth(note.progress), note.depth, note.laneOffset);
  }
}

function drawRiverMacroDetail(g, w, h, t, d) {
  const notes = riverVisibleNotesAt(t)
    .sort((a, b) => Math.abs(t - a.event.on) - Math.abs(t - b.event.on))
    .slice(0, 5)
    .sort((a, b) => a.depth - b.depth);
  g.save();
  g.globalCompositeOperation = 'screen';
  for (const note of notes) {
    const progress = smooth(note.progress);
    const headU = lerp(.96, .04, progress);
    const duration = Math.max(.12, note.event.off - note.event.on);
    const lengthU = .072 + Math.min(2.5, duration) * .078;
    const u = headU + lengthU * .34;
    const point = riverFlowFieldPoint(w, h, u, note.laneOffset,
                                      120 + note.event.index, t, d);
    const before = riverFlowFieldPoint(w, h, u - .003, note.laneOffset,
                                       120 + note.event.index, t, d);
    const after = riverFlowFieldPoint(w, h, u + .003, note.laneOffset,
                                      120 + note.event.index, t, d);
    const heading = Math.atan2(after.y - before.y, after.x - before.x);
    const onset = Math.exp(-Math.abs(t - note.event.on) * 3.4);
    const color = NOTE_COLORS[note.event.pitch % 12];
    const radius = w * (.013 + note.depth * .018)
                 * (1 + d.bassBody * .18 + onset * .36);
    g.save();
    g.translate(point.x, point.y);
    g.rotate(heading + Math.PI * .5);
    for (let ring = 0; ring < 3; ring++) {
      const q = ring / 2;
      const eddy = new Path2D();
      const wobble = Math.sin(t * (.8 + q * .24)
                            + note.event.pitch * .31 + ring) * .12;
      eddy.ellipse(0, 0,
                   radius * (1.05 + q * .62 + wobble),
                   radius * (.34 + q * .16 + d.masterBody * .08),
                   wobble * .35, 0, TAU);
      pathStroke(g, eddy, color, .65 + note.depth * 1.15,
                 .16 + onset * .28 + (1 - q) * .1, 7 + note.depth * 13);
    }
    for (let mote = 0; mote < 6; mote++) {
      const orbit = t * (.46 + note.depth * .22)
                  + mote / 6 * TAU + note.event.index;
      const orbitRadius = radius * (1.18 + (mote % 3) * .23);
      glowDot(g, Math.cos(orbit) * orbitRadius,
              Math.sin(orbit) * orbitRadius * .42,
              .55 + note.depth * 1.5, color,
              .22 + onset * .26);
    }
    g.restore();
  }
  g.restore();
}

const RIVER_SPIRO_COLORS = ['#68eee0', '#ffd56c', '#ff77bd', '#8d8cff',
                            '#71c9ff', '#ff8a68'];

function riverSpiroPoint(w, h, u, layer, t, scale = 1) {
  const family = layer % 3;
  const outer = [7, 5, 8][family];
  const inner = [3, 2, 3][family];
  const pen = outer * (.53 + hash(layer * 4.17) * .19);
  const turns = inner;
  const direction = layer % 2 ? -1 : 1;
  const rotation = t * (.025 + family * .008) * direction
                 + layer * .39;
  const theta = u * TAU * turns + rotation;
  const ratio = (outer - inner) / inner;
  const normalizer = outer - inner + pen;
  const nested = (.48 + layer / 17 * .76) * scale;
  const radius = Math.min(w, h) * .61 * nested;
  const x = ((outer - inner) * Math.cos(theta)
           + pen * Math.cos(ratio * theta)) / normalizer;
  const y = ((outer - inner) * Math.sin(theta)
           - pen * Math.sin(ratio * theta)) / normalizer;
  return {
    x: w * .52 + x * radius,
    y: h * .47 + y * radius * (.82 + family * .045),
  };
}

function riverSpiroMorphPath(w, h, t, d, layer, morph, scale) {
  const points = [];
  const laneOffset = lerp(-.15, .15, layer / 17);
  for (let index = 0; index <= 96; index++) {
    const q = index / 96;
    const river = riverFlowFieldPoint(w, h, lerp(-.14, 1.14, q),
                                      laneOffset, 360 + layer, t, d);
    const spiro = riverSpiroPoint(w, h, q, layer, t, scale);
    const bend = smooth(clamp((morph - Math.abs(q - .5) * .13) / .87));
    points.push({
      x: lerp(river.x, spiro.x, bend),
      y: lerp(river.y, spiro.y, bend),
    });
  }
  return motionCurve(points);
}

function drawRiverSpirographField(g, w, h, t, d, morph, scale = 1,
                                  opacity = 1) {
  const paths = [];
  for (let layer = 0; layer < 18; layer++) {
    paths.push(riverSpiroMorphPath(w, h, t, d, layer, morph, scale));
  }

  const saturation = smooth(clamp((morph - .18) / .72));
  if (saturation > .01) {
    g.save();
    g.globalCompositeOperation = 'screen';
    g.lineCap = 'round';
    g.lineJoin = 'round';
    g.filter = `blur(${Math.round(8 + saturation * 13)}px)`;
    for (let layer = 17; layer >= 0; layer -= 3) {
      g.strokeStyle = RIVER_SPIRO_COLORS[layer % RIVER_SPIRO_COLORS.length];
      g.globalAlpha = opacity * saturation * (.028 + d.masterBody * .022);
      g.lineWidth = h * (.075 + layer / 17 * .045);
      g.stroke(paths[layer]);
    }
    g.restore();
  }

  for (let layer = 0; layer < paths.length; layer++) {
    const color = RIVER_SPIRO_COLORS[layer % RIVER_SPIRO_COLORS.length];
    const depth = layer / 17;
    pathStroke(g, paths[layer], color,
               .72 + depth * 1.45 + d.masterBody * .45,
               opacity * (.16 + saturation * .28 + depth * .12),
               5 + saturation * 13 + depth * 7);
  }
}

function drawRiverSpiroNoteRibbons(g, w, h, t, d, scale, alpha = 1) {
  const visible = riverVisibleNotesAt(t).sort((a, b) => a.depth - b.depth);
  for (const note of visible) {
    const duration = Math.max(.12, note.event.off - note.event.on);
    const length = .035 + Math.min(2.5, duration) * .042;
    const head = 1 - smooth(note.progress) + note.event.index * .013;
    const layer = Math.round(note.pitchHeight * 17);
    const points = [];
    for (let index = 0; index <= 28; index++) {
      points.push(riverSpiroPoint(w, h, head + length * index / 28,
                                  layer, t, scale));
    }
    const path = motionCurve(points);
    const color = NOTE_COLORS[note.event.pitch % 12];
    const onset = Math.exp(-Math.abs(t - note.event.on) * 4.2);
    const edgeFade = smooth(clamp(note.progress / .12))
                   * smooth(clamp((1 - note.progress) / .14));
    pathStroke(g, path, color, 1.1 + note.depth * 2.5,
               alpha * edgeFade * (.48 + note.event.velocity * .34),
               9 + note.depth * 16);
    const tip = points[0];
    glowDot(g, tip.x, tip.y, 1.8 + note.depth * 3.5 + onset * 2,
            color, alpha * edgeFade * (.4 + onset * .45));
  }
}

function drawSpiroSwimmerTraces(g, w, h, t, d, progress, scale) {
  const reveal = smooth(clamp((progress - .12) / .64));
  if (reveal <= .001) return;
  for (let actor = 0; actor < 8; actor++) {
    const u = actor / 8 + (t - riverScene.startSec) * (.018 + actor * .0007);
    const layer = 3 + actor * 2;
    const points = [];
    for (let step = 0; step < 14; step++) {
      points.push(riverSpiroPoint(w, h, u - step * .0085,
                                  layer, t, scale));
    }
    const tail = motionCurve(points);
    const color = RIVER_SPIRO_COLORS[(actor + 2) % RIVER_SPIRO_COLORS.length];
    pathStroke(g, tail, color, .65 + actor * .055,
               reveal * (.16 + actor * .018), 7 + actor);
    glowDot(g, points[0].x, points[0].y, 1.4 + actor * .18,
            color, reveal * .34);
  }
}

function drawRiverSpirographBend(g, w, h, t, d, shot) {
  const p = smooth(shot.p);
  const local = clamp((t - riverScene.startSec)
                    / Math.max(.001, riverScene.endSec - riverScene.startSec));
  g.fillStyle = '#020716';
  g.fillRect(0, 0, w, h);

  if (p < .97) {
    withCamera(g, w, h, riverCamera({...shot, kind: 'river-tail-notation'}, w, h), () => {
      drawRiverWorld(g, w, h, t, d, local, shot);
      drawRiverFlowMotes(g, w, h, t, d);
      drawRiverNoteRibbons(g, w, h, t, d);
      drawRiverSchool(g, w, h, t, d);
    });
  }

  const veil = smooth(clamp((p - .04) / .84));
  g.save();
  g.globalCompositeOperation = 'source-over';
  g.globalAlpha = veil * .76;
  const gradient = g.createRadialGradient(w * .52, h * .47, 1,
                                          w * .52, h * .47, w * .72);
  gradient.addColorStop(0, '#160627');
  gradient.addColorStop(.58, '#07152b');
  gradient.addColorStop(1, '#02040d');
  g.fillStyle = gradient;
  g.fillRect(0, 0, w, h);
  g.restore();

  const scale = 1 + p * .08;
  drawRiverSpirographField(g, w, h, t, d, p, scale);
  drawSpiroSwimmerTraces(g, w, h, t, d, p, scale);
  drawRiverSpiroNoteRibbons(g, w, h, t, d, scale,
                            smooth(clamp((p - .2) / .66)));
  return local;
}

function drawTinyOrbitMouth(g, x, y, size, rotation, t, d, phase,
                            color, alpha) {
  const mouth = mouthAt(t + phase * .012);
  const open = .06 + mouth.open * .34 + d.voiceSustain * .17
             + Math.max(0, Math.sin(t * 2.1 + phase)) * d.echoBody * .045;
  const wide = .42 + mouth.wide * .16 - mouth.round * .07;
  g.save();
  g.translate(x, y);
  g.rotate(rotation);
  g.scale(size, size);
  const upper = new Path2D();
  const lower = new Path2D();
  const interior = new Path2D();
  upper.moveTo(-wide, 0);
  upper.bezierCurveTo(-wide * .58, -.12 - mouth.wide * .06,
                      -wide * .2, -.09, 0, -.035);
  upper.bezierCurveTo(wide * .2, -.09,
                       wide * .58, -.12 - mouth.wide * .06, wide, 0);
  lower.moveTo(-wide, 0);
  lower.bezierCurveTo(-wide * .44, open,
                       wide * .44, open, wide, 0);
  interior.moveTo(-wide, 0);
  interior.bezierCurveTo(-wide * .58, -.12 - mouth.wide * .06,
                         -wide * .2, -.09, 0, -.035);
  interior.bezierCurveTo(wide * .2, -.09,
                          wide * .58, -.12 - mouth.wide * .06, wide, 0);
  interior.bezierCurveTo(wide * .44, open,
                         -wide * .44, open, -wide, 0);
  interior.closePath();
  g.save();
  g.globalCompositeOperation = 'source-over';
  g.globalAlpha = alpha * .86;
  g.fillStyle = '#05020d';
  g.fill(interior);
  g.restore();
  depthKnockout(g, upper, 6.8 / size, alpha * .72);
  depthKnockout(g, lower, 6.8 / size, alpha * .72);
  pathStroke(g, upper, color, 1.8 / size, alpha, 7 / size);
  pathStroke(g, lower, '#ff9db7', 1.58 / size, alpha * .98, 7 / size);
  if (open > .085) {
    const teeth = new Path2D();
    teeth.moveTo(-wide * .6, open * .1);
    teeth.bezierCurveTo(-wide * .18, open * .21,
                         wide * .18, open * .21, wide * .6, open * .1);
    pathStroke(g, teeth, '#fff8e8', .72 / size,
               alpha * (.22 + mouth.teeth * .62), 2.5 / size);
  }
  if (open > .13) {
    const inner = new Path2D();
    inner.moveTo(-wide * .55, open * .54);
    inner.bezierCurveTo(-wide * .16, open * .79,
                         wide * .2, open * .77, wide * .57, open * .5);
    pathStroke(g, inner, '#ff5c94', .66 / size,
               alpha * clamp((open - .1) * 4.2), 3 / size);
  }
  g.restore();
}

function drawRiverMouthMicrocosm(g, w, h, t, d, shot) {
  const p = smooth(shot.p);
  const local = clamp((t - riverScene.startSec)
                    / Math.max(.001, riverScene.endSec - riverScene.startSec));
  const scale = 1.08 + p * .12;
  const gradient = g.createRadialGradient(w * .52, h * .47, 1,
                                          w * .52, h * .47, w * .75);
  gradient.addColorStop(0, '#240834');
  gradient.addColorStop(.42, '#071a33');
  gradient.addColorStop(1, '#02030c');
  g.fillStyle = gradient;
  g.fillRect(0, 0, w, h);
  const camera = {
    x: -w * .14 * p,
    y: h * (.035 * p + Math.sin(p * Math.PI) * .028),
    zoom: 1 + p * .23,
    roll: p * .17,
    pitch: 1,
  };
  withCamera(g, w, h, camera, () => {
    const fieldOpacity = lerp(1, .39, smooth(clamp(shot.p / .24)));
    drawRiverSpirographField(g, w, h, t, d, 1, scale, fieldOpacity);
    drawRiverSpiroNoteRibbons(g, w, h, t, d, scale, .96);

    const mouths = [];
    const count = 12;
    for (let index = 0; index < count; index++) {
      const layer = 1 + (index * 7) % 17;
      const u = index / count + (t - riverScene.startSec)
              * (.014 + (index % 3) * .003);
      const point = riverSpiroPoint(w, h, u, layer, t, scale);
      const before = riverSpiroPoint(w, h, u - .002, layer, t, scale);
      const after = riverSpiroPoint(w, h, u + .002, layer, t, scale);
      const depth = .5 + .5 * Math.sin(u * TAU + index * 1.73);
      const tangent = Math.atan2(after.y - before.y, after.x - before.x);
      mouths.push({index, point, depth,
        rotation: Math.sin(tangent) * .28
                + Math.sin(t * .31 + index * 1.4) * .05,
        reveal: smooth(clamp((shot.p * 2.8 - index / count * .36) / .36)),
      });
    }
    mouths.sort((a, b) => a.depth - b.depth);
    for (const mouth of mouths) {
      const size = h * (.055 + mouth.depth * .112)
                 * (1 + d.voiceSustain * .18);
      const color = NOTE_COLORS[(mouth.index * 5) % 12];
      glowDot(g, mouth.point.x, mouth.point.y, size * .11, color,
              mouth.reveal * (.08 + mouth.depth * .11));
      drawTinyOrbitMouth(g, mouth.point.x, mouth.point.y, size,
                         mouth.rotation, t, d, mouth.index * .83,
                         color, mouth.reveal * (.48 + mouth.depth * .52));
    }
  });
  return local;
}

function signalMagnitude(id, t, radius = .045) {
  let total = 0, weight = 0;
  for (let index = -4; index <= 4; index++) {
    const q = index / 4;
    const sampleWeight = 1 - Math.abs(q) * .52;
    total += Math.abs(signalAt(id, t + q * radius)) * sampleWeight;
    weight += sampleWeight;
  }
  return weight ? clamp(total / weight) : 0;
}

let chorusGuitarEventsCache = null;

function chorusGuitarEvents() {
  if (chorusGuitarEventsCache) return chorusGuitarEventsCache;
  chorusGuitarEventsCache = (performanceControls.notes?.['guitar-notes'] || [])
    .filter(event => event.on >= 148
                  && event.on < (currentTurnsScene?.endSec || riverScene.endSec) + .2
                  && event.off - event.on > .035)
    .map((event, index) => ({...event, index}));
  return chorusGuitarEventsCache;
}

function guitarNoteLayout(event) {
  const pitchHeight = clamp((event.pitch - 37) / 38);
  return {
    pitchHeight,
    depth: hash(event.index * 4.39 + event.pitch * .67),
    impact: .22 + hash(event.index * 7.17 + 2) * .56,
  };
}

function chorusGuitarVisibleAt(t) {
  const leadIn = .38, release = 1.25;
  return chorusGuitarEvents().map(event => {
    const start = event.on - leadIn;
    const end = event.off + release;
    return {event, start, end, progress: clamp((t - start) / (end - start)),
            ...guitarNoteLayout(event)};
  }).filter(note => t >= note.start && t <= note.end)
    .sort((a, b) => a.depth - b.depth);
}

function guitarRibPoints(w, h, t, d, shot, note) {
  const points = [];
  const event = note.event;
  const duration = Math.max(.05, event.off - event.on);
  const signed = signalAt('guitar', t);
  const pluck = Math.exp(-Math.abs(t - event.on) * 4.6);
  for (let index = 0; index <= 42; index++) {
    const q = index / 42;
    const envelope = Math.sin(q * Math.PI);
    const carrier = signalAt('guitar', t - (q - note.impact) * .008);
    const vibration = carrier * envelope * h * (.0025 + pluck * .0075)
                    + signed * envelope * h * .0018;
    if (shot.kind === 'river-heaven-drumwall') {
      const lane = lerp(h * .78, h * .13, note.pitchHeight);
      points.push({
        x: lerp(-w * .22, w * 1.22, q),
        y: lane + Math.sin(q * TAU + event.index * .37) * h * (.035 + note.depth * .055)
           - envelope * h * (.055 + Math.min(1.2, duration) * .045) + vibration,
      });
    } else if (shot.kind === 'river-guitar-vault') {
      const apex = h * lerp(.5, .07, note.pitchHeight);
      const depthLift = note.depth * h * .09;
      points.push({
        x: lerp(-w * .28, w * 1.28, q),
        y: lerp(h * (1.04 + note.depth * .12), apex - depthLift, envelope)
           + Math.sin(q * TAU + event.index) * h * .018 + vibration,
      });
    } else {
      const angle = q * TAU * (1.05 + note.depth * .18)
                  + event.index * .31 + t * .025;
      const radius = lerp(w * .045, w * (.58 + note.depth * .18), q);
      points.push({
        x: w * .52 + Math.cos(angle) * radius,
        y: h * .47 + Math.sin(angle) * radius * (.46 + note.pitchHeight * .2)
           + vibration,
      });
    }
  }
  return points;
}

function drawChorusGuitarRibs(g, w, h, t, d, shot, foreground = false) {
  const notes = chorusGuitarVisibleAt(t)
    .filter(note => (note.depth > .56) === foreground);
  for (const note of notes) {
    const points = guitarRibPoints(w, h, t, d, shot, note);
    const path = motionCurve(points);
    const event = note.event;
    const onset = Math.exp(-Math.abs(t - event.on) * 5.4);
    const after = smooth(clamp((t - event.on) / .16));
    const release = 1 - smooth(clamp((t - event.off) / 1.25));
    const reveal = smooth(clamp(note.progress / .13)) * release;
    const color = NOTE_COLORS[event.pitch % 12];
    const width = 1.1 + note.depth * 2.7 + event.velocity * 1.2;
    pathStroke(g, path, color, width * 6.2,
               reveal * (.035 + onset * .08), 18 + note.depth * 24);
    pathStroke(g, path, color, width,
               reveal * (.42 + event.velocity * .35 + onset * .2),
               8 + note.depth * 15);
    const impactIndex = Math.round(note.impact * (points.length - 1));
    const impact = points[impactIndex];
    glowDot(g, impact.x, impact.y,
            2.4 + note.depth * 5.5 + onset * 8,
            color, reveal * (.35 + onset * .62));
    if (onset > .08 && after < .98) {
      for (let echo = 0; echo < 3; echo++) {
        const spread = h * (after * (.035 + echo * .025));
        const echoPath = new Path2D();
        echoPath.moveTo(impact.x - spread * 1.4, impact.y);
        echoPath.bezierCurveTo(impact.x - spread * .4,
                               impact.y - spread * (.35 + echo * .12),
                               impact.x + spread * .4,
                               impact.y + spread * (.35 + echo * .12),
                               impact.x + spread * 1.4, impact.y);
        pathStroke(g, echoPath, color, .55 + echo * .25,
                   onset * (1 - after) * .42, 5 + echo * 3);
      }
    }
  }
}

function fillMembrane(g, path, color, alpha, blur) {
  g.save();
  g.globalCompositeOperation = 'screen';
  g.globalAlpha = alpha;
  g.fillStyle = color;
  g.shadowColor = color;
  g.shadowBlur = blur;
  g.fill(path);
  g.restore();
}

function drawChorusDrumMembranes(g, w, h, t, d, shot) {
  const low = clamp(signalMagnitude('drum-low', t, .07) * 1.35 + d.drums * .24);
  const mid = clamp(signalMagnitude('drum-mid', t, .045) * 1.25 + d.drums * .18);
  const high = clamp(signalMagnitude('drum-high', t, .028) * 1.15 + d.drums * .12);
  const travel = t - 156.883333;

  const floor = new Path2D();
  floor.moveTo(-w * .3, h * 1.18);
  floor.lineTo(-w * .3, h * (.72 - low * .13));
  floor.bezierCurveTo(w * .12, h * (.58 - low * .08),
                       w * .42, h * (.85 + low * .06),
                       w * .73, h * (.65 - low * .11));
  floor.bezierCurveTo(w * 1.02, h * (.54 - low * .05),
                       w * 1.18, h * (.78 + low * .08),
                       w * 1.3, h * (.68 - low * .1));
  floor.lineTo(w * 1.3, h * 1.18);
  floor.closePath();
  fillMembrane(g, floor, '#b32c64', .12 + low * .24, 28 + low * 35);
  pathStroke(g, floor, '#ff678a', 1.3 + low * 5.2,
             .22 + low * .44, 10 + low * 18);

  const canopy = new Path2D();
  canopy.moveTo(-w * .25, -h * .2);
  canopy.lineTo(w * 1.25, -h * .2);
  canopy.lineTo(w * 1.25, h * (.18 + high * .08));
  canopy.bezierCurveTo(w * .84, h * (.31 + mid * .07),
                        w * .53, h * (.05 - high * .04),
                        w * .21, h * (.27 + mid * .08));
  canopy.bezierCurveTo(w * .04, h * (.35 + high * .05),
                        -w * .11, h * (.11 - high * .05),
                        -w * .25, h * (.22 + high * .04));
  canopy.closePath();
  fillMembrane(g, canopy, '#4b3fb8', .1 + high * .2, 24 + high * 28);
  pathStroke(g, canopy, '#a9a0ff', 1 + high * 3.4,
             .18 + high * .37, 8 + high * 14);

  for (let side = -1; side <= 1; side += 2) {
    const fold = new Path2D();
    const edgeX = side < 0 ? -w * .22 : w * 1.22;
    const innerX = w * (.5 + side * (.31 - mid * .11));
    fold.moveTo(edgeX, -h * .15);
    fold.bezierCurveTo(innerX, h * (.12 + mid * .12),
                        innerX - side * w * (.07 + high * .04),
                        h * (.62 - mid * .11), edgeX, h * 1.15);
    fold.lineTo(edgeX + side * w * .35, h * 1.15);
    fold.lineTo(edgeX + side * w * .35, -h * .15);
    fold.closePath();
    fillMembrane(g, fold, side < 0 ? '#176b80' : '#7c245e',
                 .055 + mid * .16, 20 + mid * 24);
    pathStroke(g, fold, side < 0 ? '#69e6dc' : '#ff78a2',
               1 + mid * 3.8, .14 + mid * .35, 8 + mid * 14);
  }

  for (let seam = 0; seam < 11; seam++) {
    const q = seam / 10;
    const x = lerp(-w * .08, w * 1.08, q);
    const bend = Math.sin(travel * (.45 + q * .16) + seam * .78)
               * w * (.025 + mid * .035);
    const path = new Path2D();
    path.moveTo(x, -h * .12);
    path.bezierCurveTo(x + bend, h * .18,
                        x - bend * (1.2 + high * .7), h * .69,
                        x + bend * .55, h * 1.12);
    const color = seam % 3 === 0 ? '#ffd06e'
                : seam % 3 === 1 ? '#72e9db' : '#a9a0ff';
    pathStroke(g, path, color, .55 + high * 1.5,
               .1 + high * .25, 4 + high * 8);
    if (high > .16) {
      const glintQ = ((travel * (.16 + q * .07) + q * 1.7) % 1 + 1) % 1;
      glowDot(g, x + bend * Math.sin(glintQ * Math.PI),
              lerp(-h * .05, h * 1.05, glintQ),
              1 + high * 3.5, color, .16 + high * .36);
    }
  }
  return {low, mid, high};
}

function drawChorusDivaFalls(g, w, h, t, d, shot) {
  const events = noteEventsBetween('diva-notes', t - 2.1, t + .6)
    .filter(event => event.on < riverScene.endSec + .2
                  && event.off > 156.1);
  for (const event of events) {
    const start = event.on - .55, end = event.off + 1.1;
    if (t < start || t > end) continue;
    const p = clamp((t - start) / Math.max(.1, end - start));
    const pitch = clamp((event.pitch - 30) / 45);
    const color = NOTE_COLORS[event.pitch % 12];
    const x = w * lerp(.1, .9, pitch);
    const depth = hash(event.index * 2.71 + event.pitch);
    const points = [];
    for (let index = 0; index <= 26; index++) {
      const q = index / 26;
      const y = lerp(-h * .35, h * 1.35, q + p * .18 - .09);
      points.push({
        x: x + Math.sin(q * TAU * 1.1 - t * .3 + event.index)
             * w * (.035 + depth * .075),
        y,
      });
    }
    const fade = smooth(clamp(p / .12)) * smooth(clamp((1 - p) / .16));
    pathStroke(g, motionCurve(points), color, 4 + depth * 11,
               fade * (.025 + d.masterBody * .045), 20 + depth * 22);
    pathStroke(g, motionCurve(points), color, .7 + depth * 1.8,
               fade * (.2 + event.velocity * .28), 8 + depth * 12);
  }
}

function drawWallChorusSwimmers(g, w, h, t, d, shot) {
  const elapsed = t - 156.883333;
  for (let actor = 0; actor < 4; actor++) {
    const depth = .18 + actor * .21;
    const u = ((actor * .23 + elapsed * (.035 + actor * .004)) % 1 + 1) % 1;
    const pathAt = q => {
      if (shot.kind === 'river-heaven-drumwall') {
        return {x: .08 + q * .84,
                y: .24 + actor * .13 + Math.sin(q * TAU + actor) * .09};
      }
      if (shot.kind === 'river-guitar-vault') {
        return {x: -.08 + q * 1.16,
                y: .7 - Math.sin(q * Math.PI) * (.32 + actor * .045)};
      }
      const angle = q * TAU * 1.2 + actor * .9;
      const radius = .06 + q * .53;
      return {x: .52 + Math.cos(angle) * radius,
              y: .47 + Math.sin(angle) * radius * .52};
    };
    drawPathSwimmer(g, w, h, t, d, pathAt, u, {
      size: w * (.045 + depth * .05), phase: actor * 1.3,
      speed: .78 + actor * .08, alpha: .16 + depth * .35,
      crossScale: .72 + depth * .25,
      ripples: actor === 3,
    });
  }
}

function wallChorusCamera(shot, w, h) {
  const p = clamp(shot.p);
  if (shot.kind === 'river-heaven-drumwall') {
    return mixCamera({x: w * .03, y: -h * .03, zoom: .9, roll: -.04, pitch: .93},
                     {x: -w * .08, y: h * .045, zoom: 1.16, roll: .09, pitch: .9}, p);
  }
  if (shot.kind === 'river-guitar-vault') {
    return mixCamera({x: w * .14, y: h * .08, zoom: .88, roll: -.5, pitch: .79},
                     {x: -w * .06, y: -h * .04, zoom: 1.13, roll: -.16, pitch: .9}, p);
  }
  return mixCamera({x: w * .04, y: h * .02, zoom: 1.02, roll: .03, pitch: .94},
                   {x: -w * .18, y: -h * .11, zoom: 2.08, roll: .72, pitch: .86}, p);
}

function drawRiverWallChorus(g, w, h, t, d, shot) {
  const local = clamp((t - riverScene.startSec)
                    / Math.max(.001, riverScene.endSec - riverScene.startSec));
  const gradient = g.createRadialGradient(w * .51, h * .45, 1,
                                          w * .51, h * .45, w * .82);
  gradient.addColorStop(0, shot.kind === 'river-guitar-vault' ? '#25103b' : '#151b42');
  gradient.addColorStop(.5, '#07162d');
  gradient.addColorStop(1, '#02030c');
  g.fillStyle = gradient;
  g.fillRect(0, 0, w, h);

  if (shot.kind === 'river-heaven-drumwall') {
    const inherited = 1 - smooth(clamp(shot.p / .24));
    if (inherited > .001) {
      drawRiverSpirographField(g, w, h, t, d, 1, 1.2, inherited * .72);
      for (let mouth = 0; mouth < 6; mouth++) {
        const point = riverSpiroPoint(w, h, mouth / 6 + t * .012,
                                      2 + mouth * 2, t, 1.2);
        drawTinyOrbitMouth(g, point.x, point.y, h * .06,
                           (mouth - 2.5) * .08, t, d, mouth,
                           NOTE_COLORS[(mouth * 5) % 12], inherited * .52);
      }
    }
  }

  withCamera(g, w, h, wallChorusCamera(shot, w, h), () => {
    drawChorusDivaFalls(g, w, h, t, d, shot);
    drawChorusGuitarRibs(g, w, h, t, d, shot, false);
    const drum = drawChorusDrumMembranes(g, w, h, t, d, shot);
    drawWallChorusSwimmers(g, w, h, t, d, shot);
    drawChorusGuitarRibs(g, w, h, t, d, shot, true);

    if (shot.kind === 'river-chorus-plunge') {
      const billing = .78 + d.voiceFeature * .38 + d.voiceSustain * .22;
      drawMarsFaceActor(g, w * .52, h * .48, h * billing,
                        '#ffe0a0', t, d, 6.2, .88, -.04, true);
      const aperture = new Path2D();
      aperture.ellipse(w * .52, h * .47,
                       w * (.08 + shot.p * .17 + drum.low * .03),
                       h * (.11 + shot.p * .15 + drum.mid * .025),
                       t * .035, 0, TAU);
      pathStroke(g, aperture, '#7ff0db', 1.2 + drum.high * 2.4,
                 .28 + d.masterBody * .24, 11 + drum.high * 12);
    }
  });
  return local;
}

function currentRoutePoint(w, h, q, lane, t, d) {
  const travel = t - currentTurnsScene.startSec;
  const broad = Math.sin(q * TAU * 1.05 - travel * .27 + lane * 4.1)
              * h * (.075 + d.bassBody * .027);
  const follow = Math.sin(q * TAU * .48 + travel * .11 + lane * 2.3)
               * h * .038;
  return {
    x: lerp(-w * .24, w * 1.24, q),
    y: h * (.72 - q * .43 + lane) + broad + follow,
  };
}

function currentTurnPoint(w, h, q, lane, t, d, morph) {
  const angle = q * TAU * 1.12 + t * .025 + lane * 5.2;
  const radius = lerp(w * .04, w * .66, q);
  const tunnel = {
    x: w * .52 + Math.cos(angle) * radius,
    y: h * .47 + Math.sin(angle) * radius * .52,
  };
  const route = currentRoutePoint(w, h, q, lane, t, d);
  const hook = Math.sin(q * Math.PI) * w * .12;
  route.x += hook * Math.cos(q * Math.PI * 1.35);
  route.y -= hook * .42 * Math.sin(q * Math.PI * 1.25);
  const localMorph = smooth(clamp((morph - Math.abs(q - .52) * .16) / .84));
  return {x: lerp(tunnel.x, route.x, localMorph),
          y: lerp(tunnel.y, route.y, localMorph)};
}

function drawCurrentField(g, w, h, t, d, shot, alpha = 1) {
  const turnMorph = shot.kind === 'current-switchyard-turn' ? smooth(shot.p) : 1;
  const subtract = shot.kind === 'current-answer-contact'
    ? smooth(clamp((shot.p - .46) / .54)) : 0;
  const paths = [];
  for (let lane = 0; lane < 9; lane++) {
    const laneOffset = lerp(-.14, .14, lane / 8);
    const points = [];
    for (let index = 0; index <= 54; index++) {
      const q = index / 54;
      points.push(shot.kind === 'current-switchyard-turn'
        ? currentTurnPoint(w, h, q, laneOffset, t, d, turnMorph)
        : currentRoutePoint(w, h, q, laneOffset, t, d));
    }
    paths.push(motionCurve(points));
  }
  g.save();
  g.globalCompositeOperation = 'screen';
  g.lineCap = 'round';
  g.lineJoin = 'round';
  for (let lane = 8; lane >= 0; lane -= 2) {
    const color = RIVER_SPIRO_COLORS[lane % RIVER_SPIRO_COLORS.length];
    g.strokeStyle = color;
    g.globalAlpha = alpha * (1 - subtract * .86) * (.025 + d.masterBody * .035);
    g.lineWidth = h * (.055 + lane / 8 * .032 + d.bassBody * .025);
    g.filter = `blur(${12 + lane}px)`;
    g.stroke(paths[lane]);
  }
  g.restore();
  for (let lane = 0; lane < paths.length; lane++) {
    const depth = lane / 8;
    const color = RIVER_SPIRO_COLORS[lane % RIVER_SPIRO_COLORS.length];
    pathStroke(g, paths[lane], color,
               .7 + depth * 1.75 + d.bassBody * .5,
               alpha * (1 - subtract * .82) * (.14 + depth * .2),
               6 + depth * 10);
  }
}

function guitarSwitchBranch(w, h, event, t) {
  const layout = guitarNoteLayout(event);
  const pivot = {x: w * .62, y: h * .42};
  const side = (event.pitch + event.index) % 2 ? 1 : -1;
  const endpoint = {
    x: w * (.62 + side * (.38 + layout.depth * .18)),
    y: h * lerp(.82, .08, layout.pitchHeight),
  };
  const path = new Path2D();
  path.moveTo(pivot.x, pivot.y);
  path.bezierCurveTo(pivot.x + side * w * (.08 + layout.depth * .09),
                      pivot.y - h * (.19 - layout.pitchHeight * .11),
                      endpoint.x - side * w * (.12 + layout.depth * .05),
                      endpoint.y + h * Math.sin(event.index * 1.7) * .08,
                      endpoint.x, endpoint.y);
  return {path, pivot, endpoint, ...layout};
}

function drawGuitarSwitchyard(g, w, h, t, d, shot, memory = 1) {
  const visible = chorusGuitarEvents().filter(event => {
    const end = event.off + 1.7;
    return t >= event.on - .25 && t <= end && event.on < 170.35;
  });
  for (const event of visible) {
    const branch = guitarSwitchBranch(w, h, event, t);
    const onset = Math.exp(-Math.abs(t - event.on) * 5.6);
    const reveal = smooth(clamp((t - event.on + .25) / .3));
    const release = 1 - smooth(clamp((t - event.off) / 1.7));
    const alpha = memory * reveal * release;
    const color = NOTE_COLORS[event.pitch % 12];
    const width = 1 + branch.depth * 2.1 + event.velocity;
    pathStroke(g, branch.path, color, width * 5.8,
               alpha * (.025 + onset * .08), 18 + branch.depth * 20);
    pathStroke(g, branch.path, color, width,
               alpha * (.34 + event.velocity * .35 + onset * .24),
               7 + branch.depth * 13);
    glowDot(g, branch.pivot.x, branch.pivot.y,
            2.5 + onset * 8 + branch.depth * 3.5,
            color, alpha * (.3 + onset * .62));
  }
}

function drawCurrentRudders(g, w, h, t, d, shot, alpha = 1) {
  const energies = [
    clamp(signalMagnitude('drum-low', t, .07) * 1.35 + d.drums * .2),
    clamp(signalMagnitude('drum-mid', t, .045) * 1.25 + d.drums * .16),
    clamp(signalMagnitude('drum-high', t, .028) * 1.16 + d.drums * .12),
  ];
  const colors = ['#ff6688', '#6ce6d7', '#a9a0ff'];
  const pivotX = w * .62, pivotY = h * .42;
  for (let rudder = 0; rudder < 3; rudder++) {
    const energy = energies[rudder];
    const angle = -.95 + rudder * .92 + energy * (rudder - 1) * .26;
    const length = Math.min(w, h) * (.42 + rudder * .1 + energy * .13);
    const normalX = -Math.sin(angle), normalY = Math.cos(angle);
    const tipX = pivotX + Math.cos(angle) * length;
    const tipY = pivotY + Math.sin(angle) * length;
    const spread = length * (.18 + energy * .12);
    const sail = new Path2D();
    sail.moveTo(pivotX, pivotY);
    sail.bezierCurveTo(pivotX + normalX * spread,
                        pivotY + normalY * spread,
                        tipX + normalX * spread * .55,
                        tipY + normalY * spread * .55,
                        tipX, tipY);
    sail.bezierCurveTo(tipX - normalX * spread * (.7 + energy * .25),
                        tipY - normalY * spread * (.7 + energy * .25),
                        pivotX - normalX * spread * .42,
                        pivotY - normalY * spread * .42,
                        pivotX, pivotY);
    sail.closePath();
    fillMembrane(g, sail, colors[rudder],
                 alpha * (.035 + energy * .11), 18 + energy * 24);
    pathStroke(g, sail, colors[rudder], .8 + energy * 3.1,
               alpha * (.16 + energy * .3), 7 + energy * 12);
  }
  return energies;
}

let currentDivaEventsCache = null;

function currentDivaEvents() {
  if (currentDivaEventsCache) return currentDivaEventsCache;
  currentDivaEventsCache = (performanceControls.notes?.['diva-notes'] || [])
    .filter(event => event.on >= 166.8 && event.on < currentTurnsScene.endSec + .7)
    .map((event, index) => ({...event, index}));
  return currentDivaEventsCache;
}

function drawCurrentDivaSignals(g, w, h, t, d, shot, alpha = 1) {
  const events = currentDivaEvents().filter(event =>
    t >= event.on - .55 && t <= event.off + 1.05);
  for (const event of events) {
    const start = event.on - .55, end = event.off + 1.05;
    const progress = clamp((t - start) / Math.max(.08, end - start));
    const pitch = clamp((event.pitch - 35) / 40);
    const lane = lerp(.13, -.13, pitch);
    const depth = hash(event.index * 3.31 + event.pitch * .7);
    const headQ = lerp(.04, .96, smooth(progress));
    const duration = Math.max(.1, event.off - event.on);
    const length = .08 + Math.min(2.2, duration) * .07;
    const points = [];
    for (let index = 0; index <= 24; index++) {
      const q = headQ - length * (1 - index / 24);
      points.push(shot.kind === 'current-switchyard-turn'
        ? currentTurnPoint(w, h, q, lane, t, d, smooth(shot.p))
        : currentRoutePoint(w, h, q, lane, t, d));
    }
    const edgeFade = smooth(clamp(progress / .12))
                   * smooth(clamp((1 - progress) / .15));
    const onset = Math.exp(-Math.abs(t - event.on) * 4.8);
    const color = NOTE_COLORS[event.pitch % 12];
    pathStroke(g, motionCurve(points), color, 4 + depth * 10,
               alpha * edgeFade * (.025 + depth * .035), 18 + depth * 20);
    pathStroke(g, motionCurve(points), color, .8 + depth * 2,
               alpha * edgeFade * (.34 + event.velocity * .3),
               7 + depth * 12);
    const head = points.at(-1);
    glowDot(g, head.x, head.y, 1.8 + depth * 4 + onset * 2.8,
            color, alpha * edgeFade * (.3 + onset * .5));
  }
}

function currentSwimmerPath(w, h, q, lane, t, d, shot, actor) {
  if (shot.kind === 'current-switchyard-turn') {
    return currentTurnPoint(w, h, q, lane, t, d, smooth(shot.p));
  }
  const leader = currentRoutePoint(w, h, q, lane * .28, t, d);
  if (shot.kind === 'current-following-wake') {
    const join = smooth(clamp((shot.p - actor * .15 + .08) / .42));
    const separate = currentRoutePoint(w, h, q, lane + (actor - 1.5) * .08, t, d);
    return {x: lerp(separate.x, leader.x, join),
            y: lerp(separate.y, leader.y, join)};
  }
  return leader;
}

function drawCurrentSwimmers(g, w, h, t, d, shot, alpha = 1) {
  const elapsed = t - riverScene.startSec;
  for (let actor = 0; actor < 4; actor++) {
    const depth = .18 + actor * .21;
    const u = ((actor * .23 + elapsed * (.034 + actor * .004)) % 1 + 1) % 1;
    const lane = lerp(-.1, .1, actor / 3);
    const pathAt = q => {
      const point = currentSwimmerPath(w, h, q, lane, t, d, shot, actor);
      return {x: point.x / w, y: point.y / h};
    };
    drawPathSwimmer(g, w, h, t, d, pathAt, u, {
      size: w * (.046 + depth * .052), phase: actor * 1.31,
      speed: .78 + actor * .08,
      alpha: alpha * (.14 + depth * .42),
      crossScale: .7 + depth * .28,
      ripples: actor === 3,
    });
  }
}

function currentCamera(shot, w, h) {
  if (shot.kind === 'current-switchyard-turn') {
    return mixCameraLinear(
      {x: -w * .18, y: -h * .11, zoom: 2.08, roll: .72, pitch: .86},
      {x: w * .06, y: 0, zoom: .95, roll: -.32, pitch: .9}, shot.p);
  }
  if (shot.kind === 'current-following-wake') {
    return mixCameraLinear(
      {x: w * .06, y: 0, zoom: .95, roll: -.32, pitch: .9},
      {x: -w * .1, y: -h * .04, zoom: 1.08, roll: -.08, pitch: .94}, shot.p);
  }
  return mixCamera(
    {x: w * .12, y: h * .04, zoom: 1.14, roll: .08, pitch: .92},
    {x: 0, y: 0, zoom: .82, roll: -.02, pitch: .96}, shot.p);
}

function drawCurrentNarrator(g, w, h, t, d, shot) {
  let x, y, size, alpha, cant;
  if (shot.kind === 'current-switchyard-turn') {
    const migrate = smooth(clamp(shot.p / .42));
    x = lerp(w * .52, w * .06, migrate);
    y = lerp(h * .48, h * .76, migrate);
    size = h * lerp(.82, .43, migrate);
    alpha = .9;
    cant = lerp(-.04, -.15, migrate);
  } else if (shot.kind === 'current-following-wake') {
    const cross = smooth(shot.p);
    x = lerp(w * .07, w * .95, cross);
    y = lerp(h * .76, h * .7, cross);
    size = h * lerp(.42, .32, cross);
    alpha = .72;
    cant = lerp(-.14, .1, cross);
  } else {
    x = w * lerp(.95, .89, smooth(shot.p));
    y = h * lerp(.7, .77, smooth(shot.p));
    size = h * lerp(.32, .27, smooth(shot.p));
    alpha = lerp(.66, .35, smooth(clamp((shot.p - .62) / .38)));
    cant = .1;
  }
  drawMarsFaceActor(g, x, y, size, '#ffe0a0', t, d, 6.7,
                    alpha, cant, true);
}

function drawAnswerSpeakers(g, w, h, t, d, shot) {
  const revealA = smooth(clamp((shot.p - .08) / .28));
  const revealB = smooth(clamp((shot.p - .2) / .3));
  const lowLight = 1 - smooth(clamp((shot.p - .68) / .32)) * .42;
  const answerDrivers = {...d,
    echoBody: Math.max(d.echoBody, d.voiceFeature * .62, d.drumBody * .24),
    voiceSustain: Math.max(d.voiceSustain, d.masterBody * .22),
  };
  drawMarsFaceActor(g, w * .28, h * .31, h * .29,
                    '#79ead7', t, answerDrivers, 2.2,
                    revealA * lowLight * .78, -.08, false);
  drawMarsFaceActor(g, w * .71, h * .23, h * .23,
                    '#ffaf82', t + .075, answerDrivers, 4.8,
                    revealB * lowLight * .68, .09, false);
}

function drawAnswerCurves(g, w, h, t, d, shot) {
  const origins = [
    {x: w * .28, y: h * .34, color: '#79ead7', delay: .25, bend: -1},
    {x: w * .71, y: h * .27, color: '#ffaf82', delay: .38, bend: 1},
  ];
  for (const origin of origins) {
    const reveal = smooth(clamp((shot.p - origin.delay) / .36));
    if (reveal <= 0) continue;
    const endX = lerp(origin.x, -w * .15, reveal);
    const endY = lerp(origin.y, h * (.66 + origin.bend * .08), reveal);
    const curve = new Path2D();
    curve.moveTo(origin.x, origin.y);
    curve.bezierCurveTo(origin.x + origin.bend * w * .16,
                         origin.y + h * .12,
                         w * (.42 - origin.bend * .14), h * .55,
                         endX, endY);
    pathStroke(g, curve, origin.color, 1.1 + d.masterBody * 1.4,
               reveal * (.34 + d.drumBody * .18), 9 + d.drums * 12);
    glowDot(g, endX, endY, 2 + d.drums * 4.5,
            origin.color, reveal * (.35 + d.drums * .35));
  }
}

function drawCurrentTurnsScene(g, w, h, t, d, shot) {
  const local = clamp((t - currentTurnsScene.startSec)
                    / Math.max(.001, currentTurnsScene.endSec - currentTurnsScene.startSec));
  const subtraction = shot.kind === 'current-answer-contact'
    ? smooth(clamp((shot.p - .46) / .54)) : 0;
  const gradient = g.createRadialGradient(w * .48, h * .43, 1,
                                          w * .48, h * .43, w * .86);
  gradient.addColorStop(0, subtraction > .5 ? '#0a1022' : '#1d153e');
  gradient.addColorStop(.5, '#071329');
  gradient.addColorStop(1, '#01030a');
  g.fillStyle = gradient;
  g.fillRect(0, 0, w, h);

  withCamera(g, w, h, currentCamera(shot, w, h), () => {
    drawCurrentDivaSignals(g, w, h, t, d, shot, 1 - subtraction * .7);
    drawCurrentField(g, w, h, t, d, shot, 1);
    if (shot.kind === 'current-switchyard-turn') {
      drawGuitarSwitchyard(g, w, h, t, d, shot, 1);
      drawCurrentRudders(g, w, h, t, d, shot, 1);
    } else if (shot.kind === 'current-following-wake') {
      drawGuitarSwitchyard(g, w, h, t, d, shot, .42 * (1 - shot.p));
    }
    drawCurrentSwimmers(g, w, h, t, d, shot, 1 - subtraction * .9);
  });

  if (shot.kind === 'current-answer-contact') {
    g.save();
    g.globalCompositeOperation = 'source-over';
    g.globalAlpha = subtraction * (.36 + d.drums * .12);
    g.fillStyle = '#01030a';
    g.fillRect(0, 0, w, h);
    g.restore();
    drawAnswerCurves(g, w, h, t, d, shot);
    drawAnswerSpeakers(g, w, h, t, d, shot);
  }
  drawCurrentNarrator(g, w, h, t, d, shot);
  return local;
}

function outroDrumBands(t, d) {
  return {
    low: clamp(signalMagnitude('drum-low', t, .07) * 1.35 + d.drums * .18),
    mid: clamp(signalMagnitude('drum-mid', t, .045) * 1.28 + d.drums * .14),
    high: clamp(signalMagnitude('drum-high', t, .028) * 1.18 + d.drums * .1),
  };
}

function outroPerspective(t, shot) {
  if (shot.kind === 'outro-left-call') return 'left';
  if (shot.kind === 'outro-right-response') return 'right';
  const lyric = activeLyric(t);
  if (!lyric) return t < 191.8 ? 'right' : 'left';
  if (lyric.id === 'lyrics-mtejg0j5') return 'right';
  if (lyric.id === 'lyrics-mtejafmv') return 'both';
  return lyric.speaker === 'Them 2' ? 'right' : 'left';
}

function outroPhraseProgress(t, shot) {
  const lyric = activeLyric(t);
  if (!lyric) return shot.p;
  return clamp((t - lyric.startSec) / Math.max(.08, lyric.endSec - lyric.startSec));
}

function outroCamera(shot, w, h, t, side) {
  const q = ['outro-crosscut-reprise', 'outro-goodnight-cascade'].includes(shot.kind)
    ? outroPhraseProgress(t, shot) : shot.p;
  if (shot.kind === 'outro-time-tunnel') {
    return mixCameraLinear(
      {x: w * .035, y: h * .025, zoom: 1.02, roll: -.055, pitch: .94},
      {x: -w * .085, y: -h * .055, zoom: 1.26, roll: .16, pitch: .89}, q);
  }
  if (side === 'right') {
    return mixCameraLinear(
      {x: -w * .045, y: h * .03, zoom: .96, roll: -.075, pitch: .94},
      {x: w * .055, y: -h * .035, zoom: 1.11, roll: -.015, pitch: .9}, q);
  }
  return mixCameraLinear(
    {x: w * .055, y: h * .02, zoom: .98, roll: .065, pitch: .94},
    {x: -w * .035, y: -h * .055, zoom: 1.17, roll: .125, pitch: .9}, q);
}

function fillOutroBackground(g, w, h, t, d, side) {
  const left = side !== 'right';
  const cx = left ? w * .25 : w * .76;
  const cy = left ? h * .55 : h * .42;
  const gradient = g.createRadialGradient(cx, cy, 2, cx, cy, w * .92);
  gradient.addColorStop(0, left ? '#162a42' : '#3a1536');
  gradient.addColorStop(.46, left ? '#07162a' : '#160d27');
  gradient.addColorStop(1, '#01030a');
  g.fillStyle = gradient;
  g.fillRect(0, 0, w, h);

  const pulse = .018 + d.masterBody * .035;
  g.save();
  g.globalCompositeOperation = 'screen';
  g.globalAlpha = pulse;
  g.fillStyle = left ? '#54d9cf' : '#ff6f91';
  const veil = new Path2D();
  veil.moveTo(-w * .2, h * (left ? .9 : .18));
  veil.bezierCurveTo(w * .28, h * (left ? .54 : .42),
                     w * .67, h * (left ? .65 : .29),
                     w * 1.2, h * (left ? .16 : .82));
  veil.lineTo(w * 1.2, left ? -h * .2 : h * 1.2);
  veil.lineTo(-w * .2, left ? -h * .2 : h * 1.2);
  veil.closePath();
  g.fill(veil);
  g.restore();
}

function drawOutroBassHorizon(g, w, h, t, d, side, alpha = 1) {
  const direction = side === 'right' ? -1 : 1;
  const phase = (t - lowLightOutroScene.startSec) * .24 * direction;
  const path = new Path2D();
  path.moveTo(-w * .18, h * (.59 + Math.sin(phase) * .025));
  path.bezierCurveTo(w * .21, h * (.39 + Math.sin(phase + 1.2) * .08),
                     w * .61, h * (.73 + Math.sin(phase + 2.4) * .07),
                     w * 1.18, h * (.45 + Math.sin(phase + 3.2) * .04));
  const color = side === 'right' ? '#ff9b7d' : '#69e6dc';
  pathStroke(g, path, color, 1.2 + d.bassBody * 3.2,
             alpha * (.25 + d.bassBody * .28), 10 + d.bassBody * 15);
  const echo = new Path2D();
  echo.moveTo(-w * .18, h * .66);
  echo.bezierCurveTo(w * .27, h * (.47 + Math.cos(phase) * .07),
                     w * .67, h * (.78 + Math.sin(phase) * .05),
                     w * 1.18, h * .53);
  pathStroke(g, echo, side === 'right' ? '#b08cff' : '#ffe08d',
             .55 + d.bassBody, alpha * (.08 + d.bassBody * .11), 6);
}

function drawOutroPerspectiveWorld(g, w, h, t, d, side, alpha = 1) {
  const bands = outroDrumBands(t, d);
  drawOutroBassHorizon(g, w, h, t, d, side, alpha);
  if (side === 'left') {
    for (let lane = 0; lane < 8; lane++) {
      const points = [];
      for (let index = 0; index <= 40; index++) {
        const q = index / 40;
        const drift = (t - lowLightOutroScene.startSec) * (.018 + lane * .0007);
        points.push({
          x: lerp(-w * .2, w * 1.2, q),
          y: h * (.78 - q * .47 + (lane - 3.5) * .025)
             + Math.sin(q * TAU * 1.04 - drift * TAU + lane * .62)
               * h * (.045 + d.bassBody * .035),
        });
      }
      const color = ['#65e3d7', '#69bde8', '#a994ff', '#ffe08a'][lane % 4];
      pathStroke(g, motionCurve(points), color,
                 .6 + lane * .13 + d.bassBody * .9,
                 alpha * (.1 + lane * .012 + d.masterBody * .08),
                 5 + lane);
    }
  } else {
    const cx = w * .36, cy = h * .55;
    for (let band = 0; band < 9; band++) {
      const q = band / 8;
      const rx = w * (.18 + q * .65 + bands.low * .025);
      const ry = h * (.07 + q * .34 + bands.mid * .022);
      const path = new Path2D();
      path.ellipse(cx + Math.sin(t * .11 + band) * w * .018,
                   cy + Math.cos(t * .09 + band) * h * .016,
                   rx, ry, -.32 + t * .014 + q * .16, 0, TAU);
      const color = ['#ff7b8f', '#ffad79', '#b28cff', '#73e2d6'][band % 4];
      pathStroke(g, path, color, .7 + bands.mid * 2 + q,
                 alpha * (.08 + q * .075 + bands.high * .14),
                 6 + q * 10);
    }
  }
}

let outroDivaEventsCache = null;

function outroDivaEvents() {
  if (outroDivaEventsCache) return outroDivaEventsCache;
  const end = signoffOutroScene?.endSec || 199.25;
  outroDivaEventsCache = (performanceControls.notes?.['diva-notes'] || [])
    .filter(event => event.on >= 173.2 && event.on < end + 1)
    .map((event, index) => ({...event, index}));
  return outroDivaEventsCache;
}

function drawOutroDivaPackets(g, w, h, t, d, tunnel, side, alpha = 1) {
  const events = outroDivaEvents().filter(event =>
    t >= event.on - .5 && t <= event.off + 1.15);
  for (const event of events) {
    const start = event.on - .5, end = event.off + 1.15;
    const p = clamp((t - start) / Math.max(.12, end - start));
    const pitch = clamp((event.pitch - 30) / 48);
    const depth = hash(event.index * 3.83 + event.pitch * .37);
    const color = NOTE_COLORS[event.pitch % 12];
    const points = [];
    const length = .06 + Math.min(2.6, event.off - event.on) * .055;
    for (let index = 0; index <= 18; index++) {
      const u = clamp(p - length * (1 - index / 18));
      if (tunnel) {
        const angle = pitch * TAU + u * 2.2 + t * .035;
        const radius = lerp(w * .035, w * .78, smooth(u));
        const vx = side === 'right' ? w * .31 : w * .66;
        const vy = side === 'right' ? h * .6 : h * .39;
        points.push({x: vx + Math.cos(angle) * radius,
                     y: vy + Math.sin(angle) * radius * .54});
      } else {
        const q = u;
        points.push({
          x: lerp(-w * .08, w * 1.08, q),
          y: h * lerp(.78, .2, pitch)
             + Math.sin(q * TAU + event.index) * h * (.035 + depth * .035),
        });
      }
    }
    const edge = smooth(clamp(p / .13)) * smooth(clamp((1 - p) / .14));
    const onset = Math.exp(-Math.abs(t - event.on) * 5.2);
    const path = motionCurve(points);
    pathStroke(g, path, color, 3 + depth * 7,
               alpha * edge * (.025 + depth * .03), 15 + depth * 16);
    pathStroke(g, path, color, .65 + depth * 1.6,
               alpha * edge * (.28 + event.velocity * .34), 6 + depth * 8);
    const head = points.at(-1);
    glowDot(g, head.x, head.y, 1.5 + depth * 3.5 + onset * 3,
            color, alpha * edge * (.28 + onset * .55));
  }
}

function drawOutroTimeTunnel(g, w, h, t, d, shot, side = 'left', alpha = 1) {
  const bands = outroDrumBands(t, d);
  const travel = t - lowLightOutroScene.startSec;
  const fullReprise = shot.start >= 185.8;
  const vx = w * (.56 + Math.sin(travel * .19) * .13);
  const vy = h * (.42 + Math.cos(travel * .16) * .1);
  const palette = side === 'right'
    ? ['#ff6f91', '#ffab73', '#b08cff', '#65e2d7']
    : ['#67e5d7', '#6cb9ef', '#b394ff', '#ffd879'];

  for (let ring = 0; ring < 18; ring++) {
    const cycle = ((ring / 18 + travel * (.11 + d.bassBody * .025)) % 1 + 1) % 1;
    const q = smooth(cycle);
    const rx = w * (.025 + q * q * (1.02 + bands.low * .09));
    const ry = h * (.018 + q * q * (.67 + bands.mid * .07));
    const cx = lerp(vx, w * (.5 + Math.sin(travel * .12) * .1), q)
             + Math.sin(ring * 1.31 + travel * .38) * w * bands.mid * .016;
    const cy = lerp(vy, h * .53, q)
             + Math.cos(ring * 1.07 + travel * .31) * h * bands.mid * .018;
    const path = new Path2D();
    path.ellipse(cx, cy, rx, ry,
                 -.18 + Math.sin(travel * .08) * .16 + q * .12,
                 0, TAU);
    const color = palette[ring % palette.length];
    if (ring % 3 === 0) {
      fillMembrane(g, path, color,
                   alpha * (.012 + bands.low * .022 + (fullReprise ? .012 : 0)),
                   16 + bands.low * 20);
    }
    pathStroke(g, path, color,
               .65 + q * 1.75 + bands.low * 2.7,
               alpha * (.11 + q * .16 + bands.mid * .16),
               6 + q * 11 + bands.high * 9);
    if (bands.high > .12 && ring % 2 === 0) {
      const a = travel * (1.5 + bands.high) + ring * .8;
      glowDot(g, cx + Math.cos(a) * rx, cy + Math.sin(a) * ry,
              1.2 + bands.high * 4.8, color,
              alpha * (.18 + bands.high * .48));
    }
  }

  for (let seam = 0; seam < 14; seam++) {
    const angle = seam / 14 * TAU + travel * .026;
    const ex = vx + Math.cos(angle) * w * 1.15;
    const ey = vy + Math.sin(angle) * h * .9;
    const bend = Math.sin(seam * 1.73 + travel * .42) * w * (.035 + bands.mid * .035);
    const path = new Path2D();
    path.moveTo(vx, vy);
    path.bezierCurveTo(vx + Math.cos(angle + .7) * w * .12 + bend,
                       vy + Math.sin(angle + .7) * h * .1,
                       ex - Math.cos(angle) * w * .34 - bend,
                       ey - Math.sin(angle) * h * .28,
                       ex, ey);
    pathStroke(g, path, palette[seam % palette.length],
               .45 + bands.high * 1.5,
               alpha * (.07 + bands.high * .19), 5 + bands.high * 8);
  }
  drawOutroDivaPackets(g, w, h, t, d, true, side, alpha);
  drawOutroBassHorizon(g, w, h, t, d, side, alpha * .72);
}

function drawOutroFace(g, w, h, t, d, side, shot, alpha = 1) {
  const phrase = outroPhraseProgress(t, shot);
  const cascade = shot.kind === 'outro-goodnight-cascade';
  const lyric = activeLyric(t);
  let scaleStep = 0;
  if (cascade && lyric) {
    if (lyric.id === 'lyr-082') scaleStep = 1;
    else if (lyric.id === 'lyr-083') scaleStep = 2;
  }
  const right = side === 'right';
  const x = right ? w * (.84 + scaleStep * .018) : w * (.15 - scaleStep * .012);
  const y = right ? h * .43 : h * .56;
  const size = h * (.61 + scaleStep * .19 + (shot.kind === 'outro-left-call' ? .08 : 0));
  const color = right ? '#79ead7' : '#ffe09b';
  drawMarsFaceActor(g, x, y, size, color, t, d,
                    right ? 4.6 : 6.4, alpha, right ? .08 : -.09, true);

  const echo = clamp(d.echoBody * .7 + d.voiceSustain * .16);
  if (echo > .05) {
    for (let trace = 0; trace < 2; trace++) {
      const delay = (trace + 1) * (.025 + echo * .018);
      const path = new Path2D();
      const sx = x + (right ? -1 : 1) * size * (.12 + trace * .055);
      const sy = y + size * (.055 + trace * .025);
      path.moveTo(sx - size * .055, sy);
      path.bezierCurveTo(sx - size * .018, sy - size * (.018 + phrase * .008),
                         sx + size * .022, sy + size * (.02 + delay),
                         sx + size * .065, sy - size * .004);
      pathStroke(g, path, right ? '#ffad83' : '#79e4dc',
                 .55 + echo * .8, alpha * echo * (.14 - trace * .035), 6);
    }
  }
}

function drawTunnelPhoneticTraces(g, w, h, t, d, shot) {
  const lyric = activeLyric(t);
  if (!lyric || d.voiceSustain < .02) return;
  const side = outroPerspective(t, shot);
  const right = side === 'right';
  const x = right ? w * .76 : w * .24;
  const y = h * (.42 + Math.sin(t * .7) * .07);
  const width = w * (.045 + d.voiceFeature * .055);
  const open = h * (.012 + d.voiceFeature * .048);
  const path = new Path2D();
  path.moveTo(x - width, y);
  path.bezierCurveTo(x - width * .32, y - open,
                     x + width * .25, y - open * .8,
                     x + width, y);
  path.bezierCurveTo(x + width * .32, y + open,
                     x - width * .26, y + open * 1.15,
                     x - width, y);
  pathStroke(g, path, right ? '#79ead7' : '#ffe09b',
             1 + d.voiceFeature * 2.4,
             .28 + d.voiceSustain * .46, 11 + d.voiceFeature * 15);
}

function drawOutroFinalIris(g, w, h, t, d, shot) {
  const finalStart = lyrics.find(item => item.id === 'lyrics-mtejafmv')?.startSec || 197.583;
  const finalEnd = lyrics.find(item => item.id === 'lyrics-mtejafmv')?.endSec || 198.15;
  const mixEnd = signoffOutroScene?.endSec || 199.25;
  const gather = smooth(clamp((t - finalStart + .12) / .68));
  const collapse = smooth(clamp((t - finalEnd) / Math.max(.1, mixEnd - finalEnd)));
  const breath = smooth(clamp((t - shot.start) / Math.max(.1, finalStart - shot.start)));
  fillOutroBackground(g, w, h, t, d, breath < .72 ? 'right' : 'left');

  const camera = mixCameraLinear(
    {x: 0, y: 0, zoom: 1.05, roll: .05, pitch: .94},
    {x: -w * .03, y: -h * .02,
     zoom: lerp(.76, 1.08, gather), roll: lerp(-.14, .19, gather), pitch: .92},
    smooth(clamp(shot.p * 1.08)));

  withCamera(g, w, h, camera, () => {
    const radiusScale = lerp(1, .055, collapse);
    const motifAlpha = lerp(.95, .25, collapse);
    for (let ring = 0; ring < 15; ring++) {
      const base = Math.min(w, h) * (.18 + ring * .045) * radiusScale;
      const drift = (1 - gather) * Math.sin(ring * 2.1 + t * .16) * w * .11;
      const rotation = t * (.024 + ring * .0009) + ring * .19;
      const color = ['#ffe09b', '#73e4d8', '#ff7f91', '#aa92ff', '#ffb16f'][ring % 5];
      const path = new Path2D();
      path.ellipse(w * .5 + drift, h * .5,
                   base * (1 + gather * .11 * Math.sin(ring * 1.37)),
                   base * (.48 + ring * .006 + gather * .07),
                   rotation, 0, TAU);
      if (ring % 3 === 1) {
        path.ellipse(w * .5 - drift * .42, h * .5,
                     base * .74, base * (.31 + gather * .05),
                     -rotation * .73, 0, TAU);
      }
      if (ring % 4 === 0) {
        fillMembrane(g, path, color,
                     motifAlpha * (.012 + gather * .014), 16 + gather * 14);
      }
      pathStroke(g, path, color,
                 1.05 + ring * .085 + d.bassBody * 1.8,
                 motifAlpha * (.24 + (ring % 3) * .045), 9 + ring * .5);
    }
    glowDot(g, w * .5, h * .5,
            (3 + gather * 8 + d.bassBody * 3) * lerp(1, .35, collapse),
            '#c2f2c1', motifAlpha * (.16 + gather * .28));
    if (collapse < .96) {
      drawOutroDivaPackets(g, w, h, t, d, true, 'left', 1 - collapse * .82);
    }
  });

  if (gather > .05 && collapse < .72) {
    const faceAlpha = gather * (1 - collapse) * .72;
    drawMarsFaceActor(g, -w * .015, h * .51, h * .58,
                      '#ffe09b', t, d, 6.4, faceAlpha, -.09, true);
    drawMarsFaceActor(g, w * 1.015, h * .48, h * .54,
                      '#79ead7', t, d, 4.6, faceAlpha, .08, true);
  }

  if (collapse > .72) {
    const q = smooth(clamp((collapse - .72) / .28));
    const trace = new Path2D();
    const span = w * lerp(.14, .025, q);
    trace.moveTo(w * .5 - span, h * .5 + span * .14);
    trace.bezierCurveTo(w * .5 - span * .35, h * .5 - span * .33,
                        w * .5 + span * .36, h * .5 + span * .29,
                        w * .5 + span, h * .5 - span * .12);
    pathStroke(g, trace, '#b8f0c3', lerp(2.2, .8, q),
               lerp(.62, .18, q), lerp(18, 5, q));
  }
}

function drawOutroScene(g, w, h, t, d, shot) {
  const start = lowLightOutroScene?.startSec || 174.033333;
  const end = signoffOutroScene?.endSec || 199.25;
  const local = clamp((t - start) / Math.max(.001, end - start));
  if (shot.kind === 'outro-final-iris') {
    drawOutroFinalIris(g, w, h, t, d, shot);
    return local;
  }

  const side = outroPerspective(t, shot);
  fillOutroBackground(g, w, h, t, d, side === 'both' ? 'left' : side);
  withCamera(g, w, h, outroCamera(shot, w, h, t, side), () => {
    if (shot.kind === 'outro-time-tunnel') {
      drawOutroTimeTunnel(g, w, h, t, d, shot,
                          t < 181 ? 'left' : (side === 'right' ? 'right' : 'left'), 1);
    } else {
      drawOutroPerspectiveWorld(g, w, h, t, d, side, 1);
      drawOutroDivaPackets(g, w, h, t, d, false, side, .9);
      if (['outro-crosscut-reprise', 'outro-goodnight-cascade'].includes(shot.kind)) {
        drawOutroTimeTunnel(g, w, h, t, d, shot, side, .22);
      }
    }

    const tunnelOnly = shot.kind === 'outro-time-tunnel' && t >= 185.883;
    if (!tunnelOnly) drawOutroFace(g, w, h, t, d, side, shot, 1);
    else drawTunnelPhoneticTraces(g, w, h, t, d, shot);
  });
  return local;
}

function drawTrackedText(g, text, centerX, y, tracking) {
  const glyphs = [...text];
  const widths = glyphs.map(glyph => g.measureText(glyph).width);
  const total = widths.reduce((sum, width) => sum + width, 0)
              + Math.max(0, glyphs.length - 1) * tracking;
  let x = centerX - total * .5;
  for (let index = 0; index < glyphs.length; index++) {
    g.fillText(glyphs[index], x, y);
    x += widths[index] + tracking;
  }
}

function drawCodaOrbitResidue(g, w, h, t, p) {
  const fade = 1 - smooth(clamp((p - .48) / .42)) * .62;
  for (let orbit = 0; orbit < 9; orbit++) {
    const q = orbit / 8;
    const path = new Path2D();
    const cx = w * .5 + Math.sin(t * .08 + orbit * 1.7) * w * .035;
    const cy = h * .36 + Math.cos(t * .07 + orbit * 1.3) * h * .025;
    path.ellipse(cx, cy,
                 w * (.08 + q * .32), h * (.025 + q * .095),
                 t * (.006 + orbit * .0007) + orbit * .24, 0, TAU);
    const color = ['#73e4d8', '#ffe09b', '#a98fff', '#ff8c98'][orbit % 4];
    pathStroke(g, path, color, .45 + q * .55,
               fade * (.018 + q * .018), 5 + q * 4);
  }
}

function drawProductionCoda(g, w, h, t, d, shot) {
  const p = clamp(shot.p);
  const titleP = smooth(clamp((p - .045) / .28));
  const copyP = smooth(clamp((p - .29) / .2));
  const background = g.createRadialGradient(w * .5, h * .38, 1,
                                             w * .5, h * .42, w * .82);
  background.addColorStop(0, '#0a1a2a');
  background.addColorStop(.52, '#050b18');
  background.addColorStop(1, '#010309');
  g.fillStyle = background;
  g.fillRect(0, 0, w, h);
  drawCodaOrbitResidue(g, w, h, t, p);

  const uncoil = smooth(clamp(p / .32));
  const breathe = 1 + Math.sin(p * Math.PI * 2.2) * (1 - uncoil) * .12;
  const span = w * lerp(.026, .42, uncoil) * breathe;
  const y = h * lerp(.51, .38, uncoil);
  const leftCurve = new Path2D();
  leftCurve.moveTo(w * .5, y);
  leftCurve.bezierCurveTo(w * .5 - span * .18, y - h * .035 * uncoil,
                          w * .5 - span * .72, y + h * .02,
                          w * .5 - span, y - h * .005);
  const rightCurve = new Path2D();
  rightCurve.moveTo(w * .5, y);
  rightCurve.bezierCurveTo(w * .5 + span * .18, y + h * .03 * uncoil,
                           w * .5 + span * .72, y - h * .022,
                           w * .5 + span, y + h * .004);
  pathStroke(g, leftCurve, '#73e4d8', lerp(1.6, .75, uncoil),
             lerp(.52, .18, uncoil), lerp(15, 6, uncoil));
  pathStroke(g, rightCurve, '#ffe09b', lerp(1.6, .75, uncoil),
             lerp(.52, .18, uncoil), lerp(15, 6, uncoil));
  glowDot(g, w * .5, y, lerp(4.5, 1.2, uncoil), '#b9efbf',
          lerp(.62, .08, uncoil));

  g.save();
  g.textAlign = 'left';
  g.textBaseline = 'alphabetic';
  g.font = `500 ${Math.round(Math.min(w, h) * .112)}px Georgia, 'Times New Roman', serif`;
  const titleGradient = g.createLinearGradient(w * .2, 0, w * .8, 0);
  titleGradient.addColorStop(0, '#79eadc');
  titleGradient.addColorStop(.45, '#f7f1df');
  titleGradient.addColorStop(1, '#ffe09b');
  g.fillStyle = titleGradient;
  g.globalAlpha = titleP * .94;
  g.shadowColor = '#b9f1cc';
  g.shadowBlur = 8 + titleP * 13;
  drawTrackedText(g, 'RIVERS OF MARS', w * .5,
                  h * lerp(.405, .35, titleP), lerp(15, 5.5, titleP));
  g.restore();

  g.save();
  g.textAlign = 'center';
  g.textBaseline = 'middle';
  g.globalAlpha = copyP;
  const rise = h * (1 - copyP) * .02;
  g.font = `600 ${Math.round(Math.min(w, h) * .026)}px ui-monospace, SFMono-Regular, Consolas, monospace`;
  g.fillStyle = '#9fded5';
  g.fillText('A DAW-AUTHORED REGISTER DROVE EVERY CUT.', w * .5, h * .54 + rise);

  g.font = `500 ${Math.round(Math.min(w, h) * .028)}px ui-sans-serif, system-ui, sans-serif`;
  g.fillStyle = '#f0eadb';
  g.fillText('voice → faces   ·   drums → tunnel   ·   bass → depth',
             w * .5, h * .645 + rise);
  g.fillStyle = '#d7c9ee';
  g.fillText('MIDI pitch, duration & velocity → color in motion',
             w * .5, h * .715 + rise);

  g.font = `500 ${Math.round(Math.min(w, h) * .021)}px ui-monospace, SFMono-Regular, Consolas, monospace`;
  g.fillStyle = '#7894a8';
  g.fillText('SCENE-DIRECTED  ·  CODE-RENDERED  ·  NO GENERATED FOOTAGE',
             w * .5, h * .855 + rise);
  g.restore();
  return p;
}

function drawRiverScene(g, w, h, t, d, shot) {
  if (shot.kind === 'river-spirograph-bend') {
    return drawRiverSpirographBend(g, w, h, t, d, shot);
  }
  if (shot.kind === 'river-mouth-microcosm') {
    return drawRiverMouthMicrocosm(g, w, h, t, d, shot);
  }
  if (['river-heaven-drumwall', 'river-guitar-vault',
       'river-chorus-plunge'].includes(shot.kind)) {
    return drawRiverWallChorus(g, w, h, t, d, shot);
  }
  const local = clamp((t - riverScene.startSec)
                    / Math.max(.001, riverScene.endSec - riverScene.startSec));
  g.fillStyle = '#020716';
  g.fillRect(0, 0, w, h);
  withCamera(g, w, h, riverCamera(shot, w, h), () => {
    drawRiverWorld(g, w, h, t, d, local, shot);
    drawRiverFlowMotes(g, w, h, t, d);
    drawRiverNoteRibbons(g, w, h, t, d);
    if (shot.kind === 'river-current-macro') {
      drawRiverMacroDetail(g, w, h, t, d);
    }
    drawRiverSchool(g, w, h, t, d);
  });
  return local;
}

const INSPECTION_COLORS = ['#72e4ff', '#f5f7ed', '#ff6b7f', '#a7a0ff',
                           '#75f0c5', '#ffc36f'];

function drawInspectionFragment(g, x, y, size, rotation, color, energy,
                                variant = 0, alpha = 1) {
  g.save();
  g.translate(x, y);
  g.rotate(rotation);
  const width = size * (1.18 + (variant % 3) * .16);
  const height = size * (.5 + (variant % 4) * .08);
  const shard = new Path2D();
  shard.moveTo(-width, 0);
  shard.bezierCurveTo(-width * .52, -height * (1 + energy * .14),
                       width * .08, -height * (.42 + variant * .025),
                       width, -height * .08);
  shard.bezierCurveTo(width * .62, height * (.56 + energy * .18),
                      -width * .12, height * (.8 - variant * .025),
                      -width, 0);
  g.globalCompositeOperation = 'screen';
  g.globalAlpha = alpha * (.035 + energy * .055);
  g.fillStyle = color;
  g.fill(shard);
  pathStroke(g, shard, color, .75 + energy * 1.25,
             alpha * (.48 + energy * .4), 4 + energy * 9);
  const registration = new Path2D();
  registration.moveTo(-width * .34, height * .02);
  registration.bezierCurveTo(-width * .12, -height * .14,
                              width * .12, height * .13,
                              width * .34, -height * .02);
  pathStroke(g, registration, '#f8fbff', .55 + energy * .45,
             alpha * (.2 + energy * .38), 3);
  g.restore();
}

function inspectionStateBlend(a, b, p) {
  const q = smooth(p);
  return {
    x: lerp(a.x, b.x, q), y: lerp(a.y, b.y, q),
    scale: lerp(a.scale, b.scale, q),
    rotation: lerp(a.rotation, b.rotation, q),
  };
}

function inspectionFragmentPose(index, progress, w, h, d, cameraShift = 0,
                                worldSpin = 0) {
  const side = index % 2 ? 1 : -1;
  const angle = index / 12 * TAU + .38;
  const offstage = {
    x: side < 0 ? -w * (.12 + hash(index) * .22) : w * (1.12 + hash(index) * .2),
    y: h * (.2 + hash(index + 3) * .68),
    scale: .25, rotation: side * (1.2 + hash(index + 8)),
  };
  const column = index % 4, row = Math.floor(index / 4);
  const table = {
    x: w * (.27 + column * .155 + (row % 2) * .025),
    y: h * (.42 + row * .135 + Math.sin(index * 1.7) * .018),
    scale: .68 + row * .12,
    rotation: (column - 1.5) * .08 + side * .07,
  };
  const pattern = {
    x: w * (.5 + Math.cos(angle * 1.03) * (.23 + (index % 3) * .012)),
    y: h * (.54 + Math.sin(angle * 1.7) * (.18 + (index % 2) * .025)),
    scale: .76 + Math.sin(angle) * .12,
    rotation: angle * .42 + side * .28,
  };
  const sphere = {
    x: w * (.5 + Math.cos(angle) * (.23 + Math.sin(angle * 2) * .025)),
    y: h * (.49 + Math.sin(angle) * .27 * (.48 + Math.abs(Math.cos(angle)) * .52)),
    scale: .6 + (Math.sin(angle) + 1) * .27,
    rotation: angle + Math.PI * .5,
  };
  const mars = {
    x: w * (.5 + Math.cos(angle) * .18),
    y: h * (.46 + Math.sin(angle) * .27),
    scale: .64 + (Math.sin(angle) + 1) * .2,
    rotation: angle + Math.PI * .5 + .22,
  };
  let pose;
  if (progress < .285) pose = inspectionStateBlend(offstage, table, progress / .285);
  else if (progress < .553) pose = inspectionStateBlend(table, pattern, (progress - .285) / .268);
  else if (progress < .827) pose = inspectionStateBlend(pattern, sphere, (progress - .553) / .274);
  else pose = inspectionStateBlend(sphere, mars, (progress - .827) / .173);
  const bassLift = d.bassBody * Math.sin(angle) * h * .035;
  pose.y -= bassLift;
  pose.depth = .5;
  if (cameraShift > 0) {
    const q = smooth(cameraShift);
    const latitude = Math.sin((index + 1) * 2.399) * .76;
    const longitude = angle + worldSpin;
    const depth = .5 + Math.sin(longitude) * .5;
    const latitudeScale = Math.cos(latitude);
    const sideView = {
      x: w * .61 + Math.cos(longitude) * w * .255 * latitudeScale,
      y: h * .44 + Math.sin(latitude) * h * .205
                   - Math.cos(longitude) * Math.sin(latitude) * h * .035,
      scale: (.58 + depth * .38) * (1 - Math.abs(latitude) * .08),
      rotation: pose.rotation - .2 + worldSpin * .22
                  + Math.sin(longitude) * .18,
    };
    pose = inspectionStateBlend(pose, sideView, q);
    pose.depth = lerp(.5, depth, q);
  }
  return pose;
}

function drawInspectionTable(g, w, h, t, d, progress, cameraShift = 0) {
  g.save();
  g.globalCompositeOperation = 'source-over';
  g.fillStyle = '#020712';
  g.fillRect(0, 0, w, h);
  const pool = g.createRadialGradient(w * .5, h * .5, 0,
                                      w * .5, h * .5, w * .68);
  pool.addColorStop(0, `rgba(37,100,132,${.16 + d.masterBody * .12})`);
  pool.addColorStop(.42, 'rgba(17,36,62,.18)');
  pool.addColorStop(1, '#02071200');
  g.fillStyle = pool;
  g.fillRect(0, 0, w, h);
  g.restore();

  const tableFade = (1 - cameraShift) * (1 - smooth((progress - .74) / .2));
  const tableVisibility = .04 + tableFade * .96;
  const tilt = d.bassBody * .055;
  g.save();
  g.globalCompositeOperation = 'screen';
  g.globalAlpha = .035 + tableFade * .565;
  const plane = new Path2D();
  plane.moveTo(w * .12, h * (.31 + tilt));
  plane.bezierCurveTo(w * .34, h * (.24 - tilt), w * .66, h * (.24 - tilt), w * .88, h * (.31 + tilt));
  plane.bezierCurveTo(w * .96, h * .55, w * .86, h * .82, w * .72, h * .86);
  plane.bezierCurveTo(w * .54, h * .92, w * .3, h * .9, w * .12, h * .8);
  plane.bezierCurveTo(w * .04, h * .61, w * .05, h * .43, w * .12, h * (.31 + tilt));
  g.fillStyle = 'rgba(13,30,48,.42)';
  g.fill(plane);
  pathStroke(g, plane, '#77ddff', 1 + d.masterBody * 1.4,
             tableVisibility * (.32 + tableFade * .34), 7 + d.masterBody * 8);
  for (let row = 0; row < 7; row++) {
    const q = row / 6;
    const y = h * lerp(.34, .82, q);
    const inset = w * lerp(.14, .065, q);
    const line = new Path2D();
    line.moveTo(inset, y);
    line.bezierCurveTo(w * .34, y - h * (.018 + tilt),
                       w * .66, y + h * (.018 - tilt), w - inset, y);
    pathStroke(g, line, row % 2 ? '#365f78' : '#4e8098', .55,
               tableFade * (.18 + d.masterBody * .1), 2);
  }
  for (let column = 0; column < 9; column++) {
    const q = column / 8;
    const x0 = w * lerp(.13, .87, q);
    const x1 = w * lerp(.07, .93, q);
    const line = new Path2D();
    line.moveTo(x0, h * .31);
    line.bezierCurveTo(lerp(x0, x1, .35) + Math.sin(q * Math.PI) * w * .012,
                        h * .46, lerp(x0, x1, .72) - Math.sin(q * Math.PI) * w * .008,
                        h * .69, x1, h * .83);
    pathStroke(g, line, '#436f88', .5, tableFade * .22, 2);
  }
  g.restore();

  const scanAge = t - d.drumEvent.eventTime;
  if (scanAge >= 0 && scanAge < .7) {
    const q = smooth(scanAge / .7);
    const x = lerp(w * .08, w * .92, q);
    const scan = new Path2D();
    scan.moveTo(x - w * .04, h * .28);
    scan.bezierCurveTo(x + w * .025, h * .43, x - w * .02, h * .68,
                       x + w * .055, h * .86);
    pathStroke(g, scan, '#ff7e91', 1 + d.drums * 3,
               tableVisibility * (1 - q) * (.18 + d.drums * .72), 12);
  }
}

function drawInspectionCosmos(g, w, h, t, d, cameraShift) {
  if (cameraShift <= 0) return;
  const q = smooth(cameraShift);
  const pivotStart = inspectionWorldLyric?.startSec ?? t;
  const elapsed = Math.max(0, t - pivotStart);
  g.save();
  g.globalCompositeOperation = 'screen';

  for (let index = 0; index < 92; index++) {
    const depth = .2 + hash(index + 41) * .8;
    const drift = elapsed * (.0007 + depth * .0018);
    const x = w * ((hash(index * 3 + 7) + drift + 1) % 1);
    const y = h * (.04 + hash(index * 5 + 19) * .72);
    const twinkle = .62 + Math.sin(t * (.35 + depth * .7) + index * 2.1) * .22;
    const size = .35 + depth * 1.45;
    const alpha = q * (.08 + depth * .28) * twinkle;
    g.globalAlpha = alpha;
    g.fillStyle = index % 11 === 0 ? '#ff91a2'
                : index % 5 === 0 ? '#aaa5ff' : '#d9f8ff';
    g.beginPath();
    g.ellipse(x, y, size * 1.3, size * .72, hash(index + 4) * 1.8, 0, TAU);
    g.fill();
    if (depth > .8 && index % 4 === 0) {
      const sparkle = new Path2D();
      sparkle.moveTo(x - size * 3, y);
      sparkle.bezierCurveTo(x - size, y - size * .18,
                             x + size, y + size * .18, x + size * 3, y);
      sparkle.moveTo(x, y - size * 2.1);
      sparkle.bezierCurveTo(x - size * .12, y - size * .7,
                             x + size * .12, y + size * .7, x, y + size * 2.1);
      pathStroke(g, sparkle, g.fillStyle, .4 + depth * .45, alpha * .72, 4);
    }
  }

  const galaxyX = w * .22;
  const galaxyY = h * .27;
  const galaxyTilt = -.28 + d.bassBody * .08;
  const galaxyScale = .86 + d.drums * .18;
  for (let arm = 0; arm < 4; arm++) {
    const path = new Path2D();
    const armPhase = arm / 4 * TAU + elapsed * .055;
    for (let step = 0; step <= 38; step++) {
      const f = step / 38;
      const angle = armPhase + f * TAU * 1.18;
      const radius = w * (.008 + f * .105) * galaxyScale;
      const localX = Math.cos(angle) * radius;
      const localY = Math.sin(angle) * radius * .32;
      const x = galaxyX + localX * Math.cos(galaxyTilt)
                         - localY * Math.sin(galaxyTilt);
      const y = galaxyY + localX * Math.sin(galaxyTilt)
                         + localY * Math.cos(galaxyTilt);
      if (step === 0) path.moveTo(x, y); else path.lineTo(x, y);
    }
    pathStroke(g, path, arm % 2 ? '#8d98ff' : '#63dff1',
               .45 + d.drums * .7,
               q * (.055 + d.drums * .13), 5 + d.drums * 5);
  }
  const core = g.createRadialGradient(galaxyX, galaxyY, 0,
                                      galaxyX, galaxyY, w * .075);
  core.addColorStop(0, `rgba(240,251,255,${q * (.2 + d.drums * .25)})`);
  core.addColorStop(.22, `rgba(110,218,241,${q * (.1 + d.drums * .14)})`);
  core.addColorStop(1, 'rgba(30,70,100,0)');
  g.globalAlpha = 1;
  g.fillStyle = core;
  g.fillRect(galaxyX - w * .1, galaxyY - h * .16, w * .2, h * .32);

  const eventAge = t - d.drumEvent.eventTime;
  if (eventAge >= 0 && eventAge < .85) {
    const birth = smooth(eventAge / .85);
    const eventIndex = Math.floor(d.drumEvent.eventTime * 11) % 9;
    const eventAngle = eventIndex / 9 * TAU + elapsed * .04;
    const radius = w * lerp(.018, .118, birth);
    const x = galaxyX + Math.cos(eventAngle) * radius;
    const y = galaxyY + Math.sin(eventAngle) * radius * .34;
    const flare = new Path2D();
    flare.moveTo(x - w * .012 * (1 - birth), y);
    flare.bezierCurveTo(x - w * .003, y - h * .002,
                         x + w * .003, y + h * .002,
                         x + w * .012 * (1 - birth), y);
    flare.moveTo(x, y - h * .018 * (1 - birth));
    flare.bezierCurveTo(x - w * .001, y - h * .004,
                         x + w * .001, y + h * .004,
                         x, y + h * .018 * (1 - birth));
    pathStroke(g, flare, eventIndex % 2 ? '#ff8da2' : '#ecfbff',
               .8 + d.drums * 1.2, q * (1 - birth) * (.3 + d.drums * .55), 8);
  }
  g.restore();
}

function drawInspectionWorldStage(g, w, h, t, d, cameraShift) {
  if (cameraShift <= 0) return;
  const q = smooth(cameraShift);
  drawInspectionCosmos(g, w, h, t, d, cameraShift);
  g.save();
  g.globalCompositeOperation = 'screen';
  g.globalAlpha = q;

  const horizon = new Path2D();
  horizon.moveTo(-w * .08, h * .7);
  horizon.bezierCurveTo(w * .24, h * (.62 + d.bassBody * .025),
                         w * .69, h * (.67 - d.bassBody * .035),
                         w * 1.08, h * .5);
  pathStroke(g, horizon, '#5ad5ef', 1.1 + d.masterBody * 1.7,
             .24 + d.masterBody * .2, 7 + d.masterBody * 8);

  const vanishingX = w * .88;
  const vanishingY = h * .54;
  for (let ray = 0; ray < 9; ray++) {
    const f = ray / 8;
    const startX = lerp(-w * .12, w * .72, f);
    const startY = h * lerp(1.05, .73, f);
    const path = new Path2D();
    path.moveTo(startX, startY);
    path.bezierCurveTo(lerp(startX, vanishingX, .38),
                        lerp(startY, vanishingY, .38) + h * Math.sin(f * Math.PI) * .035,
                        lerp(startX, vanishingX, .78),
                        lerp(startY, vanishingY, .78) - h * .018,
                        vanishingX, vanishingY);
    pathStroke(g, path, ray % 3 ? '#284f67' : '#447d93', .55,
               .12 + d.masterBody * .08, 2);
  }
  for (let arc = 0; arc < 6; arc++) {
    const f = arc / 5;
    const path = new Path2D();
    const y = h * lerp(.72, 1.02, f);
    path.moveTo(-w * .08, y);
    path.bezierCurveTo(w * .25, y - h * (.06 + f * .05),
                        w * .66, y - h * (.025 + f * .04),
                        w * 1.06, lerp(y, vanishingY, .72));
    pathStroke(g, path, '#315f76', .6, .12 + d.masterBody * .1, 2);
  }

  const orbital = new Path2D();
  orbital.ellipse(w * .61, h * .44, w * .36, h * .115,
                  -.21 + d.bassBody * .06, 0, TAU);
  pathStroke(g, orbital, '#ff7087', 1 + d.bassBody * 2.1,
             .14 + d.bassBody * .24, 9 + d.bassBody * 10);

  const nearArc = new Path2D();
  nearArc.moveTo(w * .13, h * 1.04);
  nearArc.bezierCurveTo(w * .31, h * .76, w * .55, h * .7, w * .84, h * .79);
  pathStroke(g, nearArc, '#6ce5ff', 2 + d.masterBody * 2.4,
             .16 + d.masterBody * .22, 12);
  g.restore();
}

function drawInspectionConnections(g, poses, w, h, d, progress, cameraShift = 0,
                                   worldSpin = 0) {
  const reveal = smooth((progress - .24) / .24);
  if (reveal <= 0) return;
  const pairs = [[0, 5], [5, 9], [9, 2], [2, 7], [7, 11], [11, 3],
                 [3, 8], [8, 1], [1, 6], [6, 10]];
  for (let index = 0; index < pairs.length; index++) {
    const [aIndex, bIndex] = pairs[index];
    const a = poses[aIndex], b = poses[bIndex];
    const path = new Path2D();
    path.moveTo(a.x, a.y);
    const bow = (index % 2 ? 1 : -1) * h * (.035 + d.bassBody * .045);
    path.bezierCurveTo(lerp(a.x, b.x, .3), lerp(a.y, b.y, .3) + bow,
                       lerp(a.x, b.x, .7), lerp(a.y, b.y, .7) - bow,
                       b.x, b.y);
    pathStroke(g, path, index % 3 ? '#5bcbe8' : '#ff7188',
               .55 + d.masterBody * .9,
               reveal * (.1 + d.masterBody * .25), 4 + d.masterBody * 7);
  }
  if (progress > .5) {
    const globe = smooth((progress - .5) / .32);
    const cx = lerp(w * .5, w * .61, cameraShift);
    const cy = lerp(h * .49, h * .44, cameraShift);
    for (let ring = 0; ring < 4; ring++) {
      const path = new Path2D();
      path.ellipse(cx, cy,
                   w * (.18 + ring * .025 + cameraShift * .035) * globe,
                   h * (.08 + ring * .055 - cameraShift * .018) * globe,
                   (ring - 1.5) * .34 + d.bassBody * .12
                     + cameraShift * (.34 + ring * .035 + worldSpin * .14), 0, TAU);
      pathStroke(g, path, ring % 2 ? '#86eaff' : '#ff7889',
                 .6 + d.masterBody, globe * (.12 + d.masterBody * .22), 5);
    }
  }
}

function drawInspectionPerformers(g, w, h, t, d, lyric, cameraShift = 0) {
  const lyricIndex = lyric ? lyrics.indexOf(lyric) : 0;
  const activeSide = lyricIndex % 2 ? 1 : -1;
  for (const side of [-1, 1]) {
    const active = side === activeSide;
    const energy = active ? d.voiceFeature : d.echoBody * .45;
    const worldFocus = cameraShift * (side < 0 ? 1 : .35);
    const baseSize = Math.min(w, h) * (active ? .19 + energy * .14 : .115);
    const size = baseSize * lerp(1, side < 0 ? 1.55 : .72, cameraShift);
    const baseX = side < 0 ? w * .13 : w * .87;
    const x = lerp(baseX, side < 0 ? w * .045 : w * 1.015, cameraShift);
    const baseY = h * (.24 + Math.sin(t * 1.1 + side) * .025 - energy * .035);
    const y = lerp(baseY, side < 0 ? h * .59 : h * .25, cameraShift);
    const rotation = side * (-.13 - energy * .08) + Math.sin(t * 2.2) * .018;
    drawFrontFeatures(g, x, y, size, t, d, energy,
                      side < 0 ? '#7ce8ff' : '#ff7f91', side * 2.3,
                      (active ? .62 + energy * .35 : .22)
                        * lerp(1, side < 0 ? .92 : .22, worldFocus),
                      rotation - cameraShift * .12);
  }
}

function drawInspectionScene(g, w, h, t, d, shot) {
  const progress = clamp((t - patternScene.startSec)
                       / Math.max(.001, patternScene.endSec - patternScene.startSec));
  const pivotStart = inspectionWorldLyric?.startSec
    ?? (patternScene.startSec + (patternScene.endSec - patternScene.startSec) * .64);
  const cameraShift = smooth((t - pivotStart) / 1.05);
  const worldSpin = Math.max(0, t - pivotStart) * .24;
  drawInspectionTable(g, w, h, t, d, progress, cameraShift);
  drawInspectionWorldStage(g, w, h, t, d, cameraShift);
  const poses = [];
  const lyric = activeLyric(t);
  const lyricIndex = lyric ? lyrics.indexOf(lyric) : 0;
  const selected = ((lyricIndex % 12) + 12) % 12;
  for (let index = 0; index < 12; index++) {
    const pose = inspectionFragmentPose(index, progress, w, h, d, cameraShift,
                                        worldSpin);
    const isSelected = index === selected;
    if (isSelected) {
      pose.y -= d.voiceFeature * h * .055;
      pose.scale *= 1 + d.voiceFeature * .22;
      pose.rotation += d.voice * .55;
    }
    poses.push(pose);
  }
  drawInspectionConnections(g, poses, w, h, d, progress, cameraShift, worldSpin);
  const drawOrder = poses.map((pose, index) => ({pose, index}))
    .sort((a, b) => a.pose.depth - b.pose.depth);
  for (const {pose, index} of drawOrder) {
    const energy = index === selected ? d.voiceFeature : d.masterBody * .42;
    drawInspectionFragment(g, pose.x, pose.y,
                           Math.min(w, h) * .055 * pose.scale,
                           pose.rotation, INSPECTION_COLORS[index % INSPECTION_COLORS.length],
                           energy, index,
                           (.38 + pose.scale * .28) * lerp(.76, 1.15, pose.depth));
  }
  drawInspectionPerformers(g, w, h, t, d, lyric, cameraShift);
  return progress;
}

function drawGardenPatternTransitionFrame(g, w, h, t, d, progress) {
  const collapse = smooth(clamp(progress + d.drums * .035 + d.masterBody * .02));
  const red = Math.round(lerp(4, 2, collapse));
  const green = Math.round(lerp(17, 7, collapse));
  const blue = Math.round(lerp(20, 18, collapse));
  g.save();
  g.globalCompositeOperation = 'source-over';
  g.fillStyle = `rgb(${red},${green},${blue})`;
  g.fillRect(0, 0, w, h);
  g.restore();

  const gardenColors = ['#4ee0b0', '#e98db9', '#f2ce72'];
  const inspectionColors = ['#72e4ff', '#ff6b7f', '#f5f7ed'];
  for (let ring = 0; ring < 8; ring++) {
    const q = ring / 7;
    const path = new Path2D();
    const cx = w * .5;
    const cy = lerp(h * .46, h * .59, collapse);
    const rx = w * lerp(.12 + q * .075, .16 + q * .05, collapse);
    const ry = h * lerp(.13 + q * .07, .035 + q * .026, collapse);
    path.ellipse(cx, cy, rx, ry, lerp(Math.sin(t * .13) * .06, -.08, collapse), 0, TAU);
    pathStroke(g, path, collapse < .52 ? gardenColors[ring % 3] : inspectionColors[ring % 3],
               1 + d.masterBody * 3 + d.drums * 1.5,
               .22 + d.masterBody * .22, 7 + d.drums * 9);
  }

  for (let index = 0; index < 12; index++) {
    const angle = index / 12 * TAU + .28;
    const gardenX = w * (.5 + Math.cos(angle) * .31);
    const gardenY = h * (.47 + Math.sin(angle) * .3);
    const column = index % 4, row = Math.floor(index / 4);
    const tableX = w * (.27 + column * .155 + (row % 2) * .025);
    const tableY = h * (.42 + row * .135);
    const x = lerp(gardenX, tableX, collapse);
    const y = lerp(gardenY, tableY, collapse);
    const rotation = lerp(angle + Math.PI * .5, (column - 1.5) * .08, collapse);
    drawInspectionFragment(g, x, y, Math.min(w, h) * lerp(.075, .045, collapse),
                           rotation, collapse < .5 ? gardenColors[index % 3]
                                                  : inspectionColors[index % 3],
                           d.masterBody + d.drums * .4, index,
                           .4 + collapse * .45);
  }

  const aperture = new Path2D();
  aperture.ellipse(w * .5, lerp(h * .29, h * .58, collapse),
                   lerp(w * .055, w * .39, collapse),
                   lerp(h * .13, h * .12, collapse),
                   lerp(.08, -.08, collapse), 0, TAU);
  g.save();
  g.globalCompositeOperation = 'source-over';
  g.fillStyle = `rgba(1,4,12,${.78 + collapse * .16})`;
  g.fill(aperture);
  g.restore();
  pathStroke(g, aperture, collapse < .5 ? '#72e5b3' : '#80e8ff',
             1.2 + d.masterBody * 2.2, .36 + collapse * .4, 10);

  if (collapse > .46) {
    const gridReveal = smooth((collapse - .46) / .54);
    for (let line = 0; line < 7; line++) {
      const q = line / 6;
      const y = h * lerp(.42, .75, q);
      const path = new Path2D();
      path.moveTo(w * lerp(.28, .11, q), y);
      path.bezierCurveTo(w * .38, y - h * .015, w * .62, y + h * .015,
                         w * lerp(.72, .89, q), y);
      pathStroke(g, path, '#5ea5bc', .55, gridReveal * .28, 3);
    }
  }
}

function drawLyric(g, w, h, lyric, voice) {
  if (!lyric) return;
  const color = lyric.speaker === 'Them 1' ? '#ffc08a'
              : lyric.speaker === 'Them 2' ? '#8ff7df' : '#eef4ff';
  const size = Math.round(Math.min(w, h) * .034);
  g.save();
  g.globalCompositeOperation = 'screen';
  g.textAlign = 'center';
  g.textBaseline = 'middle';
  g.font = `350 ${size}px ui-sans-serif, system-ui, sans-serif`;
  g.shadowColor = color;
  g.shadowBlur = 8 + voice * 13;
  g.globalAlpha = .82 + voice * .16;
  g.fillStyle = color;
  g.fillText(lyric.text, w * .5, h * .91);
  g.shadowBlur = 0;
  const measured = Math.min(w * .68, g.measureText(lyric.text).width * 1.08);
  const underline = new Path2D();
  underline.moveTo(w * .5 - measured * .5, h * .945);
  underline.bezierCurveTo(w * .5 - measured * .18, h * (.942 - voice * .006),
                          w * .5 + measured * .16, h * (.95 + voice * .005),
                          w * .5 + measured * .5, h * .944);
  pathStroke(g, underline, color, .8 + voice * .7, .24 + voice * .25, 5);
  g.restore();
}

function drawFrame(g, t, w, h) {
  const scene = sceneAt(t);
  let local = scene?.id === 'scene-mars-unmasking'
    ? clamp((t - scene.startSec) / (scene.endSec - scene.startSec))
    : (t % 14.533333) / 14.533333;
  const d = driversAt(t);
  const lyric = activeLyric(t);
  const shot = shotAt(t);
  const isOpening = OPENING_SHOT_KINDS.includes(shot.kind);
  const isGarden = GARDEN_SHOT_KINDS.includes(shot.kind);
  const isMidiNetwork = MIDI_NETWORK_SHOT_KINDS.includes(shot.kind)
    || scene?.id === 'scene-mtejqrtr';
  const isReceiver = RECEIVER_SHOT_KINDS.includes(shot.kind)
    || scene?.id === 'scene-mtejt6in';
  const isPattern = PATTERN_SHOT_KINDS.includes(shot.kind)
    || scene?.id === 'scene-pattern-aperture';
  const isSemantic = SEMANTIC_SHOT_KINDS.includes(shot.kind)
    || scene?.id === 'scene-semantic-rocket-weather';
  const isCurrent = CURRENT_SHOT_KINDS.includes(shot.kind)
    || scene?.id === 'scene-current-turns-home';
  const isOutro = OUTRO_SHOT_KINDS.includes(shot.kind)
    || scene?.id === 'scene-low-light-outro'
    || scene?.id === 'scene-mtekxa2z';
  const isCoda = CODA_SHOT_KINDS.includes(shot.kind)
    || scene?.id === 'scene-production-coda';
  const isRiver = RIVER_SHOT_KINDS.includes(shot.kind)
    || scene?.id === 'scene-rivers-of-mars';
  const isMars = scene?.id === 'scene-mars-unmasking'
    || (!isOpening && !isMidiNetwork && !isReceiver && !isGarden && !isPattern && !isSemantic
        && !isCurrent && !isOutro && !isCoda && !isRiver
        && MARS_SHOT_KINDS.includes(shot.kind));
  const transitionStart = gardenPatternTransition?.startSec
    ?? ((patternScene?.startSec ?? 77.25) - .533333);
  const transitionEnd = gardenPatternTransition?.endSec
    ?? ((patternScene?.startSec ?? 77.25) + 1.416667);
  const isGardenPatternTransition = Boolean(patternScene)
    && t >= transitionStart && t < transitionEnd;
  let displayedShot = shot;
  if (isOpening) {
    local = drawOpeningSequence(g, w, h, t, d, shot);
  } else if (isMidiNetwork) {
    local = drawMidiNetworkScene(g, w, h, t, d, shot);
  } else if (isReceiver) {
    local = drawReceiverScene(g, w, h, t, d, shot);
  } else if (isGardenPatternTransition) {
    local = clamp((t - transitionStart) / Math.max(.001, transitionEnd - transitionStart));
    drawGardenPatternTransitionFrame(g, w, h, t, d, local);
    displayedShot = {...shot, name: 'garden → inspection aperture'};
  } else if (isGarden) {
    local = drawGardenFrame(g, w, h, t, d, shot);
  } else if (isPattern) {
    local = drawInspectionScene(g, w, h, t, d, shot);
  } else if (isSemantic) {
    local = drawSemanticScene(g, w, h, t, d, shot);
  } else if (isCurrent) {
    local = drawCurrentTurnsScene(g, w, h, t, d, shot);
  } else if (isOutro) {
    local = drawOutroScene(g, w, h, t, d, shot);
  } else if (isCoda) {
    local = drawProductionCoda(g, w, h, t, d, shot);
  } else if (isRiver) {
    local = drawRiverScene(g, w, h, t, d, shot);
  } else {
    drawAtmosphere(g, w, h, t, d, local);
    drawPeripheralActivity(g, w, h, t, d, false);
    if (isMars) drawMarsNoteTrails(g, w, h, t, d, shot, false);
    const q = easeInOut(shot.p);
    if (shot.index === 0) drawOpeningFormation(g, w, h, t, d, local, q);
    else if (shot.index === 1) drawOverheadFormation(g, w, h, t, d, local, q);
    else if (shot.index === 2) drawSpinningFormation(g, w, h, t, d, local, q);
    else if (shot.index === 3) drawBreakFormation(g, w, h, t, d, local, q);
    else if (shot.index === 4) drawCounterfeitLine(g, w, h, t, d, local, q);
    else if (shot.index === 5) drawDigFormation(g, w, h, t, d, local, q);
    else drawFinalKaleidoscope(g, w, h, t, d, local, q);
    if (isMars) drawMarsNoteTrails(g, w, h, t, d, shot, true);
    drawPeripheralActivity(g, w, h, t, d, true);
  }
  drawReceiverGardenOpticalOverlay(g, w, h, t, d);
  drawLyric(g, w, h, lyric, d.voice);

  if (isMars && !isGardenPatternTransition && local < .16) {
    g.save();
    g.globalCompositeOperation = 'screen';
    g.globalAlpha = smooth(local / .08) * (1 - smooth((local - .1) / .06));
    g.fillStyle = '#ffd8aa';
    g.font = `500 ${Math.round(Math.min(w, h) * .033)}px ui-monospace, SFMono-Regular, Consolas, monospace`;
    g.textAlign = 'center';
    g.letterSpacing = `${Math.max(2, w * .004)}px`;
    g.fillText('SUBJECT: MARS', w * .5, h * .18);
    g.restore();
  }
  return {drivers: d, lyric, scene, progress: local, shot: displayedShot};
}

function resize(w = innerWidth, h = innerHeight) {
  const dpr = offline ? 1 : Math.min(devicePixelRatio || 1, 2);
  canvas.width = Math.max(2, Math.round(w * dpr));
  canvas.height = Math.max(2, Math.round(h * dpr));
  canvas.style.width = `${w}px`;
  canvas.style.height = `${h}px`;
  work.width = canvas.width;
  work.height = canvas.height;
}

function updateReadout(t, state) {
  if (offline) return;
  scrub.value = t;
  const minutes = Math.floor(t / 60);
  clock.value = `${minutes}:${(t - minutes * 60).toFixed(2).padStart(5, '0')}`;
  captionEl.textContent = state.lyric?.text || '';
  driversEl.querySelector('.driver-title').textContent =
    `DAW → picture · ${state.shot?.name || 'scene'}`;
  const values = {
    'lead-vocal': state.drivers.voice,
    'backing-vocals': state.drivers.echo,
    drums: state.drivers.drums,
    guitar: state.drivers.guitar,
    bass: state.drivers.bass,
    master: state.drivers.master,
  };
  for (const [id, value] of Object.entries(values)) {
    const row = driversEl.querySelector(`[data-id="${id}"]`);
    row.querySelector('i').style.width = `${clamp(value) * 100}%`;
    row.querySelector('b').textContent = value.toFixed(2);
  }
}

function previewDraw(t) {
  const state = drawFrame(ctx, t, canvas.width, canvas.height);
  updateReadout(t, state);
}

function animationLoop() {
  if (!offline) {
    if (!audio.paused) {
      previewTime = audio.currentTime;
      if (previewTime >= selectedScene.endSec) {
        if (loopToggle.checked) {
          audio.currentTime = selectedScene.startSec;
          previewTime = selectedScene.startSec;
        } else {
          audio.pause();
          playButton.textContent = 'Play';
          previewTime = selectedScene.endSec - .001;
        }
      }
    }
    previewDraw(previewTime);
  }
  requestAnimationFrame(animationLoop);
}

function selectScene(id) {
  selectedScene = prototypeScenes.find(scene => scene.id === id) || selectedScene;
  previewTime = selectedScene.startSec;
  audio.currentTime = previewTime;
  scrub.value = previewTime;
  history.replaceState(null, '', `?scene=${encodeURIComponent(selectedScene.id)}`);
  previewDraw(previewTime);
}

playButton.addEventListener('click', async () => {
  if (audio.paused) {
    if (audio.currentTime < selectedScene.startSec || audio.currentTime >= selectedScene.endSec) {
      audio.currentTime = selectedScene.startSec;
    }
    await audio.play();
    playButton.textContent = 'Pause';
  } else {
    audio.pause();
    playButton.textContent = 'Play';
  }
});
sceneSelect.addEventListener('change', () => selectScene(sceneSelect.value));
scrub.addEventListener('input', () => {
  previewTime = Number(scrub.value);
  audio.currentTime = previewTime;
  previewDraw(previewTime);
});
addEventListener('keydown', event => {
  if (event.code !== 'Space' || event.repeat || /INPUT|SELECT|TEXTAREA/.test(event.target.tagName)) return;
  event.preventDefault();
  playButton.click();
});
addEventListener('resize', () => { if (!offline) resize(); });

window.setRenderSize = (w, h) => {
  offline = true;
  transport.hidden = true;
  driversEl.hidden = true;
  captionEl.hidden = true;
  transport.style.display = 'none';
  driversEl.style.display = 'none';
  captionEl.style.display = 'none';
  resize(w, h);
};

window.renderFrame = (t, frameDt, samples = 1) => {
  const n = Math.max(1, Math.round(samples));
  ctx.save();
  ctx.globalCompositeOperation = 'source-over';
  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.globalCompositeOperation = 'lighter';
  ctx.globalAlpha = 1 / n;
  for (let i = 0; i < n; i++) {
    drawFrame(workCtx, t + (i + .5) / n * frameDt, work.width, work.height);
    ctx.drawImage(work, 0, 0);
  }
  ctx.restore();
};

window.__probe = (t, samples = 1, repetitions = 8) => {
  // Canvas draw/filter work is synchronous enough for this to be a useful
  // end-to-end page-side measure. Capture/encoding is deliberately excluded;
  // world_render.py measures that separately around the DevTools readback.
  const runs = Math.max(1, Math.round(repetitions));
  const started = performance.now();
  for (let i = 0; i < runs; i++) {
    window.renderFrame(t + i / 1000, 1 / 60, samples);
  }
  return {drawMs: (performance.now() - started) / runs, simMs: 0, gpuMs: 0};
};

window.__driversAt = driversAt;
window.__sceneAt = sceneAt;
window.__project = {project, timeline, beatmap, compiled};
window.__gpu = graphicsBackend();
resize();
previewDraw(previewTime);
animationLoop();
window.__ready = true;
