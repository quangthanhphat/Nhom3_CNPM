import os
import psycopg2
from dotenv import load_dotenv

load_dotenv("src/.env")

database_url = os.environ.get("POSTGREE_DATABASE_URL")

if not database_url:
    raise RuntimeError("POSTGREE_DATABASE_URL not found")

database_url = database_url.replace(
    "postgresql+psycopg2://",
    "postgresql://"
)

connection = psycopg2.connect(database_url)
connection.autocommit = True

cursor = connection.cursor()

cursor.execute("""
    SELECT
        pid,
        usename,
        state,
        wait_event_type,
        wait_event,
        query
    FROM pg_stat_activity
    WHERE datname = current_database()
    ORDER BY pid
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
connection.close()