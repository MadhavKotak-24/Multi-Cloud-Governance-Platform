import psycopg2
import psycopg2.extras

DB_CONFIG = {
    "dbname": "cloudgov",
    "user": "postgres",
    "password": "Postgres123!@#",   # change if different
    "host": "localhost",
    "port": 5432,
}

def get_connection():
    return psycopg2.connect(
        **DB_CONFIG,
        cursor_factory=psycopg2.extras.RealDictCursor
    )