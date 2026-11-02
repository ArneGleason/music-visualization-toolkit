const $ = id => document.getElementById(id);

let config = await (await fetch('/api')).json();

const video = $('video'), still = $('still'), scrub = $('scrub');

let frame = 1, serial = 0, loading = false, starting = false, jumpDirty = false;

video.src = '/media?v=' + config.revision;

scrub.max = config.count;

$('name').textContent = config.name + ' · ' + config.fps + ' fps';

$('jump').min = config.masterStart;

$('jump').max = config.masterStart + config.count - 1;

function currentShotIndex() {
  const master = config.masterStart + frame - 1;
  return (config.shots || []).findIndex(s => s.startFrame <= master && master < s.endFrameExclusive);
}

function showShots() {
  const shots = config.shots || [];
  $('shot-nav').hidden = !shots.length;
  $('shot-select').replaceChildren();
  shots.forEach((shot, index) => {
    const option = document.createElement('option');
    option.value = index;
    const scene = shot.sceneId ? `Scene ${shot.sceneId.replace(/^S/, '')} · ${shot.sceneName} / ` : '';
    option.textContent = shot.mediaType === 'planning' ? shot.title : `${scene}Shot ${String(shot.shotNumber).padStart(2, '0')} · ${shot.title}`;
    $('shot-select').append(option);
  });
  shotCounters();
}

function shotCounters() {
  const index = currentShotIndex();
  $('shot-select').value = index < 0 ? '' : String(index);
  $('previous-shot').disabled = index <= 0;
  $('next-shot').disabled = index < 0 || index >= (config.shots || []).length - 1;
  const shot = (config.shots || [])[index];
  $('shot-timing').hidden = !shot;
  if (shot) {
    const frames = shot.endFrameExclusive - shot.startFrame;
    $('shot-duration').textContent = `Play length: ${(frames / config.fps).toFixed(3)}s · ${frames} frames`;
    $('source-start').textContent = shot.mediaType === 'video' && shot.sourceInFrame != null
      ? `Clip start: ${(shot.sourceInFrame / (shot.sourceFps || config.fps)).toFixed(3)}s · frame ${shot.sourceInFrame}`
      : shot.mediaType === 'planning' ? 'Lyrics on black · scenes not planned' : 'Clip start: — (still image)';
  }
}

function seekShot(index) {
  const shot = (config.shots || [])[index];
  if (shot) seek(shot.startFrame - config.masterStart + 1);
}

showShots();
$('previous-shot').onclick = () => seekShot(currentShotIndex() - 1);
$('next-shot').onclick = () => seekShot(currentShotIndex() + 1);
$('shot-select').onchange = () => seekShot(Number($('shot-select').value));

function lyricTime(master) {
  const seconds = (master - (config.masterFrameBase ?? 1)) / config.fps;
  return Math.floor(seconds / 60) + ':' + (seconds % 60).toFixed(3).padStart(6, '0');
}

function activeLyric() {
  const master = config.masterStart + frame - 1;
  return (config.lyrics || []).find(line => line.startFrame <= master && master < line.endFrameExclusive);
}

function adjacentLyric(direction) {
  const master = config.masterStart + frame - 1, lines = config.lyrics || [];
  const active = activeLyric();
  return direction < 0
    ? [...lines].reverse().find(line => line.startFrame < (active ? active.startFrame : master))
    : lines.find(line => line.startFrame > master);
}

function seekLyric(line) {
  if (line) seek(line.startFrame - config.masterStart + 1);
}

function lyricCounters() {
  const line = activeLyric(), previous = adjacentLyric(-1), next = adjacentLyric(1);
  $('lyric-select').value = line ? line.label : '';
  $('previous-lyric').disabled = !previous;
  $('next-lyric').disabled = !next;
  $('lyric-context').textContent = line
    ? `${line.label} · ${lyricTime(line.startFrame)} · master frame ${line.startFrame} · length ${((line.endFrameExclusive - line.startFrame) / config.fps).toFixed(3)}s`
    : config.lyricError ? `Lyric index unavailable: ${config.lyricError}`
    : (config.lyrics || []).length ? `Instrumental / lyric gap${previous ? ' · after ' + previous.label : ''}${next ? ' · next ' + next.label + ' at ' + lyricTime(next.startFrame) : ''}` : '';
}

