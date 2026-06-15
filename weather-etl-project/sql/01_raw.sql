CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.weather_hourly (
    city TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    time TIMESTAMP,
    temperature_2m DOUBLE PRECISION,
    relative_humidity_2m INTEGER,
    wind_speed_10m DOUBLE PRECISION,
    surface_pressure DOUBLE PRECISION,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    run_id TEXT
);
