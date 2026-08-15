import pandas as pd
from pathlib import Path


NORMAL_FILE = Path(
    "results/raw/normal_results.csv"
)

CONCURRENT_FILE = Path(
    "results/raw/benchmark_results.csv"
)

OUTPUT_FILE = Path(
    "results/final_results.csv"
)


def main():

    normal = pd.read_csv(
        NORMAL_FILE
    )

    concurrent = pd.read_csv(
        CONCURRENT_FILE
    )

    # Keep only the latest clean concurrency
    # result for each database/client combination.
    concurrent = (
        concurrent
        .drop_duplicates(
            subset=[
                "database",
                "workload",
                "clients",
            ],
            keep="first",
        )
    )

    final = pd.concat(
        [
            normal,
            concurrent,
        ],
        ignore_index=True,
    )

    final = final.sort_values(
        [
            "workload",
            "clients",
            "database",
        ]
    ).reset_index(
        drop=True
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    final.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("=" * 70)
    print("FINAL BENCHMARK RESULTS")
    print("=" * 70)

    print()
    print(
        f"Normal results: {len(normal)}"
    )

    print(
        f"Concurrency results: {len(concurrent)}"
    )

    print(
        f"Final results: {len(final)}"
    )

    print()

    print(
        final.to_string(
            index=False
        )
    )

    print()
    print(
        f"Saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()