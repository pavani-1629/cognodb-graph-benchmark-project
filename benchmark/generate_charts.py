import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


INPUT = "results/final_results.csv"

OUTPUT_DIR = Path(
    "results/charts"
)


def create_latency_chart(
    df,
    workload,
    metric,
):
    data = df[
        (df["workload"] == workload)
        & (df["clients"] == 1)
    ]

    if data.empty:
        return

    data = data.sort_values(
        "database"
    )

    plt.figure(
        figsize=(10, 6)
    )

    plt.bar(
        data["database"],
        data[metric]
    )

    plt.xlabel(
        "Database"
    )

    plt.ylabel(
        f"{metric}"
    )

    plt.title(
        f"{workload} - {metric}"
    )

    plt.xticks(
        rotation=30
    )

    plt.tight_layout()

    filename = (
        f"{workload}_{metric}.png"
        .replace(" ", "_")
    )

    plt.savefig(
        OUTPUT_DIR / filename,
        dpi=200
    )

    plt.close()


def create_concurrency_chart(
    df,
):
    data = df[
        df["workload"]
        == "mixed_read_write"
    ]

    if data.empty:
        return

    for metric in [
        "throughput_ops_sec",
        "p50_ms",
        "p95_ms",
    ]:

        plt.figure(
            figsize=(10, 6)
        )

        for database in sorted(
            data["database"].unique()
        ):

            subset = data[
                data["database"]
                == database
            ].sort_values(
                "clients"
            )

            plt.plot(
                subset["clients"],
                subset[metric],
                marker="o",
                label=database,
            )

        plt.xlabel(
            "Concurrent clients"
        )

        plt.ylabel(
            metric
        )

        plt.title(
            f"Concurrency - {metric}"
        )

        plt.legend()

        plt.tight_layout()

        plt.savefig(
            OUTPUT_DIR
            / f"concurrency_{metric}.png",
            dpi=200
        )

        plt.close()


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df = pd.read_csv(INPUT)

    for workload in [
        "1-hop",
        "2-hop",
        "3-hop",
        "point_lookup",
        "aggregation",
    ]:

        for metric in [
            "p50_ms",
            "p95_ms",
        ]:

            create_latency_chart(
                df,
                workload,
                metric
            )

    create_concurrency_chart(
        df
    )

    print(
        "Charts generated successfully."
    )


if __name__ == "__main__":
    main()