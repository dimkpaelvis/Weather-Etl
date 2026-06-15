
  
    

  create  table "weather_db"."analytics"."stg_weather__dbt_tmp"
  
  
    as
  
  (
    

SELECT *
FROM (
    SELECT
        city,
        latitude,
        longitude,
        time,
        temperature_2m AS temperature_c,
        relative_humidity_2m AS relative_humidity,
        wind_speed_10m AS wind_speed,
        surface_pressure,
        run_id,
        ROW_NUMBER() OVER (
            PARTITION BY city, time
            ORDER BY run_id DESC
        ) AS row_num
    FROM raw.weather_hourly
    WHERE
        temperature_2m IS NOT NULL
        AND relative_humidity_2m BETWEEN 0 AND 100
        AND wind_speed_10m >= 0
) t
WHERE row_num = 1
  );
  