
  create view "weather_db"."analytics"."alert_extreme_weather__dbt_tmp"
    
    
  as (
    

SELECT
    city,
    time,
    temperature_c,
    wind_speed,
    relative_humidity
FROM "weather_db"."analytics"."stg_weather"
WHERE
    temperature_c > 35
    OR wind_speed > 20
    OR relative_humidity > 90
  );