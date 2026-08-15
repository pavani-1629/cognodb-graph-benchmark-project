from abc import ABC, abstractmethod


class GraphDatabase(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def verify_connection(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def create_schema(self):
        pass

    @abstractmethod
    def load_data(self, nodes_file, edges_file):
        pass

    @abstractmethod
    def run_query(self, query, params=None):
        pass

    @abstractmethod
    def close(self):
        pass