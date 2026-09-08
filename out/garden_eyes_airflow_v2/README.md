# Eyes motion plus airflow review

Owner review pending. Does not supersede protected production s019 yet.

- Preview:1514..1650 at24fps,136frames, moth then eyes, one master soundtrack.
- Clean eyes:1569..1650 at24fps,81frames, no audio or lyrics.
- Underlying take:out/garden_eyes_motion_v1/base.mp4 source0..81, no stretching.
- Source origin1569 is a visual-only exception to the earlier .5second lead.
- No processed exit handles; later source defects still rule out long handles.
- Camera: smoothed robust background similarity, approximately9% push.
- Depth is authored, not recovered geometry. Foliage occlusion is approximate.
- Actual Blender3D motes, three bands, bass-speed/drum-brightness modulation.
- Forward helical turbulence, short motion streaks, layered optical bloom.
- Moving colored-eye clearance masks; keep eyes legible.
- Font fix is shared, but only newly rendered previews include it.
- No generation credits, mastering, commits or changes to old production timing.

Rebuild with python prepare.py, Blender -b -P render_particles.py, then
python assemble.py, using paths from the project root. The wrapper reuses
tools/garden_airflow.py, checks replacement anchors and fails if they change.
The first transparent-layer diagnostic under frames/ is not the delivery;
composite/ holds the linear-light Blender renders used for clean.mp4.
