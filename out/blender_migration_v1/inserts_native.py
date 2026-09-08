"""Native normalized reframing of original source, no baked crop inputs."""
from pathlib import Path
O=Path(__file__).resolve().parent
prefix=(O/'lights2_native.py').read_text().split("if family=='receiver':",1)[0]
exec(compile(prefix,str(O/'lights2_native.py'),'exec'))
cx,cy,cw,ch=data['crop_xywh'];iw,ih=data['source_dimensions']
coords=b.combine([(cx+x/1280*cw)/iw,1-(cy+y/720*ch)/ih,0]);b.plug(coords,tex.inputs['Vector'])
em=b.n.new('ShaderNodeEmission');b.plug(tex.outputs[0],em.inputs[0]);mo=b.n.new('ShaderNodeOutputMaterial');b.plug(em.outputs[0],mo.inputs[0])
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.filepath=str(out)+'/'
bpy.ops.wm.save_as_mainfile(filepath=str(D/f'{family}_{W}.blend'))
for f in frames:s.frame_set(f);s.render.filepath=str(out/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
