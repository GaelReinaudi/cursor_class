"""
Quick connectivity check for the demo Postgres.
Run: python db_health.py   (requires psycopg2-binary)
"""
import psycopg2
import sys
from commons.logger import sentry_logger as logger

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
    logger.info("✅  Postgres is reachable.")
except Exception as exc:
    logger.error(f"❌  Postgres connection failed: {exc}")
    sys.exit(1) 