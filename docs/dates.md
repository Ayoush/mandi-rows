# Date formats

mandi-rows accepts two date formats:

| Format | Example | Accepted |
|--------|---------|----------|
| DD/MM/YYYY | 15/04/2024 | Yes |
| ISO 8601 | 2024-04-15 | Yes |

All other formats are rejected.

## Rejected formats

- `15-04-2024` (hyphen with DD first) — ambiguous, rejected
- `04/15/2024` (MM/DD/YYYY) — rejected
- `15/04/24` (2-digit year) — rejected
- `31/02/2024` (invalid calendar date) — rejected with reason `INVALID_DATE`

## Timezone

Mandi prices are date-only values. No timezone is recorded or required. Do not add a timezone suffix.
