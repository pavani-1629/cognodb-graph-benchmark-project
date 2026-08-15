import pandas as pd
from pathlib import Path
import re


INPUT = Path("results/raw/resource_usage.csv")
OUTPUT = Path("results/resource_summary.csv")


def memory_to_mib(value):
    """
    Convert Docker memory usage such as:
    '897.9MiB / 3.695GiB'
    into the used MiB value.
    """

    value = str(value)

    match = re.search(
        r"([\d.]+)(MiB|GiB)",
        value
    )

    if not match:
        return None

    number = float(match.group(1))
    unit = match.group(2)

    if unit == "GiB":
        return number * 1024

    return number


def cpu_to_float(value):
    return float(
        str(value)
        .replace("%", "")
    )


def main():

    df = pd.read_csv(INPUT)

    df["cpu_percent"] = (
        df["cpu_percent"]
        .apply(cpu_to_float)
    )

    df["memory_mib"] = (
        df["memory_usage"]
        .apply(memory_to_mib)
    )

    summary = (
        df.groupby("container")
        .agg(
            avg_cpu_percent=(
                "cpu_percent",
                "mean"
            ),

            peak_cpu_percent=(
                "cpu_percent",
                "max"
            ),

            avg_memory_mib=(
                "memory_mib",
                "mean"
            ),

            peak_memory_mib=(
                "memory_mib",
                "max"
            ),
        )
        .reset_index()
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
        "Resource summary written to:"
    )

    print(OUTPUT)

    print()

    print(
        summary.to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()