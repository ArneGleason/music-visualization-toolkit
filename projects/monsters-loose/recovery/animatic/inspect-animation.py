import bpy
bpy.ops.wm.open_mainfile(filepath=r'C:\audio\shared\amtw-runtime\jobs\monsters-loose-word-timing-20260913\animatic\MonstersLoose-scene-roughout-v04.blend')
s=bpy.context.scene
a=s.animation_data.action
print('ACTION',a)
for layer in a.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    if 'offset_y' in fc.data_path:
     print(fc.data_path, [(p.co[:]) for p in fc.keyframe_points][:8])
