# Contributing to mandi-rows

Welcome! mandi-rows is part of **Intervues Lab**. This guide explains everything you need.

---

## Quick overview

1. Find an issue, comment `I'll take this` to claim it.
2. Fork → branch → code → tests → PR.
3. Gremlin (AI reviewer) comments. A human mentor approves.
4. Fix feedback, get merged.

---

## Fork and clone

```bash
git clone https://github.com/YOUR-USERNAME/mandi-rows.git
cd mandi-rows
git remote add upstream https://github.com/Ayoush/mandi-rows.git
```

## Set up the environment

```bash
make dev       # creates venv, installs, lints, tests
make test      # tests only
make lint      # ruff only
```

## Commit style

Conventional Commits:

```
feat(schema): add arrival-quantity column
fix(money): rupee comma parsed as thousands separator
docs: add column dictionary to docs/columns.md
test(dates): 31/02 rejected as invalid date
```

## Adding a market file

1. Add a frozen CSV in `spec/markets/<market-name>.csv` (max 50 rows).
2. Add expected flags in `fixtures/expected/<market-name>.json`.
3. Update `registry/files.json`.
4. Add a test that loads both files and calls `check()`.
5. Run `make test`.

**One market file per PR, max 50 rows.** Larger files slow CI and are harder to review.

## What a good PR looks like

- One market file or one fix per PR.
- All tests pass locally.
- PR description fills every section.
- Names one alternative you rejected.

## Review flow

1. **Gremlin** posts automated feedback.
2. Fix issues, comment `ready for mentor review`.
3. **Human mentor** approves and merges.
