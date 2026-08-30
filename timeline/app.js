const $ = (q) => document.querySelector(q);
const els = {
  title: $('#title'), play: $('#play'), save: $('#save'), status: $('#status'),
  snap: $('#snap'), zoom: $('#zoom'), scroll: $('#scroll'), timeline: $('#timeline'),
  ruler: $('#ruler'), tracks: $('#tracks'), labels: $('#trackLabels'),
  playhead: $('#playhead'), barClock: $('#barClock'), timeClock: $('#timeClock'),
  audio: $('#audio'), unplaced: $('#unplaced'), unplacedCount: $('#unplacedCount'),
  empty: $('#emptySelection'), form: $('#itemForm'), del: $('#delete'),
  fieldId: $('#fieldId'), fieldText: $('#fieldText'), fieldStart: $('#fieldStart'),
  fieldEnd: $('#fieldEnd'), fieldDrivers: $('#fieldDrivers'), fieldAi: $('#fieldAi'),
  choreographyFields: $('#choreographyFields'), fieldRendererShot: $('#fieldRendererShot'),
  fieldMetaphors: $('#fieldMetaphors'),
  fieldCamera: $('#fieldCamera'), fieldFormation: $('#fieldFormation'),
  fieldInteractions: $('#fieldInteractions'),
  blockingPanel: $('#blockingPanel'), blockingPreview: $('#blockingPreview'),
  blockingElements: $('#blockingElements'), addBlockingElement: $('#addBlockingElement'),
  blockingElementForm: $('#blockingElementForm'), fieldElementId: $('#fieldElementId'),
  fieldElementLabel: $('#fieldElementLabel'), fieldElementKind: $('#fieldElementKind'),
  fieldElementLayer: $('#fieldElementLayer'), fieldElementEntrance: $('#fieldElementEntrance'),
  fieldElementAction: $('#fieldElementAction'), fieldElementExit: $('#fieldElementExit'),
  fieldElementPath: $('#fieldElementPath'),
  fieldImprovRow: $('#fieldImprovRow'), fieldImprov: $('#fieldImprov'),
  fieldSuggestion: $('#fieldSuggestion'), deleteDialog: $('#deleteDialog'),
  deleteForm: $('#deleteForm'), deleteMessage: $('#deleteMessage'),
  deleteInput: $('#deleteConfirmInput'), deleteCancel: $('#deleteCancel'),
  deleteCommit: $('#deleteCommit')
};

let project, timeline, beatmap, waveforms = {tracks: []}, grid = [], byBar = new Map();
let pxPerSec = +els.zoom.value, duration = 0, currentTime = 0;
let selected = null, dirty = false, raf = 0, auditionEnd = null;
let selectedBlockingElementId = null;
let referencesCollapsed = localStorage.getItem('referenceWaveformsCollapsed') === 'true';

const fmtTime = t => {
  t = Math.max(0, t);
  const min = Math.floor(t / 60), sec = t - min * 60;
  return `${min}:${sec.toFixed(3).padStart(6, '0')}`;
};

function buildGrid() {
  byBar = new Map(beatmap.bars.map(b => [+b.bar, b]));
  grid = [];
  for (const bar of beatmap.bars) {
    bar.beats.forEach((sec, i) => grid.push({sec: +sec, bar: +bar.bar, beat: i + 1}));
  }
  grid.sort((a, b) => a.sec - b.sec);
}

function parsePos(value) {
  const p = String(value || '').trim().split('.').map(Number);
  if (!p.length || p.some(Number.isNaN)) throw new Error(`Invalid position “${value}”`);
  return {bar: p[0], beat: p[1] || 1, tick: p[2] || 0};
}

function posToSec(value) {
  const p = parsePos(value), bar = byBar.get(p.bar);
  if (!bar || p.beat < 1 || p.beat > bar.beats.length) throw new Error(`Position ${value} is outside the grid`);
  const a = +bar.beats[p.beat - 1];
  if (!p.tick) return a;
  const nextBar = byBar.get(p.bar + 1);
  const b = p.beat < bar.beats.length ? +bar.beats[p.beat] : +(nextBar?.beats[0]);
  if (!Number.isFinite(b)) throw new Error(`Position ${value} cannot be interpolated`);
  return a + (b - a) * p.tick / beatmap.ppq;
}

function secToPos(sec, snapTicks = +els.snap.value) {
  let lo = 0, hi = grid.length - 1;
  while (lo < hi) {
    const mid = Math.ceil((lo + hi) / 2);
    if (grid[mid].sec <= sec) lo = mid; else hi = mid - 1;
  }
  let i = Math.max(0, Math.min(lo, grid.length - 2));
  const a = grid[i], b = grid[i + 1];
  let tick = Math.round(((sec - a.sec) / Math.max(.000001, b.sec - a.sec)) * beatmap.ppq);
  if (snapTicks) tick = Math.round(tick / snapTicks) * snapTicks;
  let point = a;
  if (tick >= beatmap.ppq) { point = b; tick = 0; }
  tick = Math.max(0, Math.min(beatmap.ppq - 1, tick));
  return `${point.bar}.${point.beat}${tick ? `.${tick}` : ''}`;
}

