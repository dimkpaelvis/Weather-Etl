import os
import psycopg2
from contextlib import contextmanager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure all required environment variables are set for database connection
required_vars = ["WEATHER_DB_HOST", "WEATHER_DB_PORT", "WEATHER_DB_NAME", "WEATHER_DB_USER", "WEATHER_DB_PASSWORD"]

# Check for missing environment variables and raise an error if any are not set
for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"Missing environment variable: {var}")

# Context manager to handle database connections safely, ensuring proper cleanup and error handling
@contextmanager
def get_connection():
    try:
        # Attempt to establish a connection to the PostgreSQL database using credentials from environment variables, with a connection timeout of 5 seconds
        conn = psycopg2.connect(
            host=os.getenv("WEATHER_DB_HOST"),
            port=os.getenv("WEATHER_DB_PORT"),
            dbname=os.getenv("WEATHER_DB_NAME"),
            user=os.getenv("WEATHER_DB_USER"),
            password=os.getenv("WEATHER_DB_PASSWORD"),
            connect_timeout=5
        )
        # Yield the connection object to the caller for use within the context block
        yield conn
    except psycopg2.OperationalError as e:
        raise RuntimeError(f"Database connection failed: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
