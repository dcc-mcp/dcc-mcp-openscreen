from dcc_mcp_openscreen.server import OpenScreenMcpServer

def test_server_constructs():
    server = OpenScreenMcpServer(port=0)
    assert server is not None
