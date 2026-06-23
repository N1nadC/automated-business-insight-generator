import pandas as pd
from sqlalchemy import text
from database.db_connection import engine

def run_query(query):
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)