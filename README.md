# Graph Database Benchmark

A reproducible benchmark comparing CognoDB, Neo4j, Memgraph, FalkorDB, and ArangoDB using a common graph dataset and a consistent workload methodology.

## 1. Objective

The objective of this project is to compare graph database performance across:

- 1-hop traversal
- 2-hop traversal
- 3-hop traversal
- Point lookup
- Aggregation
- Concurrent mixed read/write workloads

The benchmark measures query latency using p50 and p95 percentiles, concurrent throughput, failures, and observable resource usage.

---

## 2. Databases

The benchmark evaluates:

1. CognoDB
2. Neo4j
3. Memgraph
4. FalkorDB
5. ArangoDB

Neo4j, Memgraph, FalkorDB, and ArangoDB were deployed locally using Docker.

CognoDB was accessed through its configured connection.

---

## 3. Dataset

The benchmark uses the project's generated graph dataset containing:

- User nodes
- Friendship relationships

The same logical graph workload is used across the compared databases.

Dataset files are located under:

```text
data/sample/
```
