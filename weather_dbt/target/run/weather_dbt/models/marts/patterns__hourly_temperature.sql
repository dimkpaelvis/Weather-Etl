
  
    

  create  table "weather_db"."analytics"."patterns__hourly_temperature__dbt_tmp"
  
  
    as
  
  (
    

SELECT
    city,
    EXTRACT(HOUR FROM time) AS hour,
    AVG(temperature_c) AS avg_temp
FROM "weather_db"."analytics"."stg_weather"
GROUP BY city, hour
ORDER BY city, hour
  );
  