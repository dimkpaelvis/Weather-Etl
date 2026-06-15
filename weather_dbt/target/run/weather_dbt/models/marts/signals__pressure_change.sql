
  create view "weather_db"."analytics"."signals__pressure_change__dbt_tmp"
    
    
  as (
    

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
FROM "weather_db"."analytics"."stg_weather"
ORDER BY city, time
  );