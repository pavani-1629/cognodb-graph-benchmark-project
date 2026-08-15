from benchmark.config import (
    WARMUP_ITERATIONS,
    MEASURED_ITERATIONS,
)

from benchmark.databases import create_database
from benchmark.queries import AGGREGATION_CYPHER
from benchmark.runner import run_latency_benchmark


DATABASES = [
    "cognodb",
    "neo4j",
    "memgraph",
    "falkordb",
]


def main():

    # Aggregation doesn't need start nodes.
    dummy_nodes = [1]

    for database_name in DATABASES:

        print()
        print("=" * 60)
        print(f"DATABASE: {database_name}")
        print("=" * 60)

        db = create_database(database_name)

        try:

            db.connect()
            db.verify_connection()

            results = run_latency_benchmark(
                db=db,
                start_nodes=dummy_nodes,
                query=AGGREGATION_CYPHER,
                warmup_iterations=WARMUP_ITERATIONS,
                measured_iterations=MEASURED_ITERATIONS,
            )

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