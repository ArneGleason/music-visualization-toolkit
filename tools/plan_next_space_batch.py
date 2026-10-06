"""Write the five-note continuation specification without changing the edit."""
import json
import pathlib


def main():
    base=pathlib.Path('projects/a-right-little-something')
    register=json.loads((base/'shots/shotlist.json').read_text(encoding='utf-8'))
    notes=json.loads((base/'generated/review/listening-notes.json').read_text(encoding='utf-8'))
    phrases=json.loads((base/'generated/animatic/animatic-data.json').read_text(encoding='utf-8'))['phrases']
    lock=register['shots'][0]['promptLock']
    definitions=[
        ('space-006',581,'World below',
         'Proposed replacement for the last 52 frames of opening-005. Cut on To to a wide view: tiny ship at the upper-left, immense planet below. A modest widening settles before the next cut.',
         [18,-25,14],[20,-28,16],[0,2,-3],[0,3,-4],36,[0,0,0],[0,0,0],
         'Cut from hands at the boundary to the world below; do not force a two-second trip through the shell.',
         'ImageGen wide starting frame from this geometry, then restrained Kling drift. A cut is safer than an ambitious shell-crossing reveal.'),
        ('space-007',633,'The map opens outward',
         'Three-quarter interior medium shot. Harper summons a floating spatial diagram and spreads her fingers. The planet diagram reduces to an orbital system, then a local-star network. Continue across the musical gap to her reaction at frame 737.',
         [1.6,-1.6,1.4],[1.6,-1.6,1.4],[0,0,1],[0,0,1],30,[0,0,0],[0,0,0],
         'Hard cut into the interior; fixed camera lets the map carry the movement. Cut to her reaction after the map settles.',
         'ImageGen establishes Harper, her hand pose and a faint diagram. Kling handles the performance; Blender supplies an independently composited planet/system/star expansion and stable invented glyphs. Keep diagram labels away from the lyric strip.'),
        ('space-008',737,'Small cabin, enormous space',
         'Medium-close reaction: she glances from the map to the boundary, curiosity becoming restless longing. Let the diagram fade. Begin her gentle approach without a cut on The windows.',
         [-.8,-2,1.4],[-1.5,-2.1,.95],[-.13,0,1.04],[-.13,-1.2,1.04],30,[0,0,0],[0,-1.2,0],
         'Start one continuous reaction-to-window take, shared with space-009. No new starting-frame reset at 789.',
         'One six-second Kling take spanning 737–853 with half-second handles. Beginning and ending reference poses constrain the drift. Blender checks the path and boundary clearance.'),
        ('space-009',789,'Drawn to the boundary',
         'Continue the same take and screen direction. Harper floats toward the window, face and palms near the field but still inside. Keep one small metal-band cue so she reads as inside her ship, not outside it.',
         [-1.5,-2.1,.95],[-1.5,-2.1,.95],[-.13,-1.2,1.04],[-.13,-2.05,1.04],30,[0,-1.2,0],[0,-2.05,0],
         'Continuation of space-008; this is a blocking beat, not an edit cut. Cut closer at frame 854.',
         'Use the same generated source as space-008. This ending composition constrains the single continuous take; add local cyan contact glow only if needed.'),
        ('space-010',854,'The cosmos in her eyes',
         'Close portrait at the boundary. Eyes dominate, with restrained reflected stars and a curved planet light. Hold a tiny breathing movement. Never turn the reflection into a second literal miniature planet beside her face.',
         [-.35,-2.6,1.18],[-.32,-2.6,1.17],[-.13,-2.05,1.04],[-.13,-2.05,1.04],30,[0,-2.05,0],[0,-2.05,0],
         'Cut in at Show you just how big you are. End at Stretch your arms wide; no direction beyond that phrase has been assumed.',
         'ImageGen close portrait from the approved Harper reference, using Blender only for framing. Kling provides micro-expression; reflected cosmic light can be composited if generation makes it unstable.')]
    shots=[]
    for ident,frame,title,description,ca,cb,ta,tb,lens,fa,fb,transition,approach in definitions:
        note=next(n for n in notes['notes'] if n.get('start_frame')==frame and n['status']=='open')
        shots.append(dict(id=ident,noteId=note['id'],title=title,description=description,
                          cameraStart=ca,cameraEnd=cb,targetStart=ta,targetEnd=tb,lens=lens,
                          figureStart=fa,figureEnd=fb,figurePose='float',interior=frame!=581,
                          hologram=frame==633,transition=transition,generationApproach=approach,
                          editGroup='reaction-window-continuous' if frame in (737,789) else ident,
                          promptLock=lock,lyrics=[p['text'] for p in phrases if frame<=p['startFrame']<dict(zip([581,633,737,789,854],[633,737,789,854,912]))[frame]]))
    spec=dict(id='space-notes-v01',proposal=True,notesRevision=notes['revision'],
              baseBlend='generated/blockout-moon-identities/sphere-ship-blockout.blend',
              output='generated/storyboard/space-notes-v01',blendFilename='space-notes-v01.blend',
              handlesFrames=12,endPhrase='lyr-013',shots=shots)
    (base/'storyboard-space-notes.json').write_text(json.dumps(spec,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


if __name__=='__main__':
    main()
