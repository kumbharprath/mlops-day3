# Day 3 MLOps — Executable Workshop Project

See the separate `Day3_Step_by_Step_Hands_on_Guide.md` for Labs 1–15.

Quick start from project root (Git Bash):

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
python -m black --check scripts/ tests/
python -m flake8 scripts/ tests/ --max-line-length=88 --extend-ignore=E203,W503
python -m scripts.create_dataset
python -m scripts.validate_data
python -m pytest tests/ -v
python -m scripts.evaluate
```

The CSV and reports are generated and intentionally ignored by Git.
