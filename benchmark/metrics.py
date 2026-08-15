import statistics


def percentile(values, percentile):

    if not values:
        return None

    values = sorted(values)

    index = (
        len(values) - 1
    ) * percentile / 100

    lower = int(index)
    upper = lower + 1

    if upper >= len(values):
        return values[lower]

    weight = index - lower

    return (
        values[lower]
        + weight
        * (
            values[upper]
            - values[lower]
        )
    )


def summarize(values):

    if not values:
        return {
            "count": 0,
            "min_ms": None,
            "max_ms": None,
            "mean_ms": None,
            "p50_ms": None,
            "p95_ms": None,
        }

    return {
        "count": len(values),
        "min_ms": min(values),
        "max_ms": max(values),
        "mean_ms": statistics.mean(values),
        "p50_ms": percentile(
            values,
            50
        ),
        "p95_ms": percentile(
            values,
            95
        ),
    }