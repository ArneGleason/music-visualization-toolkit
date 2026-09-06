"""Native Blender emitter particles and animated attraction/vortex/turbulence."""
import json
import math
import pathlib
import sys
import bpy
import numpy as np

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import garden_dust_pilot as pilot
from screen_sync_pilot import command, material

ROOT=pilot.ROOT
OUT=ROOT/"out/garden_dust_fields"
PRE=24


def field(name, kind, location, strength):
    bpy.ops.object.effector_add(type=kind, location=location)
    obj=bpy.context.object; obj.name=name; obj.field.strength=strength
    return obj


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"composite").mkdir(exist_ok=True)
    times,bass,events=pilot.controls()
    bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
    sc=bpy.context.scene
    sc.render.engine="BLENDER_EEVEE"
    sc.render.resolution_x=1920; sc.render.resolution_y=1080; sc.render.resolution_percentage=100
    sc.render.fps=24; sc.render.image_settings.file_format="PNG"
    sc.view_settings.view_transform="Standard"; sc.view_settings.look="None"
    sc.world=bpy.data.worlds.new("Garden darkness"); sc.world.color=(0,0,0)
    sc.gravity=(0,0,0); sc.frame_start=1; sc.frame_end=PRE+68
    bpy.ops.object.camera_add(location=(0,0,15))
    sc.camera=bpy.context.object; sc.camera.data.type="ORTHO"; sc.camera.data.ortho_scale=15.36
    bpy.ops.mesh.primitive_plane_add(size=2)
    plate=bpy.context.object; plate.name="Unchanged garden plate"; plate.scale=(7.68,4.32,1)
    mat=material("Photographic garden",(1,1,1))
    tex=mat.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image=bpy.data.images.load(str(ROOT/"codex/out/forest_fauna_eyes_a.jpg"))
    emit=next(n for n in mat.node_tree.nodes if n.type=="EMISSION")
    mat.node_tree.links.new(tex.outputs["Color"],emit.inputs["Color"])
    plate.data.materials.append(mat)
    # Restore original foreground outside the chosen atmospheric window and
    # over the eyes. Photo UVs register exactly; these are conservative holdouts.
    def patch(name,coords):
        mesh=bpy.data.meshes.new(name)
        mesh.from_pydata([((x-768)/100,(432-y)/100,4) for x,y in coords],[],[list(range(len(coords)))])
        mesh.uv_layers.new()
        for loop in mesh.loops:
            x,y=coords[loop.vertex_index]
            mesh.uv_layers.active.data[loop.index].uv=(x/1536,1-y/864)
        obj=bpy.data.objects.new(name,mesh); sc.collection.objects.link(obj); mesh.materials.append(mat)
    for coords in [[(0,0),(1536,0),(1536,250),(0,250)],
                   [(0,665),(1536,665),(1536,864),(0,864)],
                   [(0,250),(550,250),(550,665),(0,665)],
                   [(1000,250),(1536,250),(1536,665),(1000,665)]]:
        patch("Foreground holdout",coords)
    for x,y,r in pilot.EYES:
        patch("Eye holdout",[(x+r*math.cos(a),y+r*math.sin(a)) for a in np.linspace(0,math.tau,48,endpoint=False)])
    emitters=[]
    for i,(x,y) in enumerate([(-1.75,-1.85),(1.35,-1.25)]):
        sm,opacity=pilot.sprite_material(100+i,(.22,.65,.43) if i==0 else (.78,.61,.26))
        opacity.default_value=.52
        bpy.ops.mesh.primitive_plane_add(size=2,location=(100+i*3,100,0))
        sprite=bpy.context.object; sprite.name=f"Luminous mote instance {i}"
        sprite.data.materials.append(sm)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=6,radius=.36,location=(x,y,.7))
        obj=bpy.context.object; obj.name=f"Pollen emitter {i+1}"
        obj.show_instancer_for_render=False
        bpy.ops.object.particle_system_add()
        ps=obj.particle_systems[-1]; ps.seed=19027+i
        settings=ps.settings; settings.type="EMITTER"
        settings.count=850; settings.frame_start=1; settings.frame_end=PRE+68
        settings.lifetime=75; settings.lifetime_random=.25
        settings.normal_factor=.35; settings.factor_random=.32
        settings.effector_weights.gravity=0; settings.brownian_factor=.13; settings.damping=.09
        settings.render_type="OBJECT"; settings.instance_object=sprite
        settings.particle_size=.055; settings.size_random=.7; settings.use_rotations=False
        ps.point_cache.frame_start=1; ps.point_cache.frame_end=PRE+68
        emitters.append(obj)
    attract=field("Gathering centre — bass", "HARMONIC",(0,-.4,.7),2)
    vortex=field("Spiral — bass and choreography", "VORTEX",(0,-.4,.7),.7)
    scatter=field("Drum repulsion", "FORCE",(0,-.4,.7),0)
    scatter.field.falloff_power=0
    turbulence=field("Living air", "TURBULENCE",(0,-.4,.7),.35)
    turbulence.field.size=1.1; turbulence.field.seed=27
    # Tempo-grid anchors drive centre travel; audio transients drive scatter.
    cues=json.loads((ROOT/"generated/overlay_cues.json").read_text())
    beats=[b["frame"] for b in cues["beats"]]
    controls=[]
    for f in range(1,PRE+69):
        sec=(pilot.FIRST+f-PRE-1)/24
        t=sec-pilot.FIRST/24
        level=float(np.interp(sec,times,bass))
        beatphase=float(np.interp(sec*24,beats,np.arange(len(beats))))
        hit=sum(e["strength"]*math.exp(-(sec-e["song_sec"])/.14)
                for e in events if 0<=sec-e["song_sec"]<.65)
        centre=(.6*math.sin(beatphase*math.pi*.5),-.05+.55*math.cos(beatphase*math.pi*.5),.7)
        for obj in (attract,vortex,scatter):
            obj.location=centre; obj.keyframe_insert("location",frame=f)
        # Attraction relaxes on impact, then reforms the loose cloud.
        attract.field.strength=max(.25,2.2+level*1.8-hit*3)
        vortex.field.strength=.55+level*.7
        scatter.field.strength=hit*3.2
        turbulence.field.strength=.22+.35*hit
        for obj in (attract,vortex,scatter,turbulence):
            obj.field.keyframe_insert("strength",frame=f)
        for i,obj in enumerate(emitters):
            obj.location.x=(-1.75 if i==0 else 1.35)+.2*math.sin(beatphase*math.pi+i)
            obj.keyframe_insert("location",frame=f)
        controls.append({"frame":pilot.FIRST+f-PRE-1,"bass":level,"drum":hit,"centre":centre})
    for f in range(1,PRE+69):
        sc.frame_set(f)
        # Force evaluation every frame to maintain the emitter simulation cache.
        bpy.context.view_layer.update()
        if f<=PRE:
            continue
        sc.render.filepath=str(OUT/"composite"/f"{f-PRE-1:04d}.png")
        bpy.ops.render.render(write_still=True)
    command(["ffmpeg","-y","-v","error","-framerate","24","-i",str(OUT/"composite/%04d.png"),
        "-ss",str(pilot.FIRST/24),"-i",str(ROOT/"audio/song.wav"),"-t",str(68/24),
        "-vf","scale=1280:720:flags=lanczos","-c:v","libx264","-crf","17","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","256k","-movflags","+faststart",str(OUT/"garden_fields.mp4")])
    (OUT/"controls.json").write_text(json.dumps({"shot":"s019","song_frames":[1527,1595],
        "simulation_preroll_frames":PRE,"editorial_lead_handle_frames":0,"emitters":2,
        "emitted_particles_total":1700,"fields":["HARMONIC","VORTEX","FORCE","TURBULENCE"],
        "controls":controls,"notes":"Native emitter simulation; repeat from frame 1. No tracked geometry."},indent=2))
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"garden_fields.blend"))
    print("GARDEN FIELDS COMPLETE")


if __name__=="__main__":
    main()
