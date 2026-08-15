from benchmark.config import (
    WARMUP_ITERATIONS,
    MEASURED_ITERATIONS,
    START_NODE_COUNT,
    RANDOM_SEED,
)

from benchmark.databases import create_database

from benchmark.start_nodes import get_start_nodes

from benchmark.runner import run_latency_benchmark

from benchmark.metrics import summarize

from pathlib import Path
import csv


NODES_FILE = "data/sample/nodes.csv"

OUTPUT_FILE = Path(
    "results/raw/normal_results.csv"
)


# ============================================================
# CYPHER QUERIES
# ============================================================

CYPHER_WORKLOADS = {

    "1-hop": """
    MATCH (u:User {id: $id})
          -[:FRIENDS_WITH]->(friend)
    RETURN DISTINCT friend.id
    """,

    "2-hop": """
    MATCH (u:User {id: $id})
          -[:FRIENDS_WITH*2]->(friend)
    RETURN DISTINCT friend.id
    """,

    "3-hop": """
    MATCH (u:User {id: $id})
          -[:FRIENDS_WITH*3]->(friend)
    RETURN DISTINCT friend.id
    """,

    "point_lookup": """
    MATCH (u:User {id: $id})
    RETURN u.id
    """,

    "aggregation": """
    MATCH ()-[r:FRIENDS_WITH]->()
    RETURN count(r) AS relationship_count
    """,
}


# ============================================================
# ARANGODB QUERIES
# ============================================================

ARANGO_WORKLOADS = {

    "1-hop": """
    FOR v, e, p IN 1..1 OUTBOUND
        CONCAT("users/", @id)
        friendships
        RETURN DISTINCT v._key
    """,

    "2-hop": """
    FOR v, e, p IN 2..2 OUTBOUND
        CONCAT("users/", @id)
        friendships
        RETURN DISTINCT v._key
    """,

    "3-hop": """
    FOR v, e, p IN 3..3 OUTBOUND
        CONCAT("users/", @id)
        friendships
        RETURN DISTINCT v._key
    """,

    "point_lookup": """
    FOR u IN users
        FILTER u._key == @id
        RETURN u._key
    """,

    "aggregation": """
    FOR edge IN friendships
        COLLECT WITH COUNT INTO relationship_count
        RETURN relationship_count
    """,
}


DATABASES = [
    "cognodb",
    "neo4j",
    "memgraph",
    "falkordb",
    "arangodb",
]


def save_results(rows):

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = [
            "database",
            "workload",
            "clients",
            "iterations",
            "successful",
            "failed",
            "throughput_ops_sec",
            "p50_ms",
            "p95_ms",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(rows)


def main():

    print("=" * 70)
    print("FINAL NORMAL BENCHMARK COLLECTION")
    print("=" * 70)

    print()
    print(
        f"Warm-up iterations: {WARMUP_ITERATIONS}"
    )

    print(
        f"Measured iterations: {MEASURED_ITERATIONS}"
    )

    print(
        f"Start nodes: {START_NODE_COUNT}"
    )

    print(
        f"Random seed: {RANDOM_SEED}"
    )

    # --------------------------------------------------------
    # Same start nodes for every database
    # --------------------------------------------------------

    start_nodes = get_start_nodes(
        NODES_FILE,
        count=START_NODE_COUNT,
        seed=RANDOM_SEED
    )

    rows = []

    # --------------------------------------------------------
    # Database loop
    # --------------------------------------------------------

    for database_name in DATABASES:

        print()
        print("=" * 70)
        print(
            f"DATABASE: {database_name}"
        )
        print("=" * 70)

        db = create_database(
            database_name
        )

        # ArangoDB uses AQL.
        # Other four use the Cypher/OpenCypher queries.
        if database_name == "arangodb":

            workloads = ARANGO_WORKLOADS

        else:

            workloads = CYPHER_WORKLOADS

        try:

            db.connect()

            db.verify_connection()

            print(
                "✅ Connection successful"
            )

            # ------------------------------------------------
            # Workload loop
            # ------------------------------------------------

            for workload_name, query in workloads.items():

                print()
                print(
                    f"Running {workload_name}..."
                )

                try:

                    # Aggregation does not need @id.
                    if workload_name == "aggregation":

                        dummy_nodes = [1]

                        results = run_latency_benchmark(
                            db=db,
                            start_nodes=dummy_nodes,
                            query=query,
                            warmup_iterations=WARMUP_ITERATIONS,
                            measured_iterations=MEASURED_ITERATIONS,
                            use_node_id=False,
                        )

                    else:

                        results = run_latency_benchmark(
                            db=db,
                            start_nodes=start_nodes,
                            query=query,
                            warmup_iterations=WARMUP_ITERATIONS,
                            measured_iterations=MEASURED_ITERATIONS,
                            use_node_id=True,
                        )

                    row = {
                        "database": database_name,
                        "workload": workload_name,
                        "clients": 1,
                        "iterations": MEASURED_ITERATIONS,
                        "successful": MEASURED_ITERATIONS,
                        "failed": 0,
                        "throughput_ops_sec": 0,
                        "p50_ms": results["p50_ms"],
                        "p95_ms": results["p95_ms"],
                    }

                    rows.append(row)

                    print(
                        f"p50: "
                        f"{results['p50_ms']:.3f} ms"
                    )

                    print(
                        f"p95: "
                        f"{results['p95_ms']:.3f} ms"
                    )

                except Exception as error:

                    print(
                        f"❌ {workload_name} failed:"
                    )

                    print(
                        f"{type(error).__name__}: "
                        f"{error}"
                    )

                    rows.append({
                        "database": database_name,
                        "workload": workload_name,
                        "clients": 1,
                        "iterations": MEASURED_ITERATIONS,
                        "successful": 0,
                        "failed": MEASURED_ITERATIONS,
                        "throughput_ops_sec": 0,
                        "p50_ms": "",
                        "p95_ms": "",
                    })

        except Exception as error:

            print(
                f"❌ Database failed: "
                f"{type(error).__name__}: {error}"
            )

        finally:

            db.close()

            print(
                f"Closed {database_name}"
            )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    save_results(rows)

    print()
    print("=" * 70)
    print("BENCHMARK COLLECTION COMPLETE")
    print("=" * 70)

    print()
    print(
        f"Results saved to:"
    )

    print(
        OUTPUT_FILE
    )

    print()
    print(
        f"Total rows: {len(rows)}"
    )


if __name__ == "__main__":
    main()