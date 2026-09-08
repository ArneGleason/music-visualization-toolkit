from pathlib import Path
import json,subprocess,hashlib
O=Path(__file__).resolve().parent
receipts=[]
for family,count,ids in [('aerial',77,['opening_need_landscape']),('probe',192,['s009','s011'])]:
    D=O/family
    assert all((D/f'native_1280/{f:04d}.png').is_file() for f in range(1,count+1))
    clean=D/'native_clean.mp4'
    if not clean.exists():
        subprocess.run(['ffmpeg','-v','error','-n','-framerate','24','-start_number','1','-i',str(D/'native_1280/%04d.png'),'-frames:v',str(count),'-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(clean)],check=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(clean),'-f','null','-'],check=True)
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height,nb_frames,r_frame_rate','-of','json',str(clean)]))['streams']
    assert len(info)==1 and info[0]['nb_frames']==str(count) and info[0]['r_frame_rate']=='24/1'
    receipts.append({'family':family,'shot_ids':ids,'status':'native_candidate_rendered_not_promoted',
        'recipe':f'out/blender_migration_v1/{family}_native.py',
        'blend':f'out/blender_migration_v1/{family}/{family}_1280.blend',
        'clean':f'out/blender_migration_v1/{family}/native_clean.mp4',
        'frames':count,'fps':24,'audio':False,'sha256':hashlib.sha256(clean.read_bytes()).hexdigest(),
        'qa':json.loads((D/'qa.json').read_text()),
        'mapping':[[205,282,0,77]] if family=='aerial' else [[719,805,0,86],[856,911,137,192]]})
(O/'native_candidates.json').write_text(json.dumps(receipts,indent=2))
print('Both native candidates decoded and frame-count checked. No production replacements made.')
