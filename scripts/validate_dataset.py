from pathlib import Path
import csv


EDGES_FILE = Path("data/sample/edges.csv")
NODES_FILE = Path("data/sample/nodes.csv")


def main():
    with open(EDGES_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        edges = list(reader)

    with open(NODES_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        nodes = list(reader)

    print("Dataset validation")
    print("------------------")

    print(f"Relationships: {len(edges):,}")
    print(f"Nodes:         {len(nodes):,}")

    missing_edges = 0

    for edge in edges:
        if not edge["source"] or not edge["target"]:
            missing_edges += 1

    print(f"Invalid edges: {missing_edges:,}")

    node_ids = {node["id"] for node in nodes}

    missing_nodes = 0

    for edge in edges:
        if edge["source"] not in node_ids:
            missing_nodes += 1

        if edge["target"] not in node_ids:
            missing_nodes += 1

    print(f"Missing node references: {missing_nodes:,}")

    if len(edges) == 100_000 and missing_edges == 0 and missing_nodes == 0:
        print()
        print("Dataset validation PASSED.")
    else:
        print()
        print("Dataset validation FAILED.")


if __name__ == "__main__":
    main()