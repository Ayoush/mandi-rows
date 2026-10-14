# mandi-rows

> Cleaners and checkers for public mandi price CSV snapshots: Agmarknet-style columns, vendored in-repo, no API key needed.

**Offline · Vendor frozen snapshots · MIT**

[![CI](https://github.com/Ayoush/mandi-rows/actions/workflows/ci.yml/badge.svg)](https://github.com/Ayoush/mandi-rows/actions/workflows/ci.yml)

---

## Run it in 5 minutes

**Prerequisites:** Python 3.12+

```bash
git clone https://github.com/Ayoush/mandi-rows.git
cd mandi-rows
make dev
```

`make dev` sets up a virtualenv, installs dependencies, runs the linter, and runs the full test suite. Everything runs offline — no API key, no network.

**In Codespaces or devcontainer:** click **Code → Codespaces → Create codespace on main** or **Reopen in Container** in VS Code.

---

## What this is

Agmarknet publishes daily mandi price CSVs for hundreds of markets. Real CSVs have dirty data: missing prices, rupees formatted with commas ("1,250"), UTF-8 BOM headers, duplicate market-day rows. This repo vendors a frozen snapshot and catalogs the cleaning rules as tests.

Each unit of work is one market file in `spec/markets/` and its expected rejection reasons. New daily files are infinite; CI stays fast because we work on a frozen subset.

---

## Project layout

```
src/mandi_rows/
  load.py      # CSV loader (BOM, encoding)
  check.py     # Row-level validation
  money.py     # Rupee string → paise integer
  report.py    # Flag report with stable row indices
  alias.py     # Commodity alias normalization
  schema.py    # Column schema and types
  cli.py       # mandi check command
  rollup.py    # Monthly modal-price rollup
spec/markets/  # Vendored CSV snapshots (frozen)
fixtures/
  raw/         # Input CSV files
  expected/    # Expected flag output JSON
registry/
  files.json   # AI planner reads this
docs/
  columns.md   # Column dictionary
  dates.md     # Date format rules
  outliers.md  # Flag vs error policy
```

---

## Quick example

```bash
# Check a market file for problems
python -m mandi_rows.cli check spec/markets/indore-wheat.csv

# Output:
# {"file": "indore-wheat.csv", "rows": 10, "flags": [{"row": 3, "reason": "MISSING_PRICE"}]}
```
## Documentation

- [Agmarknet CSV Columns](docs/columns.md) — Column names, data types, descriptions, and example values.
- [Date Format Rules](docs/dates.md) — Supported date formats.
- [Outlier Policy](docs/outliers.md) — How flags and errors are handled.
- [Commodities and Data Source](docs/commodities.md) — Agmarknet dataset, CSV structure, and commodity categories.
---

## Stack

| Layer | Tool |
|-------|------|
| Language | Python 3.12 |
| Testing | pytest |
| Lint / Format | ruff |
| Type checking | mypy |

---

## Contributing

New here? Start with a [`good first issue`](../../issues?q=label%3A%22good+first+issue%22). See [CONTRIBUTING.md](CONTRIBUTING.md).
