
  
    

  create  table "weather_db"."analytics"."daily_overview__dbt_tmp"
  
  
    as
  
  (
    

SELECT
    city,
    DATE(time) AS date,
    AVG(temperature_c) AS avg_temp,
    AVG(relative_humidity) AS avg_humidity,
    AVG(wind_speed) AS avg_wind
FROM "weather_db"."analytics"."stg_weather"
GROUP BY city, DATE(time)
  );
  