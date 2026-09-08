# Green light and continuous particles

Review variation on outro_fx_notes_v2/preview_numbered_final.mp4. Same 492-frame numbered edit, master origin4362 at24fps, no changed cuts. Await owner review.

- Restore green for room and close-up sprites. Earlier blue was the implementation of the previous color request; latest request supersedes it.
- Sprite is now a bright pearl-green core plus separate green body/bloom, added to a linear-light conversion of the background. No opacity interpolation or dark layer. No intermediate 8-bit sprite clipping. Runtime assertion verifies the light never reduces any background channel (one-code-value tolerance).
- Additional close-up particles run throughout both shots6 and7, not switched on at the internal boundary. Staggered lifetimes, smooth individual entrance/exit, near-constant brightness with a small smoothed musical response.
- Existing B2 violet particle layer is selectively normalized using its recorded voice-envelope gain, outside a protected artifact region. This reduces synchronous appearance from gain changes while preserving the warm artifact pulse. Approximate color isolation, not a newly tracked particle simulation.
- Room stays at prior reduced strength. TV, artifact in shot8, natural lights-down, accepted landscape reflection and soft iris retained. Shot8 lip sync still unresolved; titles placeholder retained.

Creative Production source-preservation guidance: effects-only revision; previous versions and source footage preserved. No new generation, mastering, or production shotlist changes.
