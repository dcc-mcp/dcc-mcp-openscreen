from dcc_mcp_core.skill import skill_entry, skill_success
from ._client import run, path_arg
@skill_entry
def main(project, output=None, quality="source", **_):
    args=["export",path_arg(project),"--quality",quality]
    if output: args += ["--out",path_arg(output)]
    return skill_success("OpenScreen export completed.", **run(args, timeout=1800))
