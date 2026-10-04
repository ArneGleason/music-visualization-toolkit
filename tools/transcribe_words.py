"""Run local, unprompted Whisper; preserve raw word timestamps for review."""
import argparse
import json
import pathlib
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=pathlib.Path)
    parser.add_argument("--roles", nargs="+", default=["leadRenaissance", "audio"])
    args = parser.parse_args()
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from timeline import load_project
    project, base = load_project(args.project)
    runtime = project["alignmentRuntime"]
    sys.path.insert(0, runtime["extensions"])
    import torch
    import whisper
    torch.set_num_threads(6)
    model = whisper.load_model(runtime["model"], device="cuda",
                               download_root=runtime["modelCache"])
    out = base / "generated" / "transcription"
    out.mkdir(parents=True, exist_ok=True)
    for role in args.roles:
        target = out / f"{role}.whisper.raw.json"
        if target.exists():
            print("Retaining existing", target.name, flush=True)
            continue
        source = pathlib.Path(project["sources"][role])
        if not source.is_absolute():
            source = base / source
        start = time.monotonic()
        print("Transcribing", role, flush=True)
        result = model.transcribe(str(source), language="en", word_timestamps=True,
                                  condition_on_previous_text=False, temperature=0,
                                  verbose=False)
        result["provenance"] = {"source": str(source), "model": runtime["model"],
                                "prompted": False, "clock": "source_seconds"}
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(role, round(time.monotonic()-start, 1), result["text"], flush=True)


if __name__ == "__main__":
    main()
