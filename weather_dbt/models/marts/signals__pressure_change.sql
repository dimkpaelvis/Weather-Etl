{{ config(materialized='view') }}

SELECT
    city,
    time,
    surface_pressure,
    LAG(surface_pressure) OVER (
        PARTITION BY city ORDER BY time
    ) AS previous_pressure,
    surface_pressure - LAG(surface_pressure) OVER (
        PARTITION BY city ORDER BY time
    ) AS pressure_change
FROM {{ ref('stg_weather') }}
ORDER BY city, time