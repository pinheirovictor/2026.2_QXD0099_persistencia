import os
import psycopg2
from psycopg2.extras import RealDictCursor

# pip install psycopg2

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "astronomia"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "2023"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )
    
def get_cursor(connection):
    return connection.cursor(cursor_factory=RealDictCursor)