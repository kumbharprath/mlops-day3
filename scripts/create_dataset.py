from pathlib import Path

import numpy as np
import pandas as pd


def create_dataset(n=1000, seed=42):
    rng = np.random.default_rng(seed)
    distance = rng.uniform(1, 15, n)
    raining = rng.integers(0, 2, n)
    heavy_traffic = rng.integers(0, 2, n)
    score = -3 + 0.2 * distance + 0.9 * raining + 1.2 * heavy_traffic
    probability = 1 / (1 + np.exp(-score))
    late = rng.binomial(1, probability)
    return pd.DataFrame(
        {
            "order_id": range(1, n + 1),
            "distance_km": distance.round(2),
            "raining": raining,
            "heavy_traffic": heavy_traffic,
            "late_delivery": late,
        }
    )


def main():
    Path("data").mkdir(exist_ok=True)
    df = create_dataset()
    df.to_csv("data/deliveries.csv", index=False)
    print("Dataset created")
    print("Rows:", len(df))
    print("Columns:", list(df.columns))


if __name__ == "__main__":
    main()
