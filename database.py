# Importing required libraries
import os
from io import StringIO
from sqlalchemy import create_engine
import pandas as pd

# Function to connect to the PostgreSQL database
def connect_to_db():
    db_url = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
    engine = create_engine(db_url)
    return engine

# Function to get data from a table within a specified time range
def get_data_from_table(table_name: str, start_time: str, end_time: str):
    engine = connect_to_db()
    query = f'SELECT * FROM "{table_name}"'
    
    if start_time and end_time:
        query += f" WHERE time >= '{start_time}' AND time <= '{end_time}'"
    
    df = pd.read_sql_query(query, engine)
    engine.dispose()
    return df

# Function to get data from a table as a CSV file within a specified time range
def get_data_from_table_as_csv(table_name: str, start_time: str = None, end_time: str = None):
    df = get_data_from_table(table_name, start_time, end_time)
    csv_data = StringIO()
    df.to_csv(csv_data, index=False)
    csv_data.seek(0)
    return csv_data

# Function to get CSV data from a table within a specified time range
def get_csv_data(table_name: str, start_time=None, end_time=None):
    df = get_data_from_table(table_name, start_time, end_time)
    return df.to_csv(index=False)