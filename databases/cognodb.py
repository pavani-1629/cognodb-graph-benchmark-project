import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

from .base import GraphDatabase as GraphDatabaseInterface


load_dotenv()


class CognoDB(GraphDatabaseInterface):

    def __init__(self):
        self.uri = os.getenv("COGNODB_URI")
        self.username = os.getenv("COGNODB_USER")
        self.password = os.getenv("COGNODB_PASSWORD")

        if not self.uri:
            raise ValueError("COGNODB_URI is not set")

        self.driver = None

    def connect(self):
        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password)
        )

    def verify_connection(self):
        self.driver.verify_connectivity()

    def clear(self):
        with self.driver.session() as session:
            session.run(
                "MATCH (n) DETACH DELETE n"
            ).consume()

    def create_schema(self):
        with self.driver.session() as session:
            session.run(
                """
                CREATE CONSTRAINT user_id_unique IF NOT EXISTS
                FOR (u:User)
                REQUIRE u.id IS UNIQUE
                """
            ).consume()

    def load_data(self, nodes_file, edges_file):

        from benchmark.load_utils import read_nodes, read_edges, batched

        node_count = 0
        edge_count = 0

        node_query = """
        UNWIND $rows AS row
        CREATE (:User {id: row.id})
        """

        with self.driver.session() as session:

            for batch in batched(
                read_nodes(nodes_file),
                1000
            ):

                session.run(
                    node_query,
                    rows=batch
                ).consume()

                node_count += len(batch)

        edge_query = """
        UNWIND $rows AS row

        MATCH (source:User {id: row.source})
        MATCH (target:User {id: row.target})

        CREATE (source)-[:FRIENDS_WITH]->(target)
        """

        with self.driver.session() as session:

            for batch in batched(
                read_edges(edges_file),
                1000
            ):

                session.run(
                    edge_query,
                    rows=batch
                ).consume()

                edge_count += len(batch)

        return {
            "nodes": node_count,
            "edges": edge_count
        }

    def run_query(self, query, params=None):
        with self.driver.session() as session:
            result = session.run(
                query,
                params or {}
            )

            return list(result)

    def close(self):
        if self.driver:
            self.driver.close()