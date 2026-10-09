from dcc_mcp_core.skill import skill_entry, skill_success

from ._client import path_arg, run


@skill_entry
def main(project, output, **_): return skill_success("OpenScreen project packed.", **run(["pack", path_arg(project), "--out", path_arg(output)], timeout=600))
