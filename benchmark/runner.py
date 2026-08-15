import random
import time

from benchmark.metrics import summarize


def run_latency_benchmark(
    db,
    start_nodes,
    query,
    warmup_iterations,
    measured_iterations,
    use_node_id=True,
):
    # -------------------------
    # Warm-up
    # -------------------------

    for i in range(warmup_iterations):

        if use_node_id:
            node_id = start_nodes[
                i % len(start_nodes)
            ]

            params = {"id": node_id}

        else:
            params = {}

        db.run_query(
            query,
            params
        )

    # -------------------------
    # Measurement
    # -------------------------

    latencies = []

    rng = random.Random(42)

    for _ in range(measured_iterations):

        if use_node_id:
            node_id = rng.choice(
                start_nodes
            )

            params = {"id": node_id}

        else:
            params = {}

        start = time.perf_counter()

        db.run_query(
            query,
            params
        )

        end = time.perf_counter()

        latency_ms = (
            end - start
        ) * 1000

        latencies.append(
            latency_ms
        )

    return summarize(latencies)