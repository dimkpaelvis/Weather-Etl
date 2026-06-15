

SELECT
    city,
    DATE(time) AS date,
    AVG(temperature_c) AS daily_avg_temp,
    AVG(AVG(temperature_c)) OVER (
        PARTITION BY city
        ORDER BY DATE(time)
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_7d_avg
FROM "weather_db"."analytics"."stg_weather"
GROUP BY city, DATE(time)