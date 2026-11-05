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


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        # Leap years: divisible by 4, and century years only if divisible by 400.
        ("29/02/2024", date(2024, 2, 29)),
        ("2024-02-29", date(2024, 2, 29)),
        ("29/02/2000", date(2000, 2, 29)),
        ("28/02/2023", date(2023, 2, 28)),
        # 30-day month boundary.
        ("30/04/2024", date(2024, 4, 30)),
        ("2024-06-30", date(2024, 6, 30)),
        ("30/09/2024", date(2024, 9, 30)),
        ("30/11/2024", date(2024, 11, 30)),
        # 31-day month boundary.
        ("31/01/2024", date(2024, 1, 31)),
        ("31/03/2024", date(2024, 3, 31)),
        ("31/05/2024", date(2024, 5, 31)),
        ("31/07/2024", date(2024, 7, 31)),
        ("31/08/2024", date(2024, 8, 31)),
        ("31/10/2024", date(2024, 10, 31)),
        ("2024-12-31", date(2024, 12, 31)),
        # Single-digit day and month are accepted in DD/MM/YYYY.
        ("1/1/2024", date(2024, 1, 1)),
        ("1/12/2024", date(2024, 12, 1)),
        ("9/9/2024", date(2024, 9, 9)),
    ],
)
def test_accepts_valid_dates(text, expected):
    assert parse_date(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        # Feb 29 in a non-leap year, including 1900 (century year not divisible by 400).
        "29/02/2023",
        "29/02/1900",
        "2023-02-29",
        "30/02/2024",
        # 31st of a 30-day month.
        "31/04/2024",
        "31/06/2024",
        "31/09/2024",
        "31/11/2024",
        "2024-04-31",
        # Day or month out of range.
        "0/1/2024",
        "32/01/2024",
        "1/0/2024",
        "1/13/2024",
        "2024-13-01",
        "2024-00-10",
        "2024-01-00",
    ],
)
def test_rejects_impossible_dates(text):
    with pytest.raises(ValueError):
        parse_date(text)


@pytest.mark.parametrize(
    "text",
    [
        "",
        "   ",
        "15-08-2024",
        "15/08/24",
        "2024/08/15",
        "2024-1-1",
        "2024-08-15T00:00:00",
        "15 Aug 2024",
    ],
)
def test_rejects_unsupported_formats(text):
    with pytest.raises(ValueError, match="Cannot parse date"):
        parse_date(text)
