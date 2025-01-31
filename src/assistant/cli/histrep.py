import datetime
import argparse
from signal import signal, SIGPIPE, SIG_DFL


from assistant.history import get_history


def main():
    signal(SIGPIPE, SIG_DFL)

    # parse command line arguments
    parser = argparse.ArgumentParser(
        description="Generate a report of VSCode editor history"
    )
    # first argument is mandatory: date
    parser.add_argument("date", type=str, help="Date to display history for")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    args = parser.parse_args()
    date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()

    history = get_history(verbose=args.verbose, date=date)
    print(history)
