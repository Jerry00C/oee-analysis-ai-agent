from __future__ import annotations

from pathlib import Path
from decimal import Decimal, InvalidOperation
import re
import pandas as pd


PERCENT_COLUMNS = {
    # DB schema constraints imply these must be 0..1
    "scrap_rate",
    "efficiency",
    "utilization",
    "oee",
    "labor_efficiency",
}

# DB schema column groups
INT_COLUMNS = {
    "parts_produced",
    "parts_scrapped",
    "child_part_count",
    "accounting_job",
    "original_good_pieces",
    "department_no",
    "workcenter_key",
    "part_key",
    "part_no",
    "part_revision",
    "operation_no",
    "part_operation_key",
    "crew_size",
}

NUMERIC_4COLS = {
    "planned_production_hrs",
    "actual_uptime_hrs",
    "downtime_hrs",
    "earned_machine_hrs",
    "earned_labor_hrs",
    "actual_labor_hrs",
    "labor_rate",
    "workcenter_rate",
    # includes percent-based numeric(10,4) columns too; handled separately below
    "scrap_rate",
    "efficiency",
    "utilization",
    "oee",
    "labor_efficiency",
    "oee",
}


def _clean_number_text(s: str) -> str:
    # Remove thousands separators; keep decimals.
    return s.replace(",", "").strip()


def _parse_decimal_4(s: str) -> str | None:
    """
    Returns a string representation rounded to 4 decimal places.
    """
    s = s.strip()
    if s == "":
        return None

    s = _clean_number_text(s)
    try:
        d = Decimal(s)
    except InvalidOperation:
        return None

    # Always store with up to 4 decimal places so COPY into numeric(10,4) is predictable.
    return f"{d.quantize(Decimal('0.0001'))}"


def _normalize_value(col: str, raw: str) -> str:
    # Preserve empty values
    raw = "" if raw is None else str(raw)
    raw = raw.strip()
    if raw == "":
        return ""

    is_percent_col = col in PERCENT_COLUMNS

    # Percent values come like: "4.11%" or "66.61%"
    if is_percent_col and raw.endswith("%"):
        num = raw[:-1].strip()
        dec4 = _parse_decimal_4(num)
        if dec4 is None:
            return raw
        # Convert percentage to fraction.
        frac = (Decimal(dec4) / Decimal("100")).quantize(Decimal("0.0001"))
        return f"{frac}"

    # Some exports may omit the '%' sign but still use percent scale (e.g. "2.95" meaning 2.95%).
    # For percent columns, if the parsed value is > 1, assume it's in 0..100 and convert to 0..1.
    if is_percent_col:
        s = _clean_number_text(raw)
        try:
            d = Decimal(s)
        except InvalidOperation:
            return raw
        if d > 1:
            frac = (d / Decimal("100")).quantize(Decimal("0.0001"))
            return f"{frac}"

    # For numeric(10,4) columns: remove thousands separators.
    if col in NUMERIC_4COLS:
        dec4 = _parse_decimal_4(raw)
        return raw if dec4 is None else dec4

    # For int columns: remove thousands separators then parse as int.
    if col in INT_COLUMNS:
        s = _clean_number_text(raw)
        try:
            # Some CSVs might have "2.0" - int-cast after parsing.
            if "." in s:
                return str(int(Decimal(s)))
            return str(int(s))
        except (InvalidOperation, ValueError):
            return raw

    # Other columns: leave as-is (is_primary, text, etc.)
    return raw


def normalize_csv_numbers(csv_path: Path) -> None:
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)

    # Normalize only columns that exist in the file.
    for col in df.columns:
        if col in PERCENT_COLUMNS or col in NUMERIC_4COLS or col in INT_COLUMNS:
            df[col] = df[col].apply(lambda x: _normalize_value(col, x))

    # Write in-place with a backup.
    backup_path = csv_path.with_suffix(csv_path.suffix + ".bak")
    if not backup_path.exists():
        df.to_csv(backup_path, index=False)

    df.to_csv(csv_path, index=False)

    print(f"Normalized: {csv_path}")


def normalize_dir(dir_path: Path) -> None:
    csv_paths = sorted(dir_path.glob("*.csv"))
    if not csv_paths:
        raise FileNotFoundError(f"No CSV files found in {dir_path}")

    for csv_path in csv_paths:
        normalize_csv_numbers(csv_path)


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent
    primary_dir = repo_root / "asset/processed/daily-shift/primary"
    normalize_dir(primary_dir)

