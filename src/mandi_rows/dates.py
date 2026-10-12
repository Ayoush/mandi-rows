"""Date parsing for Agmarknet formats."""
from datetime import date
import re

_DMY_RE = re.compile(r"^(\d{1,2})/(\d{1,2})/(\d{4})$")
_ISO_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")


def parse_date(s: str) -> date:
    """
    Parse a date string in DD/MM/YYYY or YYYY-MM-DD format.
    Raises ValueError for invalid dates (including 31/02/YYYY).
    """
    s = s.strip()
    m = _DMY_RE.match(s)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return date(y, mo, d)  # raises ValueError for invalid dates

    m2 = _ISO_RE.match(s)
    if m2:
        y, mo, d = int(m2.group(1)), int(m2.group(2)), int(m2.group(3))
        return date(y, mo, d)

    raise ValueError(f"Cannot parse date: '{s}'. Expected DD/MM/YYYY or YYYY-MM-DD")
