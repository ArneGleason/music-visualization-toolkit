"""Space-filling 3D curl advection: a lightweight fluid-like look study, not CFD."""
import json
import math
import pathlib
import sys
import bpy
import numpy as np

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import garden_dust_pilot as pilot
from screen_sync_pilot import command,material
ROOT=pilot.ROOT
OUT=ROOT/"out/garden_airflow"
PULSE_LIGHT="--pulse-light" in sys.argv
BLOOM_DEPTH="--bloom-depth" in sys.argv
if PULSE_LIGHT:
    OUT=ROOT/"out/garden_airflow_pulse"
if BLOOM_DEPTH:
    PULSE_LIGHT=True
    OUT=ROOT/"out/garden_airflow_bloom_depth"
COUNT=3600
WISPS=100
DT=1/192


def curl(pos,t):
    x,y,z=(pos*.85).T
    # Curl of a trigonometric vector potential: no attracting point/sink.
    return np.column_stack((
        -np.sin(x+t)*np.sin(y)-np.cos(z-t)*np.cos(x),
        -np.sin(y+t)*np.sin(z)-np.cos(x+t)*np.cos(y),
        -np.sin(z-t)*np.sin(x)-np.cos(y+t)*np.cos(z)))


def batch(name,count):
    vertices=np.zeros((count*4,3))
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(vertices.tolist(),[],[(4*i,4*i+1,4*i+2,4*i+3) for i in range(count)])
    uv=mesh.uv_layers.new()
    uv.data.foreach_set("uv",np.tile([0,0,1,0,1,1,0,1],count))
    colors=mesh.color_attributes.new(name="Tint",type="FLOAT_COLOR",domain="CORNER")
    mat,_=pilot.sprite_material(200,(.3,.55,.4))
    nodes,links=mat.node_tree.nodes,mat.node_tree.links
    tint=nodes.new("ShaderNodeVertexColor"); tint.layer_name="Tint"
    emission=next(n for n in nodes if n.type=="EMISSION")
    mix=next(n for n in nodes if n.type=="MIX_SHADER")
    opacity=mix.inputs[0].links[0].from_node
    links.new(tint.outputs["Alpha"],opacity.inputs[1])
    links.new(tint.outputs["Color"],emission.inputs[0])
    obj=bpy.data.objects.new(name,mesh); bpy.context.scene.collection.objects.link(obj)
    mesh.materials.append(mat)
    return mesh,colors


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"frames").mkdir(exist_ok=True)
    times,bass,events=pilot.controls()
    bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
    sc=bpy.context.scene; sc.render.engine="BLENDER_EEVEE"
    sc.render.resolution_x=1920; sc.render.resolution_y=1080; sc.render.resolution_percentage=100
    sc.render.fps=24; sc.render.image_settings.file_format="PNG"
    sc.view_settings.view_transform="Standard"; sc.view_settings.look="None"
    sc.world=bpy.data.worlds.new("Garden air"); sc.world.color=(0,0,0)
    bpy.ops.object.camera_add(location=(0,0,22))
    sc.camera=bpy.context.object; sc.camera.data.type="PERSP"; sc.camera.data.lens=50
    sc.camera.data.sensor_width=36; sc.camera.data.sensor_fit="HORIZONTAL"
    bpy.ops.mesh.primitive_plane_add(size=2)
    plate=bpy.context.object; plate.name="Garden perspective plate"; plate.scale=(7.92,4.455,1)
    mat=material("Original garden",(1,1,1))
    tex=mat.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image=bpy.data.images.load(str(ROOT/"codex/out/forest_fauna_eyes_a.jpg"))
    emission=next(n for n in mat.node_tree.nodes if n.type=="EMISSION")
    mat.node_tree.links.new(tex.outputs["Color"],emission.inputs[0]); plate.data.materials.append(mat)
    mesh,colors=batch("Fine airborne motes",COUNT)
    haze,haze_colors=batch("Broken wisps in the same flow",WISPS)
    halos=[]
    if BLOOM_DEPTH:
        halos=[(*batch("Dust optical halo",COUNT),3.,.20),
               (*batch("Dust broad bloom",COUNT),8.,.025)]
    rng=np.random.default_rng(19031)
    n=COUNT+WISPS
    pos=rng.uniform([-6,-3.6,.3],[6,3.6,8],(n,3))
    layer=np.arange(n)%3
    if BLOOM_DEPTH:
        # Separate replenishing depth bands; broad distribution reaches the edges.
        pos[:,:2]=rng.uniform([-8.5,-5.2],[8.5,5.2],(n,2))
        pos[:,2]=np.array([.3,3.,6.])[layer]+rng.uniform(0,2.3,n)
    vel=np.zeros_like(pos)
    size=rng.uniform(.010,.023,COUNT)
    sparkle=rng.uniform(.55,1,COUNT)
    phase=rng.uniform(0,math.tau,n)
    palette=np.tile([.26,.52,.38,1.],(n,1))
    palette[::5,:3]=[.55,.48,.27]
    blockers=[(np.array([-4.1,-.4,4.5]),np.array([1.25,2.1,2.])),
              (np.array([4.0,-.2,4.8]),np.array([1.45,2.2,2.])),
              (np.array([0,3.1,3.8]),np.array([2.3,.6,1.2]))]
    diagnostics=[]
    light_envelope=0.
    for frame in range(-24,68):
        for sub in range(8):
            sec=(pilot.FIRST+frame+(sub+.5)/8)/24
            t=sec-pilot.FIRST/24
            level=float(np.interp(sec,times,bass))
            flow=curl(pos,t*.65)*(1.55+.7*level)
            flow += np.array([.7,.25,.45])
            if BLOOM_DEPTH:
                flow*=np.array([.75,1.1,1.5])[layer,None]
            pulse=0.
            for j,event in enumerate(events):
                age=sec-event["song_sec"]
                if 0<=age<.65:
                    hit=event["strength"]*math.exp(-age/.17)
                    pulse+=hit
                    origin=np.array([-3+(j%3)*3,.6*math.sin(j),3.5])
                    delta=pos-origin
                    distance=np.linalg.norm(delta,axis=1)
                    influence=np.exp(-(distance/4)**2)*hit
                    flow += delta/np.maximum(distance[:,None],.4)*influence[:,None]*4.5
            target=min(pulse,1.)
            tau=.022 if target>light_envelope else .20
            light_envelope+=(target-light_envelope)*(1-math.exp(-DT/tau))
            # Broad proxy leaves deflect the velocity; not a recovered 3D mesh.
            for centre,radii in blockers:
                rel=(pos-centre)/radii
                distance=np.linalg.norm(rel,axis=1)
                normal=rel/radii
                normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-5)
                inward=np.minimum(np.sum(flow*normal,axis=1),0)
                weight=np.clip((1.5-distance)*2,0,1)
                flow-=normal*inward[:,None]*weight[:,None]
                flow+=normal*np.maximum(1.05-distance,0)[:,None]*4
            vel += (flow-vel)*(1-math.exp(-DT/.055))
            pos += vel*DT
            # Continuous reservoir with edge fade hides periodic replenishment.
            pos=(pos-np.array([-7,-4.3,.2]))%np.array([14,8.6,8.2])+np.array([-7,-4.3,.2])
            if BLOOM_DEPTH:
                pos[:,:2]=(pos[:,:2]+[7,4.3])%[14,8.6]-[7,4.3]
                bottom=np.array([.3,3.,6.])[layer]
                pos[:,2]=(pos[:,2]-bottom)%2.3+bottom
        if frame<0:
            continue
        width=(22-pos[:,2])*.72
        sx=768+pos[:,0]/width*1536
        sy=432-pos[:,1]/width*1536
        visibility=np.minimum.reduce([np.ones(n),np.clip((sx-25)/120,0,1),
            np.clip((1511-sx)/120,0,1),np.clip((sy-20)/90,0,1),np.clip((810-sy)/100,0,1),
            np.clip((pos[:,2]-.2)/.7,0,1),np.clip((8.4-pos[:,2])/.7,0,1)])
        if BLOOM_DEPTH:
            bottom=np.array([.3,3.,6.])[layer]
            visibility=np.minimum.reduce([np.ones(n),np.clip((sx+80)/100,0,1),
                np.clip((1616-sx)/100,0,1),np.clip((sy+60)/80,0,1),
                np.clip((924-sy)/100,0,1),np.clip((pos[:,2]-bottom)/.25,0,1),
                np.clip((bottom+2.3-pos[:,2])/.25,0,1)])
        for x,y,r in pilot.EYES:
            visibility*=np.clip((np.hypot(sx-x,sy-y)-r*.75)/25,0,1)
        # Distant motes disappear behind broad foreground foliage silhouettes.
        for x,y,rx,ry,z in [(260,520,200,270,5),(1280,490,240,280,5),(760,100,360,90,4)]:
            inside=np.sqrt(((sx-x)/rx)**2+((sy-y)/ry)**2)
            visibility*=np.where(pos[:,2]<z,np.clip((inside-.85)/.3,0,1),1)
        rgba=palette.copy()
        light_gain=1.15+1.35*light_envelope if PULSE_LIGHT else 1.
        if BLOOM_DEPTH:
            light_gain=3.0+7.0*light_envelope
        # Emission only: no increase in opacity, coverage, size or population.
        rgba[:,:3]*=light_gain
        rgba[:COUNT,3]=visibility[:COUNT]*sparkle*(.16+.11*min(pulse,1))
        rgba[COUNT:,3]=visibility[COUNT:]*(.028+.014*min(pulse,1))
        if BLOOM_DEPTH:
            rgba[:COUNT,:3]*=np.array([.7,1.,1.15])[layer[:COUNT],None]
            rgba[COUNT:,:3]*=.4
        for m,c,start,count in [(mesh,colors,0,COUNT),(haze,haze_colors,COUNT,WISPS)]:
            p=pos[start:start+count]
            if start==0:
                r=size
                if BLOOM_DEPTH:
                    r=size*np.array([.65,1.,1.45])[layer[:COUNT]]
                # A short velocity-aligned trace makes fast motes fluid, not dots.
                direction=vel[:COUNT,:2]
                length=np.linalg.norm(direction,axis=1)
                direction=direction/np.maximum(length[:,None],1e-5)
                along=direction*(r+.008*np.minimum(length,5))[:,None]
                across=np.column_stack((-direction[:,1],direction[:,0]))*r[:,None]
            else:
                angle=phase[start:]+t*.4
                along=np.column_stack((np.cos(angle),np.sin(angle)))*.38
                across=np.column_stack((-np.sin(angle),np.cos(angle)))*.11
            vertices=np.repeat(p[:,None,:],4,axis=1)
            vertices[:,:,:2]+=np.stack((-along-across,along-across,along+across,-along+across),axis=1)
            m.vertices.foreach_set("co",vertices.astype(np.float32).ravel()); m.update()
            c.data.foreach_set("color",np.repeat(rgba[start:start+count],4,axis=0).astype(np.float32).ravel())
            if BLOOM_DEPTH and start==0:
                # Layered Gaussian halos approximate lens bloom only around dust.
                # Not a global image glare filter, and not physical light scattering.
                for hm,hc,spread,energy in halos:
                    hv=p[:,None,:]+(vertices-p[:,None,:])*spread
                    hm.vertices.foreach_set("co",hv.astype(np.float32).ravel()); hm.update()
                    tint=rgba[:COUNT].copy(); tint[:,3]*=energy
                    hc.data.foreach_set("color",np.repeat(tint,4,axis=0).astype(np.float32).ravel())
        diagnostics.append({"frame":pilot.FIRST+frame,"drum":pulse,"bass":level,
                            "light_gain":light_gain,
                            "visible_motes":int(np.sum(visibility[:COUNT]>.2)),
                            "mean_speed":float(np.linalg.norm(vel,axis=1).mean())})
        sc.render.filepath=str(OUT/"frames"/f"{frame:04d}.png")
        bpy.ops.render.render(write_still=True)
    command(["ffmpeg","-y","-v","error","-framerate","24","-i",str(OUT/"frames/%04d.png"),
        "-ss",str(pilot.FIRST/24),"-i",str(ROOT/"audio/song.wav"),"-t",str(68/24),
        "-vf","scale=1280:720:flags=lanczos","-c:v","libx264","-crf","17","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","256k","-movflags","+faststart",str(OUT/"garden_airflow.mp4")])
    (OUT/"controls.json").write_text(json.dumps({"shot":"s019","song_frames":[1527,1595],
        "method":"curl-field advection, not gas solver","motes":COUNT,"wisps":WISPS,
        "light_pulse":PULSE_LIGHT,"light_gain_range":[1.15,2.5] if PULSE_LIGHT else [1,1],
        "bloom_depth":BLOOM_DEPTH,"bloom_depth_gain_range":[3,10] if BLOOM_DEPTH else None,
        "depth_bands":[[.3,2.6],[3,5.3],[6,8.3]] if BLOOM_DEPTH else None,
        "light_envelope_attack_release_sec":[.022,.20],
        "substeps":8,"seed":19031,"approximate_depth":True,"diagnostics":diagnostics},indent=2))
    print("GARDEN AIRFLOW COMPLETE")


if __name__=="__main__":
    main()
