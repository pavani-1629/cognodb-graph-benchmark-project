import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")


driver = GraphDatabase.driver(
    uri,
    auth=(username, password)
)


try:
    driver.verify_connectivity()

    print("Connected to Neo4j!")

    with driver.session() as session:
        result = session.run(
            'RETURN "Neo4j is working" AS status'
        )

        record = result.single()

        print(record["status"])

finally:
    driver.close()