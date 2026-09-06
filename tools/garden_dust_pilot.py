"""Blender-native emissive particle sprites; static plate, deterministic audio motion."""
import json
import math
import pathlib
import sys
import bpy
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import screen_sync_pilot as base
import screen_sync_phosphor as scope

ROOT = base.ROOT
OUT = ROOT/"out/garden_dust_pilot"
FIRST, END, FPS = 1527, 1595, 24
EYES = [(355,248,40),(415,248,40),(595,210,25),(611,210,25),
        (1122,260,40),(1163,260,40),(799,368,28),(819,368,28),
        (636,453,22),(652,453,22),(980,461,34),(1019,461,34),
        (1328,480,50),(1420,480,50),(185,550,60),(284,550,60)]


def controls():
    base.FIRST, base.END = FIRST, END
    bass = base.read_bass()
    drums = scope.read_stem("Drum Kit", "drums", 100, 2800)
    times = np.arange(FIRST/FPS-1, END/FPS+1/192, 1/192)
    def rms(source):
        samples, offset, _ = source
        samples = np.asarray(samples)
        values = []
        for t in times:
            index = int((t-offset)*8000)
            chunk = samples[max(0,index-80):index+1]
            values.append(float(np.sqrt(np.mean(chunk*chunk))))
        return np.asarray(values)
    b, d = rms(bass), rms(drums)
    b /= max(np.quantile(b,.95),1e-5)
    smooth = []
    state = 0.
    for value in b:
        tau = .15 if value>state else .4
        state += (min(value,1.5)-state)*(1-math.exp(-1/(192*tau)))
        smooth.append(state)
    onset = np.maximum(0,d-np.roll(d,4))
    onset[:4] = 0
    candidates = [i for i in range(1,len(onset)-1)
                  if onset[i]>onset[i-1] and onset[i]>=onset[i+1]
                  and onset[i]>np.quantile(onset,.88)]
    picked = []
    for i in sorted(candidates,key=lambda j:onset[j],reverse=True):
        if all(abs(times[i]-times[j])>=.25 for j in picked):
            picked.append(i)
    maximum = max(float(onset.max()),1e-6)
    events = [{"song_sec":float(times[i]),"strength":float(onset[i]/maximum)}
              for i in sorted(picked) if FIRST/FPS-.6<=times[i]<END/FPS]
    return times, np.asarray(smooth), events


