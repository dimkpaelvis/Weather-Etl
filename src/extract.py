''' 

Asks the user for a city name 
Converts city → latitude + longitude 
Fetches current weather for that location 
Extracts: temperature windspeed time 
Saves the data into a CSV file 
''' 

import requests 
import csv 
from datetime import datetime 
import os 

def safe_get(url, params=None): # Helper function to handle API requests with error handling and timeouts
    try:
        response = requests.get(url, params=params, timeout=(5, 10)) # Set connection timeout to 5 seconds and read timeout to 10 seconds
        response.raise_for_status() # Raise an exception for HTTP errors (4xx and 5xx)
        return response.json() # Return the JSON response if the request was successful
    except requests.exceptions.Timeout: # Handle timeout exceptions separately to provide a clear error message
        raise RuntimeError("API request timed out") # Handle other types of request exceptions (e.g., connection errors, HTTP errors) and provide a clear error message
    except requests.exceptions.RequestException as e: # Catch all other request-related exceptions and raise a RuntimeError with the original exception message for better debugging
        raise RuntimeError(f"API request failed: {e}")  # Handle other types of request exceptions (e.g., connection errors, HTTP errors) and provide a clear error message

def geocoding(city):
    city_url = 'https://geocoding-api.open-meteo.com/v1/search'
    data = safe_get(city_url, params={"name": city})

    if "results" not in data or not data["results"]:
        return None, None

    result = data["results"][0]
    return result["latitude"], result["longitude"]

def main():
    base_url = 'https://api.open-meteo.com/v1/forecast'
    continent = input(" Pick a number from the for the following continents." \
    "1. Europe 2. North America 3. Asia 4. Australia 5. Africa: ")
    if continent == '1':
        cities = ['London', 'Paris', 'Berlin', 'Madrid', 'Rome'] # Example European cities
    elif continent == '2':
        cities = ['New York', 'Los Angeles', 'Chicago', 'Toronto', 'Mexico City'] # Example North American cities
    elif continent == '3':
        cities = ['Tokyo', 'Shanghai', 'Mumbai', 'Seoul', 'Bangkok'] # Example Asian cities
    elif continent == '4':
        cities = ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide'] # Example Australian cities
    elif continent == '5':
        cities = ['Lagos', 'Cairo', 'Kinshasa', 'Johannesburg', 'Nairobi'] # Example African cities
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    os.makedirs("weather-etl-project/data/raw", exist_ok=True)  # Ensure the directory exists before the loop
    for city in cities:
        latitude, longitude = geocoding(city)

        if latitude is None:
            print(f"City not found: {city}")
            continue

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "wind_speed_10m",
                "surface_pressure"
            ],
            "forecast_days": 5
        }

        data = safe_get(base_url, params=params) # Fetch weather data using the safe_get function to handle potential API issues

        hourly = data.get("hourly", {})
        time = hourly.get("time", [])
        temp = hourly.get("temperature_2m", [])
        hum = hourly.get("relative_humidity_2m", [])
        wind = hourly.get("wind_speed_10m", [])
        pres = hourly.get("surface_pressure", [])

        row_limit = min(len(time), len(temp), len(hum), len(wind), len(pres), 50)

        fields = ['City','Latitude', 'Longitude', 'Time', 'Temperature_2m', 'Relative_Humidity_2m', 'Wind_Speed_10m', 'Surface_Pressure'] 

        data_rows = []

        for t, temp_val, hum_val, wind_val, pres_val in zip(
            time[:row_limit],
            temp[:row_limit],
            hum[:row_limit],
            wind[:row_limit],
            pres[:row_limit],
        ): # Limit to 50 rows to avoid excessive data and potential API limits
            results = [city, latitude, longitude, t, temp_val, hum_val, wind_val, pres_val]
            data_rows.append(results)

        # Save data to CSV file 

        file_path = f'weather-etl-project/data/raw/weather_{continent}_{date_str}.csv' # Use date in filename for uniqueness 

        file_exists = os.path.isfile(file_path) # Check if file already exists 
        file_empty = not file_exists or os.path.getsize(file_path) == 0  # Check if file does not exist or is empty

        with open(file_path, 'a', newline='', encoding='utf-8') as csvfile: # Open file in append mode (will create if not exists) 

            writer = csv.writer(csvfile) 

            if file_empty: # Write header if file does not exist or is empty

                writer.writerow(fields)  # Write header only if file does not exist or is empty

            writer.writerows(data_rows)  # Write data rows 

        if data_rows:
            last_row = data_rows[-1]
            print(
                f"Data saved! {city} -> {last_row[4]}°C at {last_row[3]} with humidity at {last_row[5]} "
                f"and wind speed of {last_row[6]}km/h"
            )
        else:
            print(f"Data saved! {city} -> no hourly rows were written.")

if __name__ == "__main__": 
    main() 

