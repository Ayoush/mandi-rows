"""Known-market validation through the library and CSV CLI."""

import json
from datetime import date
from pathlib import Path

import pytest
from typer.testing import CliRunner

from mandi_rows.check import RowFlag, check_rows
from mandi_rows.cli import app
from mandi_rows.load import MandiRow


def _row(market: str, state: str, *, modal_price: int = 1200) -> MandiRow:
    return MandiRow(
        state=state,
        district="",
        market=market,
        commodity="Onion",
        variety="Other",
        arrival_date=date(2024, 8, 15),
        min_price=1000,
        max_price=1500,
        modal_price=modal_price,
    )


def test_azadpur_wrong_state_is_nonfatal_flag() -> None:
    result = check_rows([_row("Azadpur", "Maharashtra")])
    assert result.ok
    assert result.errors == []
    assert result.flags == [
        RowFlag(
            0,
            "state",
            "MARKET_STATE_MISMATCH",
            "Market 'Azadpur' is expected in 'Delhi', got 'Maharashtra'",
        )
    ]


@pytest.mark.parametrize(
    ("market", "state"),
    [
        ("Azadpur", "Delhi"),
        ("  aZaDpUr  ", "  dELHi  "),
        ("Jamshedpur", "Jharkhand"),
        ("Dahod", "Gujarat"),
        ("Unknown market", "Maharashtra"),
        ("", "Delhi"),
        ("Dahod APMC", "Maharashtra"),  # Do not guess suffixes or aliases.
    ],
)
def test_matching_or_unknown_market_has_no_flags(market: str, state: str) -> None:
    result = check_rows([_row(market, state)])
    assert result.ok
    assert result.flags == []


def test_normalized_market_still_flags_a_mismatch() -> None:
    result = check_rows([_row("  AZADPUR ", " Maharashtra ")])
    assert [flag.code for flag in result.flags] == ["MARKET_STATE_MISMATCH"]


def test_market_flag_preserves_row_index_and_price_checks() -> None:
    result = check_rows([_row("Azadpur", "Delhi"), _row("Azadpur", "Maharashtra", modal_price=-1)])
    assert not result.ok
    assert [(flag.row_index, flag.code) for flag in result.flags] == [
        (1, "MARKET_STATE_MISMATCH"),
        (1, "MODAL_OUTSIDE_RANGE"),
    ]
    assert [(error.row_index, error.code) for error in result.errors] == [(1, "NEGATIVE_PRICE")]


def test_lookup_contains_at_least_fifty_distinct_markets() -> None:
    path = Path(__file__).resolve().parents[1] / "data" / "known_markets.json"
    pairs = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=list)
    assert len(pairs) >= 50
    assert all(isinstance(k, str) and k.strip() for k, _ in pairs)
    assert all(isinstance(v, str) and v.strip() for _, v in pairs)
    assert len({market.strip().casefold() for market, _ in pairs}) == len(pairs)
    assert dict(pairs)["Azadpur"] == "Delhi"
    result = check_rows([_row(market, state) for market, state in pairs])
    assert result.ok
    assert result.flags == []


def test_csv_cli_reports_only_the_incorrect_known_pair(tmp_path: Path) -> None:
    path = tmp_path / "markets.csv"
    path.write_text(
        "State,District,Market,Commodity,Variety,Arrival_Date,Min_Price,Max_Price,Modal_Price\n"
        "Delhi,,Azadpur,Onion,Other,15/08/2024,1000,1500,1200\n"
        "Maharashtra,,Azadpur,Onion,Other,15/08/2024,1000,1500,1200\n"
        "Delhi,,Unknown market,Onion,Other,15/08/2024,1000,1500,1200\n",
        encoding="utf-8",
    )
    response = CliRunner().invoke(app, ["check", str(path), "--json"])
    assert response.exit_code == 0, response.output
    result = json.loads(response.output)
    assert result["ok"] is True
    assert result["row_count"] == 3
    assert result["errors"] == []
    assert len(result["flags"]) == 1
    assert result["flags"][0]["row"] == 1
    assert result["flags"][0]["field"] == "state"
    assert result["flags"][0]["code"] == "MARKET_STATE_MISMATCH"
