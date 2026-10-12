"""CLI entry point for mandi-rows."""
import json
from pathlib import Path

import typer

from .load import load_csv
from .check import check_rows
from .rollup import rollup_daily

app = typer.Typer(name="mandi", help="Agmarknet mandi price data tools.")


@app.command("check")
def cmd_check(
    csv_file: Path = typer.Argument(..., help="Path to Agmarknet CSV file"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """Load and validate a mandi CSV file, printing any flags or errors."""
    rows = load_csv(csv_file)
    result = check_rows(rows)

    if json_output:
        typer.echo(
            json.dumps(
                {
                    "ok": result.ok,
                    "row_count": len(rows),
                    "flags": [
                        {"row": f.row_index, "field": f.field, "code": f.code, "message": f.message}
                        for f in result.flags
                    ],
                    "errors": [
                        {"row": f.row_index, "field": f.field, "code": f.code, "message": f.message}
                        for f in result.errors
                    ],
                }
            )
        )
    else:
        typer.echo(f"Loaded {len(rows)} rows from {csv_file}")
        if result.errors:
            for e in result.errors:
                typer.echo(f"  ERROR row {e.row_index}: [{e.code}] {e.message}")
        if result.flags:
            for f in result.flags:
                typer.echo(f"  FLAG  row {f.row_index}: [{f.code}] {f.message}")
        if result.ok:
            typer.echo("  OK (no errors)")


@app.command("rollup")
def cmd_rollup(
    csv_file: Path = typer.Argument(..., help="Path to Agmarknet CSV file"),
    weekly: bool = typer.Option(False, "--weekly", help="Aggregate by week instead of day"),
) -> None:
    """Aggregate prices by day (default) or week."""
    rows = load_csv(csv_file)
    result = rollup_daily(rows)
    typer.echo(f"Rolled up {len(rows)} rows into {len(result)} aggregates")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
