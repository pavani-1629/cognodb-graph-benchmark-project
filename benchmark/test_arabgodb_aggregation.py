from benchmark.config import (
    WARMUP_ITERATIONS,
    MEASURED_ITERATIONS,
)

from benchmark.databases import create_database
from benchmark.arangodb_queries import AGGREGATION_AQL
from benchmark.runner import run_latency_benchmark


def main():

    db = create_database("arangodb")

    try:

        db.connect()
        db.verify_connection()

        results = run_latency_benchmark(
        db=db,
        start_nodes=[1],
        query=AGGREGATION_AQL,
        warmup_iterations=WARMUP_ITERATIONS,
        measured_iterations=MEASURED_ITERATIONS,
        use_node_id=False,
        )

        print()
        print("ArangoDB aggregation")
        print("--------------------")

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