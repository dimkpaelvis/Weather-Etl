
  create view "weather_db"."analytics"."quality__weather_anomalies__dbt_tmp"
    
    
  as (
    

SELECT *
FROM "weather_db"."analytics"."stg_weather"
WHERE
    temperature_c < -50
    OR temperature_c > 60
    OR relative_humidity < 0
    OR relative_humidity > 100
  );