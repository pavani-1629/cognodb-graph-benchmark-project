import csv
import subprocess
import time
from pathlib import Path


OUTPUT = Path("results/raw/resource_usage.csv")

CONTAINERS = [
    "benchmark-neo4j",
    "benchmark-memgraph",
    "benchmark-falkordb",
    "benchmark-arangodb",
]


def get_stats():

    command = [
        "docker",
        "stats",
        "--no-stream",
        "--format",
        "{{.Name}},{{.CPUPerc}},{{.MemUsage}},{{.MemPerc}}",
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )

    rows = []

    for line in result.stdout.strip().splitlines():

        parts = line.split(",", 3)

        if len(parts) != 4:
            continue

        name, cpu, memory, memory_percent = parts

        if name not in CONTAINERS:
            continue

        rows.append({
            "timestamp": time.time(),
            "container": name,
            "cpu_percent": cpu,
            "memory_usage": memory,
            "memory_percent": memory_percent,
        })

    return rows


def main():

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    print("Starting Docker resource monitoring...")
    print("Press Ctrl+C to stop.")

    file_exists = OUTPUT.exists()

    with open(
        OUTPUT,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "timestamp",
                "container",
                "cpu_percent",
                "memory_usage",
                "memory_percent",
            ],
        )

        if not file_exists:
            writer.writeheader()

        try:

            while True:

                rows = get_stats()

                for row in rows:

                    writer.writerow(row)

                    print(
                        f"{row['container']:<25} "
                        f"CPU={row['cpu_percent']:<8} "
                        f"MEM={row['memory_usage']:<20} "
                        f"MEM%={row['memory_percent']}"
                    )

                file.flush()

                print("-" * 80)

                time.sleep(1)

        except KeyboardInterrupt:

            print("\nMonitoring stopped.")


if __name__ == "__main__":
    main()