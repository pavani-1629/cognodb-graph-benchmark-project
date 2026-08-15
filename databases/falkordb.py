from falkordb import FalkorDB

from .base import GraphDatabase as GraphDatabaseInterface


class FalkorDBAdapter(GraphDatabaseInterface):

    def __init__(self):
        self.client = None
        self.graph = None

    def connect(self):
        self.client = FalkorDB(
            host="localhost",
            port=6379
        )

        self.graph = self.client.select_graph(
            "benchmark"
        )

    def verify_connection(self):
        self.client.connection.ping()

    def clear(self):
        self.graph.query(
            "MATCH (n) DETACH DELETE n"
        )

    def create_schema(self):
        pass

    def load_data(self, nodes_file, edges_file):

        from benchmark.load_utils import read_nodes, read_edges, batched

        node_count = 0
        edge_count = 0

        node_query = """
        UNWIND $rows AS row
        CREATE (:User {id: row.id})
        """

        for batch in batched(
            read_nodes(nodes_file),
            1000
        ):

            self.graph.query(
                node_query,
                params={"rows": batch}
            )

            node_count += len(batch)

        edge_query = """
        UNWIND $rows AS row

        MATCH (source:User {id: row.source})
        MATCH (target:User {id: row.target})

        CREATE (source)-[:FRIENDS_WITH]->(target)
        """

        for batch in batched(
            read_edges(edges_file),
            1000
        ):

            self.graph.query(
                edge_query,
                params={"rows": batch}
            )

            edge_count += len(batch)

        return {
            "nodes": node_count,
            "edges": edge_count
        }

    def run_query(self, query, params=None):
        if params:
            return self.graph.query(
                query,
                params
            )

        return self.graph.query(query)

    def close(self):
        pass