from datetime import datetime
import glob
import os

from load import load_weather
from pipeline_logger import (
    start_run,
    complete_run,
    fail_run,
    is_file_processed
)

from extract import main as extract_main


def main():
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    total_files = 0
    total_rows = 0

    try:
        print(f"PIPELINE START | run_id={run_id}")
        start_run(run_id)

        # ✅ STEP 1: EXTRACT
        print("Running extract step...")
        extract_main()

        # ✅ STEP 2: LOAD (RAW ONLY)
        files = glob.glob("weather-etl-project/data/raw/*.csv")

        for file in files:

            if is_file_processed(file):
                print(f"Skipping already processed file: {file}")
                continue

            print(f"Processing file: {file}")
            rows = load_weather(file, run_id)

            total_files += 1
            total_rows += rows

        # ✅ STEP 3: TRANSFORM (DBT)
        print("Running dbt transformations...")
        os.system("cd weather-etl-project/dbt && dbt run")

        print("Running dbt tests...")
        os.system("cd weather-etl-project/dbt && dbt test")

        # ✅ COMPLETE
        complete_run(run_id, total_files, total_rows)

        print(f"PIPELINE COMPLETE ✅ | run_id={run_id}")

    except Exception as e:
        print(f"PIPELINE FAILED ❌ | {e}")
        fail_run(run_id, str(e))


if __name__ == "__main__":
    main()