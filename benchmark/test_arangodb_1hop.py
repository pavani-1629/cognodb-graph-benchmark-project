from benchmark.config import (
    WARMUP_ITERATIONS,
    MEASURED_ITERATIONS,
    START_NODE_COUNT,
    RANDOM_SEED,
)

from benchmark.databases import create_database
from benchmark.arangodb_queries import ONE_HOP_AQL
from benchmark.runner import run_latency_benchmark
from benchmark.start_nodes import get_start_nodes


NODES_FILE = "data/sample/nodes.csv"


def main():

    start_nodes = get_start_nodes(
        NODES_FILE,
        count=START_NODE_COUNT,
        seed=RANDOM_SEED
    )

    db = create_database("arangodb")

    try:

        db.connect()
        db.verify_connection()

        results = run_latency_benchmark(
            db=db,
            start_nodes=start_nodes,
            query=ONE_HOP_AQL,
            warmup_iterations=WARMUP_ITERATIONS,
            measured_iterations=MEASURED_ITERATIONS,
        )

        print()
        print("ArangoDB 1-hop traversal")
        print("------------------------")

        print(
            f"p50: {results['p50_ms']:.3f} ms"
        )

        print(
            f"p95: {results['p95_ms']:.3f} ms"
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()