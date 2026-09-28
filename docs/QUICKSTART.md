# Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m unittest discover -s tests
python -m openops.cli.main demo
```

Windows: `.venv\Scripts\activate`.

For HTTP mode: `openops serve`, then call `GET /health` on port 8080.