function showLyrics() {
  const lines = config.lyrics || [];
  $('lyric-nav').hidden = !lines.length;
  const gap = document.createElement('option');
  gap.value = ''; gap.textContent = '— Instrumental / between lyric lines —'; gap.disabled = true;
  $('lyric-select').replaceChildren(gap);
  for (const line of lines) {
    const option = document.createElement('option');
    option.value = line.label;
    option.textContent = `${line.label} · ${lyricTime(line.startFrame)} · ${line.text}`;
    $('lyric-select').append(option);
  }
  lyricCounters();
}
showLyrics();
$('previous-lyric').onclick = () => seekLyric(adjacentLyric(-1));
$('next-lyric').onclick = () => seekLyric(adjacentLyric(1));
$('lyric-select').onchange = () => seekLyric((config.lyrics || []).find(line => line.label === $('lyric-select').value));

function reference() {

  return config.name + ' — master frame ' + (config.masterStart + frame - 1) +

    ', preview frame ' + frame + ', ' + config.fps + ' fps' +
    (activeLyric() ? ` · ${activeLyric().label}: ${activeLyric().text}` : ' · lyric gap / instrumental');

}

function counters() {

  const master = config.masterStart + frame - 1;

  $('master').textContent = 'Master ' + master;

  $('preview').textContent = 'Preview ' + frame + ' / ' + config.count;

  const seconds = (master - (config.masterFrameBase ?? 1)) / config.fps;

  $('time').textContent = Math.floor(seconds / 60) + ':' + (seconds % 60).toFixed(3).padStart(6, '0');

  scrub.value = frame;
  if (!jumpDirty) $('jump').value = master;
  shotCounters();
  lyricCounters();

}

function mediaReady(test, events) {
  if (test()) return Promise.resolve();
  return new Promise((resolve, reject) => {
    const cleanup = () => {
      clearTimeout(timer);
      events.forEach(event => video.removeEventListener(event, check));
      video.removeEventListener('error', failed);
    };
    const check = () => { if (test()) { cleanup(); resolve(); } };
    const failed = () => { cleanup(); reject(new Error('Media not ready')); };
    const timer = setTimeout(failed, 6000);
    events.forEach(event => video.addEventListener(event, check));
    video.addEventListener('error', failed);
  });
}

async function seek(target) {
  const ticket = ++serial;
  starting = false;
  video.pause(); $('play').textContent = 'Play';
  frame = Math.max(1, Math.min(config.count, Math.round(target)));
  if (!Number.isFinite(frame)) frame = 1;
  counters();
  loading = true; $('mark').disabled = true;
  $('status').textContent = 'Loading exact frame…';
  // Keep decoder seeks separate from the exact still: stale completions may
  // never move the playhead or cover a newly started video.
  mediaReady(() => video.readyState >= 1, ['loadedmetadata']).then(() => {
    if (ticket === serial) video.currentTime = (frame - 1 + 0.25) / config.fps;
  }).catch(() => {});
  const image = new Image();
  image.src = '/frame?n=' + frame + '&v=' + config.revision;
  try {
    await image.decode();
    if (ticket !== serial) return;
    still.src = image.src; still.hidden = false;
    $('status').textContent = 'Paused on exact frame ' + frame;
  } catch {
    if (ticket === serial) $('status').textContent = 'Could not decode frame. Try stepping again.';
  } finally {
    if (ticket === serial) { loading = false; $('mark').disabled = false; }
  }
}

async function toggle() {
  if (starting || !video.paused) { await seek(frame); return; }
  const ticket = ++serial;
  starting = true; loading = false; $('mark').disabled = false;
  $('play').textContent = 'Pause'; $('status').textContent = 'Starting playback…';
  // Play at the end means replay, including after a pending ended event.
  if (frame >= config.count) { frame = 1; counters(); }
  try {
    if (video.error) video.load();
    await mediaReady(() => video.readyState >= 1, ['loadedmetadata']);
    if (ticket !== serial) return;
    video.currentTime = (frame - 1) / config.fps;
    await mediaReady(() => !video.seeking && video.readyState >= 2, ['seeked', 'loadeddata', 'canplay']);
    if (ticket !== serial) return;
    await video.play();
    if (ticket !== serial) return;
    starting = false; still.hidden = true;
    $('status').textContent = 'Playing — pause to choose an exact frame';
  } catch {
    if (ticket !== serial) return;
    starting = false; video.pause(); $('play').textContent = 'Play';
    $('status').textContent = 'Playback could not start. Press Play to retry.';
    // Recover the decoder without reloading the page or losing notes.
    video.load();
  }
}

