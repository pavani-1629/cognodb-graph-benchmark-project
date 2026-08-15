from databases.cognodb import CognoDB
from databases.neo4j import Neo4j
from databases.memgraph import Memgraph
from databases.falkordb import FalkorDBAdapter
from databases.arangodb import ArangoDBAdapter


DATABASES = {
    "cognodb": CognoDB,
    "neo4j": Neo4j,
    "memgraph": Memgraph,
    "falkordb": FalkorDBAdapter,
    "arangodb": ArangoDBAdapter,
}


def create_database(name):

    name = name.lower()

    if name not in DATABASES:
        raise ValueError(
            f"Unknown database: {name}"
        )

    return DATABASES[name]()