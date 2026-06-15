
  create view "weather_db"."analytics"."metrics__temperature_variability__dbt_tmp"
    
    
  as (
    

SELECT
    city,
    DATE(time) AS date,
    STDDEV(temperature_c) AS temp_variability
FROM "weather_db"."analytics"."stg_weather"
GROUP BY city, DATE(time)
ORDER BY temp_variability DESC
  );