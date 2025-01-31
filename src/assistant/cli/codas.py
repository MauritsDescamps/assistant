import argparse
from assistant.llm import terminal_assistant


def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, nargs=1, help="Input text")
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        help="Model name",
        default="qwen2.5-coder:7b-instruct",
    )
    return parser.parse_args()


def main():
    args = argparser()

    output = terminal_assistant(args.input, args.model)
    print(output)
