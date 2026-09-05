# dcc-mcp-openscreen

Standalone DCC-MCP adapter for [OpenScreen](https://github.com/getopenscreen/openscreen).

The adapter exposes only typed, bounded CLI operations. Set `DCC_MCP_OPENSCREEN_PATH` when the executable is not on `PATH`. It does not automate the desktop UI; DCC window selection and unsupported UI actions remain owned by `dcc-cua` / `ui-control`.

## Run

```powershell
python -m pip install -e .
dcc-mcp-openscreen
```

Tools: `openscreen__sources`, `openscreen__record`, and `openscreen__export`.

## License

MIT
