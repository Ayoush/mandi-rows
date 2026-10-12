# mandi-rows — 12-week roadmap (Oct–Dec 2026)

## M1 — Foundation (wk 1–2, Oct 6–19)

**Goal:** Beginner track open. CI green. Missing price and date validation work.

- [x] Repository setup, CI, devcontainer
- [ ] docs/columns.md — column dictionary
- [ ] docs/dates.md — date format rules
- [ ] docs/outliers.md — flag vs error policy
- [ ] Missing modal price flagged test
- [ ] Modal above max flagged test
- [ ] Date parse test (31/02 rejected)
- [ ] Duplicate market-day test
- [ ] Unit spelling alias test

---

## M2 — Core product works end-to-end (wk 3–6, Oct 20 – Nov 16)

**Goal:** `mandi check` CLI works. Indore wheat file added. Month rollup works.

- [ ] Indore wheat file (spec/markets/indore-wheat.csv)
- [ ] mandi check CLI
- [ ] Month rollup (mean of modal, ignores flagged rows)
- [ ] Commodity alias "Gwar" → "Guar"
- [ ] Arrival-quantity column (optional, negative rejected)

---

## M3 — Bugs and advanced features (wk 7–10, Nov 17 – Dec 14)

**Goal:** All known bugs fixed. 5+ market files in the catalog.

- [ ] Fix rupee comma parsed as thousands separator
- [ ] Fix UTF-8 BOM failing the loader
- [ ] Fix empty file reported as success
- [ ] Fix sort order changing row indices
- [ ] Fix alias applied twice

---

## M4 — Polish and v1.0 (wk 11–12, Dec 15–28)

**Goal:** 10+ market files. Public v1.0 release.

- [ ] CHANGELOG.md
- [ ] v1.0 GitHub release
