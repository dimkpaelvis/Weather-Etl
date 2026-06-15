from db_connection import get_connection
from datetime import datetime

# This module provides functions to log the ETL pipeline runs and track processed files in the database.
def start_run(run_id): 
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO etl.pipeline_runs (run_id, started_at, status)
                VALUES (%s, %s, %s)
                """,
                (run_id, datetime.now(), "RUNNING")
            )
        conn.commit()


# Additional functions to update run status, log processed files, and check if a file has been processed can be added here.
def complete_run(run_id, files_processed, rows_loaded):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE etl.pipeline_runs
                SET completed_at = %s,
                    status = %s,
                    files_processed = %s,
                    rows_loaded = %s
                WHERE run_id = %s
                """,
                (datetime.now(), "SUCCESS", files_processed, rows_loaded, run_id)
            )
        conn.commit()


# In case of an error during the ETL process, this function can be called to mark the run as failed and log the error message.
def fail_run(run_id, error_msg):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE etl.pipeline_runs
                SET completed_at = %s,
                    status = %s,
                    error_message = %s
                WHERE run_id = %s
                """,
                (datetime.now(), "FAILED", str(error_msg), run_id)
            )
        conn.commit()

# This function logs the processed file in the database, along with the run_id and the number of rows loaded.
def log_file_processed(file_name, run_id, row_count):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO etl.processed_files (file_name, run_id, row_count)
                VALUES (%s, %s, %s)
                ON CONFLICT (file_name) DO NOTHING
                """,
                (file_name, run_id, row_count)
            )
        conn.commit()


# This function checks if a file has already been processed by querying the processed_files table in the database. It returns True if the file has been processed, and False otherwise.
def is_file_processed(file_name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 1 FROM etl.processed_files
                WHERE file_name = %s
                """,
                (file_name,)
            )
            return cur.fetchone() is not None