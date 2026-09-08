"""Inspect saved native scenes, not just the Python recipes that built them."""
from pathlib import Path
import bpy,json
O=Path(__file__).resolve().parent
families=['opening','birds','guide','bloom','pressure','swim043','swim044','swim047','tunnel','titles','pieces','meant']
records=[]
for family in families:
    for width in [1280,1920]:
        path=O/family/f'{family}_{width}.blend'
        if not path.exists():continue
        bpy.ops.wm.open_mainfile(filepath=str(path))
        s=bpy.context.scene;images=[];errors=[]
        for image in bpy.data.images:
            if image.source not in {'FILE','SEQUENCE','MOVIE'}:continue
            p=Path(bpy.path.abspath(image.filepath)).resolve()
            # This batch must depend only on the extracted untreated source plate.
            if family=='titles' or not p.is_relative_to((O/family/'plates').resolve()):errors.append('Unexpected image dependency: '+str(p))
            if not p.exists():errors.append('Missing original plate: '+str(p))
            images.append({'path':str(p),'source':image.source})
        if (s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage)!=(width,width*9//16,100):errors.append('Resolution mismatch')
        if s.render.fps!=24 or s.render.fps_base!=1:errors.append('Timebase mismatch')
        if not Path(s.render.filepath).resolve().is_relative_to(O.resolve()):errors.append('Output outside migration folder')
        if any(i.source=='GENERATED' and i.name not in {'Render Result','Viewer Node'} for i in bpy.data.images):errors.append('Generated image buffer needs manual dependency audit')
        text=[o.data.body for o in s.objects if o.type=='FONT']
        if family=='titles':
            for expected in ['RIVERS OF MARS','Human imagination and direction, AI-assisted craft','Arne Gleason · Human']:
                if expected not in text:errors.append('Title copy missing: '+expected)
        records.append({'family':family,'width':width,'blend':str(path),'frame_range':[s.frame_start,s.frame_end],'images':images,'objects':len(s.objects),'text':text,'errors':errors,'status':'dependency_check_pass' if not errors else 'manual_review_required'})
(O/'batch3_blend_audit.json').write_text(json.dumps(records,indent=2))
print(json.dumps({'checked':len(records),'errors':[r for r in records if r['errors']]},indent=2))
