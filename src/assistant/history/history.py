from datetime import datetime, timedelta, date

from assistant.history import get_zsh_history, get_browser_history, get_code_history

MAX_PAUSE = timedelta(minutes=10)
TS_FORMAT = "%Y-%m-%d %H:%M"


def get_history(
    formatted=True,
    verbose=False,
    date: date = None,
):
    zsh_history = get_zsh_history(date=date)
    browser_history = get_browser_history(include_personal=True, date=date)
    code_history = get_code_history(date=date)

    history = zsh_history + browser_history + code_history

    history = list(sorted(history, key=lambda x: x[0]))
    history = [(ts, resource) for ts, resource in history if resource.strip()]

    if formatted:
        history = format_history(history, verbose=verbose)

    return history


def format_history(history: list[tuple], verbose: bool = False) -> str:
    result = ""
    starts = [0]
    stops = []
    for i in range(1, len(history)):
        time_diff_previous = history[i][0] - history[i - 1][0]
        if time_diff_previous > MAX_PAUSE or history[i][1] != history[i - 1][1]:
            starts.append(i)
            stops.append(i - 1)
    stops.append(len(history) - 1)
    assert len(starts) == len(
        stops
    ), f"Found {len(starts)} starts and {len(stops)} stops"

    if verbose:
        for timestamp, resource in history:
            result += f"{timestamp.strftime(TS_FORMAT)} - {resource}\n"
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
            start_str = start.strftime(TS_FORMAT)
            stop_str = stop.strftime(TS_FORMAT)
            if start == stop:
                result += f"{start_str} - {resource}\n"
            else:
                result += f"{start_str} - {resource}\n"
                if stop - start > timedelta(minutes=4):
                    result += f"{stop_str}   (duration: {stop-start})\n"
    return result
