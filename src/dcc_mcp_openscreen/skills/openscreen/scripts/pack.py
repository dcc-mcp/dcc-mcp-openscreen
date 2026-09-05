from dcc_mcp_core.skill import skill_entry, skill_success
from ._client import run, path_arg
@skill_entry
def main(project, output, **_): return skill_success("OpenScreen project packed.", **run(["pack", path_arg(project), "--out", path_arg(output)], timeout=600))
