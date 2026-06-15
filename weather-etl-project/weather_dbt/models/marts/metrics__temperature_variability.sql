{{ config(materialized='view') }}

SELECT
    city,
    DATE(time) AS date,
    STDDEV(temperature_c) AS temp_variability
FROM {{ ref('stg_weather') }}
GROUP BY city, DATE(time)
ORDER BY temp_variability DESC