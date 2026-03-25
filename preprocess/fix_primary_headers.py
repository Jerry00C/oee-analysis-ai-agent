from __future__ import annotations

from pathlib import Path
import shutil

import pandas as pd


OLD_TO_NEW = {
    "date": "date_of_shift",
    "Department": "department",
    "Workcenter": "workcenter",
    "Part Name": "part_name",
    "Operation": "operation",
    "Operators": "operators",
    "Note": "note",
    "Planned Production Hours": "planned_production_hrs",
    "Actual Uptime Hours": "actual_uptime_hrs",
    "Downtime Hours": "downtime_hrs",
    "Parts Produced": "parts_produced",
    "Parts Scrapped": "parts_scrapped",
    "Scrap Rate": "scrap_rate",
    "Earned Machine Hours": "earned_machine_hrs",
    "Efficiency": "efficiency",
    "Utilization": "utilization",
    "OEE": "oee",
    "Earned Labor Hours": "earned_labor_hrs",
    "Actual Labor Hours": "actual_labor_hrs",
    "Labor Efficiency": "labor_efficiency",
    "Labor Rate": "labor_rate",
    "Workcenter Rate": "workcenter_rate",
    "Child_Part_Count": "child_part_count",
    "Accounting Job": "accounting_job",
    "Original Good Pieces": "original_good_pieces",
    "Department_No": "department_no",
    "Manager_First_Name": "manager_first_name",
    "Manager_Middle_Name": "manager_middle_name",
    "Manager_Last_Name": "manager_last_name",
    "Workcenter_Key": "workcenter_key",
    "Part_Key": "part_key",
    "Part_No": "part_no",
    "Part_Revision": "part_revision",
    "Operation_No": "operation_no",
    "Part_Operation_Key": "part_operation_key",
    "Crew_Size": "crew_size",
}

# Match your DB schema (`daily_shift`), minus `id` and `created_at`.
# Note: your provided list omitted `operation_no`, but the DB schema defines it as NOT NULL.
EXPECTED_HEADERS = [
    "is_primary",
    "date_of_shift",
    "department",
    "workcenter",
    "part_name",
    "operation",
    "operators",
    "note",
    "planned_production_hrs",
    "actual_uptime_hrs",
    "downtime_hrs",
    "parts_produced",
    "parts_scrapped",
    "scrap_rate",
    "efficiency",
    "utilization",
    "oee",
    "earned_machine_hrs",
    "earned_labor_hrs",
    "actual_labor_hrs",
    "labor_efficiency",
    "labor_rate",
    "workcenter_rate",
    "child_part_count",
    "accounting_job",
    "original_good_pieces",
    "department_no",
    "manager_first_name",
    "manager_middle_name",
    "manager_last_name",
    "workcenter_key",
    "part_key",
    "part_no",
    "part_revision",
    "operation_no",
    "part_operation_key",
    "crew_size",
]


def _backup_file(path: Path) -> None:
    backup_path = path.with_suffix(path.suffix + ".bak")
    if not backup_path.exists():
        shutil.copy2(path, backup_path)


def fix_primary_csv_headers(primary_dir: Path) -> None:
    csv_paths = sorted(primary_dir.glob("*.csv"))
    if not csv_paths:
        raise FileNotFoundError(f"No CSVs found in: {primary_dir}")

    for csv_path in csv_paths:
        df = pd.read_csv(csv_path)
        df = df.rename(columns={k: v for k, v in OLD_TO_NEW.items() if k in df.columns})

        missing = [h for h in EXPECTED_HEADERS if h not in df.columns]
        if missing:
            raise ValueError(
                f"Header fix failed for {csv_path.name}. Missing columns: {missing}. "
                f"Existing columns: {list(df.columns)}"
            )

        # Drop any extra columns (e.g. `Department_Unassigned_Hours`) and enforce DB order.
        df = df[EXPECTED_HEADERS]

        _backup_file(csv_path)
        df.to_csv(csv_path, index=False)

        print(f"Fixed headers: {csv_path.name}")


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent
    primary_dir = repo_root / "asset/processed/daily-shift/primary"
    fix_primary_csv_headers(primary_dir)

