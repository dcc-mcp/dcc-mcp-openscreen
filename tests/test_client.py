"""Executable CLI protocol and Windows background process regressions."""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture
def client():
    path = (
        Path(__file__).parents[1]
        / "src/dcc_mcp_openscreen/skills/openscreen/scripts/_client.py"
    )
    spec = importlib.util.spec_from_file_location("openscreen_cli_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.skipif(os.name != "nt", reason="Windows console contract")
def test_run_preserves_json_without_allocating_console(client, monkeypatch):
    monkeypatch.setattr(client, "executable", lambda: sys.executable)
    code = "import ctypes,json;print(json.dumps(dict(event='done',success=True,console=ctypes.windll.kernel32.GetConsoleWindow(),result=6*7)))"
    assert client.run(["-c", code], timeout=10) == {
        "event": "done",
        "success": True,
        "console": 0,
        "result": 42,
    }


def test_nonzero_failure_preserves_stderr(client, monkeypatch):
    monkeypatch.setattr(client, "executable", lambda: sys.executable)
    with pytest.raises(RuntimeError, match="openscreen failure"):
        client.run(
            [
                "-c",
                "import sys;print('openscreen failure',file=sys.stderr);sys.exit(7)",
            ],
            timeout=10,
        )


@pytest.mark.skipif(os.name != "nt", reason="Windows console contract")
def test_record_sends_cooperative_stop_without_allocating_console(client, monkeypatch):
    real_spawn = subprocess.Popen
    code = (
        "import ctypes,json,sys; message=sys.stdin.readline().strip(); "
        "print(json.dumps(dict(event='done',success=True,received=message,console=ctypes.windll.kernel32.GetConsoleWindow())))"
    )

    def spawn(argv, **kwargs):
        assert argv[1] == "record"
        return real_spawn([sys.executable, "-c", code], **kwargs)

    monkeypatch.setattr(client.subprocess, "Popen", spawn)
    assert client.record([], duration=0, timeout=10) == {
        "event": "done",
        "success": True,
        "received": "stop",
        "console": 0,
    }


@pytest.mark.skipif(os.name != "nt", reason="Windows process cleanup contract")
@pytest.mark.parametrize("failure", ["nonzero", "timeout", "missing"])
def test_record_cleanup_failure_still_reaps_owned_root(client, monkeypatch, failure):
    real_spawn = subprocess.Popen
    children = []

    class Child:
        def __init__(self, **kwargs):
            self.process = real_spawn(
                [sys.executable, "-c", "import time;time.sleep(60)"], **kwargs
            )
            children.append(self.process)
            self.first_wait = True

        def __getattr__(self, name):
            return getattr(self.process, name)

        def communicate(self, timeout):
            if self.first_wait:
                self.first_wait = False
                raise subprocess.TimeoutExpired("record", timeout)
            return self.process.communicate(timeout=timeout)

    def cleanup(argv, **kwargs):
        assert argv[0] == "taskkill"
        if failure == "timeout":
            raise subprocess.TimeoutExpired(argv, 5)
        if failure == "missing":
            raise FileNotFoundError("taskkill unavailable")
        return subprocess.CompletedProcess(argv, 1, "", "taskkill refused")

    monkeypatch.setattr(
        client.subprocess, "Popen", lambda argv, **kwargs: Child(**kwargs)
    )
    monkeypatch.setattr(client.subprocess, "run", cleanup)
    try:
        with pytest.raises(RuntimeError, match="process-tree cleanup failed"):
            client.record([], duration=0, timeout=10)
        assert children[0].poll() is not None
    finally:
        for process in children:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=5)
