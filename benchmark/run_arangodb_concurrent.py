
from benchmark.result_store import save_result
from benchmark.config import (
    CONCURRENT_CLIENTS,
    OPERATIONS_PER_CLIENT,
    READ_PERCENTAGE,
)

from benchmark.concurrent import (
    run_concurrent_workload
)

from benchmark.databases import (
    create_database
)

from benchmark.start_nodes import (
    get_start_nodes
)

from benchmark.arangodb_queries import (
    CONCURRENT_READ_AQL,
    CONCURRENT_WRITE_AQL,
)

from benchmark.metrics import (
    summarize
)


NODES_FILE = "data/sample/nodes.csv"


def main():

    start_nodes = get_start_nodes(
        NODES_FILE,
        count=100,
        seed=42
    )

    print("=" * 70)
    print("DATABASE: arangodb")
    print("=" * 70)

    for clients in CONCURRENT_CLIENTS:

        print()
        print(
            f"Clients: {clients}"
        )

        result = run_concurrent_workload(
            db_factory=lambda: create_database(
                "arangodb"
            ),
            start_nodes=start_nodes,
            read_query=CONCURRENT_READ_AQL,
            write_query=CONCURRENT_WRITE_AQL,
            clients=clients,
            operations_per_client=OPERATIONS_PER_CLIENT,
            read_percentage=READ_PERCENTAGE,
            seed=42,
        )

        summary = summarize(
            result["latencies"]
        )

        save_result(
            database="arangodb",
            workload="mixed_read_write",
            clients=clients,
            iterations=result["total_operations"],
            successful=result["successful_operations"],
            failed=result["failed_operations"],
            throughput_ops_sec=result["throughput_ops_sec"],
            p50_ms=summary["p50_ms"],
            p95_ms=summary["p95_ms"],
        )

        print(
            f"Operations: "
            f"{result['total_operations']}"
        )

        print(
            f"Successful: "
            f"{result['successful_operations']}"
        )

        print(
            f"Failed: "
            f"{result['failed_operations']}"
        )

        print(
            f"Throughput: "
            f"{result['throughput_ops_sec']:.2f} ops/sec"
        )

        if summary["count"]:

            print(
                f"p50: "
                f"{summary['p50_ms']:.3f} ms"
            )

            print(
                f"p95: "
                f"{summary['p95_ms']:.3f} ms"
            )


if __name__ == "__main__":
    main()