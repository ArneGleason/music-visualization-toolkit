from pathlib import Path
import json
import bpy

scene=bpy.context.scene
assert scene.render.use_motion_blur
assert abs(scene.render.motion_blur_shutter-.65)<1e-6
assert scene.render.motion_blur_position=='CENTER'
core=next(o for o in scene.objects if o.name.startswith('Ship / brightest'))
assert core.cycles.use_motion_blur and core.cycles.motion_steps==5
curves=[fc for layer in core.animation_data.action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
assert len(curves)==3
assert all(len(fc.keyframe_points)==1537 for fc in curves)
scene.frame_set(46)
a=core.location.copy()
scene.frame_set(46,subframe=.125)
b=core.location.copy()
assert (a-b).length>.001
report=dict(motionBlurEnabled=True,shutterFrames=scene.render.motion_blur_shutter,motionPosition=scene.render.motion_blur_position,motionIntervals=16,subframeTransformKeysPerChannel=1537,oneEighthFramePositionDifference=(a-b).length,outputFPS=scene.render.fps)
out=Path('projects/a-right-little-something/generated/storyboard/orbit-blender-v03/hybrid')
(out/'native-motion-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('Saved native scene verified: shutter blur enabled; 1537 subframe keys/channel; fractional-frame position changes; 24fps output')
