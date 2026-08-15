import pandas as pd
from pathlib import Path


INPUT = Path(
    "results/raw/benchmark_results.csv"
)

OUTPUT = Path(
    "results/summary.csv"
)


def main():

    df = pd.read_csv(INPUT)

    summary = (
        df[
            [
                "database",
                "workload",
                "clients",
                "throughput_ops_sec",
                "p50_ms",
                "p95_ms",
                "failed",
            ]
        ]
        .sort_values(
            [
                "workload",
                "clients",
                "database",
            ]
        )
    )

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    summary.to_csv(
        OUTPUT,
        index=False
    )

    print(
        f"Summary written to {OUTPUT}"
    )

    print()
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()