function snapSec(sec) {
  const pos = secToPos(Math.max(0, Math.min(duration, sec)));
  return {pos, sec: posToSec(pos)};
}

function markDirty(message = 'Unsaved changes') {
  dirty = true;
  els.save.disabled = false;
  els.status.textContent = message;
  els.status.classList.remove('error');
}

function setStatus(message, error = false) {
  els.status.textContent = message;
  els.status.classList.toggle('error', error);
}

function allItems() {
  return timeline.tracks.flatMap(track => track.items.map(item => ({track, item})));
}

function itemLabel(item) {
  return item.text || item.prompt || item.name || item.id;
}

const SVG_NS = 'http://www.w3.org/2000/svg';
const blockingKindMarkup = {
  performer: '<path d="M-8,-3 Q0,-9 8,-3 M-7,2 Q0,8 7,2 M-8,-3 l-3,-2 M8,-3 l3,-2"/><path d="M-6,11 Q0,15 6,11"/>',
  chorus: '<path d="M0,-10 Q-8,-4 -7,5 M0,-10 Q8,-4 7,5 M-7,5 Q0,12 7,5"/>',
  object: '<path d="M0,-10 C8,-9 11,-2 9,5 C6,11 -5,12 -10,4 C-12,-3 -7,-9 0,-10Z"/>',
  environment: '<path d="M-13,7 C-7,-8 4,-10 13,5 M-11,10 C-3,4 5,4 12,9"/>',
};

function blockingFor(item, create = false) {
  if (!item.blocking && create) item.blocking = {camera: '', formation: '', elements: [], interactions: []};
  if (item.blocking && !Array.isArray(item.blocking.elements)) item.blocking.elements = [];
  if (item.blocking && !Array.isArray(item.blocking.interactions)) item.blocking.interactions = [];
  return item.blocking || null;
}

function selectedBlockingElement() {
  const blocking = selected?.track.type === 'choreography' ? blockingFor(selected.item) : null;
  return blocking?.elements.find(element => element.id === selectedBlockingElementId) || null;
}

function formatMotionPath(points) {
  return (points || []).map(point => `${Number(point[0]).toFixed(0)},${Number(point[1]).toFixed(0)}`).join(' ');
}

function parseMotionPath(value) {
  const points = String(value || '').trim().split(/\s+/).filter(Boolean).map(token => {
    const pair = token.split(',').map(Number);
    if (pair.length !== 2 || pair.some(n => !Number.isFinite(n) || n < 0 || n > 100)) {
      throw new Error('Motion path uses percent pairs such as 10,60 42,35 88,55');
    }
    return pair;
  });
  if (!points.length) throw new Error('Motion path needs at least one point');
  return points;
}

function formatInteractions(interactions) {
  return (interactions || []).map(item =>
    `${Number(item.window?.[0] || 0).toFixed(2)}-${Number(item.window?.[1] ?? 1).toFixed(2)} | ${item.id} | ${item.initiator} -> ${item.responder} | ${item.action}`
  ).join('\n');
}

function parseInteractions(value) {
  return String(value || '').split(/\r?\n/).map(line => line.trim()).filter(Boolean).map(line => {
    const match = line.match(/^(\d*\.?\d+)\s*[-–]\s*(\d*\.?\d+)\s*\|\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*\|\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*(?:->|→)\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*\|\s*(.+)$/);
    if (!match) throw new Error('Interaction lines use: 0.10-0.70 | id | initiator -> responder | action');
    const start = Number(match[1]), end = Number(match[2]);
    if (start < 0 || end > 1 || end <= start) throw new Error('Interaction windows must increase within 0..1');
    return {id: match[3], initiator: match[4], responder: match[5],
            window: [start, end], action: match[6].trim()};
  });
}

function blockingPoint(points, progress) {
  if (!points?.length) return [50, 50];
  if (points.length === 1) return points[0];
  const scaled = Math.max(0, Math.min(.999999, progress)) * (points.length - 1);
  const i = Math.floor(scaled), f = scaled - i;
  return [points[i][0] + (points[i + 1][0] - points[i][0]) * f,
          points[i][1] + (points[i + 1][1] - points[i][1]) * f];
}

function blockingSvgPath(points) {
  const p = (points || []).map(([x, y]) => [15 + x * 2.7, 13 + y * 1.38]);
  if (!p.length) return '';
  if (p.length === 1) return `M${p[0][0]},${p[0][1]} l.01,.01`;
  let d = `M${p[0][0]},${p[0][1]}`;
  for (let i = 1; i < p.length - 1; i++) {
    const mid = [(p[i][0] + p[i + 1][0]) / 2, (p[i][1] + p[i + 1][1]) / 2];
    d += ` Q${p[i][0]},${p[i][1]} ${mid[0]},${mid[1]}`;
  }
  const last = p.at(-1), prior = p.at(-2);
  d += ` Q${prior[0]},${prior[1]} ${last[0]},${last[1]}`;
  return d;
}

