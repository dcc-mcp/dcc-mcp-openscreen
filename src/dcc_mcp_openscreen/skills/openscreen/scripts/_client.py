from __future__ import annotations
import json, os, subprocess, time
from pathlib import Path

def executable() -> str:
    return os.getenv("DCC_MCP_OPENSCREEN_PATH", "openscreen")

def _events(stdout: str) -> list[dict]:
    out=[]
    for line in stdout.splitlines():
        try: out.append(json.loads(line))
        except json.JSONDecodeError: pass
    return out

def run(args: list[str], *, timeout: float = 900.0) -> dict:
    try:
        proc=subprocess.run([executable(), *args, "--json"], capture_output=True, text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"OpenScreen CLI timed out after {timeout:.0f}s; verify permissions and headless build") from exc
    return _finish(proc.returncode, proc.stdout, proc.stderr)

def record(args: list[str], *, duration: int, timeout: float) -> dict:
    proc=subprocess.Popen([executable(), "record", *args, "--json"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        time.sleep(duration)
        if proc.poll() is None and proc.stdin:
            proc.stdin.write("stop\n"); proc.stdin.flush()
        stdout, stderr=proc.communicate(timeout=max(10.0, timeout-duration))
    except subprocess.TimeoutExpired as exc:
        proc.kill(); proc.communicate()
        raise RuntimeError("OpenScreen recording did not stop after a cooperative stop request") from exc
    return _finish(proc.returncode, stdout, stderr)

def _finish(code: int, stdout: str, stderr: str) -> dict:
    events=_events(stdout)
    done=next((e for e in reversed(events) if e.get("event")=="done"), None)
    if code != 0 or not done or done.get("success") is False:
        detail=(stderr or "OpenScreen command failed").strip()
        if not events and not detail: detail="OpenScreen produced no JSON events; verify a headless-capable build"
        raise RuntimeError(detail[-2000:])
    return done

def path_arg(value: str) -> str:
    path=Path(value).expanduser().resolve()
    if len(str(path))>4096: raise ValueError("path too long")
    return str(path)
