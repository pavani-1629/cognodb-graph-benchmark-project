import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def run_concurrent_workload(
    db_factory,
    start_nodes,
    read_query,
    write_query,
    clients,
    operations_per_client=25,
    read_percentage=70,
    seed=42,
):
    """
    Run a mixed read/write workload using multiple clients.

    read_percentage:
        Percentage of operations that are reads.

    Returns:
        latency measurements,
        total operations,
        successful operations,
        failed operations,
        elapsed time
    """

    latencies = []
    successful = 0
    failed = 0

    start_time = time.perf_counter()

    def worker(worker_id):

        nonlocal successful
        nonlocal failed

        db = db_factory()

        local_latencies = []
        local_successful = 0
        local_failed = 0

        rng = random.Random(
            seed + worker_id
        )

        try:

            db.connect()
            db.verify_connection()

            for _ in range(operations_per_client):

                node_id = rng.choice(
                    start_nodes
                )

                is_read = (
                    rng.random() * 100
                    < read_percentage
                )

                if is_read:

                    query = read_query

                    params = {
                        "id": node_id
                    }

                else:

                    query = write_query

                    target_id = rng.choice(
                        start_nodes
                    )

                    params = {
                        "source": node_id,
                        "target": target_id
                    }

                try:

                    start = time.perf_counter()

                    db.run_query(
                        query,
                        params
                    )

                    end = time.perf_counter()

                    latency_ms = (
                        end - start
                    ) * 1000

                    local_latencies.append(
                        latency_ms
                    )

                    local_successful += 1

                except Exception as error:

                    local_failed += 1

                    print(
                        f"Worker {worker_id} "
                        f"operation failed: "
                        f"{type(error).__name__}: "
                        f"{error}"
                    )

        finally:

            db.close()

        return (
            local_latencies,
            local_successful,
            local_failed
        )

    with ThreadPoolExecutor(
        max_workers=clients
    ) as executor:

        futures = [
            executor.submit(
                worker,
                worker_id
            )
            for worker_id in range(clients)
        ]

        for future in as_completed(futures):

            (
                worker_latencies,
                worker_successful,
                worker_failed
            ) = future.result()

            latencies.extend(
                worker_latencies
            )

            successful += (
                worker_successful
            )

            failed += (
                worker_failed
            )

    elapsed = (
        time.perf_counter()
        - start_time
    )

    total_operations = (
        successful + failed
    )

    throughput = (
        successful / elapsed
        if elapsed > 0
        else 0
    )

    return {
        "latencies": latencies,
        "total_operations": total_operations,
        "successful_operations": successful,
        "failed_operations": failed,
        "elapsed_seconds": elapsed,
        "throughput_ops_sec": throughput,
    }