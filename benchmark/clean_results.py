import pandas as pd
from pathlib import Path


INPUT = Path("results/raw/benchmark_results.csv")
OUTPUT = Path("results/raw/benchmark_results_clean.csv")


def main():

    df = pd.read_csv(INPUT)

    # Keep only the first result for each
    # database + workload + client combination.
    #
    # The first 15 rows are the latest clean run.
    clean = (
        df.drop_duplicates(
            subset=[
                "database",
                "workload",
                "clients",
            ],
            keep="first",
        )
        .sort_values(
            [
                "workload",
                "clients",
                "database",
            ]
        )
        .reset_index(drop=True)
    )

    clean.to_csv(
        OUTPUT,
        index=False
    )

    print(
        f"Clean results written to: {OUTPUT}"
    )

    print()
    print(
        f"Rows: {len(clean)}"
    )

    print()
    print(
        clean.to_string(index=False)
    )


if __name__ == "__main__":
    main()