function renderBlockingPreview() {
  if (!selected || selected.track.type !== 'choreography') return;
  const blocking = blockingFor(selected.item, true);
  els.blockingPreview.innerHTML = '';
  const grid = document.createElementNS(SVG_NS, 'path');
  grid.setAttribute('class', 'stage-grid');
  grid.setAttribute('d', 'M15 151 Q150 123 285 151 M15 13 L15 151 M285 13 L285 151 M150 13 L150 151');
  els.blockingPreview.append(grid);
  for (const element of blocking.elements) {
    const path = document.createElementNS(SVG_NS, 'path');
    path.setAttribute('class', `motion-path${element.id === selectedBlockingElementId ? ' selected' : ''}`);
    path.setAttribute('d', blockingSvgPath(element.path));
    els.blockingPreview.append(path);
    const node = document.createElementNS(SVG_NS, 'g');
    node.setAttribute('class', `blocking-node${element.id === selectedBlockingElementId ? ' selected' : ''}`);
    node.dataset.elementId = element.id;
    node.dataset.layer = element.layer || 'midground';
    node.innerHTML = `${blockingKindMarkup[element.kind] || blockingKindMarkup.object}<text x="13" y="4">${escapeHtml(element.id)}</text>`;
    node.addEventListener('click', event => {
      event.stopPropagation(); selectedBlockingElementId = element.id; fillBlockingInspector();
    });
    els.blockingPreview.append(node);
  }
  updateBlockingProgress();
}

function updateBlockingProgress() {
  if (!selected || selected.track.type !== 'choreography') return;
  const blocking = blockingFor(selected.item);
  if (!blocking) return;
  const start = posToSec(selected.item.start || selected.item.at);
  const end = selected.item.end ? posToSec(selected.item.end) : start + 1;
  const progress = Math.max(0, Math.min(1, (currentTime - start) / Math.max(.001, end - start)));
  for (const element of blocking.elements) {
    const [x, y] = blockingPoint(element.path, progress);
    const node = els.blockingPreview.querySelector(`[data-element-id="${CSS.escape(element.id)}"]`);
    if (node) node.setAttribute('transform', `translate(${15 + x * 2.7} ${13 + y * 1.38})`);
  }
}

function fillBlockingInspector() {
  const isChoreography = selected?.track.type === 'choreography';
  els.choreographyFields.hidden = !isChoreography;
  els.blockingPanel.hidden = !isChoreography;
  if (!isChoreography) return;
  const blocking = blockingFor(selected.item, true);
  els.fieldRendererShot.value = blocking.rendererShot || '';
  els.fieldCamera.value = blocking.camera || '';
  els.fieldFormation.value = blocking.formation || '';
  els.fieldInteractions.value = formatInteractions(blocking.interactions);
  if (!blocking.elements.some(element => element.id === selectedBlockingElementId)) {
    selectedBlockingElementId = blocking.elements[0]?.id || null;
  }
  els.blockingElements.innerHTML = '';
  for (const element of blocking.elements) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = element.id === selectedBlockingElementId ? 'selected' : '';
    button.textContent = element.id;
    button.title = element.label || element.id;
    button.onclick = () => { selectedBlockingElementId = element.id; fillBlockingInspector(); };
    els.blockingElements.append(button);
  }
  const element = selectedBlockingElement();
  els.blockingElementForm.hidden = !element;
  if (element) {
    els.fieldElementId.value = element.id;
    els.fieldElementLabel.value = element.label || '';
    els.fieldElementKind.value = element.kind || 'object';
    els.fieldElementLayer.value = element.layer || 'midground';
    els.fieldElementEntrance.value = element.entrance || '';
    els.fieldElementAction.value = element.action || '';
    els.fieldElementExit.value = element.exit || '';
    els.fieldElementPath.value = formatMotionPath(element.path);
  }
  renderBlockingPreview();
}

function layoutLanes(items) {
  const lanes = [];
  return items.map(item => {
    const start = posToSec(item.start), end = item.end ? posToSec(item.end) : start + .05;
    let lane = lanes.findIndex(lastEnd => lastEnd <= start);
    if (lane < 0) lane = lanes.length;
    lanes[lane] = end;
    return {item, start, end, lane};
  });
}

function appendSelectionUnderlay(container) {
  if (!selected) return;
  const {track, item} = selected;
  const anchor = item.start || item.at;
  if (!anchor || item.timingStatus === 'unplaced') return;
  const start = posToSec(anchor);
  const end = item.end ? posToSec(item.end) : start;
  const underlay = document.createElement('div');
  underlay.className = 'selection-underlay';
  underlay.style.setProperty('--selection', track.color || '#b7ff5a');
  underlay.style.left = `${Math.max(0, start) * pxPerSec}px`;
  underlay.style.width = `${Math.max(2, (end - start) * pxPerSec)}px`;
  container.prepend(underlay);
}

