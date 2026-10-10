# dcc-mcp-openscreen

Standalone DCC-MCP adapter for [OpenScreen](https://github.com/getopenscreen/openscreen).

The adapter exposes only typed, bounded CLI operations. Set `DCC_MCP_OPENSCREEN_PATH` when the executable is not on `PATH`. It does not automate the desktop UI; DCC window selection and unsupported UI actions remain owned by `dcc-cua` / `ui-control`.

<!-- dcc-mcp-coverage-pointer:start -->
<!-- Generated from dcc-mcp-catalog.yml by scripts/generate_adapter_pointer.py in dcc-mcp/dcc-mcp-core. Do not edit by hand. -->
## Part of the DCC-MCP host matrix

**dcc-mcp-openscreen** — OpenScreen adapter for DCC-MCP — capture discovery, screen
recording and video export workflows through typed CLI operations.

It is one of **47 host adapters** in the DCC-MCP catalog. Every adapter speaks the same
MCP protocol and builds on the same core runtime contract; each one exposes the tools
its own host needs on top of that.

- [All host adapters and install metadata](https://dcc-mcp.github.io/ecosystem)
- [Host matrix on the core README](https://github.com/dcc-mcp/dcc-mcp-core#readme)
- [Showcase](https://dcc-mcp.github.io/showcase)

This block is generated from the catalog entry in
[`dcc-mcp-catalog.yml`](https://github.com/dcc-mcp/dcc-mcp-core/blob/main/dcc-mcp-catalog.yml).
Re-run the generator after changing the catalog.
<!-- dcc-mcp-coverage-pointer:end -->

## Run

```powershell
python -m pip install -e .
dcc-mcp-openscreen
```

Tools: `openscreen__sources`, `openscreen__record`, and `openscreen__export`.

## License

MIT
