#!/usr/bin/env python3
"""
Render the 3D world offline, with temporal supersampling.

    python3 tools/world_render.py --blur 8 --fps 60
    python3 tools/world_render.py --section turn --blur 4 --width 1280

Drives world/index.html in headless Chrome, stepping time deterministically —
nothing depends on wall-clock, so the output is frame-exact and repeatable.

The motion blur happens on the GPU, in the page: renderFrame(t, 1/fps, N)
advances the whole simulation N times inside one output frame and averages the
results in an offscreen 2D canvas at 1/N with 'lighter' compositing. That
matters for cost — 8x supersampling is 8 cheap GPU renders, and only ONE frame
is read back per output frame. In the Python visualiser 8x meant eight full
CPU rasterisations, which is why it ran at 30x realtime.

Frames are piped straight into ffmpeg; the audio is muxed from audio/song.wav.
"""
from __future__ import annotations

import argparse
import pathlib
import base64
import collections
import subprocess
import sys
import threading
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, load  # noqa: E402


def serve(port):
    sys.argv = ["serve.py", str(port)]
    import serve as s                                    # noqa: F401
    raise SystemExit


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-o", "--out", type=pathlib.Path, default=ROOT / "out" / "world.mp4")
    ap.add_argument("--section")
    ap.add_argument("--from", dest="t_from", type=float,
                    help="start time in seconds (overrides --section)")
    ap.add_argument("--dur", type=float, help="length in seconds")
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--blur", type=int, default=8, help="sub-frames per output frame")
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--port", type=int, default=8751)
    ap.add_argument("--headless", action="store_true",
                    help="run without a window — WARNING: falls back to software GL")
    ap.add_argument("--probe", type=int, default=0,
                    help="time N frames, report the rate, and stop")
    ap.add_argument("--jpeg", type=int, default=94, help="frame quality; 0 = PNG")
    ap.add_argument("--crf", type=int, default=17, help="x264 quality; lower is better")
    ap.add_argument("--preset", default="medium", help="x264 speed/quality preset")
    ap.add_argument("--abr", default="256k", help="audio bitrate")
    ap.add_argument("--audio", type=pathlib.Path, default=ROOT / "audio" / "song.wav")
    ap.add_argument("--page", default="world",
                    help="which visualiser to drive: world | stage")
    ap.add_argument("--query", default="",
                    help="query string passed to the visualiser page")
    ap.add_argument("--capture", default="dataurl",
                    choices=["dataurl", "post", "element", "cdp"],
                    help="how a finished frame leaves the browser "
                         "(see tools/capture_bench.py)")
    a = ap.parse_args()

    from playwright.sync_api import sync_playwright

    W = a.width
    H = int(W * 9 / 16) // 2 * 2
    # Both pages expose the same contract (__ready, setRenderSize,
    # renderFrame, an #out canvas); they differ only in where their span
    # information lives.
    if a.page == "stage":
        if not (ROOT / "stage" / "data.json").exists():
            raise SystemExit("no stage/data.json — run: ./run.sh laser")
        spans = load(ROOT / "stage" / "data.json")
        dur = spans["duration"]
        secs = [(x["id"], x["t0"], x["t1"]) for x in spans["sections"]]
    else:
        shots = load(ROOT / "world" / "shots.json")
        dur = shots["duration"]
        secs = [(x["section"], x["t0"], x["t1"]) for x in shots["shots"]]
    t0, t1 = 0.0, dur
    if a.t_from is not None:
        # An arbitrary window, at whatever quality the rest of the flags say.
        # The point of a test render is to exercise the SETTINGS, so this
        # deliberately changes nothing else.
        t0 = max(0.0, a.t_from)
        t1 = min(dur, t0 + (a.dur if a.dur else 15.0))
    elif a.section:
        s = [x for x in secs if x[0] == a.section]
        if not s:
            raise SystemExit("sections: " + ", ".join(
                dict.fromkeys(x[0] for x in secs)))
        t0, t1 = s[0][1], s[-1][2]

    a.out = a.out.resolve()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    tmp = a.out.with_name(f".{a.out.stem}.partial{a.out.suffix}")
    codec = "png" if a.jpeg <= 0 else "mjpeg"
    # -nostats is the other half of the deadlock fix: the drain thread stops
    # the pipe filling, but there is no reason to generate a progress line
    # several times a second that nobody reads. Warnings and errors still come
    # through, and now they are actually findable in the log.
    cmd = ["ffmpeg", "-y", "-hide_banner", "-nostats", "-loglevel", "warning",
           "-f", "image2pipe", "-vcodec", codec, "-r", str(a.fps), "-i", "-"]
    if a.audio.exists():
        cmd += ["-ss", f"{t0:.4f}", "-i", str(a.audio), "-c:a", "aac",
                "-b:a", a.abr, "-shortest"]
    # This content is almost entirely smooth glow gradients on black, which is
    # the worst case for 8-bit banding — far more than detail loss, banding is
    # what will make a master look cheap. `-tune film` would smooth it further
    # and lose the beams' hard cores, so instead: a low CRF, a slow preset, and
    # psychovisual settings left alone.
    cmd += ["-c:v", "libx264", "-preset", a.preset, "-crf", str(a.crf),
            "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
            "-color_trc", "bt709", "-colorspace", "bt709",
            "-movflags", "+faststart", str(tmp)]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                          stderr=subprocess.PIPE)

    # DRAIN ffmpeg's stderr, continuously, on its own thread.
    #
    # Without this the render deadlocks. ffmpeg writes a progress line to
    # stderr several times a second; the pipe buffer is 64KB; once it fills,
    # ffmpeg blocks trying to write to it, which means it stops reading stdin,
    # which means our next frame write blocks, and both processes sit there
    # waiting for each other forever. On a short render it never fills and
    # everything looks fine — it is a bug that only appears on the long job you
    # actually care about.
    ff_log = collections.deque(maxlen=40)

    def _drain(pipe, sink):
        try:
            for line in iter(pipe.readline, b""):
                sink.append(line.decode("utf-8", "replace").rstrip())
        except Exception:                                    # noqa: BLE001
            pass
    threading.Thread(target=_drain, args=(ff.stderr, ff_log), daemon=True).start()

    # In `post` mode the page sends each finished frame to the asset server,
    # which writes it straight down ffmpeg's throat — the frames never enter
    # this process, and never touch the devtools protocol. Otherwise the
    # server is just the static server and we do the writing here.
    srv_cmd = [sys.executable, str(ROOT / "tools" / "serve.py"), str(a.port)]
    if a.capture == "post":
        srv_cmd += ["--sink", "-"]
        srv = subprocess.Popen(srv_cmd, cwd=ROOT, stdout=ff.stdin,
                               stderr=subprocess.DEVNULL)
    else:
        srv = subprocess.Popen(srv_cmd, cwd=ROOT, stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
    time.sleep(1.2)

    n = int(round((t1 - t0) * a.fps))
    started = time.time()
    try:
        with sync_playwright() as p:
            # Headless Chromium has no GPU access and silently software-
            # rasterises. For a render job a visible window is a small price
            # for a real GPU, so headed is the default.
            args = ["--disable-frame-rate-limit", "--ignore-gpu-blocklist",
                    "--enable-gpu-rasterization", "--enable-zero-copy"]
            if sys.platform == "darwin":
                args += ["--use-angle=metal"]
            if a.headless:
                args += ["--enable-unsafe-swiftshader"]
            br = p.chromium.launch(headless=bool(a.headless), args=args)
            pg = br.new_page(viewport={"width": W, "height": H})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            query = a.query.lstrip("?")
            suffix = f"?{query}" if query else ""
            pg.goto(f"http://127.0.0.1:{a.port}/{a.page}/index.html{suffix}")
            pg.wait_for_function("window.__ready===true", timeout=60000)
            gpu = pg.evaluate("window.__gpu") or "?"
            soft = "swiftshader" in gpu.lower() or "software" in gpu.lower()
            print(f"  renderer  {gpu}")
            if soft:
                print("  !! software rasteriser — every sub-frame is on the CPU.")
                print("     Drop --headless, or lower --width/--blur.")
            pg.evaluate(f"window.setRenderSize({W},{H})")
            out = pg.locator("#out")
            shot_kw = {"type": "png"} if a.jpeg <= 0 else {"type": "jpeg", "quality": a.jpeg}
            mime = "image/png" if a.jpeg <= 0 else "image/jpeg"
            q = 1.0 if a.jpeg <= 0 else a.jpeg / 100.0
            cdp = pg.context.new_cdp_session(pg) if a.capture == "cdp" else None
            clip = {"x": 0, "y": 0, "width": W, "height": H, "scale": 1}
            DATAURL_JS = (f"document.getElementById('out')"
                          f".toDataURL('{mime}',{q})")
            POST_JS = ("async () => { const c = document.getElementById('out');"
                       f" const b = await new Promise(r => c.toBlob(r,'{mime}',{q}));"
                       " await fetch('/frame', {method:'POST', body:b});"
                       " return b.size; }")

            def grab():
                """Pull one finished frame out of the page and into ffmpeg."""
                if a.capture == "post":
                    pg.evaluate(POST_JS)                    # server does the writing
                elif a.capture == "dataurl":
                    u = pg.evaluate(DATAURL_JS)
                    ff.stdin.write(base64.b64decode(u[u.index(",") + 1:]))
                elif a.capture == "cdp":
                    d = cdp.send("Page.captureScreenshot", {
                        "format": "jpeg" if a.jpeg > 0 else "png",
                        "quality": max(1, a.jpeg), "clip": clip,
                        "captureBeyondViewport": False})["data"]
                    ff.stdin.write(base64.b64decode(d))
                else:
                    ff.stdin.write(out.screenshot(**shot_kw))

            print(f"  capture   {a.capture}")

            if a.probe:
                st = time.time()
                for k in range(a.probe):
                    pg.evaluate(f"window.renderFrame({t0 + k/a.fps},{1/a.fps},{a.blur})")
                    grab()
                el = time.time() - st
                r = a.probe / el
                full = (t1 - t0) * a.fps / r / 60
                print(f"  {a.probe} frames in {el:.1f}s  =  {r:.1f} fps")
                print(f"  this span ({t1-t0:.0f}s) would take {full:.1f} min")
                # Where the time actually goes. GL calls queue asynchronously,
                # so the page forces the frame to complete before stopping the
                # clock — otherwise this would measure submission, not work.
                if pg.evaluate("typeof window.__probe === 'function'"):
                    b = pg.evaluate(f"window.__probe({t0 + 1.0},{a.blur},8)")
                    cap = max(0.0, 1000.0 / r - b["frameMs"])
                    print()
                    print(f"  per output frame at blur {a.blur}:")
                    print(f"    simulation (CPU/JS)   {b['simMs']:7.1f} ms")
                    print(f"    render     (GPU)      {b['gpuMs']:7.1f} ms")
                    print(f"    capture    (readback) {cap:7.1f} ms")
                    tot = b["simMs"] + b["gpuMs"] + cap
                    if tot > 0:
                        worst = max([("simulation", b["simMs"]), ("GPU render", b["gpuMs"]),
                                     ("frame capture", cap)], key=lambda x: x[1])
                        print(f"    -> {worst[0]} dominates "
                              f"({100*worst[1]/tot:.0f}% of the frame)")
                br.close()
                return
            for f in range(n):
                t = t0 + f / a.fps
                pg.evaluate(f"window.renderFrame({t},{1/a.fps},{a.blur})")
                grab()
                if f % (a.fps * 5) == 0:
                    el = time.time() - started
                    rate = (f + 1) / max(el, 1e-6)
                    eta = (n - f) / max(rate, 1e-6)
                    print(f"\r  {t - t0:6.1f}s / {t1 - t0:.1f}s   "
                          f"{rate:4.1f} fps   eta {eta/60:4.1f} min", end="", flush=True)
            br.close()
            if errs:
                print("\n  page errors:", errs[:3])
    finally:
        srv.terminate()
        try:
            srv.wait(timeout=5)
        except Exception:                                    # noqa: BLE001
            srv.kill()
        try:
            ff.stdin.close()
        except Exception:                                    # noqa: BLE001
            pass
        # `+faststart` rewrites the whole file to move the index to the front,
        # and x264 still has a lookahead to flush. On a 3½-minute 1080p60
        # master that is tens of seconds of apparently doing nothing, so say so.
        print("\n  encoding the tail and moving the index to the front "
              "(faststart) — this takes a moment...", flush=True)
        rc = ff.wait()
        if rc not in (0, None):
            print(f"  ffmpeg exited {rc}:")
            for line in list(ff_log)[-12:]:
                print("   ", line)

    tmp.replace(a.out)
    el = time.time() - started
    print(f"\rwrote {a.out}   {t1-t0:.2f}s   {W}x{H} @ {a.fps}fps   "
          f"blur x{a.blur}   in {el/60:.1f} min")


if __name__ == "__main__":
    main()