function render() {
  const width = Math.ceil(duration * pxPerSec) + 80;
  els.timeline.style.width = `${width}px`;
  els.ruler.innerHTML = '';
  for (const bar of beatmap.bars) {
    const sec = +bar.beats[0];
    if (sec < 0 || sec > duration) continue;
    const mark = document.createElement('div');
    mark.className = `bar-mark ${bar.bar % 4 === 1 ? 'major' : ''}`;
    mark.style.left = `${sec * pxPerSec}px`;
    mark.textContent = `${bar.bar}`;
    els.ruler.append(mark);
  }
  for (let sec = 0; sec <= duration; sec += 10) {
    const mark = document.createElement('div');
    mark.className = 'second-mark'; mark.style.left = `${sec * pxPerSec}px`;
    mark.textContent = fmtTime(sec).replace('.000', ''); els.ruler.append(mark);
  }

  els.tracks.innerHTML = '';
  els.labels.querySelectorAll('.track-label,.reference-label,.reference-header').forEach(n => n.remove());
  renderReferences(width);
  for (const track of timeline.tracks) {
    const timed = track.items.filter(i => i.timingStatus !== 'unplaced' && (i.start || i.at));
    timed.sort((a, b) => posToSec(a.start || a.at) - posToSec(b.start || b.at));
    const layouts = layoutLanes(timed);
    const laneCount = Math.max(1, ...layouts.map(x => x.lane + 1));
    const height = 18 + laneCount * 39;
    const row = document.createElement('div');
    row.className = 'track'; row.dataset.track = track.id;
    row.style.setProperty('--track-height', `${height}px`);
    row.style.height = `${height}px`;
    row.style.backgroundSize = `${Math.max(1, pxPerSec)}px 100%`;
    row.addEventListener('pointerdown', e => {
      if (e.target === row) seek((e.offsetX) / pxPerSec);
    });
    appendSelectionUnderlay(row);
    for (const {item, start, end, lane} of layouts) row.append(makeClip(track, item, start, end, lane));
    els.tracks.append(row);

    const label = document.createElement('div');
    label.className = 'track-label'; label.dataset.scrollLabel = 'true';
    label.style.setProperty('--track-height', `${height}px`);
    label.style.height = `${height}px`;
    label.innerHTML = `<strong style="color:${track.color || '#fff'}">${track.label}</strong><span>${track.type} · ${timed.length} placed</span>`;
    els.labels.append(label);
  }
  renderUnplaced();
  updatePlayhead();
}

function renderReferences(width) {
  const header = document.createElement('div');
  header.className = 'reference-header'; header.dataset.scrollLabel = 'true';
  header.innerHTML = `<span>AUDIO REFERENCES · ${waveforms.tracks.length}</span><button title="${referencesCollapsed ? 'Expand' : 'Collapse'} audio references">${referencesCollapsed ? '▸' : '▾'}</button>`;
  header.querySelector('button').onclick = () => {
    referencesCollapsed = !referencesCollapsed;
    localStorage.setItem('referenceWaveformsCollapsed', String(referencesCollapsed));
    render();
  };
  els.labels.append(header);
  const strip = document.createElement('div'); strip.className = 'reference-strip-head';
  appendSelectionUnderlay(strip);
  els.tracks.append(strip);
  if (referencesCollapsed) return;
  for (const waveform of waveforms.tracks) {
    const label = document.createElement('div');
    label.className = 'reference-label'; label.dataset.scrollLabel = 'true';
    label.innerHTML = `<strong style="color:${waveform.color}">${escapeHtml(waveform.label)}</strong><span>${escapeHtml(waveform.role || 'timing reference')}</span>`;
    els.labels.append(label);
    const row = document.createElement('div');
    row.className = 'reference-track'; row.dataset.reference = waveform.id;
    row.title = `${waveform.label} · silent visual reference · ${waveform.role}`;
    row.addEventListener('pointerdown', e => seek(e.offsetX / pxPerSec));
    appendSelectionUnderlay(row);
    const canvas = document.createElement('canvas');
    canvas.width = width; canvas.height = 54; row.append(canvas); els.tracks.append(row);
    drawWaveform(canvas, waveform);
  }
}

