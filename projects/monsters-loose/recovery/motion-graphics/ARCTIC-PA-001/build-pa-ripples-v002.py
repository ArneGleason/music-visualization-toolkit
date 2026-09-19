import bpy, math, sys
from pathlib import Path

out = Path(__file__).resolve().parent
root = out.parent.parent
mode = sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'pa'
reaction = mode == 'reaction'
bpy.ops.wm.read_factory_settings(use_empty=True)
s = bpy.context.scene
s.render.engine = 'BLENDER_EEVEE'

s.render.resolution_x = 1280
s.render.resolution_y = 720
s.render.resolution_percentage = 100
s.render.fps = 24
s.frame_start = 1
s.frame_end = 192 if reaction else 108
s.render.film_transparent = True
s.view_settings.view_transform = 'Standard'
bpy.ops.object.camera_add(location=(0,0,1000))
s.camera = bpy.context.object
s.camera.data.type = 'ORTHO'
s.camera.data.ortho_scale = 1280
s.camera.data.clip_end = 2000

def material(name, rgb):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*rgb,1)
    m.use_nodes = True
    n = m.node_tree.nodes
    n.clear()
    e = n.new('ShaderNodeEmission')
    e.inputs['Color'].default_value = (*rgb,1)
    o = n.new('ShaderNodeOutputMaterial')
    m.node_tree.links.new(e.outputs[0],o.inputs['Surface'])
    return m

ink = material('Warm weighted ink',(.017,.022,.024))
paper = material('Announcement ivory',(.91,.85,.68))
static = material('Broken signal ink',(.14,.10,.08))
font = bpy.data.fonts.load(str(root/'motion-graphics/HARPER-THOUGHT-001/fonts/Bangers-Regular.ttf'))

