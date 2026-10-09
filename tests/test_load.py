"""Tests for CSV loader."""
import pytest
from pathlib import Path
from mandi_rows.load import load_csv, LoadError

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
