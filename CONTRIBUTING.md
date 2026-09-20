# Contributing

Start with [docs/contributing.md](docs/contributing.md). A contribution is accepted only when a reviewer can identify its trigger, contract, example, evaluation condition, and known boundary.

Before opening a pull request, run:

```bash
python -m unittest discover -s tests -v
research-skills validate
research-skills evaluate evals/fixtures/paper-reading-demo/evidence-card.md evals/rubrics/paper-reading.yaml --source evals/fixtures/paper-reading-demo/source.md --format json
research-skills validate --run evals/fixtures/run-record-demo/run.yaml
```

Do not commit API keys, private paper PDFs, participant data, or unredacted conversation logs.
