# Day 3 — MLOps Workshop: Corrected End-to-End Hands-on Lab

**Project:** Automated Food Delivery ML Validation using GitHub Actions  
**Audience:** Beginner students | **Environment:** Windows Git Bash / Python 3.11 or 3.12  
**Scope:** Labs 1–15 (the practical content of the supplied Day 3 document, corrected for missing code/formatting).

## What you get

This Markdown guide is the student walk-through. The companion executable ZIP contains the full working project, including complete Python modules, eight tests, the GitHub Actions workflow, `requirements.txt`, and `.gitignore`. The Word manual contains these same steps and all source-file listings. Start **in the extracted `mlops-day3/` project directory**; do not create a second nested project folder.

**Learning flow:** create synthetic data → validate → train model → automated tests → Black/Flake8 → evaluate → GitHub Actions → download report → intentionally fail and fix CI.

**Important distinctions:** Data is synthetic; model metrics are demonstration results, not production certification. The provided CI validates and evaluates on push; it does **not** automatically deploy an application. MLflow and DVC are not required in this self-contained Day 3 lab.

## Project tree

```text
mlops-day3/
├── .github/workflows/ml-ci.yml
├── .gitignore
├── requirements.txt
├── scripts/
│   ├── __init__.py
│   ├── create_dataset.py
│   ├── validate_data.py
│   ├── model.py
│   └── evaluate.py
├── tests/
│   ├── __init__.py
│   ├── test_data.py
│   └── test_model.py
├── data/                 # generated CSV (ignored by Git)
└── reports/              # generated results (ignored by Git)
```

## Lab 1 — Environment and project setup

Prerequisites: Windows Git Bash, Python 3.11 or 3.12, Git, GitHub account, internet access. Use the supplied ZIP; it already includes correctly formatted project files. Do NOT recreate files by copying damaged code from the previous Word document.

1. Extract `Day3_MLOps_Executable_Project.zip` into your working folder; open Git Bash in the extracted `mlops-day3` directory.
2. Verify the working directory: `pwd` and `ls -a`. Look for `requirements.txt`, `scripts/`, `tests/`, `.github/`.
3. Create a virtual environment: `python -m venv .venv`.
4. Activate on Windows Git Bash: `source .venv/Scripts/activate` (Linux/macOS: `source .venv/bin/activate`).
5. Check Python: `python --version`.
6. Install required libraries: `python -m pip install -r requirements.txt`.
7. Verify installed tools: `python -m pytest --version`; `python -m black --version`; `python -m flake8 --version`.

Why: Isolate packages so all students run the same tools. Expected: no installation errors; `.venv` remains ignored by Git.

## Lab 2 — Create the delivery dataset

1. Open `scripts/create_dataset.py`; review the `create_dataset(n=1000, seed=42)` function.
2. From the project root run: `python -m scripts.create_dataset`.
3. Inspect: `head -n 5 data/deliveries.csv`.
4. Verify: `wc -l data/deliveries.csv` should show **1001 lines** (header + 1000 orders).

Why: Generate synthetic delivery examples with repeatable random seed. Output: `data/deliveries.csv` with `order_id`, `distance_km`, `raining`, `heavy_traffic`, and `late_delivery`. This CSV is generated, not committed.

## Lab 3 — Validate the dataset

1. Open `scripts/validate_data.py` and identify `REQUIRED_COLUMNS` and `validate_dataset(df)`.
2. Run: `python -m scripts.validate_data`.
3. Expected output: `Dataset validation passed`.
4. Explain that checks reject missing columns, empty datasets, null values, nonnumeric distances, negative distances, and non-binary flags/labels.

Why: Stop bad input before model training; validation failures exit nonzero so GitHub Actions can detect them.

## Lab 4 — Reusable model training function

1. Open `scripts/model.py`.
2. Identify `FEATURES = ["distance_km", "raining", "heavy_traffic"]`.
3. Identify `train_model(X_train, y_train, max_depth=5)` and `DecisionTreeClassifier`.
4. Explain: `fit()` learns from labeled data; returned model can call `predict()`.

Why: Separate model logic from data validation and evaluation so tests can import the same function.

## Lab 5 — Dataset unit tests

1. Open `tests/test_data.py`.
2. Review `test_valid_dataset`, `test_missing_column`, `test_negative_distance`, `test_invalid_label`, and `test_empty_dataset`.
3. Execute: `python -m pytest tests/test_data.py -v`.
4. Expected: **5 passed**.

Why: A test passes when invalid data is *correctly rejected* with `ValueError`; this is not a contradiction.

## Lab 6 — Model smoke tests

1. Open `tests/test_model.py`.
2. Review successful training, prediction count, and valid prediction labels.
3. Execute: `python -m pytest tests/test_model.py -v`.
4. Expected: **3 passed**.

Why: These smoke tests check basic behavior, not real-world production accuracy.

## Lab 7 — Entire test suite

1. Execute: `python -m pytest tests/ -v`.
2. Expected: **8 passed**.
3. Explain: CI will repeat the exact same command after Git push.

