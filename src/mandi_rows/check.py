"""Validate mandi rows and flag outliers."""
from dataclasses import dataclass, field
from .load import MandiRow


@dataclass(frozen=True)
class RowFlag:
    row_index: int
    field: str
    code: str
    message: str


@dataclass
class CheckResult:
    flags: list[RowFlag] = field(default_factory=list)
    errors: list[RowFlag] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0


def check_rows(rows: list[MandiRow]) -> CheckResult:
    """
    Check a list of MandiRow objects for logical inconsistencies.

    Flags (non-fatal, do not block processing):
    - modal_price outside [min_price, max_price]
    - min_price > max_price
    - price == 0

    Errors (fatal, block downstream processing):
    - negative price
    """
    result = CheckResult()

    for i, row in enumerate(rows):
        # Errors: negative prices
        for price_field, price_val in [
            ("min_price", row.min_price),
            ("max_price", row.max_price),
            ("modal_price", row.modal_price),
        ]:
            if price_val < 0:
                result.errors.append(
                    RowFlag(i, price_field, "NEGATIVE_PRICE", f"{price_field} is negative: {price_val}")
                )

        # Flags: logical inconsistencies
        if row.min_price > row.max_price:
            result.flags.append(
                RowFlag(i, "min_price", "MIN_GT_MAX", f"min_price {row.min_price} > max_price {row.max_price}")
            )

        if not (row.min_price <= row.modal_price <= row.max_price):
            result.flags.append(
                RowFlag(
                    i, "modal_price", "MODAL_OUTSIDE_RANGE",
                    f"modal_price {row.modal_price} outside [{row.min_price}, {row.max_price}]"
                )
            )

        if row.modal_price == 0:
            result.flags.append(RowFlag(i, "modal_price", "ZERO_PRICE", "modal_price is zero"))

    return result
