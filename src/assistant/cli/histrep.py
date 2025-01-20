#!/usr/bin/env python3

from pathlib import Path
import datetime
import argparse
import cmd
from signal import signal, SIGPIPE, SIG_DFL

import pandas as pd
import langchain

from assistant.history import get_zsh_history, get_browser_history, get_code_history


def main():
    signal(SIGPIPE, SIG_DFL)

    # parse command line arguments
    parser = argparse.ArgumentParser(
        description="Generate a report of VSCode editor history"
    )
    parser.add_argument(
        "--days", "-d", type=int, default=31, help="Number of days to display"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    parser.add_argument(
        "--with-commands", "-c", action="store_true", help="Include command history"
    )
    parser.add_argument(
        "--include-personal", "-p", action="store_true", help="Include personal history"
    )

    args = parser.parse_args()
    max_age = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(
        days=args.days
    )

    max_pause = datetime.timedelta(minutes=10)
    ts_format = "%Y-%m-%d %H:%M"

    zsh_history = get_zsh_history()
    browser_history = get_browser_history(include_personal=args.include_personal)
    code_history = get_code_history()

    history = zsh_history + browser_history + code_history

    history = list(sorted(history, key=lambda x: x[0]))
    history = [(ts, resource) for ts, resource in history if resource.strip()]
    history = [(ts, resource) for ts, resource in history if ts > max_age]

    starts = [0]
    stops = []
    for i in range(1, len(history)):
        time_diff_previous = history[i][0] - history[i - 1][0]
        if time_diff_previous > max_pause or history[i][1] != history[i - 1][1]:
            starts.append(i)
            stops.append(i - 1)
    stops.append(len(history) - 1)

    assert len(starts) == len(
        stops
    ), f"Found {len(starts)} starts and {len(stops)} stops"

    # Display the report
    if args.verbose:
        for timestamp, resource in history:
            print(f"{timestamp.strftime(ts_format)} - {resource}")
    else:
        for start_i, stop_i in zip(starts, stops):
            start = history[start_i][0]
            stop = history[stop_i][0]
            assert start <= stop, f"start {start} > stop {stop}"
            resource = history[start_i][1]
            resource_stop = history[stop_i][1]
            assert (
                resource == resource_stop
            ), f"resource {resource} != resource_stop {resource_stop}"
            start_str = start.strftime(ts_format)
            stop_str = stop.strftime(ts_format)
            if start == stop:
                print(f"{start_str} - {resource}")
            else:
                print(f"{start_str} - {resource}")
                if stop - start > datetime.timedelta(minutes=4):
                    print(f"{stop_str}   (duration: {stop-start})")
