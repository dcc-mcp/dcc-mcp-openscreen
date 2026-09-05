from dcc_mcp_core.skill import skill_entry, skill_success
from ._client import run
@skill_entry
def main(**_): return skill_success("OpenScreen sources enumerated.", **run(["sources"]))
