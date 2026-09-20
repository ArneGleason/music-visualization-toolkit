# Tour rooftop blinking lights
User approved tour003 despite earlier assistant concern about background. Add only Blender light overlays; no regeneration or credits.

prepare.py tracks five existing red beacons in the original145-frame footage at960x540 coordinates and writes build.py using SWAMP-LIGHTS-001's exact soft beacon material and pulse function. build.py renders145 transparent1916x1080 PNGs. Same29-frame cycle, sigma3.4, stagger4frames, master phase. Far small beacon is gated when obscured by the moving cast. Warm lamps unchanged.

Composite overlay/lights-%04d.png at24fps over video-tests/KLING-TOUR-003/KLING-TOUR-003-01.mp4 with FFmpeg overlay=0:0:format=auto, libx264 crf18 yuv420p, no audio,145frames, output Tour-lights-v001.mp4. Master1507..1625 exclusive uses source12..130. No cut or timing changes. Full review v34. Previous source preserved.

Follow-up backlog: review red warning-light continuity in earlier shots; user scoped this pass to the tour.
