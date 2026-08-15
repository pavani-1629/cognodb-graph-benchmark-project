import csv
import random


def get_start_nodes(
    nodes_file,
    count=100,
    seed=42
):

    with open(
        nodes_file,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        nodes = [
            int(row["id"])
            for row in reader
        ]

    random_generator = random.Random(seed)

    return random_generator.sample(
        nodes,
        count
    )