function drawWaveform(canvas, waveform) {
  const g = canvas.getContext('2d'), h = canvas.height, mid = h / 2;
  const startX = Math.round(waveform.offsetSec * pxPerSec);
  const endX = Math.min(canvas.width, Math.ceil((waveform.offsetSec + waveform.durationSec) * pxPerSec));
  g.clearRect(0, 0, canvas.width, h);
  g.fillStyle = `${waveform.color}12`; g.fillRect(Math.max(0, startX), 0, Math.max(0, endX - startX), h);
  g.strokeStyle = `${waveform.color}88`; g.lineWidth = 1;
  g.beginPath();
  for (let x = Math.max(0, startX); x < endX; x++) {
    const sec = x / pxPerSec - waveform.offsetSec;
    const index = Math.max(0, Math.min(waveform.peak.length - 1, Math.floor(sec * waveform.rate)));
    const amp = waveform.peak[index] || 0;
    g.moveTo(x + .5, mid - amp * (mid - 3)); g.lineTo(x + .5, mid + amp * (mid - 3));
  }
  g.stroke();
  g.strokeStyle = waveform.color; g.lineWidth = 1.35; g.beginPath();
  for (let x = Math.max(0, startX); x < endX; x++) {
    const sec = x / pxPerSec - waveform.offsetSec;
    const index = Math.max(0, Math.min(waveform.rms.length - 1, Math.floor(sec * waveform.rate)));
    const y = mid - (waveform.rms[index] || 0) * (mid - 4);
    if (x === Math.max(0, startX)) g.moveTo(x, y); else g.lineTo(x, y);
  }
  g.stroke();
}

function makeClip(track, item, start, end, lane) {
  const el = document.createElement('div');
  const improv = track.type === 'lyrics' && item.lyricOrigin === 'improv';
  el.className = `clip ${selected?.item === item ? 'selected' : ''} ${item.ai?.status === 'suggestion' ? 'suggestion' : ''} ${improv ? 'improv' : ''}`;
  el.tabIndex = -1;
  el.style.setProperty('--clip', track.color || '#8ea1c9');
  el.style.left = `${Math.max(0, start) * pxPerSec}px`;
  el.style.width = `${Math.max(4, (end - start) * pxPerSec)}px`;
  el.style.top = `${9 + lane * 39}px`;
  el.title = `${itemLabel(item)}\n${item.start || item.at} → ${item.end || 'cue'}${improv ? '\nIMPROV · not on lyric sheet' : ''}\nShift+←/→ · previous/next in track`;
  el.textContent = `${improv ? 'IMPROV · ' : ''}${itemLabel(item)}`;
  if (item.end) {
    const hs = document.createElement('span'), he = document.createElement('span');
    hs.className = 'handle start'; he.className = 'handle end'; el.append(hs, he);
  }
  el.addEventListener('click', e => { e.stopPropagation(); select(track, item); });
  el.addEventListener('pointerdown', e => beginDrag(e, track, item, e.target.classList.contains('start') ? 'start' : e.target.classList.contains('end') ? 'end' : 'move'));
  return el;
}

function beginDrag(e, track, item, mode) {
  e.preventDefault(); e.stopPropagation();
  const x0 = e.clientX, start0 = posToSec(item.start || item.at), end0 = item.end ? posToSec(item.end) : start0;
  if (selected?.item !== item) {
    selected = {track, item};
    render(); fillInspector();
  }
  const move = ev => {
    const dt = (ev.clientX - x0) / pxPerSec;
    if (mode === 'move') {
      const len = end0 - start0, s = snapSec(Math.max(0, start0 + dt));
      item.start = s.pos;
      if (item.end) item.end = secToPos(Math.min(duration, s.sec + len));
    } else if (mode === 'start') {
      item.start = snapSec(Math.min(end0 - .01, start0 + dt)).pos;
    } else {
      item.end = snapSec(Math.max(start0 + .01, end0 + dt)).pos;
    }
    render(); fillInspector(); markDirty();
  };
  const up = () => { window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up); };
  window.addEventListener('pointermove', move); window.addEventListener('pointerup', up);
}

function select(track, item) {
  if (selected?.item !== item) selectedBlockingElementId = null;
  selected = {track, item}; render(); fillInspector();
  focusSelectedClip();
}

function focusSelectedClip(reveal = false) {
  const clip = els.tracks.querySelector('.clip.selected');
  if (!clip) return;
  if (reveal) clip.scrollIntoView({block: 'nearest', inline: 'nearest'});
  clip.focus({preventScroll: true});
}

function selectAdjacentClip(direction) {
  if (!selected) return;
  const {track, item} = selected;
  const placed = track.items
    .filter(candidate => candidate.timingStatus !== 'unplaced' && (candidate.start || candidate.at))
    .sort((a, b) => posToSec(a.start || a.at) - posToSec(b.start || b.at));
  const index = placed.indexOf(item), next = placed[index + direction];
  if (!next) return;
  selected = {track, item: next};
  render(); fillInspector(); focusSelectedClip(true);
}

function openDeleteDialog() {
  if (!selected || els.deleteDialog.open) return;
  els.deleteMessage.textContent = `Remove “${itemLabel(selected.item)}” from ${selected.track.label}?`;
  els.deleteInput.value = '';
  els.deleteCommit.disabled = true;
  els.deleteDialog.showModal();
  els.deleteInput.focus();
}

