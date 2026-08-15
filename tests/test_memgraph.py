from neo4j import GraphDatabase


driver = GraphDatabase.driver(
    "bolt://localhost:7688",
    auth=None
)


try:
    driver.verify_connectivity()

    print("Connected to Memgraph!")

    with driver.session() as session:
        result = session.run(
            'RETURN "Memgraph is working" AS status'
        )

        record = result.single()

        print(record["status"])

finally:
    driver.close()