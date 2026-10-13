import pandas as pd
import pytest

from scripts.validate_data import validate_dataset


def valid_dataframe():
    return pd.DataFrame(
        {
            "distance_km": [2, 9, 5],
            "raining": [0, 1, 0],
            "heavy_traffic": [0, 1, 1],
            "late_delivery": [0, 1, 0],
        }
    )


def test_valid_dataset():
    assert validate_dataset(valid_dataframe()) is True


def test_missing_column():
    df = valid_dataframe().drop(columns=["raining"])
    with pytest.raises(ValueError):
        validate_dataset(df)


def test_negative_distance():
    df = valid_dataframe()
    df.loc[0, "distance_km"] = -5
    with pytest.raises(ValueError):
        validate_dataset(df)


def test_invalid_label():
    df = valid_dataframe()
    df.loc[0, "late_delivery"] = 5
    with pytest.raises(ValueError):
        validate_dataset(df)


def test_empty_dataset():
    df = valid_dataframe().iloc[0:0]
    with pytest.raises(ValueError):
        validate_dataset(df)
