import bpy
n=bpy.data.node_groups.new('P','CompositorNodeTree').nodes.new('CompositorNodeDBlur')
for name in ['Amount','Direction']:
 s=n.inputs[name];p=s.bl_rna.properties['default_value'];print(name,p.subtype,p.hard_min,p.hard_max,p.soft_min,p.soft_max,s.description)
