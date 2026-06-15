
  
    

  create  table "weather_db"."analytics"."daily__city_weather_ranking__dbt_tmp"
  
  
    as
  
  (
    

SELECT
    city,
    ROUND(AVG(temperature_c)::numeric, 2) AS avg_temp,
    ROUND(AVG(relative_humidity)::numeric, 2) AS humidity,
    ROUND(AVG(wind_speed)::numeric, 2) AS wind
FROM "weather_db"."analytics"."stg_weather"
WHERE DATE(time) = CURRENT_DATE
GROUP BY city
ORDER BY avg_temp DESC
  );
  