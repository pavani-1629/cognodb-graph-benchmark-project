import sys
import time
from pathlib import Path

from databases.cognodb import CognoDB
from databases.neo4j import Neo4j
from databases.memgraph import Memgraph
from databases.falkordb import FalkorDBAdapter
from databases.arangodb import ArangoDBAdapter


NODES_FILE = Path("data/sample/nodes.csv")
EDGES_FILE = Path("data/sample/edges.csv")


DATABASES = {
    "cognodb": CognoDB,
    "neo4j": Neo4j,
    "memgraph": Memgraph,
    "falkordb": FalkorDBAdapter,
    "arangodb": ArangoDBAdapter,
}


def main():

    if len(sys.argv) != 2:

        print(
            "Usage: python -m benchmark.load_database DATABASE"
        )

        print()
        print("Available databases:")

        for name in DATABASES:
            print(f"  {name}")

        return

    database_name = sys.argv[1].lower()

    if database_name not in DATABASES:

        print(
            f"Unknown database: {database_name}"
        )

        return

    if not NODES_FILE.exists():

        print(
            f"Missing file: {NODES_FILE}"
        )

        return

    if not EDGES_FILE.exists():

        print(
            f"Missing file: {EDGES_FILE}"
        )

        return

    database_class = DATABASES[
        database_name
    ]

    db = database_class()

    try:

        print("=" * 60)
        print(f"Loading dataset into {database_name}")
        print("=" * 60)

        print()
        print("Connecting...")

        db.connect()

        db.verify_connection()

        print("Connection successful.")

        print()
        print("Clearing existing data...")

        db.clear()

        print("Existing data cleared.")

        print()
        print("Creating schema...")

        db.create_schema()

        print("Schema ready.")

        print()
        print("Loading dataset...")

        start = time.perf_counter()

        result = db.load_data(
            NODES_FILE,
            EDGES_FILE
        )

        elapsed = time.perf_counter() - start

        nodes = result["nodes"]
        edges = result["edges"]

        print()
        print("=" * 60)
        print("LOAD COMPLETE")
        print("=" * 60)

        print(f"Nodes loaded:         {nodes:,}")
        print(f"Relationships loaded: {edges:,}")
        print(f"Load time:             {elapsed:.3f} seconds")

        if elapsed > 0:

            print(
                f"Nodes/sec:             {nodes / elapsed:,.2f}"
            )

            print(
                f"Relationships/sec:     {edges / elapsed:,.2f}"
            )

    finally:

        db.close()


if __name__ == "__main__":
    main()