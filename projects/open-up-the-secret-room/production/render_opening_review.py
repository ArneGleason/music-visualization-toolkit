"""Render the opening excerpt from the canonical shotlist and a conceptual map."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]


def run(args):
    subprocess.run(args, check=True)


def concept_map(path):
    image = Image.new("RGB", (1440, 1080), "#111b24")
    draw = ImageDraw.Draw(image)
    font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    font = ImageFont.truetype(font_path, 24)
    small = ImageFont.truetype(font_path, 20)
    title = ImageFont.truetype(font_path, 36)
    draw.text((60, 30), "SECRET ROOM / proposed entrance journey", font=title, fill="#f4e7ce")
    draw.text((60, 82), "Conceptual plan, not to scale. Interior beyond the arch is a proposal.", font=small, fill="#b3c2ca")
    boxes = [
        (70, 150, 510, 260, "1  Wreck in breach cavern", "Original shot S14-SH03"),
        (70, 320, 510, 450, "2  Statue + entrance arch", "Original S14-SH04 / amber activation"),
        (70, 520, 510, 670, "3  Empty entrance hall", "NEXT VIEW: ribs, alcoves, guide lights"),
        (660, 520, 1080, 670, "4  Screened turn / descent", "Breaks direct sightline into the city"),
        (660, 760, 1080, 910, "5  Inner city overlook", "First reveal of working civilization"),
    ]
    for x1, y1, x2, y2, name, note in boxes:
        draw.rounded_rectangle((x1, y1, x2, y2), radius=14, fill="#243440", outline="#b39a6a", width=3)
        draw.text((x1+20, y1+25), name, font=font, fill="#f4e7ce")
        draw.text((x1+20, y1+68), note, font=small, fill="#b3c2ca")
    for start, end in [((290, 260), (290, 320)), ((290, 450), (290, 520)), ((510, 595), (660, 595)), ((870, 670), (870, 760))]:
        draw.line((start, end), fill="#e8b95d", width=5)
        x, y = end
        points = [(x, y), (x-12, y-18), (x+12, y-18)] if start[0] == x else [(x, y), (x-18, y-12), (x-18, y+12)]
        draw.polygon(points, fill="#e8b95d")
    draw.text((660, 180), "REVEAL RULE", font=font, fill="#e8b95d")
    for i, line in enumerate(["No inhabitants at the entrance.", "Activation suggests concealed intelligence.", "Architecture obscures the deeper settlement.", "Working city revealed only farther inside.", "Help follows recognition of compatible aims."]):
        draw.text((660, 225+i*38), line, font=small, fill="#e0e5e5")
    draw.text((70, 735), "Third-frame camera proposal:", font=font, fill="#e8b95d")
    for i, line in enumerate(["Just inside the arch, behind the pair.", "Carry the existing warm arch light inward.", "Show an empty antechamber and a turn,", "not an immediate populated panorama."]):
        draw.text((70, 780+i*32), line, font=small, fill="#e0e5e5")
    draw.text((60, 1000), "Amber arrows = journey. Boxes describe connections, not surveyed exterior geometry.", font=small, fill="#b3c2ca")
    image.save(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', type=int, default=2)
    parser.add_argument('--shotlist', type=Path, default=BASE / 'shots/shotlist.json')
    args = parser.parse_args()
    version = f'v{args.version:03d}'
    OUT = BASE / 'generated/wip/previews/opening-reuse' / version
    OUT.mkdir(parents=True, exist_ok=True)
    score_path = args.shotlist
    score = json.loads(score_path.read_text())
    snapshot = BASE / 'production' / f'opening-reuse-{version}' / 'shotlist.json'
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    snapshot.write_text(json.dumps(score, indent=2)+'\n')
    fps = score["fps"]
    inputs, filters, hashes = [], [], {}
    end = 0
    for i, shot in enumerate(score["shots"]):
        assert shot["startFrame"] == end
        assert shot["frames"] == shot["endFrameExclusive"] - shot["startFrame"]
        source = (BASE / shot.get("videoSource", shot["starterImage"])).resolve()
        if shot.get("videoSource"):
            probe = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=nb_frames,r_frame_rate", "-of", "json", str(source)], text=True))["streams"][0]
            assert probe["r_frame_rate"] == f"{fps}/1"
            first = shot["videoEdit"]["sourceInFrame"]
            assert first + shot["frames"] <= int(probe["nb_frames"])
            inputs += ["-i", str(source)]
        else:
            first = 0
            inputs += ["-loop", "1", "-framerate", str(fps), "-i", str(source)]
        filters.append(f"[{i}:v]trim=start_frame={first}:end_frame={first+shot['frames']},setpts=PTS-STARTPTS,scale=1278:720,pad=1280:720:1:0,setsar=1[v{i}]")
        hashes[shot["id"]] = hashlib.sha256(source.read_bytes()).hexdigest()
        end = shot["endFrameExclusive"]
    filters.append("".join(f"[v{i}]" for i in range(len(score["shots"]))) + f"concat=n={len(score['shots'])}:v=1:a=0[v]")
    master = BASE / "generated/source/master.wav"
    output = OUT / f"Secret-Room-opening-reuse-{version}.mp4"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs, "-i", str(master), "-filter_complex", ";".join(filters), "-map", "[v]", "-map", f"{len(score['shots'])}:a:0", "-frames:v", str(end), "-t", str(end/fps), "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(output)])
    result = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,nb_frames,width,height,r_frame_rate", "-of", "json", str(output)], text=True))
    video = next(s for s in result["streams"] if s["codec_type"] == "video")
    assert int(video["nb_frames"]) == end and video["r_frame_rate"] == "24/1"
    assert any(s["codec_type"] == "audio" for s in result["streams"])
    samples = sorted({frame for shot in score['shots'] for frame in (shot['startFrame'], shot['endFrameExclusive']-1)})
    selection = '+'.join(f'eq(n,{frame})' for frame in samples)
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(output), "-vf", f"select='{selection}',scale=512:-1,tile=2x{len(score['shots'])}", "-frames:v", "1", str(OUT / "review-frames.jpg")])
    concept_map(OUT / "entrance-map.png")
    receipt = {"frames": end, "fps": fps, "scope": "opening excerpt only", "shotlistSHA256": hashlib.sha256(score_path.read_bytes()).hexdigest(), "sourceSHA256": hashes, "masterSHA256": hashlib.sha256(master.read_bytes()).hexdigest(), "probe": result}
    (OUT / "receipt.json").write_text(json.dumps(receipt, indent=2)+"\n")
    (OUT / ".disposable").write_text(f"Reproduce from retained source MP4s, master, shotlist snapshot and script:\n./.venv/bin/python3 projects/open-up-the-secret-room/production/render_opening_review.py --version {args.version} --shotlist {str(snapshot.relative_to(ROOT))}\n")
    print(output)


if __name__ == "__main__":
    main()
