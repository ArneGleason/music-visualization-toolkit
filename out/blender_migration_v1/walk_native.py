"""Native analytic light fields with original two-sample tapered wake."""
from pathlib import Path
O=Path(__file__).resolve().parent
exec(compile((O/'lights2_native.py').read_text().split("if family=='receiver':",1)[0],str(O/'lights2_native.py'),'exec'))
cx=b.animated('Existing light X',[v['center'][0] for v in rows]); cy=b.animated('Existing light Y',[v['center'][1] for v in rows])
strength=b.animated('Existing light vocal reinforcement',[.12*v['voice']*v['visibility'] for v in rows])
d=(x-cx)**2+(y-cy)**2
original=((-d/(2*5**2)).exp()*.45+(-d/(2*17**2)).exp()*.22+(-d/(2*42**2)).exp()*.095)*strength
signal=0
for i in range(16):
    bx=b.animated(f'Flight sample{i} X',[v['blobs'][i]['xy'][0] for v in rows]); by=b.animated(f'Flight sample{i} Y',[v['blobs'][i]['xy'][1] for v in rows])
    sigma=b.animated(f'Flight sample{i} radius',[v['blobs'][i]['sigma'] for v in rows]); weight=rows[0]['blobs'][i]['weight']
    signal+=(-((x-bx)**2+(y-by)**2)/(2*sigma**2)).exp()*weight
gain=b.animated('Green light phrase accent',[v['gain'] for v in rows]); signal*=gain
em=b.n.new('ShaderNodeEmission'); b.plug(b.combine([original*.65+signal*.60,original+signal,original*.30+signal*.38]),em.inputs[0])
mo=b.n.new('ShaderNodeOutputMaterial'); b.plug(em.outputs[0],mo.inputs[0])
t=bpy.data.node_groups.new('Native green guide additive composite','CompositorNodeTree');t.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=t;b=Builder(t)
plate=b.n.new('CompositorNodeImage');plate.image=img;plate.frame_duration=count;plate.frame_start=1;plate.use_auto_refresh=True
scale=b.n.new('CompositorNodeScale');scale.inputs['Type'].default_value='Render Size';b.plug(plate.outputs[0],scale.inputs['Image'])
rl=b.n.new('CompositorNodeRLayers')
result=b.combine([b.linear((b.display(a)+z).clamp()) for a,z in zip(b.split(scale.outputs[0]),b.split(rl.outputs['Image']))])
end=b.n.new('NodeGroupOutput');b.plug(result,end.inputs['Image'])
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.filepath=str(out)+'/'
bpy.ops.wm.save_as_mainfile(filepath=str(D/f'walk_{W}.blend'))
for f in frames:s.frame_set(f);s.render.filepath=str(out/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
