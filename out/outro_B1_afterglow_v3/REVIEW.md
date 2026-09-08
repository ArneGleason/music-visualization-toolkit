# B1 afterglow v3: rotating room projection

Owner requested substantially stronger projection, rotation around the room with depth, attention to the bed, and animation of existing right-hand equipment lights. V2 was too subdued.

V3 uses approximate curved-wall depth and a nearer raised-bed surface, sampled in angular coordinates around a central elevated projector. Violet and teal contours sweep across these receiver surfaces with surface-dependent scale and curvature. This is an artistic 2.5D depth proxy, not a solved room or motion track. The face, central performer and exterior window are excluded. Existing warm equipment lamps have staggered intensity swells and a vocal response. Artifact and motes remain the approved v1 treatment.

Status: awaiting owner review. No generated source, lip sync, production shot assignment or timing changed.

## Assembly

- `clean.mp4`: 191 frames at 24 fps, 1280x720, silent. Song origin 4165, end exclusive 4356.
- B1 visible source interval 67..97 maps to song 4232..4262.
- `preview.mp4`: 154 frames, song 4177..4331, A/B/A context with master audio once. A retains approved TV map v2.
- Separate Blender layers: v1 optical, v1 artifact lights, v3 room projection including practical lights. Do not double-stack the v1 clean or artifact effects.
- No final mastering or global flash. Earlier versions retained.
- `deliver.py` verifies complete decode, frame counts and frame rate and extracts a rendered check frame.
