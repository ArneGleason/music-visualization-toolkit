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
  fieldImprovRow: $('#fieldImprovRow'), fieldImprov: $('#fieldImprov'),
  fieldSuggestion: $('#fieldSuggestion'), deleteDialog: $('#deleteDialog'),
  deleteForm: $('#deleteForm'), deleteMessage: $('#deleteMessage'),
  deleteInput: $('#deleteConfirmInput'), deleteCancel: $('#deleteCancel'),
  deleteCommit: $('#deleteCommit')
};

let project, timeline, beatmap, waveforms = {tracks: []}, grid = [], byBar = new Map();
let pxPerSec = +els.zoom.value, duration = 0, currentTime = 0;
let selected = null, dirty = false, raf = 0, auditionEnd = null;
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
    els.empty.hidden = false; els.form.hidden = true; els.del.hidden = true; return;
  }
  const {item} = selected;
  els.empty.hidden = true; els.form.hidden = false; els.del.hidden = false;
  els.fieldId.value = item.id;
  els.fieldText.value = item.text || item.prompt || '';
  els.fieldStart.value = item.start || item.at || '';
  els.fieldEnd.value = item.end || '';
  els.fieldDrivers.value = (item.drivers || []).join(', ');
  els.fieldAi.value = item.ai?.note || '';
  els.fieldImprovRow.hidden = selected.track.type !== 'lyrics';
  els.fieldImprov.checked = selected.track.type === 'lyrics' && item.lyricOrigin === 'improv';
  els.fieldSuggestion.checked = item.ai?.status === 'suggestion';
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
  if (track.type === 'lyrics' && els.fieldImprov.checked) item.lyricOrigin = 'improv';
  else delete item.lyricOrigin;
  item.ai = {status: els.fieldSuggestion.checked ? 'suggestion' : 'accepted', note: els.fieldAi.value.trim()};
  render(); markDirty();
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
  track.items.push(item); select(track, item); markDirty();
  if (improv) { els.fieldText.focus(); els.fieldText.select(); }
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
for (const input of [els.fieldText, els.fieldStart, els.fieldEnd, els.fieldDrivers, els.fieldAi, els.fieldImprov, els.fieldSuggestion]) {
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
window.addEventListener('beforeunload', e => { if (dirty) { e.preventDefault(); e.returnValue = ''; } });
init();
