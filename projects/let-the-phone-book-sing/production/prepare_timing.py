"""Prepare source-clock vocal proxies; preserve the original files and DAW.

The stems start at project beat 7.620844841. Independent waveform correlation
against the confirmed master places its zero at beat 7, within 0.074 ms on
the lead. The original stems are PCM16 while the master is PCM24, so decode
working copies explicitly instead of assuming equal sample widths.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import wave
import zipfile

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from dawproject import parse_tempo, read_project_xml


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main():
    source = BASE / "generated/source/Let-the-Phone-Book-Sing-current.dawproject"
    root = read_project_xml(source)
    curve = parse_tempo(root)
    names = {e.get("id"): e.get("name") for e in root.iter("Track")}
    zero, origin = 7.0, 7.620844841003418
    offset = curve.sec(origin) - curve.sec(zero)
    with wave.open(str(BASE / "generated/source/master.wav"), "rb") as wav:
        rate, frames = wav.getframerate(), wav.getnframes()
    shift, stride = round(offset * rate), 6
    reports = []
    for role, name in [("lead", "Lead Vocal"), ("backing", "Backing Vocals")]:
        lane = next(e for e in root.iter("Lanes") if names.get(e.get("track")) == name)
        original = BASE / f"generated/source/{role}-original.wav"
        if not original.exists():
            member = lane.find(".//Audio/File").get("path")
            with zipfile.ZipFile(source) as archive:
                original.write_bytes(archive.read(member))
        decoded = subprocess.run(
            ["ffmpeg", "-v", "error", "-i", str(original), "-ac", "2", "-ar",
             str(rate), "-f", "s24le", "-"], capture_output=True, check=True).stdout
        output = bytearray(frames * stride)
        windows = []
        for clip in lane.findall("./Clips/Clip"):
            if clip.get("enable") != "true":
                continue
            start_beat = float(clip.get("time"))
            assert abs(start_beat - float(clip.get("playStart", "0")) - origin) < 1e-5
            start = curve.sec(start_beat) - curve.sec(zero)
            end = curve.sec(start_beat + float(clip.get("duration"))) - curve.sec(zero)
            a = max(shift, 0, round(start * rate))
            b = min(frames, round(end * rate), len(decoded) // stride + shift)
            if b > a:
                sa = a - shift
                output[a * stride:b * stride] = decoded[sa * stride:(sa + b - a) * stride]
            windows.append([start, end])
        target = BASE / f"generated/transcription/{role}-active-master-clock.wav"
        with wave.open(str(target), "wb") as wav:
            wav.setparams((2, 3, rate, 0, "NONE", "not compressed"))
            wav.writeframes(output)
        reports.append({"role": role, "sourceOffsetInMaster": offset,
                        "roundedPadSamples": shift, "enabledMasterWindows": windows,
                        "workingFile": target.relative_to(BASE).as_posix(),
                        "limitations": "Enabled-clip mask and sample-rounded pad; track devices and clip fades are not recreated. Master remains listening authority."})
    write(BASE / "generated/transcription/vocal-source-provenance.json", reports)
    config = json.loads((BASE / "project.json").read_text(encoding="utf-8"))
    config["timing"]["zeroBeat"] = zero
    config["sources"].update(lead="generated/transcription/lead-active-master-clock.wav",
                             backing="generated/transcription/backing-active-master-clock.wav")
    config["production"].update(stage="timing-and-lyric-alignment",
        timingStatus="ZeroBeat 7 verified by source/master waveform correlation; exact grid import follows.")
    write(BASE / "project.json", config)
    report = {"zeroBeat": zero, "stemOriginBeat": origin,
              "sourceOffsetInMasterSeconds": offset, "measuredLeadOffsetSeconds": 0.423625,
              "leadResidualMs": (0.423625 - offset) * 1000,
              "verification": "Five lead windows from 20 to 163 seconds agree at 8 kHz, with bass and rhythm-guitar crosschecks. Phase correlation, not listening certification.",
              "tempoPoints": len(curve.pts),
              "tempoRange": [min(v for _, v, _ in curve.pts), max(v for _, v, _ in curve.pts)],
              "timeSignature": [4, 4], "sourceMasterSampleFrames": frames,
              "vocalWorkingCopies": reports}
    write(BASE / "generated/alignment-check/timing-origin.json", report)
    manifest = json.loads((BASE / "source-manifest.json").read_text(encoding="utf-8"))
    manifest["sources"] = [r for r in manifest["sources"] if r["id"] != "dawproject"]
    with source.open("rb") as stream:
        sha = hashlib.file_digest(stream, "sha256").hexdigest()
    manifest["sources"].append({"id": "dawproject", "path": source.relative_to(BASE).as_posix(),
        "bytes": source.stat().st_size, "sha256": sha, "status": "user_supplied_current_export"})
    write(BASE / "source-manifest.json", manifest)
    print(json.dumps({k: v for k, v in report.items() if k != "vocalWorkingCopies"}, indent=2))


if __name__ == "__main__":
    main()
