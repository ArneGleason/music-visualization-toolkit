"""Small client for the installed EffectCraft 0.18.0 stdio MCP server.

Adapted from Together Anyways' saved mcp_session.py. Work stays headless;
the user's open editor is not modified. All paths are project-local except
the machine-specific CLI location in ignored project.local.json.
"""
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import threading
import time

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "generated/animatic"
local_file = BASE / "project.local.json"
local = json.loads(local_file.read_text()) if local_file.exists() else {}
install_file = BASE.parents[1] / "out/effectcraft-0.18.0/install.json"
install = json.loads(install_file.read_text()) if install_file.exists() else {}
cli_path = (os.environ.get("EFFECTCRAFT_CLI")
            or local.get("effectcraftRuntime", {}).get("cli")
            or install.get("cli") or shutil.which("effectcraft-cli"))
if not cli_path:
    raise RuntimeError("Set up the pinned EffectCraft build; see CONTINUE-HERE.md")
CLI = Path(cli_path)


class Session:
    def __init__(self, project=None):
        self.log = (OUT / "mcp-stderr.log").open("a", encoding="utf-8")
        env = os.environ.copy()
        env["EFFECTCRAFT_FONT_DIRS"] = str(OUT / "assets")
        self.process = subprocess.Popen([str(CLI), "mcp", "--gpu"] +
            (["--project", str(project)] if project else ["--empty"]),
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.log,
            text=True, encoding="utf-8", bufsize=1, env=env)
        self.queue = queue.Queue()
        self.ident = 0
        threading.Thread(target=self.read, daemon=True).start()
        self.rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
            "clientInfo": {"name": "PhoneBookTiming", "version": "1"}})
        self.process.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
        self.process.stdin.flush()

    def read(self):
        for line in self.process.stdout:
            try:
                self.queue.put(json.loads(line))
            except ValueError:
                continue

    def rpc(self, method, params):
        self.ident += 1
        ident = self.ident
        self.process.stdin.write(json.dumps({"jsonrpc": "2.0", "id": ident,
            "method": method, "params": params}, ensure_ascii=False) + "\n")
        self.process.stdin.flush()
        deadline = time.monotonic() + 120
        while True:
            result = self.queue.get(timeout=max(.1, deadline - time.monotonic()))
            if result.get("id") == ident:
                if "error" in result:
                    raise RuntimeError(result["error"])
                return result["result"]

    def call(self, name, arguments=None):
        result = self.rpc("tools/call", {"name": name, "arguments": arguments or {}})
        if result.get("isError"):
            raise RuntimeError(result)
        texts = [v["text"] for v in result.get("content", []) if v.get("type") == "text"]
        if len(texts) == 1:
            try:
                return json.loads(texts[0])
            except ValueError:
                pass
        return result

    def command(self, command, params=None):
        return self.call("execute_command", {"command": command, "params": params or {}})

    def close(self):
        self.process.stdin.close()
        try:
            self.process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            self.process.wait()
        self.log.close()
