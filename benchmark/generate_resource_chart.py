import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


INPUT = Path(
    "results/resource_summary.csv"
)

OUTPUT_DIR = Path(
    "results/charts"
)


def main():

    df = pd.read_csv(INPUT)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Average memory
    plt.figure(figsize=(10, 6))

    plt.bar(
        df["container"],
        df["avg_memory_mib"]
    )

    plt.xlabel("Database")
    plt.ylabel("Average Memory (MiB)")
    plt.title("Average Database Memory Usage")

    plt.xticks(rotation=30)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "resource_memory.png",
        dpi=200
    )

    plt.close()

    # Average CPU
    plt.figure(figsize=(10, 6))

    plt.bar(
        df["container"],
        df["avg_cpu_percent"]
    )

    plt.xlabel("Database")
    plt.ylabel("Average CPU (%)")
    plt.title("Average Database CPU Usage")

    plt.xticks(rotation=30)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "resource_cpu.png",
        dpi=200
    )

    plt.close()

    print(
        "Resource charts generated successfully."
    )


if __name__ == "__main__":
    main()