from dcc_mcp_core.skill import skill_entry, skill_success
from ._client import run, path_arg
@skill_entry
def main(duration=30, window=None, display=0, project=None, mic=False, system_audio=False, **_):
    if not isinstance(duration,int) or duration<1 or duration>3600: raise ValueError("duration must be 1..3600 seconds")
    args=["record","--duration",str(duration),"--display",str(display)]
    if window: args += ["--window", str(window)]
    if project: args += ["--project", path_arg(project)]
    if mic: args += ["--mic"]
    if system_audio: args += ["--system-audio"]
    return skill_success("OpenScreen recording completed.", **run(args, timeout=duration+120))
