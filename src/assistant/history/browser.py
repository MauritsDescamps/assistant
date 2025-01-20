import logging
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import sqlite3

logger = logging.getLogger(__name__)


def get_browser_history(include_personal: bool = False) -> list[tuple[datetime, str]]:
    browser_history_paths = []
    profiles_path = Path(
        "~/Library/Containers/com.apple.Safari/Data/Library/Safari/Profiles/"
    ).expanduser()
    for profile in profiles_path.iterdir():
        if profile.is_dir():
            browser_history_paths.append(profile / "History.db")
    if include_personal:
        browser_history_paths.append(Path("~/Library/Safari/History.db").expanduser())

    query = f"""
        SELECT 
            visit_time,
            title
        FROM 
            history_visits 
    """

    print("Processing browser history")
    unix = datetime(1970, 1, 1)  # UTC
    cocoa = datetime(2001, 1, 1)  # UTC
    delta = cocoa - unix
    result = []
    for browser_history_path in browser_history_paths:
        print(browser_history_path)
        conn = sqlite3.connect(browser_history_path)
        c = conn.cursor()
        try:
            c.execute(query)
        except sqlite3.OperationalError as e:
            print(f"Error processing {browser_history_path}: {e}")
            continue
        results = c.fetchall()
        print(f"Found {len(results)} entries in {browser_history_path}")
        for row in results:
            if row[1] is None:
                continue
            ts = datetime.fromtimestamp(int(row[0])) + delta
            ts = ts.astimezone(ZoneInfo("Europe/Brussels"))
            title = row[1]
            if not title:
                continue
            result.append((ts, "Browser: " + title))
    return result
