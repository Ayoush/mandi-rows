"""Aggregate mandi rows by day or week."""
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from .load import MandiRow


@dataclass(frozen=True)
class RollupKey:
    state: str
    market: str
    commodity: str
    period_start: date


@dataclass
class RollupRow:
    key: RollupKey
    min_price: int
    max_price: int
    avg_modal_price: float
    row_count: int


def rollup_daily(rows: list[MandiRow]) -> list[RollupRow]:
    """Group rows by (state, market, commodity, arrival_date) and aggregate prices."""
    return _rollup(rows, lambda d: d)


def rollup_weekly(rows: list[MandiRow]) -> list[RollupRow]:
    """Group rows by ISO week start (Monday) and aggregate prices."""
    def week_start(d: date) -> date:
        return d - timedelta(days=d.weekday())

    return _rollup(rows, week_start)


def _rollup(
    rows: list[MandiRow],
    period_fn: "Callable[[date], date]",  # type: ignore[name-defined]
) -> list[RollupRow]:
    from typing import Callable

    groups: dict[RollupKey, list[MandiRow]] = defaultdict(list)
    for row in rows:
        key = RollupKey(
            state=row.state,
            market=row.market,
            commodity=row.commodity,
            period_start=period_fn(row.arrival_date),
        )
        groups[key].append(row)

    result: list[RollupRow] = []
    for key, group in groups.items():
        result.append(
            RollupRow(
                key=key,
                min_price=min(r.min_price for r in group),
                max_price=max(r.max_price for r in group),
                avg_modal_price=sum(r.modal_price for r in group) / len(group),
                row_count=len(group),
            )
        )
    return result