Troubleshooting: run commands from the `mlops-day3` root, with `.venv` active.

## Lab 8 — Code quality checks: Black and Flake8

1. Verify tools: `python -m black --version` and `python -m flake8 --version`.
2. Create a **temporary** `scripts/code_quality_demo.py` file with the demo snippet below; preserve indentation exactly.
3. Run `python -m black --check scripts/code_quality_demo.py`. EXPECT a nonzero exit and message that reformatting is needed.
4. Run `python -m black scripts/code_quality_demo.py`. This modifies only formatting.
5. Run `python -m black --check scripts/code_quality_demo.py`. EXPECT success.
6. Run `python -m flake8 scripts/code_quality_demo.py --max-line-length=88 --extend-ignore=E203,W503`. EXPECT `F401` for the unused `os` import.
7. Delete the `import os` line; rerun Flake8 and expect no output.
8. Change `return total` to `return final_cost`, rerun Flake8 and observe `F821` undefined name. Restore `return total` and rerun Flake8.
9. Remove temporary demo: `rm scripts/code_quality_demo.py`.
10. Run complete project checks: `python -m black --check scripts/ tests/` and `python -m flake8 scripts/ tests/ --max-line-length=88 --extend-ignore=E203,W503`.
11. Run again: `python -m pytest tests/ -v` and expect 8 passed.

Demo source, BEFORE Black:
```python
import os

def calculate_delivery_cost(distance,rate):
  total=distance*rate
  return total

print(calculate_delivery_cost(10,5))
```

Why: Black checks/changes formatting; Flake8 detects issues like unused imports and undefined variables. CI uses `black --check` instead of automatically changing source code.

## Lab 9 — Generate model performance report

1. Ensure dataset is present: `python -m scripts.create_dataset`.
2. Open `scripts/evaluate.py`; walk through read → validate → split → train → predict → metrics → save reports.
3. Execute: `python -m scripts.evaluate`.
4. Inspect: `ls reports`; `cat reports/metrics.json`; `cat reports/classification_report.txt`.
5. Expected: `metrics.json` contains accuracy, precision, recall, f1_score; text report contains per-class metrics.

Why: The report will later be generated by a GitHub-hosted runner. Scores are computed, not assumed. A held-out split illustrates evaluation; production hyperparameter choice should use validation/cross-validation.

## Lab 10 — GitHub Actions YAML

1. Open `.github/workflows/ml-ci.yml` from the provided project (already created).
2. Explain `on: push`, `pull_request`, `workflow_dispatch`.
3. Explain `jobs`, `runs-on`, `steps`, `uses`, `run` and YAML indentation.
4. Trace these steps: checkout → Python 3.11 → install dependencies → Black → Flake8 → generate CSV → validate → pytest → evaluate → upload artifact.
5. Run the exact checks locally (from project root):
   - `python -m black --check scripts/ tests/`
   - `python -m flake8 scripts/ tests/ --max-line-length=88 --extend-ignore=E203,W503`
   - `python -m scripts.create_dataset`
   - `python -m scripts.validate_data`
   - `python -m pytest tests/ -v`
   - `python -m scripts.evaluate`
6. Expected: all succeed; report exists.

Why: YAML indentation is structural. Do not paste formatted Word text directly into the YAML file; use the ready-made `.yml` from the project ZIP.

## Lab 11 — Push to GitHub and trigger workflow

1. If you extracted the ZIP, run `git init` then `git branch -M main` in the `mlops-day3` directory.
2. Set identity if needed: `git config user.name "Workshop Student"` and `git config user.email "student@example.com"` (use your real identity for actual work).
3. Review ignored data: `git status --short` and `git status --ignored --short`.
4. Commit: `git add .` then `git commit -m "Add Day 3 ML CI pipeline"`.
5. On GitHub, create an **empty** repository named `mlops-day3` (no starter README).
6. Connect remote: `git remote add origin https://github.com/USERNAME/mlops-day3.git` (replace USERNAME).
7. Push: `git push -u origin main` and complete sign-in if prompted.
8. GitHub → repository → Actions → **ML CI Pipeline** → latest run → `validate-and-evaluate` job.
9. Expected: the job runs checks and ends successfully. If Actions are disabled, enable them in repository settings as permitted.

Why: `push` is a workflow trigger; GitHub runs the configured YAML on a separate Ubuntu machine. GitHub Actions execution cannot be verified locally.

## Lab 12 — Download CI performance report

1. Open the successful GitHub Actions run.
2. Scroll to **Artifacts** and select `model-performance-report`.
3. Download/extract ZIP; view `metrics.json` and `classification_report.txt`.
4. Explain: GitHub workflow artifacts are distinct from MLflow model artifacts and Registry versions.

Expected: reports contain numeric evaluation metrics from the runner. Artifact availability depends on the workflow's successful evaluation and the repository's artifact permissions.

## Lab 13 — Intentionally fail and repair Black check

