# Date format rules: DD/MM/YYYY vs ISO 8601

mandi-rows validates and parses arrival dates recorded in Agmarknet mandi price datasets.
This document outlines the supported formats, explains why Agmarknet relies on `DD/MM/YYYY`,
details how the parser processes date strings, and catalogs valid and invalid date examples.

---

## Why Agmarknet uses DD/MM/YYYY

Agmarknet (Agricultural Marketing Information Network), governed by the Directorate of Marketing
& Inspection (DMI) under the Ministry of Agriculture and Farmers Welfare, is India's national
portal for agricultural market data.

In India, the standard everyday and official government calendar format is Little-Endian:
**Day/Month/Year (`DD/MM/YYYY`)**.

- **Administrative standard:** State agricultural marketing boards (APMCs) and mandi operators
  enter daily arrivals using `DD/MM/YYYY`.
- **Portal exports:** Public CSV and web reports downloaded from Agmarknet retain this format
  (for example, `15/08/2024` for 15 August 2024).

However, modern software, data lakes, databases, and analytics tooling typically conform to
the international **ISO 8601 (`YYYY-MM-DD`)** standard (for example, `2024-08-15`). To bridge
raw government exports and modern data pipelines, mandi-rows supports both formats seamlessly.

---

## Supported formats

mandi-rows accepts two date formats for `Arrival_Date`:

| Format | Structure | Example | Accepted |
|---|---|---|---|
| **DD/MM/YYYY** | Day/Month/Year (slash delimiter) | `15/08/2024` (valid DD/MM/YYYY) | Yes |
| **ISO 8601** | Year-Month-Day (hyphen delimiter) | `2024-08-15` (valid ISO 8601) | Yes |

All other formats and delimiter combinations are rejected.

---

## How the parser handles both formats

Date parsing is implemented in [`src/mandi_rows/dates.py`](../src/mandi_rows/dates.py) via the `parse_date()` function.
During CSV ingestion in [`src/mandi_rows/load.py`](../src/mandi_rows/load.py), each row's `Arrival_Date` is verified.

The parser executes the following steps:

1. **Whitespace stripping:** Leading and trailing whitespace is stripped via `.strip()` (e.g., `" 15/08/2024 "` becomes `"15/08/2024"`).
2. **DD/MM/YYYY matching:** The string is first tested against the regex pattern:
   ```python
   _DMY_RE = re.compile(r"^(\d{1,2})/(\d{1,2})/(\d{4})$")
   ```
   This matches 1-2 digits for day, 1-2 digits for month, and exactly 4 digits for year, separated strictly by forward slashes (`/`). If matched, the groups are parsed as integers `(d, mo, y)` and passed to Python's `datetime.date(y, mo, d)`.
3. **ISO 8601 matching:** If the string does not match `_DMY_RE`, it is tested against:
   ```python
   _ISO_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
   ```
   This matches 4 digits for year, 2 digits for month, and 2 digits for day, separated strictly by hyphens (`-`). If matched, the groups are parsed as integers `(y, mo, d)` and passed to `datetime.date(y, mo, d)`.
4. **Calendar validation:** Instantiating `datetime.date(year, month, day)` performs strict calendar validation:
   - Verifies month is within `1..12`.
   - Verifies day is valid for the given month and year (including leap year rules for February).
   - If the date is invalid (such as `31/02/2024`), Python raises a `ValueError`.
5. **Rejection and LoadError:** If neither regex matches, or if calendar validation fails, `parse_date()` raises `ValueError(f"Cannot parse date: '{s}'. Expected DD/MM/YYYY or YYYY-MM-DD")`. The loader catches this and raises a `LoadError` indicating the row number and column.

---

## Examples

### Valid date examples

- `15/08/2024` (valid DD/MM/YYYY) — Agmarknet export format.
- `2024-08-15` (valid ISO 8601) — International standard format.
- `01/01/2024` — Single or double digit day and month with slashes.
- `29/02/2024` — Valid leap day (2024 is a leap year).

### Invalid and rejected date examples

The parser strictly enforces delimiter consistency and calendar correctness:

- `31/02/2024` (invalid - February has no 31st) — Calendar error: February never has 31 days.
- `2024/08/15` (not supported - must use `/` or `-` separator correctly) — Mixed style: year-first format must use hyphens (`-`) per ISO 8601, not slashes (`/`).
- `15-08-2024` (not supported) — Hyphens with day first are ambiguous and rejected.
- `08/15/2024` (not supported) — American `MM/DD/YYYY` format is rejected to prevent month/day ambiguity.
- `15/08/24` (not supported) — 2-digit years are rejected to prevent century ambiguity.
- `29/02/2023` (invalid) — 2023 is not a leap year.

---

## Timezone

Mandi prices are recorded as date-only business day observations.
No timestamp or timezone offset is recorded or required.
Do not add a time component, UTC offset, or timezone suffix (such as `T00:00:00Z`).
