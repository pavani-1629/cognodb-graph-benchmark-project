import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


uri = os.getenv("COGNODB_URI")
username = os.getenv("COGNODB_USER")
password = os.getenv("COGNODB_PASSWORD")


driver = GraphDatabase.driver(
    uri,
    auth=(username, password)
)


try:
    driver.verify_connectivity()

    print("Connected to CognoDB!")

    with driver.session() as session:
        result = session.run(
            'RETURN "CognoDB is working" AS status'
        )

        record = result.single()

        print(record["status"])

finally:
    driver.close()