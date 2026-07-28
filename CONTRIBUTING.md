# Contributing

Start with [docs/contributing.md](docs/contributing.md). A contribution is accepted only when a reviewer can identify its trigger, contract, example, evaluation condition, and known boundary.

Before opening a pull request, run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_repository.py
python scripts/evaluate_paper_reading.py evals/fixtures/paper-reading-demo/evidence-card.md evals/rubrics/paper-reading.yaml
```

Do not commit API keys, private paper PDFs, participant data, or unredacted conversation logs.
