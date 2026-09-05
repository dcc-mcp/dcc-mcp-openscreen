"""Safe subprocess wrapper for the OpenScreen CLI."""
from __future__ import annotations
import json, os, subprocess
from pathlib import Path

def executable() -> str:
    value=os.getenv("DCC_MCP_OPENSCREEN_PATH", "openscreen")
    return value

def run(args: list[str], *, timeout: float = 900.0) -> dict:
    proc=subprocess.run([executable(), *args, "--json"], capture_output=True, text=True, timeout=timeout, check=False)
    events=[]
    for line in proc.stdout.splitlines():
        try: events.append(json.loads(line))
        except json.JSONDecodeError: continue
    done=next((e for e in reversed(events) if e.get("event")=="done"), None)
    if proc.returncode != 0 or not done or done.get("success") is False:
        raise RuntimeError((proc.stderr or "OpenScreen command failed").strip()[-2000:])
    return done

def path_arg(value: str) -> str:
    p=Path(value).expanduser().resolve()
    if len(str(p))>4096: raise ValueError("path too long")
    return str(p)
