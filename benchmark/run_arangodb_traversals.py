from benchmark.config import (
    WARMUP_ITERATIONS,
    MEASURED_ITERATIONS,
    START_NODE_COUNT,
    RANDOM_SEED,
)

from benchmark.databases import create_database

from benchmark.arangodb_queries import (
    ONE_HOP_AQL,
    TWO_HOP_AQL,
    THREE_HOP_AQL,
)

from benchmark.runner import run_latency_benchmark

from benchmark.start_nodes import get_start_nodes


NODES_FILE = "data/sample/nodes.csv"


WORKLOADS = {
    "1-hop": ONE_HOP_AQL,
    "2-hop": TWO_HOP_AQL,
    "3-hop": THREE_HOP_AQL,
}


def main():

    print("=" * 60)
    print("ARANGODB TRAVERSAL BENCHMARK")
    print("=" * 60)

    # Same start nodes used for all three workloads
    start_nodes = get_start_nodes(
        NODES_FILE,
        count=START_NODE_COUNT,
        seed=RANDOM_SEED
    )

    db = create_database("arangodb")

    try:

        print("\nConnecting to ArangoDB...")

        db.connect()
        db.verify_connection()

        print("✅ ArangoDB connection successful")

        for workload_name, query in WORKLOADS.items():

            print()
            print("-" * 60)
            print(f"Running {workload_name}")
            print("-" * 60)

            results = run_latency_benchmark(
                db=db,
                start_nodes=start_nodes,
                query=query,
                warmup_iterations=WARMUP_ITERATIONS,
                measured_iterations=MEASURED_ITERATIONS,
                use_node_id=True,
            )

            print(
                f"p50: {results['p50_ms']:.3f} ms"
            )

            print(
                f"p95: {results['p95_ms']:.3f} ms"
            )

    finally:

        db.close()

        print("\nArangoDB connection closed.")


if __name__ == "__main__":
    main()