from dcc_mcp_core.skill import skill_entry, skill_success
from ._client import run, path_arg
@skill_entry
def main(project, min_words=2, max_words=7, **_): return skill_success("OpenScreen captions generated.", **run(["captions", path_arg(project), "--min-words", str(min_words), "--max-words", str(max_words)], timeout=1800))
