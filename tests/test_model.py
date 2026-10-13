from sklearn.model_selection import train_test_split

from scripts.create_dataset import create_dataset
from scripts.model import FEATURES, train_model


def test_model_trains_successfully():
    df = create_dataset(n=200)
    model = train_model(df[FEATURES], df["late_delivery"], max_depth=3)
    assert model is not None


def test_prediction_count():
    df = create_dataset(n=200)
    X_train, X_test, y_train, _ = train_test_split(
        df[FEATURES],
        df["late_delivery"],
        test_size=0.2,
        random_state=42,
        stratify=df["late_delivery"],
    )
    predictions = train_model(X_train, y_train).predict(X_test)
    assert len(predictions) == len(X_test)


def test_prediction_classes():
    df = create_dataset(n=200)
    predictions = train_model(df[FEATURES], df["late_delivery"]).predict(df[FEATURES])
    assert set(predictions).issubset({0, 1})
