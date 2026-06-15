import csv
from importlib.resources import files
from psycopg2.extras import execute_batch
from db_connection import get_connection
import os
import glob
from datetime import datetime
from pipeline_logger import log_file_processed

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

def get_processed_files():
    try:
        with open("weather-etl-project/data/processed_file.txt") as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        return set()

def mark_processed(file):
    with open("weather-etl-project/data/processed_file.txt", "a") as f:
        f.write(file + "\n")

def get_latest_csv(directory):
    files = glob.glob(os.path.join(directory, "*.csv"))
    
    if not files:
        raise RuntimeError("No CSV files found")

    latest_file = max(files, key=os.path.getctime)
    return latest_file



def load_weather(csv_path, run_id):
    """
    Loads weather data from a CSV file and inserts it into the raw.weather_hourly table in the database.

    Parameters:
        csv_path (str): Path to the CSV file containing weather data.
        run_id (str): Unique identifier for the ETL run, added to each row for traceability.

    The function reads the CSV, appends the run_id to each row, and performs a batch insert.
    """
    print(f"[LOAD] File: {csv_path} | run_id={run_id}")

   
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        rows = [tuple(row) for row in reader]


    print(f"[LOAD] Rows read: {len(rows)}")
    rows_with_run_id = [row + (run_id,) for row in rows]

    row_count = len(rows_with_run_id)

    with get_connection() as conn:
        with conn.cursor() as cur:
            execute_batch(
                cur,
                """
                INSERT INTO raw.weather_hourly (
                    city,
                    latitude,
                    longitude,
                    time,
                    temperature_2m,
                    relative_humidity_2m,
                    wind_speed_10m,
                    surface_pressure,
                    run_id
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT DO NOTHING
                """,
                rows_with_run_id,
                page_size=100
            )
        conn.commit()
    
    print(f"[LOAD] Complete | run_id={run_id}")
    log_file_processed(csv_path, run_id, row_count)

    return row_count


if __name__ == "__main__":
    data_dir = "weather-etl-project/data/raw"
    latest_file = get_latest_csv(data_dir)
    
    processed = get_processed_files()

    for file in files:
        if file in processed:
            continue

        load_weather(file, run_id)
        mark_processed(file)
