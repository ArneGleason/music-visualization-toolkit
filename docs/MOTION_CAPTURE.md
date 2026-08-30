# Biological-motion retargeting

The motion-capture layer preserves organic timing and joint relationships while
allowing the finished image to remain project-native vector art. Captured joints
are hidden controls, not a skeleton design.

## Project workflow

Add an Acclaim ASF/AMC source to `motionClips` in a project's `project.json`,
including source URLs, capture and output rates, selected controls, output path,
license statement, and acknowledgement. Then run:

```bash
python tools/timeline.py sync projects/rivers-of-mars/project.json
```

`tools/motion_capture.py` downloads missing source files into the ignored
project `generated/mocap/` cache, resolves forward kinematics, chooses the most
active configured window, smooths only a narrow five-sample neighborhood, and
writes a compact root-relative JSON clip under `generated/motion/`. The output
retains provenance, exact source-frame range, source/output rates, joint order,
normalization, per-frame controls, and separate root motion.

The standalone command is useful while developing a clip:

```bash
python tools/motion_capture.py projects/rivers-of-mars/project.json
```

## Retargeting rules

- Preserve capture timing between authored musical anchors; do not snap every
  joint to beats.
- Keep contacts, counter-motion, asymmetry, acceleration changes, and delayed
  extremities. These are the biological evidence.
- Map only useful controls to visible marks. In the river sequence, the capture
  ends at the waist: the upper body becomes one Bézier ribbon and the wrists
  become detached fins. A procedural flagellum continues from the waist, with
  its broad wave following bass energy and drum impulses travelling to its tip.
- Keep root scene paths, camera, scale billing, color, and interaction beats
  authored in the choreography register.
- Reusing one clip requires meaningful variation in phase, speed, direction,
  depth, scale, scene path, and responder behavior.
- Retain source and license metadata with every clip. Do not assume a public
  research dataset permits commercial or derivative use.

## Rivers of Mars reference

The prototype uses CMU Motion Capture Subject 125, Trial 6, a 120 fps freestyle
swimming performance. CMU states that its motion database is free for all uses
and requests the following acknowledgement:

> The data used in this project was obtained from mocap.cs.cmu.edu. The
> database was created with funding from NSF EIA-0196217.

Source: https://mocap.cs.cmu.edu/search.php?subjectnumber=125

Use the video renderer query `motionDebug=1` to display the point-light controls
over the finished vector reinterpretation. The normal render never draws them.
