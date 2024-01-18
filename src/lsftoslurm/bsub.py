import argparse
import subprocess
import tempfile


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Submit jobs to Slurm via LSF syntax")
    parser.add_argument("shellcode", type=str)
    return parser


def main() -> None:
    args = get_parser().parse_args()
    with tempfile.NamedTemporaryFile() as script:
        script.write("#!/bin/bash\n".encode())
        script.write(args.shellcode.encode())
        script.flush()
        subprocess.call(["sbatch", script.name])


if __name__ == "__main__":
    main()
