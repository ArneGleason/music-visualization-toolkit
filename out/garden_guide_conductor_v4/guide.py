"""A visible, above-head conductor: arrive, gather, cue the pollen release."""
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
beats = np.array([b['sec']*24 for b in json.loads(
    (ROOT/'generated/overlay_cues.json').read_text())['beats']])

def smooth(v):
    v = np.clip(v, 0, 1)
    return v*v*(3-2*v)

def position(sf):
    phase = np.interp(sf, beats, np.arange(len(beats)))
    a = (phase-np.interp(1798, beats, np.arange(len(beats))))*2*np.pi
    arrival = smooth((sf-1786)/12)
    gather = smooth((sf-1812)/12)
    release = smooth((sf-1828)/10)
    radius = 54*(1-gather)+8*gather+23*release
    cx = (1-arrival)*838+arrival*(640+radius*np.sin(a))
    cy = 78+arrival*(18*(1-gather)+5*gather)*np.cos(a)
    # Lift away from her silhouette on the cue, never through her face.
    cue = np.exp(-((sf-1828)/3.4)**2)
    cy -= 34*cue
    size = 7.2+1.3*gather+1.1*cue
    return cx, cy, size, phase, cue

def guide(pic, sf, x, y, protection):
    core = np.zeros(x.shape, np.float32)
    halo = core.copy()
    for sample in (-.30, .30):
        cx, cy, size, phase, cue = position(sf+sample)
        gain = 1.05+1.25*np.exp(-(phase%1)/.23)+1.15*cue
        for age in range(12):
            px, py, radius, _, _ = position(sf+sample-age*.32)
            d = (x-px)**2+(y-py)**2
            core += np.exp(-d/(2*(radius*(1-age*.045))**2))*np.exp(-age*.38)*.25*gain
        d = (x-cx)**2+(y-cy)**2
        halo += (np.exp(-d/(2*19**2))*.20+np.exp(-d/(2*35**2))*.065)*gain*.5
    # Keep all added light above the hairline; no implication of facial spill.
    head_clearance = 1-smooth((y-119)/24)
    fx = core[:,:,None]*np.array([.40,1.,.57])+halo[:,:,None]*np.array([.21,1.,.36])
    return pic+fx*head_clearance[:,:,None]