def mesh(name, pts, faces, mat, parent=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata(pts,[],faces)
    me.update()
    ob = bpy.data.objects.new(name,me)
    s.collection.objects.link(ob)
    ob.data.materials.append(mat)
    ob.parent = parent
    return ob

def visibility(ob,start,end):
    for f,v in [(0,True),(start-1,True),(start,False),(end,False),(end+1,True)]:
        ob.hide_render=v
        ob.keyframe_insert(data_path='hide_render',frame=f)

def stroke(name, pts, width, mat=ink, parent=None):
    cu=bpy.data.curves.new(name,'CURVE')
    cu.dimensions='3D'
    cu.resolution_u=1
    cu.bevel_depth=width
    cu.bevel_resolution=2
    sp=cu.splines.new('POLY')
    sp.points.add(len(pts)-1)
    for p,co in zip(sp.points,pts):p.co=(*co,1)
    ob=bpy.data.objects.new(name,cu)
    s.collection.objects.link(ob)
    ob.data.materials.append(mat)
    ob.parent=parent
    return ob

def burst(f):
    # Uneven impulses, not a constant shaking loop.
    return max(math.exp(-((f-c)/w)**2) for c,w in [(9,4),(24,6),(42,3),(57,6),(78,4),(99,6)])

if not reaction:
    # Tessellated image plane: deform the horn only, leaving its mount and the
    # surrounding photograph fixed. This avoids a duplicate-speaker cutout edge.
    cols,rows=160,90
    pts=[(-640+x*1280/cols,-360+y*720/rows,0) for y in range(rows+1) for x in range(cols+1)]
    faces=[]
    for y in range(rows):
        for x in range(cols):
            a=y*(cols+1)+x
            faces.append((a,a+1,a+cols+2,a+cols+1))
    m=material('Arctic PA image',(1,1,1))
    n=m.node_tree.nodes
    tex=n.new('ShaderNodeTexImage')
    tex.image=bpy.data.images.load(str(root/'assets/SCN-003-pa-arctic-v001.png'))
    m.node_tree.links.new(tex.outputs['Color'],next(v for v in n if v.type=='EMISSION').inputs['Color'])
    ob=mesh('Local horn vibration surface',pts,faces,m)
    uv=ob.data.uv_layers.new()
    for p in ob.data.polygons:
        for li in p.loop_indices:
            co=ob.data.vertices[ob.data.loops[li].vertex_index].co
            uv.data[li].uv=((co.x+640)/1280,(co.y+360)/720)
    ob.shape_key_add(name='Basis')
    key=ob.shape_key_add(name='Horn flex, mount remains fixed')
    key.slider_min=-1
    for v in key.data:
        x,y=v.co.x,v.co.y
        weight=math.exp(-(((x+207)/151)**4+((y-120)/207)**4))
        v.co.x+=4.2*weight
        v.co.y+=1.8*weight
    for f in range(1,109):
        key.value=burst(f)*math.sin(f*2.34)
        key.keyframe_insert(data_path='value',frame=f)

    # Expanding pressure fronts distort the habitat seen through the air.
    # Mouth origin is pixel(505,240); waves radiate forward through the right
    # half only. Keep the mount, left architecture and lettering stable.
    basis=[tuple(v.co) for v in ob.data.vertices]
    starts=[6,13,23,42,49,59,77,85,95]
    for f in range(1,109):
        wave=ob.shape_key_add(name='Pressure fronts frame %03d'%f)
        for v,(x,y,z) in zip(wave.data,basis):
            dx=x+135;dy=(y-120)/.78
            radius=math.hypot(dx,dy)
            direction=max(0,min(1,(dx-50)/80))
            edge=max(0,min(1,(635-x)/45))
            strength=0
            for start in starts:
                age=f-start
                if 0<=age<32:
                    front=70+age*21
                    band=(radius-front)/16
                    strength+=11*math.exp(-band*band/2)*math.cos(band*1.9)*(1-age/37)
            if radius>1:
                amount=strength*direction*edge
                v.co.x+=amount*dx/radius
                v.co.y+=amount*dy/radius*.78
        for at,value in [(f-1,0),(f,1),(f+1,0)]:
            wave.value=value;wave.keyframe_insert(data_path='value',frame=at)

    # Restrained hand-drawn ringing marks, just outside horn rim.
    for j in range(2):
        pts=[]
        for k in range(22):
            a=-.48+k/21*.96
            pts.append((-80+(j*13+32)*math.cos(a),119+(150+j*14)*math.sin(a),3))
        ob=stroke('Short ringing arc '+str(j),pts,1.7-j*.3)
        for f in range(1,109):
            ob.hide_render=not (burst(f)>.60 and f%7<5)
            ob.keyframe_insert(data_path='hide_render',frame=f)

# A continuous perimeter includes a zigzag electronic tail, no separate outlined triangle.
def balloon(start,end,lines,center,scale=1,carry=False):
    group=bpy.data.objects.new('Electronic announcement',None)
    s.collection.objects.link(group)
    contour=[]
    # Clockwise rounded cloud with slight handmade asymmetry.
    for j in range(89):
        a=math.radians(210-j*360/96)
        contour.append((216*math.cos(a)*(1+.015*math.sin(5*a)),82*math.sin(a),5))
    # Bottom-left gap is connected to a kinked electrical tail.
    contour.extend([(-189,-63,5),(-233,-75,5),(-244,-54,5),(-289,-79,5),(-395,-65,5),(-295,-46,5),(-269,-26,5),(-234,-45,5),(-206,-43,5)])
    if reaction: contour=[(-x,y,z) for x,y,z in contour]
    ob=mesh('Continuous electronic balloon paper',contour,[tuple(range(len(contour)))],paper,group)
    visibility(ob,start,end)
    # Pressure variation around a single continuous outline.
    for j in range(len(contour)):
        a=contour[j];b=contour[(j+1)%len(contour)]
        ob=stroke('Ink contour', [a,b],2.1+.45*math.sin(j*.19),ink,group)
        visibility(ob,start,end)
    for i,line in enumerate(lines):
        cu=bpy.data.curves.new('Announcement fragment','FONT')
        cu.body=line;cu.font=font;cu.align_x='CENTER';cu.align_y='CENTER';cu.size=78
        ob=bpy.data.objects.new(line,cu)
        s.collection.objects.link(ob);ob.parent=group;ob.location=(0,24-i*48,8)
        ob.data.materials.append(ink)
        visibility(ob,start+(0 if carry else i*3+2),end)
        # Brief horizontal glitches in the words, not constant text jitter.
        for f in range(start,end+1):
            t=f-start
            ob.location.x=2.4*math.sin(f*2.1) if t%19 in (10,11) else 0
            ob.keyframe_insert(data_path='location',frame=f)
    # Thin paper gaps erase parts of the text in irregular very short bursts.
    for j,(y,x,w) in enumerate([(21,-60,210),(-23,40,180),(0,0,275)]):
        ob=mesh('Momentary dropped signal',[(x-w/2,y,10),(x+w/2,y,10),(x+w/2,y+5,10),(x-w/2,y+5,10)],[(0,1,2,3)],paper,group)
        for f in range(0,s.frame_end+2):
            ob.hide_render=not(start<=f<=end and (f-start+j*4)%23 in (7,8,9))
            ob.keyframe_insert(data_path='hide_render',frame=f)
    for f in range(start,end+1):
        age=f-start
        settle=(.07*math.exp(-age/5)*math.cos(age*.4)) if not carry else 0
        group.scale=(scale*(1+settle),)*3
        group.location=(center[0]+(0 if carry else -9*math.exp(-age/5)),center[1]+.8*math.sin(f*.11),0)
        group.rotation_euler.z=math.radians(.25*math.sin(f*.09))
        for prop in ('scale','location','rotation_euler'):group.keyframe_insert(data_path=prop,frame=f)

if reaction:
    # Source frame13 is the cut-in. The bubble is clipped by the top-right
    # boundary and its tail points back offscreen toward the PA, never to Harper.
    balloon(1,51,['Z—NE…','—EIGHT—'],(555,349),.88,True)
    balloon(66,88,['—KRR—','…'],(571,361),.83,True)
else:
    balloon(6,36,['AL—','—RM…'],(355,158))
    balloon(42,71,['…Z—NE','KRR—'],(346,149),.98)
    balloon(77,108,['Z—NE…','—EIGHT—'],(354,155),1.01)

for action in bpy.data.actions:
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for curve in bag.fcurves:
                    for k in curve.keyframe_points:k.interpolation='LINEAR'
folder=out/('reaction-overlay' if reaction else 'pa-ripple-frames-v002')
folder.mkdir(exist_ok=True)
s.render.image_settings.file_format='PNG'
s.render.image_settings.color_mode='RGBA'
s.render.filepath=str(folder/'frame-')
s.frame_set(24)
bpy.ops.wm.save_as_mainfile(filepath=str(out/('Reaction-announcement-v001.blend' if reaction else 'Arctic-PA-ripples-v002.blend')))
bpy.ops.render.render(animation=True)

