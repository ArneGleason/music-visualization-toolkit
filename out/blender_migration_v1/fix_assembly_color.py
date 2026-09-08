import bpy
from pathlib import Path
O=Path(__file__).resolve().parent
s=bpy.data.scenes['RiversOfMars'];print('Previous view:',s.view_settings.view_transform,s.view_settings.look)
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
bpy.ops.wm.save_as_mainfile(filepath=str(O/'full_native_assembly.blend'))
s.frame_set(1542);s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG';s.render.filepath=str(O/'full_color_fixed.png');bpy.ops.render.render(write_still=True,scene=s.name)
