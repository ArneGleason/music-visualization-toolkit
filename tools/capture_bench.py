#!/usr/bin/env python3
"""
Find the cheapest way to get a rendered frame out of the browser.

    ./.venv/bin/python3 tools/capture_bench.py            # the laser page
    ./.venv/bin/python3 tools/capture_bench.py --page world

The probe showed the M4 Pro rendering a frame in 3.2ms and the pipeline
spending 45.7ms photographing it — so the capture path, not the GPU, sets the
render time. This times every way of getting the pixels out, on the real
machine, and says which one to use.

The candidates, roughly in order of how much machinery they go through:

  element.screenshot   what the renderer does today. Playwright asks devtools
                       to capture the page, crop to the element, encode, and
                       return the bytes base64 over the debugger socket.
  page.screenshot      the same, with the clip given directly — skips the
                       element bookkeeping.
  cdp captureScreenshot   the raw devtools call, no Playwright wrapper.
  toDataURL            the page encodes its own canvas and hands back a
                       string. No page capture, no compositor — but still
                       base64 through the debugger.
  POST to serve.py     the page encodes to a Blob and posts it to the server
                       already running for the assets. Same origin, so no
                       preflight; binary the whole way; never touches the
                       debugger protocol at all.

Every method captures the identical frame, and the sizes are printed so you
can see what quality you are paying for.
"""
from __future__ import annotations

import argparse
import base64
import pathlib
import subprocess
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT  # noqa: E402

REPS = 12


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--page", default="stage", choices=["stage", "world"])
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--blur", type=int, default=8)
    ap.add_argument("--at", type=float, default=96.0, help="time in the song")
    ap.add_argument("--port", type=int, default=8756)
    ap.add_argument("--headless", action="store_true",
                    help="no window — software GL, for smoke-testing only")
    a = ap.parse_args()

    from playwright.sync_api import sync_playwright

    W = a.width
    H = int(W * 9 / 16) // 2 * 2
    srv = subprocess.Popen([sys.executable, str(ROOT / "tools" / "serve.py"),
                            str(a.port), "--sink", "/dev/null"],
                           cwd=ROOT, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
    time.sleep(1.2)

    rows = []
    try:
        with sync_playwright() as p:
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
            pg.goto(f"http://127.0.0.1:{a.port}/{a.page}/index.html")
            pg.wait_for_function("window.__ready===true", timeout=60000)
            print(f"  renderer  {pg.evaluate('window.__gpu')}")
            print(f"  frame     {W}x{H}, blur {a.blur}\n")
            pg.evaluate(f"window.setRenderSize({W},{H})")
            for k in range(12):
                pg.evaluate(f"window.setTime({a.at - 0.4 + k * 0.03},0.03)")
            pg.evaluate(f"window.renderFrame({a.at},{1/60},{a.blur})")

            out = pg.locator("#out")
            cdp = pg.context.new_cdp_session(pg)
            clip = {"x": 0, "y": 0, "width": W, "height": H, "scale": 1}

            def bench(label, fn):
                fn()                                   # warm
                st = time.time()
                n = 0
                for _ in range(REPS):
                    n = fn()
                el = (time.time() - st) / REPS * 1000
                rows.append((label, el, n))
                print(f"    {label:34s} {el:7.1f} ms   {n/1024:7.0f} KB")

            print("  capture methods")
            bench("element.screenshot jpeg 94",
                  lambda: len(out.screenshot(type="jpeg", quality=94)))
            bench("page.screenshot jpeg 94 clip",
                  lambda: len(pg.screenshot(type="jpeg", quality=94, clip=clip)))
            bench("cdp captureScreenshot jpeg 94",
                  lambda: len(base64.b64decode(cdp.send("Page.captureScreenshot", {
                      "format": "jpeg", "quality": 94, "clip": clip,
                      "captureBeyondViewport": False})["data"])))
            bench("toDataURL jpeg 0.94",
                  lambda: len(pg.evaluate(
                      "document.getElementById('out').toDataURL('image/jpeg',0.94)")))
            bench("toDataURL webp 0.92",
                  lambda: len(pg.evaluate(
                      "document.getElementById('out').toDataURL('image/webp',0.92)")))
            bench("POST blob jpeg 0.94  (same origin)",
                  lambda: pg.evaluate("""async () => {
                      const c = document.getElementById('out');
                      const b = await new Promise(r =>
                          c.toBlob(r, 'image/jpeg', 0.94));
                      await fetch('/frame', {method: 'POST', body: b});
                      return b.size;
                  }"""))
            bench("POST blob webp 0.92  (same origin)",
                  lambda: pg.evaluate("""async () => {
                      const c = document.getElementById('out');
                      const b = await new Promise(r =>
                          c.toBlob(r, 'image/webp', 0.92));
                      await fetch('/frame', {method: 'POST', body: b});
                      return b.size;
                  }"""))

            print("\n  render cost for comparison")
            if pg.evaluate("typeof window.__probe === 'function'"):
                b = pg.evaluate(f"window.__probe({a.at},{a.blur},8)")
                print(f"    {'simulation + GPU render':34s} "
                      f"{b['simMs'] + b['gpuMs']:7.1f} ms")
                floor = b["simMs"] + b["gpuMs"]
            else:
                floor = 0.0
            br.close()
            if errs:
                print("  page errors:", errs[:2])
    finally:
        srv.terminate()

    if rows:
        rows.sort(key=lambda r: r[1])
        best, ms, _ = rows[0]
        cur = next((r[1] for r in rows if r[0].startswith("element.screenshot")), ms)
        print(f"\n  fastest: {best}  ({ms:.1f} ms)")
        print(f"  that is {cur/max(ms,1e-6):.1f}x quicker than what the renderer "
              f"uses now ({cur:.1f} ms)")
        total = ms + floor
        print(f"  a frame would cost about {total:.1f} ms  ->  {1000/total:.0f} fps")
        print(f"  the 3:41 song at 60fps: {221*60*total/1000/60:.0f} min")


if __name__ == "__main__":
    main()
