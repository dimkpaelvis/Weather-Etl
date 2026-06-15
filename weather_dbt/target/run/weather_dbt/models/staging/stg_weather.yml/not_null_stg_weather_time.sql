
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select time
from "weather_db"."analytics"."stg_weather"
where time is null



  
  
      
    ) dbt_internal_test