import os

from arango import ArangoClient
from dotenv import load_dotenv

from .base import GraphDatabase as GraphDatabaseInterface


load_dotenv()


class ArangoDBAdapter(GraphDatabaseInterface):

    def __init__(self):

        self.url = os.getenv(
            "ARANGODB_URL",
            "http://localhost:8529"
        )

        self.username = os.getenv(
            "ARANGODB_USER",
            "root"
        )

        self.password = os.getenv(
            "ARANGODB_PASSWORD"
        )

        self.client = None
        self.db = None

        self.vertex_collection = None
        self.edge_collection = None

    def connect(self):

        self.client = ArangoClient(
            hosts=self.url
        )

        self.db = self.client.db(
            "_system",
            username=self.username,
            password=self.password
        )

        if not self.db.has_database("benchmark"):
            self.db.create_database("benchmark")

        self.db = self.client.db(
            "benchmark",
            username=self.username,
            password=self.password
        )

        if not self.db.has_collection("users"):
            self.db.create_collection("users")

        if not self.db.has_collection("friendships"):
            self.db.create_collection(
                "friendships",
                edge=True
            )

        self.vertex_collection = self.db.collection(
            "users"
        )

        self.edge_collection = self.db.collection(
            "friendships"
        )

    def verify_connection(self):

        self.db.version()

    def clear(self):

        if self.db.has_collection("users"):
            self.db.collection("users").truncate()

        if self.db.has_collection("friendships"):
            self.db.collection("friendships").truncate()

    def create_schema(self):

        # ArangoDB automatically indexes _key.
        # We use the original Pokec ID as _key.
        pass

    def load_data(self, nodes_file, edges_file):

        from benchmark.load_utils import (
            read_nodes,
            read_edges,
            batched
        )

        node_count = 0
        edge_count = 0

        # -------------------------
        # Nodes
        # -------------------------

        for batch in batched(
            read_nodes(nodes_file),
            1000
        ):

            documents = [
                {
                    "_key": str(node["id"])
                }
                for node in batch
            ]

            self.vertex_collection.insert_many(
                documents,
                silent=True
            )

            node_count += len(documents)

        # -------------------------
        # Relationships
        # -------------------------

        for batch in batched(
            read_edges(edges_file),
            1000
        ):

            documents = [
                {
                    "_from": f"users/{edge['source']}",
                    "_to": f"users/{edge['target']}"
                }
                for edge in batch
            ]

            self.edge_collection.insert_many(
                documents,
                silent=True
            )

            edge_count += len(documents)

        return {
            "nodes": node_count,
            "edges": edge_count
        }

    def run_query(self, query, params=None):

        cursor = self.db.aql.execute(
            query,
            bind_vars=params or {}
        )

        return list(cursor)

    def close(self):

        pass