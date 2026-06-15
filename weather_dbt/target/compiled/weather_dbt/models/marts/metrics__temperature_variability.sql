

SELECT
    city,
    DATE(time) AS date,
    STDDEV(temperature_c) AS temp_variability
FROM "weather_db"."analytics"."stg_weather"
GROUP BY city, DATE(time)
ORDER BY temp_variability DESC