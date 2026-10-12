"""Column schema for Agmarknet mandi price data."""
from dataclasses import dataclass

# Required columns from Agmarknet CSV exports
REQUIRED_COLUMNS = [
    "State",
    "District",
    "Market",
    "Commodity",
    "Variety",
    "Arrival_Date",
    "Min_Price",
    "Max_Price",
    "Modal_Price",
]

# Optional columns that may appear
OPTIONAL_COLUMNS = [
    "Grade",
    "Unit",
    "Commodity_Code",
    "Variety_Code",
    "Arrivals_in_Qtl",
]


@dataclass(frozen=True)
class ColumnSpec:
    name: str
    dtype: str  # 'str', 'int', 'float', 'date'
    required: bool
    description: str


COLUMN_SPECS: list[ColumnSpec] = [
    ColumnSpec("State", "str", True, "State name"),
    ColumnSpec("District", "str", True, "District name"),
    ColumnSpec("Market", "str", True, "Mandi / market name"),
    ColumnSpec("Commodity", "str", True, "Commodity name"),
    ColumnSpec("Variety", "str", True, "Variety of commodity"),
    ColumnSpec("Arrival_Date", "date", True, "Date of arrival (DD/MM/YYYY or YYYY-MM-DD)"),
    ColumnSpec("Min_Price", "int", True, "Minimum price per quintal (rupees)"),
    ColumnSpec("Max_Price", "int", True, "Maximum price per quintal (rupees)"),
    ColumnSpec("Modal_Price", "int", True, "Modal (most common) price per quintal (rupees)"),
    ColumnSpec("Grade", "str", False, "Grade of commodity"),
    ColumnSpec("Unit", "str", False, "Unit of measurement"),
    ColumnSpec("Arrivals_in_Qtl", "float", False, "Quantity arrived in quintals"),
]
