# Outlier policy

## Flags, not drops

mandi-rows **flags** bad rows — it never silently drops them. A flagged row stays in the output with a `flag` object attached.

## Flag vs error

| Category | Meaning | Row kept? |
|----------|---------|----------|
| `flag` | Data quality issue, may still be useful | Yes |
| `error` | Structurally invalid, cannot be processed | Yes, but marked as error |

## Example flag

```json
{"row": 3, "reason": "MISSING_PRICE", "category": "flag"}
```

Even a row with `MISSING_PRICE` is kept in the output, because the market name, date, and commodity are still useful for market tracking.

## Example error

```json
{"row": 0, "reason": "EMPTY", "category": "error"}
```
