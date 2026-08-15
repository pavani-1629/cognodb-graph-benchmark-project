from benchmark.config import (
    WARMUP_ITERATIONS,
    MEASURED_ITERATIONS,
    START_NODE_COUNT,
    RANDOM_SEED,
)

from benchmark.databases import create_database
from benchmark.metrics import summarize
from benchmark.queries import (
    ONE_HOP_CYPHER,
    TWO_HOP_CYPHER,
    THREE_HOP_CYPHER,
)

from benchmark.runner import run_latency_benchmark
from benchmark.start_nodes import get_start_nodes


NODES_FILE = "data/sample/nodes.csv"


WORKLOADS = {
    "1-hop": ONE_HOP_CYPHER,
    "2-hop": TWO_HOP_CYPHER,
    "3-hop": THREE_HOP_CYPHER,
}


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
        print("#" * 60)
        print(f"DATABASE: {database_name}")
        print("#" * 60)

        db = create_database(
            database_name
        )

        try:

            db.connect()
            db.verify_connection()

            for workload_name, query in WORKLOADS.items():

                print()
                print(
                    f"Running {workload_name}..."
                )

                results = run_latency_benchmark(
                    db=db,
                    start_nodes=start_nodes,
                    query=query,
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