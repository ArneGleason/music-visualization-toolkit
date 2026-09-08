"""Keep manual Blender rerenders inside each recipe's output directory."""
from pathlib import Path
import bpy
O=Path(__file__).resolve().parent
for family in ['aerial','probe','receiver','specimen']:
    for width in [1280,1920]:
        p=O/family/f'{family}_{width}.blend'
        if not p.is_file():continue
        bpy.ops.wm.open_mainfile(filepath=str(p))
        bpy.context.scene.render.filepath=str(O/family/f'native_{width}')+'/'
        bpy.ops.wm.save_as_mainfile(filepath=str(p))
