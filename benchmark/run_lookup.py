from benchmark.config import (
    WARMUP_ITERATIONS,
    MEASURED_ITERATIONS,
    START_NODE_COUNT,
    RANDOM_SEED,
)

from benchmark.databases import create_database
from benchmark.queries import POINT_LOOKUP_CYPHER
from benchmark.runner import run_latency_benchmark
from benchmark.start_nodes import get_start_nodes


NODES_FILE = "data/sample/nodes.csv"


DATABASES = [
    "cognodb",
    "neo4j",
    "memgraph",
    "falkordb",
]


def main():

    start_nodes = get_start_nodes(
        NODES_FILE,
        count=START_NODE_COUNT,
        seed=RANDOM_SEED
    )

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
                start_nodes=start_nodes,
                query=POINT_LOOKUP_CYPHER,
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