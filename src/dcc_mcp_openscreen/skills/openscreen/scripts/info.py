from dcc_mcp_core.skill import skill_entry, skill_success

from ._client import path_arg, run


@skill_entry
def main(project, **_): return skill_success("OpenScreen project inspected.", **run(["info", path_arg(project)]))
