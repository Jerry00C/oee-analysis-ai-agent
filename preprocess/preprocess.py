from pathlib import Path
from datetime import date
import re
import pandas as pd

def primary_preprocess_daily_shift(input_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for file in input_dir.glob("*-primary.csv"):
        print(file)
        df = pd.read_csv(file)

        # Parse date from filenames like: 03-09-primary.csv
        # Correct the regex to handle filenames with year, e.g., '03-09-2021-primary.csv'
        m = re.match(r"^(?P<mm>\d{2})-(?P<dd>\d{2})-(?P<yyyy>\d{4})-(?P<type>primary|secondary)\.csv$", file.name)
        if not m:
            print(f"Skip (unexpected filename): {file.name}")
            continue
        mm = int(m.group("mm"))
        dd = int(m.group("dd"))
        yyyy = int(m.group("yyyy"))
        report_date = date(yyyy, mm, dd)  # change year if needed
        is_primary = m.group("type") == "primary"

        # Add columns for all rows
        df["date"] = report_date.isoformat()
        df["is_primary"] = is_primary

        # Move is_primary + date to first two columns
        first = ["is_primary", "date"]
        df = df[first + [c for c in df.columns if c not in first]]

        # Write updated CSV
        out_path = output_dir / file.name
        df.to_csv(out_path, index=False)

def secondary_preprocess_daily_shift(input_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for file in input_dir.glob("*-secondary.csv"):
        print(file)
        df = pd.read_csv(file)

        m = re.match(r"^(?P<mm>\d{2})-(?P<dd>\d{2})-(?P<type>primary|secondary)\.csv$", file.name)
        if not m:
            print(f"Skip (unexpected filename): {file.name}")
            continue

        mm = int(m.group("mm"))
        dd = int(m.group("dd"))
        report_date = date(2026, mm, dd)  # change year if needed
        is_primary = m.group("type") == "primary"

        # Add columns for all rows
        df["date"] = report_date.isoformat()
        df["is_primary"] = is_primary

        # Move is_primary + date to first two columns
        first = ["is_primary", "date"]
        df = df[first + [c for c in df.columns if c not in first]]

        # Write updated CSV
        out_path = output_dir / file.name
        df.to_csv(out_path, index=False)


if __name__ == "__main__":
    primary_preprocess_daily_shift(Path("asset/daily-shift"), Path("asset/processed/daily-shift/primary"))

    

    # secondary_preprocess_daily_shift(Path("asset/daily-shift"), Path("asset/processed/daily-shift/secondary"))
