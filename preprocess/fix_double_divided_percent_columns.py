from __future__ import annotations

from pathlib import Path
from decimal import Decimal, InvalidOperation
import shutil
import pandas as pd


# Original export headers (pre `fix_primary_headers.py`)
NEW_TO_OLD = {
    "scrap_rate": "Scrap Rate",
    "efficiency": "Efficiency",
    "utilization": "Utilization",
    "oee": "OEE",
    "labor_efficiency": "Labor Efficiency",
}

PERCENT_COLUMNS_NEW = set(NEW_TO_OLD.keys())


def _parse_percent_value(raw: str) -> Decimal | None:
    raw = "" if raw is None else str(raw)
    raw = raw.strip()
    if not raw.endswith("%"):
        return None
    num = raw[:-1].strip().replace(",", "")
    try:
        return Decimal(num)
    except InvalidOperation:
        return None


def _quantize4(d: Decimal) -> Decimal:
    return d.quantize(Decimal("0.0001"))


def fix_file(csv_path: Path) -> None:
    backup_path = csv_path.with_suffix(csv_path.suffix + ".bak")
    if not backup_path.exists():
        print(f"Skip (missing backup): {csv_path.name}")
        return

    current_df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    old_df = pd.read_csv(backup_path, dtype=str, keep_default_na=False)

    # Assume row order matches between old and current exports.
    n = min(len(current_df), len(old_df))
    if len(current_df) != len(old_df):
        print(f"Row count mismatch for {csv_path.name}: {len(old_df)} vs {len(current_df)}. Skipping.")
        return

    updated = False
    for new_col in PERCENT_COLUMNS_NEW:
        old_col = NEW_TO_OLD[new_col]
        if new_col not in current_df.columns or old_col not in old_df.columns:
            continue

        for i in range(n):
            old_raw = old_df.iloc[i][old_col]
            old_percent = _parse_percent_value(old_raw)
            if old_percent is None:
                continue

            # Values >100% get divided twice in our earlier run. Fix by multiplying by 100.
            if old_percent > Decimal("100"):
                # Set to the correct single conversion: (original_percent / 100).
                new_d = _quantize4(old_percent / Decimal("100"))
                current_df.iloc[i, current_df.columns.get_loc(new_col)] = f"{new_d}"
                updated = True

    if updated:
        backup_fix_path = csv_path.with_suffix(csv_path.suffix + ".double_fix.bak")
        if not backup_fix_path.exists():
            shutil.copy2(csv_path, backup_fix_path)
        current_df.to_csv(csv_path, index=False)
        print(f"Fixed double-divided percents: {csv_path.name}")
    else:
        print(f"No fixes needed: {csv_path.name}")


def fix_dir(primary_dir: Path) -> None:
    csv_paths = sorted(primary_dir.glob("*.csv"))
    if not csv_paths:
        raise FileNotFoundError(f"No CSVs found in {primary_dir}")

    for csv_path in csv_paths:
        fix_file(csv_path)


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent
    primary_dir = repo_root / "asset/processed/daily-shift/primary"
    fix_dir(primary_dir)

