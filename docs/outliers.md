# Outlier policy: flags vs errors

`check_rows()` in `src/mandi_rows/check.py` checks every row and returns a `CheckResult`. A problem is reported in one of two ways: as a **flag** or as an **error**.

## Flag vs error

| | Flag | Error |
|---|---|---|
| Severity | Non-fatal | Fatal |
| Effect | Informational. Processing continues. | Blocks downstream processing. |
| Stored in | `result.flags` | `result.errors` |

`result.ok` is `True` only when there are no errors. Flags do not change `result.ok`.

## No silent drop policy

mandi-rows **flags** bad rows. It never silently deletes them.

`check_rows()` does not remove or change any row. Every problem is recorded as a `RowFlag` with the row index, the field, a code, and a message. The row stays in the data, so the market name, date, and commodity are still available.

## Flags (non-fatal)

### MIN_GT_MAX
- **Cause:** `min_price` is greater than `max_price`.
- **Example:** `min_price=3000, max_price=2000` gives the message `min_price 3000 > max_price 2000`.

### MODAL_OUTSIDE_RANGE
- **Cause:** `modal_price` is not between `min_price` and `max_price`.
- **Example:** `min_price=1000, max_price=2000, modal_price=2500` gives the message `modal_price 2500 outside [1000, 2000]`.

### ZERO_PRICE
- **Cause:** `modal_price` is exactly zero.
- **Example:** `min_price=0, max_price=0, modal_price=0` gives the message `modal_price is zero`.

## Errors (fatal)

### NEGATIVE_PRICE
- **Cause:** `min_price`, `max_price`, or `modal_price` is below zero. One error is added for each negative field.
- **Example:** `min_price=-500, max_price=2000, modal_price=1500` gives the message `min_price is negative: -500`.

## Note

One row can have more than one problem. For example, a row with a negative `modal_price` gets a `NEGATIVE_PRICE` error, and it can also get flags such as `MODAL_OUTSIDE_RANGE`.
