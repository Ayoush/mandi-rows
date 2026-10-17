"""Tests for CSV loader."""
from pathlib import Path

import pytest

from mandi_rows.load import LoadError, load_csv

SAMPLE_CSV = """State,District,Market,Commodity,Variety,Arrival_Date,Min_Price,Max_Price,Modal_Price
Maharashtra,Pune,Pune,Onion,Onion,15/08/2024,1000,1500,1200
Maharashtra,Mumbai,Vashi,Tomato,Local,16/08/2024,800,1200,1000
"""


def test_loads_valid_csv(tmp_path: Path) -> None:
    p = tmp_path / "mandi.csv"
    p.write_text(SAMPLE_CSV)
    rows = load_csv(p)
    assert len(rows) == 2
    assert rows[0].state == "Maharashtra"
    assert rows[0].commodity == "Onion"
    assert rows[0].modal_price == 1200


def test_raises_on_missing_column(tmp_path: Path) -> None:
    csv_text = "State,District,Market\nMaharashtra,Pune,Pune\n"
    p = tmp_path / "bad.csv"
    p.write_text(csv_text)
    with pytest.raises(LoadError):
        load_csv(p)


def test_raises_on_bad_date(tmp_path: Path) -> None:
    csv_text = SAMPLE_CSV.replace("15/08/2024", "31/02/2024")
    p = tmp_path / "bad.csv"
    p.write_text(csv_text)
    with pytest.raises(LoadError):
        load_csv(p)


def test_raises_on_non_integer_price(tmp_path: Path) -> None:
    csv_text = SAMPLE_CSV.replace("1200", "twelve_hundred")
    p = tmp_path / "bad.csv"
    p.write_text(csv_text)
    with pytest.raises(LoadError):
        load_csv(p)


@pytest.mark.parametrize(
    ("csv_column", "error_column", "negative_price"),
    [
        ("Min_Price", "min_price", "-1"),
        ("Max_Price", "max_price", "-1500"),
        ("Modal_Price", "modal_price", "-100"),
    ],
)
def test_raises_on_negative_price(
    tmp_path: Path,
    csv_column: str,
    error_column: str,
    negative_price: str,
) -> None:
    lines = SAMPLE_CSV.strip().splitlines()
    headers = lines[0].split(",")
    values = lines[1].split(",")

    values[headers.index(csv_column)] = negative_price
    csv_text = lines[0] + "\n" + ",".join(values) + "\n"

    p = tmp_path / "negative_price.csv"
    p.write_text(csv_text)

    with pytest.raises(LoadError) as exc_info:
        load_csv(p)

    assert exc_info.value.row_num == 2
    assert exc_info.value.column == error_column
    assert exc_info.value.value == negative_price


def test_normalises_unit_when_loading_csv(tmp_path: Path) -> None:
    csv_text = (
        "State,District,Market,Commodity,Variety,Arrival_Date,"
        "Min_Price,Max_Price,Modal_Price,Unit\n"
        "Maharashtra,Pune,Pune,Onion,Onion,15/08/2024,"
        "1000,1500,1200,Quintal\n"
    )

    p = tmp_path / "unit.csv"
    p.write_text(csv_text)

    rows = load_csv(p)

    assert rows[0].unit == "Qtl"
