from langchain.tools import tool
from skills import get_daily_shift_data, get_oee_trend, get_top_scrap_day


@tool
def daily_shift_metric_tool(date_of_shift: str, workcenter: str | None = None, operation: str | None = None):
    """Fetch daily shift metrics for a given date (optionally filtered)."""
    df = get_daily_shift_data(date_of_shift, workcenter, operation)
    return df.to_json(orient="records", date_format="iso")


@tool
def oee_trend_tool(start_date: str, end_date: str, workcenter: str | None = None, operation: str | None = None):
    """Fetch OEE trend data between start_date and end_date (optionally filtered)."""
    df = get_oee_trend(start_date, end_date, workcenter, operation)
    return df.to_json(orient="records", date_format="iso")

@tool
def top_scrap_day_tool(start_date: str, end_date: str, limit=3):
    """Return the top scrap days between start_date and end_date (up to `limit`)."""
    df = get_top_scrap_day(start_date, end_date, limit)
    return df.to_json(orient="records", date_format="iso")




