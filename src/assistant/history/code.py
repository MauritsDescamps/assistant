from pathlib import Path
import json
from datetime import datetime, timezone, date
from zoneinfo import ZoneInfo

APP_SUPPORT_PATH = Path("~/Library/Application Support").expanduser()
VSCODE_HISTORY_PATH = APP_SUPPORT_PATH / "Code/User/History"
CURSOR_HISTORY_PATH = APP_SUPPORT_PATH / "Cursor/User/history"
paths = [VSCODE_HISTORY_PATH, CURSOR_HISTORY_PATH]


def get_code_history(date: date = None) -> list[tuple[datetime, str]]:
    result = []
    for path in paths:
        for sub_dir in path.iterdir():
            if sub_dir.is_dir():
                # open entries.json
                entries_file = sub_dir / "entries.json"
                if entries_file.exists():
                    with open(entries_file, "r") as f:
                        data = json.load(f)
                    for entry in data["entries"]:
                        dt_ts = datetime.fromtimestamp(
                            entry["timestamp"] / 1000, tz=timezone.utc
                        )
                        dt_ts = dt_ts.astimezone(ZoneInfo("Europe/Brussels"))
                        if date and dt_ts.date() != date:
                            continue
                        result.append((dt_ts, data["resource"]))
    return result