function closeDeleteDialog() {
  if (els.deleteDialog.open) els.deleteDialog.close();
  els.deleteInput.value = '';
  els.deleteCommit.disabled = true;
  focusSelectedClip();
}

function commitSelectedDelete() {
  if (!selected) return closeDeleteDialog();
  const {track, item} = selected, label = itemLabel(item);
  track.items = track.items.filter(candidate => candidate !== item);
  els.deleteDialog.close();
  selected = null;
  render(); fillInspector();
  markDirty(`Deleted “${label}” · save register to commit`);
}

function resolveDeleteConfirmation() {
  if (els.deleteInput.value.trim().toLowerCase() === 'delete') commitSelectedDelete();
  else closeDeleteDialog();
}

function fillInspector() {
  if (!selected) {
    els.empty.hidden = false; els.form.hidden = true; els.del.hidden = true;
    els.choreographyFields.hidden = true; els.blockingPanel.hidden = true; return;
  }
  const {item} = selected;
  els.empty.hidden = true; els.form.hidden = false; els.del.hidden = false;
  els.fieldId.value = item.id;
  els.fieldText.value = item.text || item.prompt || '';
  els.fieldStart.value = item.start || item.at || '';
  els.fieldEnd.value = item.end || '';
  els.fieldDrivers.value = (item.drivers || []).join(', ');
  els.fieldMetaphors.value = (item.metaphors || []).join(', ');
  els.fieldAi.value = item.ai?.note || '';
  els.fieldImprovRow.hidden = selected.track.type !== 'lyrics';
  els.fieldImprov.checked = selected.track.type === 'lyrics' && item.lyricOrigin === 'improv';
  els.fieldSuggestion.checked = item.ai?.status === 'suggestion';
  fillBlockingInspector();
}

function applyInspector() {
  if (!selected) return;
  const {track, item} = selected;
  const text = els.fieldText.value.trim();
  if (track.type === 'scene' || track.type === 'choreography' || track.type === 'transition') item.prompt = text;
  else item.text = text;
  if (els.fieldStart.value.trim()) {
    posToSec(els.fieldStart.value.trim()); item.start = els.fieldStart.value.trim(); delete item.at;
    item.timingStatus = 'placed';
  }
  if (els.fieldEnd.value.trim()) { posToSec(els.fieldEnd.value.trim()); item.end = els.fieldEnd.value.trim(); }
  else delete item.end;
  item.drivers = els.fieldDrivers.value.split(',').map(x => x.trim()).filter(Boolean);
  if (track.type === 'choreography') {
    item.metaphors = els.fieldMetaphors.value.split(',').map(x => x.trim()).filter(Boolean);
    const blocking = blockingFor(item, true);
    if (els.fieldRendererShot.value) blocking.rendererShot = els.fieldRendererShot.value;
    else delete blocking.rendererShot;
    blocking.camera = els.fieldCamera.value.trim();
    blocking.formation = els.fieldFormation.value.trim();
    blocking.interactions = parseInteractions(els.fieldInteractions.value);
    const element = selectedBlockingElement();
    if (element) {
      const nextId = els.fieldElementId.value.trim();
      if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(nextId)) {
        throw new Error('Element ID uses lowercase words separated by hyphens');
      }
      if (blocking.elements.some(candidate => candidate !== element && candidate.id === nextId)) {
        throw new Error(`Element ID “${nextId}” already exists in this cue`);
      }
      element.id = nextId;
      selectedBlockingElementId = nextId;
      element.label = els.fieldElementLabel.value.trim();
      element.kind = els.fieldElementKind.value;
      element.layer = els.fieldElementLayer.value;
      element.entrance = els.fieldElementEntrance.value.trim();
      element.action = els.fieldElementAction.value.trim();
      element.exit = els.fieldElementExit.value.trim();
      element.path = parseMotionPath(els.fieldElementPath.value);
    }
  }
  if (track.type === 'lyrics' && els.fieldImprov.checked) item.lyricOrigin = 'improv';
  else delete item.lyricOrigin;
  item.ai = {status: els.fieldSuggestion.checked ? 'suggestion' : 'accepted', note: els.fieldAi.value.trim()};
  render();
  if (track.type === 'choreography') fillBlockingInspector();
  markDirty();
}

function renderUnplaced() {
  els.unplaced.innerHTML = '';
  const items = allItems().filter(x => x.item.timingStatus === 'unplaced');
  els.unplacedCount.textContent = items.length;
  for (const {track, item} of items) {
    const b = document.createElement('button'); b.className = 'unplaced-item';
    b.innerHTML = `${escapeHtml(itemLabel(item))}<small style="color:${track.color}">${track.label} · place at ${secToPos(currentTime)}</small>`;
    b.onclick = () => place(track, item); els.unplaced.append(b);
  }
}

function place(track, item) {
  const start = snapSec(currentTime), p = parsePos(start.pos), next = byBar.get(p.bar + 1);
  item.start = start.pos;
  item.end = next ? `${p.bar + 1}.${p.beat}` : secToPos(Math.min(duration, start.sec + 2));
  item.timingStatus = 'placed'; select(track, item); markDirty('Cue placed — resize or edit, then save');
}

