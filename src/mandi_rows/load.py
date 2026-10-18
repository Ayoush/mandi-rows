"""Load and parse Agmarknet CSV files."""
import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from .alias import resolve_commodity, normalise_unit
from .dates import parse_date
from .schema import REQUIRED_COLUMNS

@dataclass(frozen=True)
class MandiRow:
    state: str
    district: str
    market: str
    commodity: str
    variety: str
    arrival_date: date
    min_price: int
    max_price: int
    modal_price: int
    grade: str | None = None
    unit: str | None = None
    arrivals_qtl: float | None = None


class LoadError(Exception):
    def __init__(self, row_num: int, column: str, value: str, reason: str) -> None:
        self.row_num = row_num
        self.column = column
        self.value = value
        self.reason = reason
        super().__init__(f"Row {row_num} col '{column}': {reason} (got '{value}')")


def load_csv(path: Path, resolve_aliases: bool = False) -> list[MandiRow]:
    """
    Load an Agmarknet CSV file and return a list of MandiRow objects.
    Raises LoadError on the first malformed row.
    Missing optional columns are silently ignored.
    """
    rows: list[MandiRow] = []

    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            return rows

        missing = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
        if missing:
            raise LoadError(0, ", ".join(missing), "", "Missing required columns")

        for i, raw in enumerate(reader, start=2):  # row 1 = header
            try:
                arrival_date = parse_date(raw["Arrival_Date"])
            except ValueError as e:
                raise LoadError(i, "Arrival_Date", raw["Arrival_Date"], str(e)) from e

            try:
                min_p = int(raw["Min_Price"])
                max_p = int(raw["Max_Price"])
                modal_p = int(raw["Modal_Price"])

                for column, price, value in (
                    ("min_price", min_p, raw["Min_Price"]),
                    ("max_price", max_p, raw["Max_Price"]),
                    ("modal_price", modal_p, raw["Modal_Price"]),
                ):
                    if price < 0:
                        raise LoadError(
                            i,
                            column,
                            value,
                            "Price must be non-negative",
                        )
            except ValueError as e:
                raise LoadError(i, "price", "", str(e)) from e

            arrivals = None
            if "Arrivals_in_Qtl" in raw and raw["Arrivals_in_Qtl"].strip():
                try:
                    arrivals = float(raw["Arrivals_in_Qtl"])
                except ValueError as e:
                    raise LoadError(i, "Arrivals_in_Qtl", raw["Arrivals_in_Qtl"], str(e)) from e
            commodity = raw["Commodity"].strip()
            if resolve_aliases:
                commodity = resolve_commodity(commodity)

            rows.append(
                MandiRow(
                    state=raw["State"].strip(),
                    district=raw["District"].strip(),
                    market=raw["Market"].strip(),
                    commodity=commodity,
                    variety=raw["Variety"].strip(),
                    arrival_date=arrival_date,
                    min_price=min_p,
                    max_price=max_p,
                    modal_price=modal_p,
                    grade=raw.get("Grade", "").strip() or None,
                    unit=(
                      normalise_unit(raw_unit)
                      if (raw_unit := raw.get("Unit", "").strip())
                      else None
                    ),
                    arrivals_qtl=arrivals,
                )
            )

    return rows
