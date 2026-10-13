import pandas as pd

REQUIRED_COLUMNS = {
    "distance_km",
    "raining",
    "heavy_traffic",
    "late_delivery",
}


def validate_dataset(df):
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if df.empty:
        raise ValueError("Dataset is empty")
    if df[list(REQUIRED_COLUMNS)].isnull().any().any():
        raise ValueError("Dataset contains missing values")
    if not pd.api.types.is_numeric_dtype(df["distance_km"]):
        raise ValueError("Distance must be numeric")
    if (df["distance_km"] < 0).any():
        raise ValueError("Negative distances found")
    for column in ["raining", "heavy_traffic", "late_delivery"]:
        if not df[column].isin([0, 1]).all():
            raise ValueError(f"Invalid binary values in {column}")
    return True


def main():
    df = pd.read_csv("data/deliveries.csv")
    validate_dataset(df)
    print("Dataset validation passed")


if __name__ == "__main__":
    main()
