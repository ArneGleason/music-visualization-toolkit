"""Align an explicitly reviewed phrase plan locally; keep acoustic word edges."""
import argparse
import json
import pathlib
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=pathlib.Path)
    args = parser.parse_args()
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from timeline import load_project
    project, base = load_project(args.project)
    sys.path.insert(0, project["alignmentRuntime"]["extensions"])
    import torch
    import whisper
    import stable_whisper
    torch.set_num_threads(6)
    runtime = project["alignmentRuntime"]
    model = stable_whisper.load_model(runtime["model"], device="cuda",
                                      download_root=runtime["modelCache"])
    audio = whisper.load_audio(project["sources"]["leadRenaissance"])
    offset = project["vocalOrigin"]["masterSeconds"]
    plan = base / "generated" / "transcription" / "phrase-plan.json"
    rows = json.loads(plan.read_text(encoding="utf-8"))
    results = []
    for row in rows:
        a = max(0, row["window"][0] - offset)
        b = row["window"][1] - offset
        result = model.align(audio[int(a*16000):int(b*16000)], row["text"],
                             language="en", regroup=False, word_dur_factor=None,
                             max_word_dur=None, nonspeech_skip=None, verbose=None)
        words = []
        if result:
            for segment in result.to_dict()["segments"]:
                for word in segment["words"]:
                    words.append({"text": word["word"].strip(),
                                  "sourceStart": word["start"] + a,
                                  "sourceEnd": word["end"] + a,
                                  "start": word["start"] + a + offset,
                                  "end": word["end"] + a + offset,
                                  "probability": word.get("probability")})
        results.append({**row, "words": words, "alignment": "stable-ts/large-v3-turbo"})
        print(row["id"], len(words), flush=True)
    (plan.parent / "phrases.aligned.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