1. Open `scripts/model.py` and temporarily replace the formatted `FEATURES` assignment with: `FEATURES=["distance_km","raining","heavy_traffic"]`.
2. Check: `python -m black --check scripts/`. Expect failure.
3. Commit/push: `git add scripts/model.py`; `git commit -m "Demonstrate Black check failure"`; `git push`.
4. On GitHub Actions, the new workflow should fail at **Check Black formatting**.
5. Repair: `python -m black scripts/model.py`.
6. Verify: `python -m black --check scripts/`.
7. Commit/push repair: `git add scripts/model.py`; `git commit -m "Fix formatting"`; `git push`.
8. Confirm new run passes.

Why: Show red-to-green feedback. The intentional failure is expected; do not leave the repository broken.

## Lab 14 — Intentionally fail and repair dataset validation

1. Open `scripts/create_dataset.py` and change `"distance_km": distance.round(2)` to `"distance_km": -distance.round(2)`.
2. Run `python -m scripts.create_dataset` then `python -m scripts.validate_data`. Expected error: `Negative distances found`.
3. Commit/push: `git add scripts/create_dataset.py`; `git commit -m "Demonstrate dataset validation failure"`; `git push`.
4. GitHub Actions should fail at **Validate dataset**.
5. Restore the positive distance expression.
6. Execute `python -m black --check scripts/ tests/`; `python -m scripts.create_dataset`; `python -m scripts.validate_data`; `python -m pytest tests/ -v`.
7. Commit/push repair: `git add scripts/create_dataset.py`; `git commit -m "Fix dataset generation"`; `git push`.
8. Confirm the latest CI run passes.

Why: Valid Python can still produce invalid data; MLOps pipelines need both code and data checks.

## Lab 15 — Final end-to-end verification

1. Run from project root:
   - `python -m black --check scripts/ tests/`
   - `python -m flake8 scripts/ tests/ --max-line-length=88 --extend-ignore=E203,W503`
   - `python -m scripts.create_dataset`
   - `python -m scripts.validate_data`
   - `python -m pytest tests/ -v`
   - `python -m scripts.evaluate`
2. Verify eight tests passed; `reports/metrics.json` and `reports/classification_report.txt` exist.
3. Verify latest GitHub workflow run is green and its performance-report artifact is available.
4. Explain connections: Day 1 Git/DVC versions code and data; Day 2 MLflow tracks experiments; Day 3 GitHub Actions automates validation; Day 4 will package a prediction API in FastAPI/Docker.

Troubleshooting: `ModuleNotFoundError` → activate venv, install requirements, run from root. Missing CSV → run generator. Black/Flake8 failure → inspect exact line and fix. GitHub Actions failure → open the first failing step's log.

## Source-file appendix

The following listings exactly match the executable ZIP and are suitable for copy/paste if students need to recreate individual files. Preserve the indentation.

### `requirements.txt`

```text
numpy>=1.26,<3
pandas>=2.1,<3
scikit-learn>=1.4,<2
pytest>=8,<10
black>=24,<27
flake8>=7,<9
PyYAML>=6,<7
```

### `.gitignore`

```text
.venv/
__pycache__/
.pytest_cache/
*.pyc
data/*.csv
reports/
```

### `scripts/create_dataset.py`

```python
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
```

### `scripts/validate_data.py`

```python
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
```

### `scripts/model.py`

```python
from sklearn.tree import DecisionTreeClassifier

FEATURES = ["distance_km", "raining", "heavy_traffic"]


def train_model(X_train, y_train, max_depth=5):
    model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)
    return model
```

### `tests/test_data.py`

```python
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
```

### `tests/test_model.py`

```python
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
    predictions = train_model(df[FEATURES], df["late_delivery"]).predict(
        df[FEATURES]
    )
    assert set(predictions).issubset({0, 1})
```

### `scripts/evaluate.py`

```python
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
```

### `.github/workflows/ml-ci.yml`

```yaml
name: ML CI Pipeline

on:
  push:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  validate-and-evaluate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install -r requirements.txt

      - name: Check Black formatting
        run: python -m black --check scripts/ tests/

      - name: Run Flake8
        run: python -m flake8 scripts/ tests/ --max-line-length=88 --extend-ignore=E203,W503

      - name: Generate dataset
        run: python -m scripts.create_dataset

      - name: Validate dataset
        run: python -m scripts.validate_data

      - name: Run automated tests
        run: python -m pytest tests/ -v

      - name: Generate model performance report
        run: python -m scripts.evaluate

      - name: Upload performance report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: model-performance-report
          path: reports/
          if-no-files-found: warn
```

## Validation notes

- Local validation covers Python dataset generation, data validation, eight pytest tests, model report creation, Python compilation, and (when installed) Black and Flake8.
- A GitHub-hosted run requires the student to push the repository and inspect the Actions tab. No local validation can guarantee GitHub account settings, network access, or runner availability.
- In a real project, pin tested dependency versions, review third-party GitHub Actions versions, and enforce branch protection if passing checks should be required before merging.
