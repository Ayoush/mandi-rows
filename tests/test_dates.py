"""Tests for date parsing."""
import pytest
from datetime import date
from mandi_rows.dates import parse_date


def test_parses_dmy_format():
    assert parse_date("15/08/2024") == date(2024, 8, 15)


def test_parses_iso_format():
    assert parse_date("2024-08-15") == date(2024, 8, 15)


def test_strips_whitespace():
    assert parse_date(" 01/01/2024 ") == date(2024, 1, 1)


def test_rejects_invalid_date():
    with pytest.raises(ValueError):
        parse_date("31/02/2024")


def test_rejects_unknown_format():
    with pytest.raises(ValueError):
        parse_date("2024/08/15")
