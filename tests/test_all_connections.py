from databases.cognodb import CognoDB
from databases.neo4j import Neo4j
from databases.memgraph import Memgraph
from databases.falkordb import FalkorDBAdapter
from databases.arangodb import ArangoDBAdapter


DATABASES = [
    ("CognoDB", CognoDB),
    ("Neo4j", Neo4j),
    ("Memgraph", Memgraph),
    ("FalkorDB", FalkorDBAdapter),
    ("ArangoDB", ArangoDBAdapter),
]


def test_database(name, database_class):

    print(f"\nTesting {name}...")

    db = None

    try:
        db = database_class()

        db.connect()
        db.verify_connection()

        print(f"✅ {name}: connection successful")

        return True

    except Exception as error:

        print(f"❌ {name}: connection failed")
        print(f"   {type(error).__name__}: {error}")

        return False

    finally:

        if db:
            db.close()


def main():

    results = []

    for name, database_class in DATABASES:

        success = test_database(
            name,
            database_class
        )

        results.append(
            (name, success)
        )

    print("\n")
    print("=" * 45)
    print("DATABASE CONNECTION SUMMARY")
    print("=" * 45)

    for name, success in results:

        status = "PASS" if success else "FAIL"

        print(
            f"{name:<15} {status}"
        )


if __name__ == "__main__":
    main()