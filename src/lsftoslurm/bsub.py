import argparse
import subprocess
import tempfile


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Submit jobs to Slurm via LSF syntax")

    parser.add_argument("-J", "--job_name", type=str)
    parser.add_argument("shellcode", type=str)
    return parser


def main() -> None:
    args = get_parser().parse_args()

    job_name_args = []
    if args.job_name:
        job_name_args = ["-J", args.job_name]

    with tempfile.NamedTemporaryFile() as script:
        script.write("#!/bin/bash\n".encode())
        script.write(args.shellcode.encode())
        script.flush()
        result = subprocess.run(
            ["sbatch"] + job_name_args + [script.name],
            stdout=subprocess.PIPE,
            check=False,
        )
        if result:
            stdout = result.stdout.decode()
            if stdout.startswith("Submitted batch job "):
                job_id = stdout.split()[-1]
                print(f"Job <{job_id}> is submitted to default queue <normal>.")


if __name__ == "__main__":
    main()
