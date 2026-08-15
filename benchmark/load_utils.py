import csv


def read_nodes(path):
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            yield {
                "id": int(row["id"])
            }


def read_edges(path):
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            yield {
                "source": int(row["source"]),
                "target": int(row["target"]),
            }


def batched(iterable, batch_size):
    batch = []

    for item in iterable:
        batch.append(item)

        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch