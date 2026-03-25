from db import query_supabase
from helper import print_result

def get_daily_shift_data(date_of_shift: str, department: str | None = None, workcenter: str | None = None):
    parts = []
    if date_of_shift:
        parts.append(f"date_of_shift = '{date_of_shift}'")
    if workcenter:
        parts.append(f"workcenter = '{workcenter}'")
    if department:
        parts.append(f"department = '{department}'")
    where_clause = " WHERE " + " AND ".join(parts) if parts else ""

    sql = f"""
    SELECT 
        department,
        workcenter,
        part_name,
        operation,
        planned_production_hrs,
        actual_uptime_hrs,
        downtime_hrs,
        parts_produced,
        parts_scrapped,
        scrap_rate,
        efficiency,
        utilization,
        oee,
        earned_machine_hrs,
        earned_labor_hrs,
        actual_labor_hrs,
        labor_efficiency,
        labor_rate,
        workcenter_rate,
        child_part_count,
        original_good_pieces,
        department_no,
        manager_first_name,
        manager_last_name,
        workcenter_key,
        part_key,
        part_no,
        part_revision,
        operation_no,
        part_operation_key,
        crew_size
    FROM daily_shift
    {where_clause}
    """
    return query_supabase(sql)
    


def get_oee_trend(start_date: str, end_date: str, department: str | None = None, workcenter: str | None = None):
    
    parts = []
    if workcenter:
        parts.append(f"workcenter = '{workcenter}'")
    if department:
        parts.append(f"department = '{department}'")
    where_clause = " AND ".join(parts) if parts else ""
        
    sql = f"""
    SELECT 
        date_of_shift,
        avg(oee) as avg_oee,
        avg(scrap_rate) as avg_scrap_rate,
        avg(utilization) as avg_utilization
    FROM daily_shift
    WHERE date_of_shift BETWEEN '{start_date}' AND '{end_date}'{f" AND {where_clause}" if where_clause else ""}
    """
        

    sql += """
    GROUP BY date_of_shift
    ORDER BY date_of_shift ASC
    """

    return query_supabase(sql)
    


def get_top_scrap_day(start_date: str, end_date: str, limit: int=3):

    sql = f"""
    SELECT 
        date_of_shift,
        workcenter,
        department,
        avg(scrap_rate) as avg_scrap_rate,
        sum(parts_scrapped) as total_scrapped,
        sum(parts_produced) as total_produced
    FROM daily_shift
    WHERE date_of_shift BETWEEN '{start_date}' AND '{end_date}'
    and scrap_rate is not null
    GROUP BY date_of_shift, workcenter, department
    ORDER BY avg_scrap_rate desc
    LIMIT '{limit}'
    """


    return query_supabase(sql)
    





