from databases.neo4j import Neo4j

from benchmark.metrics import summarize
from benchmark.start_nodes import get_start_nodes
from benchmark.traversal_benchmark import (
    run_traversal_benchmark
)


NODES_FILE = "data/sample/nodes.csv"


QUERY = """
MATCH (u:User {id: $id})
      -[:FRIENDS_WITH]->(friend)
RETURN friend.id
"""


def main():

    start_nodes = get_start_nodes(
        NODES_FILE,
        count=100,
        seed=42
    )

    db = Neo4j()

    try:

        db.connect()
        db.verify_connection()

        print("Connected to Neo4j.")

        latencies = run_traversal_benchmark(
            db=db,
            start_nodes=start_nodes,
            query=QUERY,
            warmup_iterations=20,
            measured_iterations=100
        )

        results = summarize(latencies)

        print()
        print("Neo4j 1-hop traversal")
        print("---------------------")

        print(
            f"Count:    {results['count']}"
        )

        print(
            f"Min:      {results['min_ms']:.3f} ms"
        )

        print(
            f"Mean:     {results['mean_ms']:.3f} ms"
        )

        print(
            f"p50:      {results['p50_ms']:.3f} ms"
        )

        print(
            f"p95:      {results['p95_ms']:.3f} ms"
        )

        print(
            f"Max:      {results['max_ms']:.3f} ms"
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()