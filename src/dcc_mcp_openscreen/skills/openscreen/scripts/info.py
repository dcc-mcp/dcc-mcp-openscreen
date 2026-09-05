from dcc_mcp_core.skill import skill_entry, skill_success
from ._client import run, path_arg
@skill_entry
def main(project, **_): return skill_success("OpenScreen project inspected.", **run(["info", path_arg(project)]))
