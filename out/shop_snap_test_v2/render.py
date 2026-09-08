"""Earlier punch-in, switching performances inside peak optical blur."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
p=ROOT/'out/shop_push_test_v1/render.py'
s=p.read_text().replace('out/shop_push_test_v1/clean.mp4','out/shop_snap_test_v2/clean.mp4')
start=s.index('for sf in range(2399,2484):')
end=s.index("subprocess.run(['ffmpeg'",start)
s=s[:start]+'''
for sf in range(2399,2484):
    if sf<2424:
        frame=plates['wide'][sf-2387]
    elif sf>=2436:
        frame=plates['close'][sf-2425]
    else:
        # Accelerate to the cut; decelerate on the close side. No face dissolve.
        use_close=sf>=2431
        plate=plates['close'][sf-2425] if use_close else plates['wide'][sf-2387]
        samples=[]
        for dt in np.linspace(-.65,.65,17):
            if not use_close:
                a=np.clip((sf+dt-2424)/6,0,1)**1.8
                left=520*a;top=(64/1.2)*a
                width=1280+(800/1.2-1280)*a
                height=720+(450/1.2-720)*a
            else:
                settle=1-smooth((sf+dt-2431)/5)
                scale=1+.075*settle
                width=1280/scale;height=720/scale
                left=(1280-width)*.50;top=(720-height)*.40
            samples.append(cv2.remap(plate,(left+x*width/1280).astype(np.float32),
                (top+y*height/720).astype(np.float32),cv2.INTER_LINEAR))
        frame=np.mean(samples,axis=0)
        # Brief radial streak plus defocus hides the arm/shoulder discontinuity.
        blur=float(np.exp(-.5*((sf-2430.5)/1.25)**2))
        streaks=[]
        for scale in np.linspace(1-.10*blur,1+.10*blur,13):
            streaks.append(cv2.remap(frame,((x-640)/scale+640).astype(np.float32),
                ((y-270)/scale+270).astype(np.float32),cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_REFLECT_101))
        frame=np.mean(streaks,axis=0)
        frame=cv2.GaussianBlur(frame,(0,0),max(.1,11*blur))
        frame=np.clip(frame,0,255).astype(np.uint8)
    cv2.imwrite(str(OUT/'frames'/f'{sf-2399:04d}.png'),frame)
''' +s[end:]
s=s.replace("'push_song_frames':[2425,2437],'close_blend_song_frames':[2434,2437]",
    "'push_song_frames':[2424,2436],'close_switch_frame':2431,'close_blend_song_frames':[], 'method':'accelerating punch, radial streak and brief defocus at hard source switch, slight overshoot settling; no face dissolve'")
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py')})
