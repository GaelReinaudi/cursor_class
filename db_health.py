"""
Quick connectivity check for the demo Postgres.
Run: python db_health.py   (requires psycopg2-binary)
"""
import psycopg2
import sys

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="demo",
        user="demo",
        password="demo",
        connect_timeout=3,
    )
    conn.close()
    print("✅  Postgres is reachable.")
except Exception as exc:
    print("❌  Postgres connection failed:", exc)
    sys.exit(1) 