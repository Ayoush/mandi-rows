"""Tests for rollup aggregation."""
from datetime import date
from mandi_rows.load import MandiRow
from mandi_rows.rollup import rollup_daily, rollup_weekly


def _row(d: str, min_p: int, max_p: int, modal_p: int) -> MandiRow:
    from mandi_rows.dates import parse_date
    return MandiRow(
        state="Maharashtra", district="Pune", market="Pune",
        commodity="Onion", variety="Onion", arrival_date=parse_date(d),
        min_price=min_p, max_price=max_p, modal_price=modal_p,
    )


def test_daily_rollup_same_day_aggregates():
    rows = [
        _row("15/08/2024", 1000, 1500, 1200),
        _row("15/08/2024", 1100, 1600, 1300),
    ]
    result = rollup_daily(rows)
    assert len(result) == 1
    assert result[0].min_price == 1000
    assert result[0].max_price == 1600
    assert result[0].avg_modal_price == 1250.0


def test_daily_rollup_different_days_separate():
    rows = [
        _row("15/08/2024", 1000, 1500, 1200),
        _row("16/08/2024", 1100, 1600, 1300),
    ]
    result = rollup_daily(rows)
    assert len(result) == 2


def test_weekly_rollup_groups_by_week():
    # 12 Aug 2024 = Monday, 13 Aug = Tuesday — same week
    rows = [
        _row("12/08/2024", 1000, 1500, 1200),
        _row("13/08/2024", 1100, 1600, 1300),
    ]
    result = rollup_weekly(rows)
    assert len(result) == 1
    assert result[0].row_count == 2
