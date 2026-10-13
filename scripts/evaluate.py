import json
from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

from scripts.model import FEATURES, train_model
from scripts.validate_data import validate_dataset


def main():
    df = pd.read_csv("data/deliveries.csv")
    validate_dataset(df)
    X = df[FEATURES]
    y = df["late_delivery"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = train_model(X_train, y_train, max_depth=5)
    predictions = model.predict(X_test)
    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(precision_score(y_test, predictions, zero_division=0)),
        "recall": float(recall_score(y_test, predictions, zero_division=0)),
        "f1_score": float(f1_score(y_test, predictions, zero_division=0)),
    }
    report = classification_report(y_test, predictions, zero_division=0)
    Path("reports").mkdir(exist_ok=True)
    with open("reports/metrics.json", "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)
    with open("reports/classification_report.txt", "w", encoding="utf-8") as file:
        file.write(report)
    print("Model performance report generated")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
