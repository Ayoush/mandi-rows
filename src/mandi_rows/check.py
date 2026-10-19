"""Validate mandi rows and flag outliers."""

import json
from dataclasses import dataclass, field
from functools import cache
from importlib.resources import files
from pathlib import Path

from .load import MandiRow


@cache
def _known_markets() -> dict[str, str]:
    """Load the bundled lookup once; editable installs use the repository data."""
    resource = files("mandi_rows").joinpath("data", "known_markets.json")
    if resource.is_file():
        text = resource.read_text(encoding="utf-8")
    else:
        text = (Path(__file__).resolve().parents[2] / "data" / "known_markets.json").read_text(
            encoding="utf-8"
        )
    mapping: dict[str, str] = json.loads(text)
    return {market.strip().casefold(): state for market, state in mapping.items()}


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
    - known market listed under an unexpected state

    Errors (fatal, block downstream processing):
    - negative price
    """
    result = CheckResult()
    known_markets = _known_markets()

    for i, row in enumerate(rows):
        expected_state = known_markets.get(row.market.strip().casefold())
        if expected_state is not None and row.state.strip().casefold() != expected_state.casefold():
            result.flags.append(
                RowFlag(
                    i,
                    "state",
                    "MARKET_STATE_MISMATCH",
                    f"Market {row.market!r} is expected in {expected_state!r}, got {row.state!r}",
                )
            )

        # Errors: negative prices
        for price_field, price_val in [
            ("min_price", row.min_price),
            ("max_price", row.max_price),
            ("modal_price", row.modal_price),
        ]:
            if price_val < 0:
                result.errors.append(
                    RowFlag(
                        i, price_field, "NEGATIVE_PRICE", f"{price_field} is negative: {price_val}"
                    )
                )

        # Flags: logical inconsistencies
        if row.min_price > row.max_price:
            result.flags.append(
                RowFlag(
                    i,
                    "min_price",
                    "MIN_GT_MAX",
                    f"min_price {row.min_price} > max_price {row.max_price}",
                )
            )

        if not (row.min_price <= row.modal_price <= row.max_price):
            result.flags.append(
                RowFlag(
                    i,
                    "modal_price",
                    "MODAL_OUTSIDE_RANGE",
                    f"modal_price {row.modal_price} outside [{row.min_price}, {row.max_price}]",
                )
            )

        if row.modal_price == 0:
            result.flags.append(RowFlag(i, "modal_price", "ZERO_PRICE", "modal_price is zero"))

    return result
