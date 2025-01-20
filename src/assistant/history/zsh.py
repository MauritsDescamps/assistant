import os
from pathlib import Path
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

ZSH_HISTORY_PATH = Path(os.environ["HOME"]) / ".config/zsh/.zsh_history"


def get_zsh_history() -> list[tuple[datetime, str]]:
    result = []
    with open(ZSH_HISTORY_PATH, "r", encoding="latin-1") as f:
        # example:
        # : 1730900933:0;ls -la  /home/mdescamps/miniconda3/envs/yanomaly_algo/bin
        # : 1730902698:0;cd /home/mdescamps/.vscode-server/extensions/ms-python.debugpy-2024.12.0-linux-x64/bundled/libs/debugpy/adapt\
        # er/../../debugpy
        # split on newlines followed by ': '
        lines = f.read().split("\n: ")
        lines[0] = lines[0][2:]  # remove leading ': '
        for line in lines:
            line = line.strip()
            if line:
                ts, rest = line.split(":", 1)
                command = rest.split(";", 1)[1].strip()
                command = command.strip()
                dt_ts = datetime.fromtimestamp(int(ts), tz=timezone.utc)
                dt_ts = dt_ts.astimezone(ZoneInfo("Europe/Brussels"))
                result.append((dt_ts, command))
    return result
