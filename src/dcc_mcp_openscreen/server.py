"""Standalone OpenScreen MCP adapter."""
from __future__ import annotations
import argparse, os, signal, threading
from pathlib import Path
from dcc_mcp_core import DccServerOptions
from dcc_mcp_core.server_base import DccServerBase
class OpenScreenMcpServer(DccServerBase):
    def __init__(self, *, port: int | None = None):
        options = DccServerOptions.from_env("openscreen", Path(__file__).parent / "skills", port=port, server_name="dcc-mcp-openscreen", instance_type="standalone", adapter_version="0.1.0", standalone_main_thread=False)
        super().__init__(options=options)
def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("--mcp-port", type=int); a=p.parse_args(argv)
    server=OpenScreenMcpServer(port=a.mcp_port); server.register_builtin_actions(); server.start()
    stopped=threading.Event(); signal.signal(signal.SIGINT, lambda *_: stopped.set())
    if hasattr(signal,"SIGTERM"): signal.signal(signal.SIGTERM, lambda *_: stopped.set())
    try: stopped.wait()
    finally: server.stop()
