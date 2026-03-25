import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
import psycopg2
import pandas as pd

# Load environment variables from .env file
load_dotenv()

def query_supabase(sql_query, params=None):
    """
    Executes a SQL query on the Supabase PostgreSQL database using SQLAlchemy.

    Args:
        sql_query (str): The SQL query to execute.
        params (dict, optional): Dictionary of parameters for the SQL query.

    Returns:
        list[dict]: List of result rows as dictionaries.
    """
    superbase_url = os.getenv("SUPERBASE_URL")
    print(superbase_url)
    
    conn = psycopg2.connect(superbase_url)
    df = pd.read_sql_query(sql_query, conn, params=params)
    conn.close()
    return df



def fjeiow():
    print("fjeiowfejiwofjwoiefjwoiejf")