{{ config(materialized='table') }}

SELECT
    city,
    EXTRACT(HOUR FROM time) AS hour,
    AVG(temperature_c) AS avg_temp
FROM {{ ref('stg_weather') }}
GROUP BY city, hour
ORDER BY city, hour