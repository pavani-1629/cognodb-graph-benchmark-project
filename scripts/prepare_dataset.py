from pathlib import Path
import gzip
import csv
import random


INPUT_FILE = Path("data/raw/soc-pokec-relationships.txt.gz")

OUTPUT_DIR = Path("data/sample")
EDGES_FILE = OUTPUT_DIR / "edges.csv"
NODES_FILE = OUTPUT_DIR / "nodes.csv"

SAMPLE_SIZE = 100_000
RANDOM_SEED = 42


def reservoir_sample_edges():
    random.seed(RANDOM_SEED)

    reservoir = []
    total_edges = 0

    print("Reading original dataset...")

    with gzip.open(INPUT_FILE, "rt", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            # Ignore comment lines if present
            if line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) < 2:
                continue

            source = int(parts[0])
            target = int(parts[1])

            total_edges += 1

            edge = (source, target)

            if len(reservoir) < SAMPLE_SIZE:
                reservoir.append(edge)
            else:
                random_index = random.randint(0, total_edges - 1)

                if random_index < SAMPLE_SIZE:
                    reservoir[random_index] = edge

    print(f"Total relationships scanned: {total_edges:,}")
    print(f"Sampled relationships: {len(reservoir):,}")

    return reservoir


def save_edges(edges):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(EDGES_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["source", "target"])

        for source, target in edges:
            writer.writerow([source, target])

    print(f"Saved edges to: {EDGES_FILE}")


def save_nodes(edges):
    nodes = set()

    for source, target in edges:
        nodes.add(source)
        nodes.add(target)

    with open(NODES_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["id"])

        for node_id in sorted(nodes):
            writer.writerow([node_id])

    print(f"Unique nodes: {len(nodes):,}")
    print(f"Saved nodes to: {NODES_FILE}")


def main():
    if not INPUT_FILE.exists():
        print("Dataset not found.")
        print("Run this first:")
        print("python scripts/download_dataset.py")
        return

    edges = reservoir_sample_edges()

    save_edges(edges)
    save_nodes(edges)

    print()
    print("Dataset preparation completed.")


if __name__ == "__main__":
    main()