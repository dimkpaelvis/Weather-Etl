CREATE SCHEMA IF NOT EXISTS etl;

-- Track pipeline runs
CREATE TABLE IF NOT EXISTS etl.pipeline_runs (
    run_id TEXT PRIMARY KEY,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    status TEXT,
    files_processed INT DEFAULT 0,
    rows_loaded INT DEFAULT 0,
    error_message TEXT
);

-- Track processed files
CREATE TABLE IF NOT EXISTS etl.processed_files (
    file_name TEXT PRIMARY KEY,
    run_id TEXT,
    processed_at TIMESTAMP DEFAULT NOW(),
    row_count INT
);