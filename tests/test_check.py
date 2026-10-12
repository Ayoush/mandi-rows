"""Tests for mandi row validation."""
from datetime import date
from mandi_rows.load import MandiRow
from mandi_rows.check import check_rows


def _row(**kwargs) -> MandiRow:  # type: ignore[return]
    defaults = dict(
        state="Maharashtra", district="Pune", market="Pune",
        commodity="Onion", variety="Onion", arrival_date=date(2024, 8, 15),
        min_price=1000, max_price=1500, modal_price=1200,
    )
    defaults.update(kwargs)
    return MandiRow(**defaults)  # type: ignore[arg-type]


def test_valid_row_no_flags():
    result = check_rows([_row()])
    assert result.ok
    assert len(result.flags) == 0


def test_negative_price_is_error():
    result = check_rows([_row(min_price=-100)])
    assert not result.ok
    assert any(e.code == "NEGATIVE_PRICE" for e in result.errors)


def test_min_gt_max_is_flag():
    result = check_rows([_row(min_price=2000, max_price=1000, modal_price=1500)])
    assert result.ok  # errors empty
    assert any(f.code == "MIN_GT_MAX" for f in result.flags)


def test_modal_outside_range_is_flag():
    result = check_rows([_row(modal_price=2000)])
    assert result.ok
    assert any(f.code == "MODAL_OUTSIDE_RANGE" for f in result.flags)


def test_zero_modal_price_is_flag():
    result = check_rows([_row(min_price=0, max_price=0, modal_price=0)])
    assert any(f.code == "ZERO_PRICE" for f in result.flags)
