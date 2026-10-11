"""Inspect the saved model's structure and reusable rendering graph."""
import json
from pathlib import Path
import bpy

OUT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(OUT/'headquarters-ark-v04.blend'))
scene=bpy.context.scene
pods=sorted((o for o in scene.objects if o.name.startswith('POD_')),key=lambda o:o.name)
assert len(pods)==6
actual=sorted(tuple(round(v,3) for v in o.location) for o in pods)
expected=sorted((x,y,0) for x,offset in [(-6,4.7),(0,7.2),(6,4.7)] for y in [-offset,offset])
assert actual==expected,(actual,expected)
graph=scene.compositing_node_group
assert graph and any(n.type=='R_LAYERS' for n in graph.nodes)
assert not any(n.type=='IMAGE' for n in graph.nodes)
brush=next(n for n in graph.nodes if n.bl_idname=='CompositorNodeKuwahara')
mix=next(n for n in graph.nodes if n.bl_idname=='ShaderNodeMix')
assert brush.inputs['Type'].default_value=='Anisotropic'
assert brush.inputs['Size'].default_value==3
assert abs(mix.inputs[0].default_value-.35)<1e-6
external=[i.filepath for i in bpy.data.images if i.source=='FILE' and not i.packed_file]
assert not external,external
assert scene.render.engine=='CYCLES' and scene.cycles.samples==96
result=dict(podCount=len(pods),podCentres=actual,compositorUsesLiveRenderLayers=True,
    cachedImageNodes=False,externalTextures=external,renderEngine=scene.render.engine,
    samples=scene.cycles.samples,viewTransform=scene.view_settings.view_transform,
    look=scene.view_settings.look,exposure=scene.view_settings.exposure,
    brushRadiusPixels=brush.inputs['Size'].default_value,brushBlend=mix.inputs[0].default_value,
    objectCount=len(scene.objects),status='Passed saved-model structure and style graph inspection')
(OUT/'saved-model-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result),flush=True)