function displayed(_, metadata) {

  if (!video.paused && !video.seeking && !starting && Math.abs(metadata.mediaTime - video.currentTime) < 0.2) {

    frame = Math.min(config.count, Math.floor(metadata.mediaTime * config.fps + 0.001) + 1);

    counters();

  }

  video.requestVideoFrameCallback(displayed);

}

if (video.requestVideoFrameCallback) video.requestVideoFrameCallback(displayed);

else video.addEventListener('timeupdate', () => {

  if (!video.paused) { frame = Math.floor(video.currentTime * config.fps) + 1; counters(); }

});

video.addEventListener('ended', () => {
  if (video.ended && !starting && !video.seeking) seek(config.count);
});

$('play').onclick = toggle;

$('back').onclick = () => seek(frame - 1);

$('next').onclick = () => seek(frame + 1);

scrub.oninput = () => seek(Number(scrub.value));

$('jump').oninput = () => { jumpDirty = true; };
$('go').onclick = () => {
  const target = Number($('jump').value) - config.masterStart + 1;
  jumpDirty = false;
  seek(target);
};

$('jump').onkeydown = e => { if (e.key === 'Enter') $('go').click(); };

$('speed').onchange = () => video.playbackRate = Number($('speed').value);

document.addEventListener('keydown', e => {

  if (e.target.matches('input:not([type=range]),textarea,select,[contenteditable=true]')) return;

  if (e.code === 'Space') { e.preventDefault(); if (!e.repeat) toggle(); }

  if (e.key === '[' || e.key === ']') {
    e.preventDefault(); seekShot(currentShotIndex() + (e.key === '[' ? -1 : 1));
  }

  if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {

    e.preventDefault(); seek(frame + (e.key === 'ArrowLeft' ? -1 : 1) * (e.shiftKey ? 10 : 1));

  }

});

$('copy').onclick = async () => {

  await navigator.clipboard.writeText(reference()); $('status').textContent = 'Copied: ' + reference();

};

function showMarks(notes) {

  $('marks').replaceChildren();

  for (const note of notes.filter(n => n.video === config.name)) {

    const li = document.createElement('li'), b = document.createElement('button'), text = document.createElement('span');

    b.textContent = 'Master ' + note.master_frame;

    b.onclick = () => seek(note.preview_frame);

    text.textContent = (note.lyric ? `${note.lyric.label} · ${note.lyric.text} — ` : '') + (note.text || 'Marked frame'); li.append(b, text); $('marks').append(li);

  }

}

$('mark').onclick = async () => {

  if (!video.paused) await seek(frame);

  if (loading) return;

  const res = await fetch('/notes', {method:'POST', headers:{'Content-Type':'application/json'},

    body:JSON.stringify({frame, revision:config.revision, text:$('note').value})});

  if (!res.ok) { $('status').textContent = 'Save failed; your note is still in the input.'; return; }

  showMarks(await res.json()); $('note').value = ''; $('status').textContent = 'Saved: ' + reference();

};

showMarks(config.notes);

const requested = Number(new URLSearchParams(location.search).get('frame'));

seek(requested > 0 ? requested - config.masterStart + 1 : 1);

// Keep one review address. Adopt the next completed render while paused,

// preserving the master playhead. Never discard a note being typed.

setInterval(async () => {

  try {

    const next = await (await fetch('/api')).json();

    if (next.revision === config.revision) {
      if (next.shotRevision !== config.shotRevision) {
        config.shots = next.shots; config.shotRevision = next.shotRevision;
        showShots();
      }
      if (next.lyricRevision !== config.lyricRevision) {
        config.lyrics = next.lyrics; config.lyricRevision = next.lyricRevision;
        config.lyricError = next.lyricError; showLyrics();
      }
      return;
    }

    if (starting || !video.paused || $('note').value) {

      $('status').textContent = 'Updated render ready — pause and save your note to load it.';

      return;

    }

    const master = config.masterStart + frame - 1;

    config = next;
    showShots();
    showLyrics();

    scrub.max = config.count;

    $('jump').min = config.masterStart;

    $('jump').max = config.masterStart + config.count - 1;

    $('name').textContent = config.name + ' · ' + config.fps + ' fps';

    video.src = '/media?v=' + config.revision;

    video.load();

    showMarks(config.notes);

    await seek(master - config.masterStart + 1);

  } catch { /* Keep the current review usable during a server restart. */ }

}, 3000);