function addItem(kind) {
  const improv = kind === 'lyrics-improv';
  const type = improv ? 'lyrics' : kind;
  const track = timeline.tracks.find(t => t.type === type);
  if (!track) return;
  const id = `${type}-${Date.now().toString(36)}`;
  const start = snapSec(currentTime), p = parsePos(start.pos), next = byBar.get(p.bar + 1);
  const item = {id, start: start.pos, end: next ? `${p.bar + 1}.${p.beat}` : secToPos(Math.min(duration, start.sec + 2)),
                timingStatus: 'placed', drivers: [], ai: {status: 'accepted', note: ''}};
  if (type === 'lyrics') {
    item.text = improv ? 'New improv lyric' : 'New lyric';
    if (improv) item.lyricOrigin = 'improv';
  } else if (type === 'notes') item.text = 'New note';
  else item.prompt = `New ${type} direction`;
  if (type === 'choreography') {
    item.blocking = {camera: '', formation: '', elements: [], interactions: []};
  }
  track.items.push(item); select(track, item); markDirty();
  if (improv) { els.fieldText.focus(); els.fieldText.select(); }
}

function addBlockingElement() {
  if (!selected || selected.track.type !== 'choreography') return;
  const blocking = blockingFor(selected.item, true);
  let n = blocking.elements.length + 1, id = `vector-element-${n}`;
  while (blocking.elements.some(element => element.id === id)) id = `vector-element-${++n}`;
  blocking.elements.push({
    id, kind: 'object', layer: 'midground', label: 'New vector element',
    entrance: 'Appears at cue start', action: 'Holds its authored motion path',
    exit: 'Clears by cue end', path: [[10, 60], [50, 40], [90, 60]],
  });
  selectedBlockingElementId = id;
  fillBlockingInspector();
  markDirty('Vector element added — name and choreograph it, then save');
  els.fieldElementLabel.focus(); els.fieldElementLabel.select();
}

function escapeHtml(s) {
  const d = document.createElement('div'); d.textContent = s; return d.innerHTML;
}

function seek(sec) {
  currentTime = Math.max(0, Math.min(duration, sec));
  if (Number.isFinite(els.audio.duration)) els.audio.currentTime = currentTime;
  updatePlayhead(); renderUnplaced();
}

function updatePlayhead() {
  els.playhead.style.left = `${currentTime * pxPerSec}px`;
  els.barClock.textContent = secToPos(currentTime);
  els.timeClock.textContent = fmtTime(currentTime);
  updateBlockingProgress();
}

function animate() {
  const playing = !els.audio.paused;
  if (playing) {
    currentTime = els.audio.currentTime;
    if (auditionEnd !== null && currentTime >= auditionEnd) {
      currentTime = auditionEnd;
      els.audio.pause();
      els.audio.currentTime = currentTime;
      auditionEnd = null;
      els.play.textContent = '▶';
    }
  }
  updatePlayhead();
  const x = currentTime * pxPerSec;
  // Follow playback, but never fight a paused editor who is scrolling to a
  // new location before placing the playhead.
  if (playing && (x < els.scroll.scrollLeft + 40 || x > els.scroll.scrollLeft + els.scroll.clientWidth - 60)) {
    els.scroll.scrollLeft = Math.max(0, x - els.scroll.clientWidth * .35);
  }
  raf = requestAnimationFrame(animate);
}

async function save() {
  try {
    // A focused text field may not have emitted `change` yet. Saving is an
    // explicit commit boundary, so always reconcile the visible inspector
    // into the register before serializing it.
    if (selected) applyInspector();
    setStatus('Saving…'); els.save.disabled = true;
    const response = await fetch('/api/timeline', {method: 'PUT', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(timeline)});
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error((result.errors || ['Save failed']).join('; '));
    dirty = false; setStatus(`Saved · ${new Date().toLocaleTimeString()}`);
  } catch (error) {
    els.save.disabled = false; setStatus(error.message, true);
  }
}

async function init() {
  try {
    const response = await fetch('/api/project');
    if (!response.ok) throw new Error(`Project API returned ${response.status}`);
    const data = await response.json();
    ({project, timeline, beatmap} = data); waveforms = data.waveforms || {tracks: []};
    duration = +beatmap.duration_sec; buildGrid();
    els.title.textContent = project.title;
    if (data.hasAudio) els.audio.src = '/api/audio'; else els.play.disabled = true;
    render(); fillInspector(); setStatus(`Register loaded · ${waveforms.tracks.length} audio references`); els.save.disabled = true;
    animate();
  } catch (error) { setStatus(error.message, true); }
}

async function togglePlayback() {
  auditionEnd = null;
  if (els.audio.paused) { els.audio.currentTime = currentTime; await els.audio.play(); els.play.textContent = '❚❚'; }
  else { els.audio.pause(); els.play.textContent = '▶'; }
}

