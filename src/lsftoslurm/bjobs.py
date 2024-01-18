import argparse
import subprocess
from datetime import datetime
from enum import Enum
from typing import List, Mapping

from pydantic import BaseModel


class JobState(str, Enum):
    RUNNING = "RUNNING"
    CANCELLED = "CANCELLED"


class Job(BaseModel):
    job_id: int
    name: str
    job_state: JobState
    user_id: int
    user_name: str
    partition: str
    batch_host: str
    submit_time: int
    nodes: str


class SQueueOutput(BaseModel):
    jobs: List[Job]


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Get slurm jobs in LSF way")
    parser.add_argument("jobids", type=str, nargs="*")
    return parser


def lsf_formatter(jobstats: List[Job]) -> str:
    lsfstates: Mapping[JobState, str] = {
        JobState.RUNNING: "RUN",
        JobState.CANCELLED: "KILL?",
    }
    string = "JOBID USER     STAT  QUEUE      FROM_HOST   EXEC_HOST   JOB_NAME   SUBMIT_TIME\n"
    for job in jobstats:
        submit_time = datetime.utcfromtimestamp((job.submit_time))
        string += (
            f"{str(job.job_id):<5s} {job.user_name or str(job.user_id):<8s} "
            f"{lsfstates[job.job_state]:<4s} {job.partition:<8} "
            f"{job.batch_host:<11s} {job.nodes:<11s} {job.name:<8s} "
            f"{submit_time}"
        )
    return string


def main() -> None:
    args = get_parser().parse_args()
    result = subprocess.run(["squeue", "--json"], stdout=subprocess.PIPE, check=False)
    stats = SQueueOutput.model_validate_json(result.stdout)
    if args.jobids:
        selected_jobs = [job for job in stats.jobs if str(job.job_id) in args.jobids]
    else:
        selected_jobs = stats.jobs
    print(lsf_formatter(selected_jobs))


if __name__ == "__main__":
    main()
