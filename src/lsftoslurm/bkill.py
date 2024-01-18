import argparse
import os
import subprocess


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Kill jobs")
    parser.add_argument("jobids", type=str, nargs="+")
    return parser


def main() -> None:
    args = get_parser().parse_args()

    for jobid in args.jobids:
        if jobid == "0":
            subprocess.call(["scancel", "-u", os.getlogin()])
        else:
            subprocess.call(["scancel", jobid])


if __name__ == "__main__":
    main()
