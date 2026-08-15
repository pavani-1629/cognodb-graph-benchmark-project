import csv
from pathlib import Path


RESULT_FILE = Path("results/raw/benchmark_results.csv")


FIELDS = [
    "database",
    "workload",
    "clients",
    "iterations",
    "successful",
    "failed",
    "throughput_ops_sec",
    "p50_ms",
    "p95_ms",
]


def save_result(
    database,
    workload,
    clients,
    iterations,
    successful,
    failed,
    throughput_ops_sec,
    p50_ms,
    p95_ms,
):
    RESULT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    file_exists = RESULT_FILE.exists()

    with open(
        RESULT_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "database": database,
            "workload": workload,
            "clients": clients,
            "iterations": iterations,
            "successful": successful,
            "failed": failed,
            "throughput_ops_sec": throughput_ops_sec,
            "p50_ms": p50_ms,
            "p95_ms": p95_ms,
        })