def sprite_material(index, color):
    mat = bpy.data.materials.new(f"Pollen light {index}")
    mat.use_nodes = True
    mat.surface_render_method = "BLENDED"
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    nodes.clear()
    uv = nodes.new("ShaderNodeTexCoord")
    dist = nodes.new("ShaderNodeVectorMath"); dist.operation = "DISTANCE"
    dist.inputs[1].default_value = (.5,.5,0)
    links.new(uv.outputs["UV"],dist.inputs[0])
    square = nodes.new("ShaderNodeMath"); square.operation = "MULTIPLY"
    links.new(dist.outputs["Value"],square.inputs[0]); links.new(dist.outputs["Value"],square.inputs[1])
    scale = nodes.new("ShaderNodeMath"); scale.operation = "MULTIPLY"; scale.inputs[1].default_value=-38
    links.new(square.outputs[0],scale.inputs[0])
    gaussian = nodes.new("ShaderNodeMath"); gaussian.operation="EXPONENT"
    links.new(scale.outputs[0],gaussian.inputs[0])
    opacity = nodes.new("ShaderNodeMath"); opacity.operation="MULTIPLY"
    links.new(gaussian.outputs[0],opacity.inputs[0]); opacity.inputs[1].default_value=.1
    clear = nodes.new("ShaderNodeBsdfTransparent")
    emission = nodes.new("ShaderNodeEmission"); emission.inputs[0].default_value=(*color,1)
    emission.inputs[1].default_value=1.4
    mix = nodes.new("ShaderNodeMixShader")
    links.new(opacity.outputs[0],mix.inputs[0]); links.new(clear.outputs[0],mix.inputs[1])
    links.new(emission.outputs[0],mix.inputs[2])
    output = nodes.new("ShaderNodeOutputMaterial"); links.new(mix.outputs[0],output.inputs[0])
    return mat, opacity.inputs[1]


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for folder in ("composite","overlay"):
        (OUT/folder).mkdir(exist_ok=True)
    times, bass, events = controls()
    bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
    scene = bpy.context.scene
    scene.render.engine="BLENDER_EEVEE"
    scene.render.resolution_x=1920; scene.render.resolution_y=1080
    scene.render.resolution_percentage=100; scene.render.fps=24
    scene.render.image_settings.file_format="PNG"
    scene.render.image_settings.color_mode="RGBA"
    scene.render.film_transparent=True
    scene.view_settings.view_transform="Standard"; scene.view_settings.look="None"
    scene.world=bpy.data.worlds.new("Dark garden"); scene.world.color=(0,0,0)
    bpy.ops.object.camera_add(location=(0,0,1000))
    scene.camera=bpy.context.object; scene.camera.data.type="ORTHO"; scene.camera.data.ortho_scale=1536
    bpy.ops.mesh.primitive_plane_add(size=2)
    plate=bpy.context.object; plate.name="Approved garden still"; plate.scale=(768,432,1)
    mat=base.material("Unchanged photographic plate",(1,1,1))
    tex=mat.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image=bpy.data.images.load(str(ROOT/"codex/out/forest_fauna_eyes_a.jpg"))
    emit=next(n for n in mat.node_tree.nodes if n.type=="EMISSION")
    mat.node_tree.links.new(tex.outputs["Color"],emit.inputs["Color"])
    plate.data.materials.append(mat)
    rng=np.random.default_rng(19027)
    particles=[]
    for i in range(56):
        depth=float(rng.uniform(.25,1))
        x=float(rng.uniform(585,925)); y=float(rng.uniform(300,635))
        size=float(rng.uniform(2.5,5.5))*(.6+depth)
        color=(.31,.65,.36) if i%3 else (.75,.61,.26)
        mat, opacity=sprite_material(i,color)
        bpy.ops.mesh.primitive_plane_add(size=2,location=(0,0,5+depth*15))
        obj=bpy.context.object; obj.name=f"Dust particle {i:02d}"
        obj.scale=(size,size,1); obj.data.materials.append(mat)
        particles.append((obj,opacity,x,y,depth,float(rng.uniform(0,math.tau)),i%4))
    for frame in range(END-FIRST):
        sec=(FIRST+frame+.5)/FPS; t=sec-FIRST/FPS
        breath=float(np.interp(sec,times,bass))
        for obj, opacity, x,y,depth,phase,group in particles:
            pulse=0.; displacement=0.
            for index,event in enumerate(events):
                age=sec-event["song_sec"]
                if 0<=age<1.2 and index%4==group:
                    pulse += event["strength"]*(1-math.exp(-age/.025))*math.exp(-age/.24)
                    displacement += event["strength"]*(1-math.exp(-age/.09))*math.exp(-age/.65)*12
            px=x+math.sin(t*.9+phase)*(8+8*breath)+math.cos(phase)*displacement
            py=y-t*(6+depth*6)+math.cos(t*.7+phase)*7-math.sin(phase)*displacement
            # Conservative corridor and eye holdouts, not a claimed depth solve.
            mask=min(1,max(0,(px-560)/40),max(0,(960-px)/50),max(0,(650-py)/50))
            for ex,ey,radius in EYES:
                mask *= min(1,max(0,(math.hypot(px-ex,py-ey)-radius)/18))
            opacity.default_value=min(.70,(.065+.60*pulse)*(.65+.35*depth))*mask
            obj.location.x=px-768; obj.location.y=432-py
        plate.hide_render=False
        scene.render.filepath=str(OUT/"composite"/f"{frame:04d}.png")
        bpy.ops.render.render(write_still=True)
        plate.hide_render=True
        scene.render.filepath=str(OUT/"overlay"/f"{frame:04d}.png")
        bpy.ops.render.render(write_still=True)
    base.command(["ffmpeg","-y","-v","error","-framerate","24","-i",str(OUT/"composite/%04d.png"),
        "-ss",str(FIRST/FPS),"-i",str(ROOT/"audio/song.wav"),"-t",str((END-FIRST)/FPS),
        "-vf","scale=1280:720:flags=lanczos","-c:v","libx264","-crf","17","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","256k","-movflags","+faststart",str(OUT/"garden_dust.mp4")])
    (OUT/"controls.json").write_text(json.dumps({"shot":"s019","fps":FPS,"song_frames":[FIRST,END],
        "particles":56,"seed":19027,"events":events,"bass_times":times.tolist(),"bass":bass.tolist(),
        "overlay":"RGBA PNG, Blender straight-alpha PNG export; alpha-over, not additive",
        "camera":"static","handles":0,"implementation":"scripted Blender emissive particle sprites, no physics emitter"},indent=2))
    print("GARDEN DUST PILOT COMPLETE")


if __name__=="__main__":
    main()
