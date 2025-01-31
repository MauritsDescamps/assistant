from argparse import ArgumentParser
from datetime import datetime
from assistant.history import get_history
from assistant.llm import time_sheets_assistant


def argparser():
    parser = ArgumentParser()
    parser.add_argument("date", type=str, help="Date to display history for")
    return parser.parse_args()


def main():
    args = argparser()
    if not hasattr(args, "date"):
        print("Please provide a date")
        return
    date = datetime.strptime(args.date, "%Y-%m-%d").date()
    history = get_history(date=date)
    # remove date from each line
    lines = [line.replace(f"{args.date} ", "") for line in history.split("\n")]
    history = "\n".join(lines)
    print(history)
    response = time_sheets_assistant(history)
    print(response)
