# Benchmark Dataset

## Source

This benchmark uses the Pokec social network dataset from the
Stanford Large Network Dataset Collection (SNAP).

Official source:

https://snap.stanford.edu/data/soc-pokec.html

## Original Dataset

The original Pokec relationship dataset contains:

- 1,632,803 nodes
- 30,622,564 directed relationships

## Benchmark Sample

For the benchmark, a reproducible sample of exactly 100,000
relationships is generated from the original relationship file.

Sampling method:

- Reservoir sampling
- Sample size: 100,000 relationships
- Random seed: 42

The sampled dataset is represented by:

- `nodes.csv`
- `edges.csv`

## Graph Model

Nodes:

`(:User)`

Relationships:

`(:User)-[:FRIENDS_WITH]->(:User)`

The original direction of the relationships is preserved.

## Reproduction

Download the original dataset:

```bash
python scripts/download_dataset.py
```
