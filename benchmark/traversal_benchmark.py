import random
import time


def run_traversal_benchmark(
    db,
    start_nodes,
    query,
    warmup_iterations=20,
    measured_iterations=100,
):

    # -------------------------
    # Warm-up
    # -------------------------

    for i in range(warmup_iterations):

        node_id = start_nodes[
            i % len(start_nodes)
        ]

        db.run_query(
            query,
            {"id": node_id}
        )

    # -------------------------
    # Measurements
    # -------------------------

    latencies = []

    random_generator = random.Random(42)

    for _ in range(measured_iterations):

        node_id = random_generator.choice(
            start_nodes
        )

        start = time.perf_counter()

        db.run_query(
            query,
            {"id": node_id}
        )

        end = time.perf_counter()

        latency_ms = (
            end - start
        ) * 1000

        latencies.append(
            latency_ms
        )

    return latencies