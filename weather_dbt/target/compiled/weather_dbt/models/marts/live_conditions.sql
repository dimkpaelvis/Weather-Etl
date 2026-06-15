

SELECT
    city,
    time,
    temperature_c,
    relative_humidity,
    wind_speed,
    CASE
        WHEN temperature_c BETWEEN 18 AND 25
         AND relative_humidity < 70
         AND wind_speed < 10
        THEN 'GOOD'
        ELSE 'BAD'
    END AS outdoor_condition
FROM "weather_db"."analytics"."stg_weather"