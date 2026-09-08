"""Native, resolution-independent closing card. Run with Blender --background --python."""
from pathlib import Path
import bpy, math

OUT = Path(__file__).resolve().parent
(OUT / 'frames').mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
s = bpy.context.scene
s.render.engine = 'CYCLES'
s.cycles.samples = 8
s.render.resolution_x = 1280
s.render.resolution_y = 720
s.render.resolution_percentage = 100
s.render.fps = 24
s.frame_start, s.frame_end = 1, 72
s.view_settings.view_transform = 'Standard'
s.view_settings.look = 'None'
s.world = bpy.data.worlds.new('Black')
s.world.use_nodes = True
s.world.node_tree.nodes['Background'].inputs[0].default_value = (0, 0, 0, 1)
cam = bpy.data.cameras.new('Card camera')
obj = bpy.data.objects.new('Camera', cam)
s.collection.objects.link(obj)
obj.location = (0, 0, 10)
cam.type = 'ORTHO'
cam.ortho_scale = 16
s.camera = obj

def material(name, color):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes
    n.clear()
    e = n.new('ShaderNodeEmission')
    e.inputs[0].default_value = (*color, 1)
    o = n.new('ShaderNodeOutputMaterial')
    m.node_tree.links.new(e.outputs[0], o.inputs[0])
    return m, e

font = bpy.data.fonts.load('C:/Windows/Fonts/segoeui.ttf')
def line(name, body, y, size, width, color, start):
    c = bpy.data.curves.new(name, 'FONT')
    c.body, c.font = body, font
    c.align_x = 'CENTER'
    c.size = size
    c.space_character = 1.08
    c.resolution_u = 24
    o = bpy.data.objects.new(name, c)
    s.collection.objects.link(o)
    m, e = material(name + ' light', color)
    c.materials.append(m)
    bpy.context.view_layer.update()
    scale = min(1, width / max(.01, o.dimensions.x))
    for f, k, offset in [(1, 0, -.12), (start, 0, -.12), (start+10, 1, 0), (72, 1, 0)]:
        o.location = (0, y + offset, 0)
        o.scale = (scale, scale, scale)
        o.keyframe_insert('location', frame=f)
        e.inputs[1].default_value = k
        e.inputs[1].keyframe_insert('default_value', frame=f)
    return o

line('Title', 'RIVERS OF MARS', .30, 1.05, 12, (.85, .78, .61), 1)
line('Subtitle', 'Human imagination and direction, AI-assisted craft', -.65, .36, 12, (.56, .66, .68), 4)
line('Human credit', 'Arne Gleason · Human', -1.45, .30, 12, (.56, .66, .68), 7)
line('Version stamp', 'v0.1.0  |  2026-09-07T20:56:35Z', -2.05, .17, 12, (.30, .35, .36), 10)

# Two familiar signal hoops assemble into one small, settled emblem.
for j, color in enumerate([(.8, .29, .055), (.04, .54, .68)]):
    c = bpy.data.curves.new('Signal hoop', 'CURVE')
    c.dimensions = '3D'
    c.bevel_depth = .013
    c.bevel_resolution = 4
    sp = c.splines.new('POLY')
    sp.points.add(191)
    for i, point in enumerate(sp.points):
        a = math.tau * i / 191
        x, y = .78 * math.cos(a), .34 * math.sin(a)
        angle = (-1 if j else 1) * .55
        point.co = (x*math.cos(angle)-y*math.sin(angle), 1.98+x*math.sin(angle)+y*math.cos(angle), 0, 1)
    ob = bpy.data.objects.new('Amber / cyan assembled world', c)
    s.collection.objects.link(ob)
    c.materials.append(material('Signal emission', color)[0])
    c.bevel_factor_end = 0
    c.keyframe_insert('bevel_factor_end', frame=1)
    c.bevel_factor_end = 1
    c.keyframe_insert('bevel_factor_end', frame=17)

t = bpy.data.node_groups.new('Native title glow', 'CompositorNodeTree')
t.interface.new_socket(name='Image', in_out='OUTPUT', socket_type='NodeSocketColor')
s.compositing_node_group = t
r = t.nodes.new('CompositorNodeRLayers')
g = t.nodes.new('CompositorNodeGlare')
g.inputs['Type'].default_value = 'Fog Glow'
g.inputs['Quality'].default_value = 'High'
g.inputs['Threshold'].default_value = .7
g.inputs['Strength'].default_value = .15
g.inputs['Size'].default_value = .15
o = t.nodes.new('NodeGroupOutput')
t.links.new(r.outputs['Image'], g.inputs['Image'])
t.links.new(g.outputs['Image'], o.inputs['Image'])
s.render.image_settings.file_format = 'PNG'
s.render.filepath = str(OUT / 'frames' / '') + '/'
s.frame_set(48)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / 'closing_titles.blend'))
bpy.ops.render.render(animation=True)
