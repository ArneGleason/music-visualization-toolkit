"""Render disjoint frame ranges from an already saved native scene."""
import bpy,sys
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:]; destination=Path(args[0]); first,last=map(int,args[1:3]); destination.mkdir(exist_ok=True)
for f in range(first,last):
    scene=bpy.context.scene; scene.frame_set(f)
    # Keep layers enabled: disabled layers can leave object animation unevaluated.
    for layer in scene.view_layers:layer.use=True
    scene.render.filepath=str(destination/f'{f:04d}.png'); bpy.ops.render.render(write_still=True)
