from pathlib import Path
import json,hashlib,subprocess,wave
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
assert not (OUT/'handoff.json').exists()
def ref(p):return {'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
lock=ROOT/'out/astronaut_reply_v1/style_lock_v2.txt'
assert ref(lock)['sha256']=='6db3e45d5777cb22ae1ee7da18b8bde8498caaffb8d96e8536f3414dea260496'
local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text());stems=list(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav'));assert len(stems)==1
jobs=[]
for name,origin,source,sha,anchor,cuts in [
 ('A3',4492,'out/outro_A2_v2/take1/base.mp4','8836ee224def240a37f4b00daa2770b52c37207142dd61f2c2262bf2864c7007',172,[(4504,4557,'Say goodnight'),(4574,4622,'Sung phrase'),(4644,4671,'Night')]),
 ('B3',4500,'out/outro_B2_v2/base.mp4','9a7056b689a77dd50fcc262540d04033c77bb6f271a899b131135ae6cca556f0',180,[(4557,4574,'To who (artifact insert planned)'),(4622,4644,'You first'),(4671,4689,'Night')])]:
    d=OUT/name;assert ref(ROOT/source)['sha256']==sha
    (d/'flow_prompt.txt').write_bytes((d/'direction.txt').read_bytes().rstrip()+b'\n\n'+lock.read_bytes())
    start=origin/24-.178348
    subprocess.run(['ffmpeg','-v','error','-n','-i',str(stems[0]),'-af',f'atrim=start={start}:duration=8,asetpts=PTS-STARTPTS','-ac','1','-ar','48000','-c:a','pcm_s16le',str(d/'guide.wav')],check=True)
    with wave.open(str(d/'guide.wav')) as w:assert (w.getnframes(),w.getframerate(),w.getnchannels())==(384000,48000,1)
    job={'take':name,'status':'ready_for_claude_not_submitted','inputs':{'first_frame':ref(d/'first_frame.png'),'prompt':ref(d/'flow_prompt.txt'),'guide':ref(d/'guide.wav'),'lock':ref(lock)},'anchor':{'source':ref(ROOT/source),'source_frame_at24':anchor,'song_frame':origin,'inspection':'Existing identity, room and prop state retained from unsynced base. No baked FX.'},'clock':{'fps':24,'indexing':'zero-based end-exclusive','song_origin':origin,'song_end_exclusive':origin+192,'requested_frames':192,'raw_stem_start_seconds':start,'stem_offset_applied_once_seconds':.178348,'additional_offset_seconds':0},'guide':'Continuous8seconds, mono48k PCM16,384000samples. Other speaker context retained, not isolated. No gating/normalization/shift. A3 and B3 have DIFFERENT origins: never interchange guides.','visible_cuts':[{'song':[a,b],'source':[a-origin,b-origin],'phrase':s} for a,b,s in cuts],'output':{'base':f'{d.relative_to(ROOT).as_posix()}/base.mp4','synced':f'{d.relative_to(ROOT).as_posix()}/synced.mp4','receipt':f'{d.relative_to(ROOT).as_posix()}/RECEIPT.md'},'authorization':{'flow':1,'kling':1,'kling_condition':'base passes visual review; material failure pause for owner, no automatic retry'},'coverage_note':'Record actual returned frames. B3 has only3 intended exit frames after last cut; do not promise full switch action after final word.'}
    (d/'handoff.json').write_text(json.dumps(job,indent=2)+'\n');jobs.append({'take':name,'manifest':str((d/'handoff.json').relative_to(ROOT)).replace('\\','/'),'status':'ready_for_claude_not_submitted'})
h={'status':'ready_for_claude_not_submitted','task':'Two closing performances, A3 then B3; at most one Flow and one gated Kling per take.','jobs':jobs,'authorization':{'max_flow_total':2,'max_kling_total':2,'no_automatic_retries':True,'no_other_generations':True},'settings':{'flow':'Veo3.1 Quality, Frames,16:9,720p,8seconds,x1; start frame only; no audio/end frame','kling':'Lip Sync, sole woman, own guide Local Dubbing0..8seconds at0:00, Sound from Video OFF'},'cost':'Expected100Flow+10Kling per take,220credits total maximum estimate. Check UI, stop if higher or unavailable. No purchases/upgrades.','polling':{'first_check_seconds':30,'interval_seconds':20,'near90percent_seconds':10,'count_tool_time':True,'respect_rate_limits':True,'no_exponential_backoff':True},'return':'Preserve originals and byte-identical base/synced; write per-take RECEIPT with hashes, native metadata/settings/costs/job IDs and review observations; add claude_result and completed status to each child. Parent done only after both complete. Do not modify old takes, assembly, FX, title, music or Git.'}
(OUT/'handoff.json').write_text(json.dumps(h,indent=2)+'\n')
print('A3/B3 guides verified, distinct origins4492/4500, original locks retained.')
