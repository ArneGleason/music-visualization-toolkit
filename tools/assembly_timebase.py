"""Time-preserving silent CFR copies for Blender's frame-based movie strips."""
import hashlib
import json
import pathlib
import subprocess
from assembly_sources import inspect_video


def conform_clip(root, clip, fps, prepare=False):
    fps = float(fps)  # 24 and 24.0 must resolve the same conversion cache.
    result = dict(clip)
    if not result.get('file'):
        return result
    if result.get('speed', 1) != 1:
        raise ValueError('Blender requires explicit timebase handling for non-unit speed')
    source = (pathlib.Path(root)/result['file']).resolve()
    rate, frames = inspect_video(str(source))
    if abs(rate-fps) < 1e-6:
        return result
    stat = source.stat()
    identity = json.dumps([str(source),stat.st_size,stat.st_mtime_ns,fps,'cfr-v1'])
    key = hashlib.sha256(identity.encode()).hexdigest()[:20]
    target = pathlib.Path(root)/'out/assembly_cfr'/f'{source.stem}_{key}.mp4'
    expected = round(frames/rate*fps)
    if not target.exists():
        if not prepare:
            raise ValueError(f'Missing time-preserving {fps} fps proxy for {source.name}; '
                             'run assembly_preflight.py --prepare-timebase')
        target.parent.mkdir(parents=True,exist_ok=True)
        temporary = target.with_suffix('.partial.mp4')
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(source),'-map','0:v:0',
            '-vf',f'setpts=PTS-STARTPTS,fps={fps}', '-frames:v',str(expected),
            '-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p',
            '-an','-movflags','+faststart',str(temporary)],check=True)
        actual_rate, actual_frames = inspect_video(str(temporary))
        if actual_rate != fps or actual_frames != expected:
            raise ValueError('CFR conversion failed frame validation')
        temporary.replace(target)
        target.with_suffix('.json').write_text(json.dumps({
            'original':str(source),'source_fps':rate,'source_frames':frames,
            'fps':fps,'frames':expected,'method':'timestamp resampling, no speed change',
            'duration_rounding_seconds':expected/fps-frames/rate,
            'audio':False,'source_identity':json.loads(identity)},indent=2))
    actual_rate, actual_frames = inspect_video(str(target))
    if actual_rate != fps or actual_frames != expected:
        raise ValueError(f'Invalid CFR cache: {target}')
    result['file'] = str(target.resolve())
    result['timebase_original'] = str(source)
    return result