async function auditionSelected() {
  if (!selected?.item?.end || selected.item.timingStatus === 'unplaced') {
    setStatus('Select a placed block with a start and end to audition');
    return;
  }
  const start = posToSec(selected.item.start || selected.item.at);
  const end = posToSec(selected.item.end);
  if (end <= start) throw new Error('The selected block must end after it starts');
  auditionEnd = end;
  currentTime = start;
  els.audio.currentTime = start;
  try {
    await els.audio.play();
    els.play.textContent = '❚❚';
  } catch (error) {
    auditionEnd = null;
    throw error;
  }
}

function isTextEditingTarget(target) {
  if (!(target instanceof Element)) return false;
  if (target.matches('textarea,[contenteditable="true"]')) return true;
  if (!target.matches('input')) return false;
  return !['button', 'checkbox', 'radio', 'range', 'submit', 'reset'].includes(target.type);
}

function isInteractiveControlTarget(target) {
  return target instanceof Element && !!target.closest('input,textarea,select,button,[contenteditable="true"]');
}

els.play.onclick = e => (e.shiftKey ? auditionSelected() : togglePlayback()).catch(error => setStatus(error.message, true));
document.addEventListener('keydown', e => {
  if (e.code === 'Delete' && selected && !els.deleteDialog.open && !isInteractiveControlTarget(e.target)) {
    e.preventDefault();
    openDeleteDialog();
    return;
  }
  const adjacentDirection = e.shiftKey && e.code === 'ArrowLeft' ? -1
    : e.shiftKey && e.code === 'ArrowRight' ? 1 : 0;
  if (adjacentDirection && selected && !isInteractiveControlTarget(e.target)) {
    e.preventDefault();
    selectAdjacentClip(adjacentDirection);
    return;
  }
  if (e.code !== 'Space' || e.repeat || isTextEditingTarget(e.target)) return;
  e.preventDefault();
  (e.shiftKey ? auditionSelected() : togglePlayback()).catch(error => setStatus(error.message, true));
});
els.audio.addEventListener('ended', () => { auditionEnd = null; els.play.textContent = '▶'; });
els.zoom.oninput = () => { pxPerSec = +els.zoom.value; render(); };
els.ruler.addEventListener('pointerdown', e => {
  // The ruler itself moves inside the scrolling viewport, so its bounding
  // rect already includes scrollLeft. Adding it again jumps too far ahead.
  seek((e.clientX - els.ruler.getBoundingClientRect().left) / pxPerSec);
});
els.scroll.addEventListener('scroll', () => els.labels.querySelectorAll('[data-scroll-label]').forEach(n => n.style.transform = `translateY(${-els.scroll.scrollTop}px)`));
els.save.onclick = save;
els.del.onclick = openDeleteDialog;
els.deleteInput.addEventListener('input', () => {
  els.deleteCommit.disabled = els.deleteInput.value.trim().toLowerCase() !== 'delete';
});
els.deleteInput.addEventListener('keydown', e => {
  if (e.key !== 'Enter' || e.isComposing) return;
  e.preventDefault();
  resolveDeleteConfirmation();
});
els.deleteForm.addEventListener('submit', e => { e.preventDefault(); resolveDeleteConfirmation(); });
els.deleteCancel.onclick = closeDeleteDialog;
els.deleteDialog.addEventListener('cancel', e => { e.preventDefault(); closeDeleteDialog(); });
for (const input of [els.fieldText, els.fieldStart, els.fieldEnd, els.fieldDrivers,
  els.fieldMetaphors, els.fieldRendererShot, els.fieldCamera, els.fieldFormation,
  els.fieldInteractions,
  els.fieldElementId, els.fieldElementLabel, els.fieldElementKind, els.fieldElementLayer,
  els.fieldElementEntrance, els.fieldElementAction, els.fieldElementExit,
  els.fieldElementPath, els.fieldAi, els.fieldImprov, els.fieldSuggestion]) {
  input.addEventListener('change', () => { try { applyInspector(); } catch (error) { setStatus(error.message, true); } });
}
els.form.addEventListener('keydown', e => {
  const editable = e.target.matches('textarea,input:not([type=checkbox]):not([readonly])');
  if (!editable || e.key !== 'Enter' || e.repeat || e.isComposing) return;
  if (e.shiftKey && e.target.matches('textarea')) return;
  e.preventDefault();
  try {
    applyInspector();
    if (e.target === els.fieldText) focusSelectedClip();
    else e.target.focus();
  } catch (error) { setStatus(error.message, true); }
});
document.querySelectorAll('[data-add]').forEach(b => b.onclick = () => addItem(b.dataset.add));
els.addBlockingElement.onclick = addBlockingElement;
window.addEventListener('beforeunload', e => { if (dirty) { e.preventDefault(); e.returnValue = ''; } });
init();
