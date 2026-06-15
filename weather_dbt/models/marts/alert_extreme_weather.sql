{{ config(materialized='view') }}

SELECT
    city,
    time,
    temperature_c,
    wind_speed,
    relative_humidity
FROM {{ ref('stg_weather') }}
WHERE
    temperature_c > 35
    OR wind_speed > 20
    OR relative_humidity > 90