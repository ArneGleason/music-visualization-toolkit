"""Local dictation worker; called by the listening-notes server."""
import json
import pathlib
import sys

project_file, audio_file = map(pathlib.Path, sys.argv[1:3])
config = json.loads(project_file.with_name("project.local.json").read_text(encoding="utf-8"))
runtime = config["alignmentRuntime"]
sys.path.insert(0, runtime["extensions"])
import torch
import whisper
torch.set_num_threads(4)
model = whisper.load_model("small", device="cuda", download_root=runtime["modelCache"])
result = model.transcribe(str(audio_file), language="en", temperature=0, verbose=None)
print(json.dumps({"text": result["text"].strip()}))
