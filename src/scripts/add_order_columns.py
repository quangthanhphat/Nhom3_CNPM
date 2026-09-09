import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()

database_url = os.environ.get("POSTGREE_DATABASE_URL")

if not database_url:
    raise RuntimeError("POSTGREE_DATABASE_URL not found")


engine = create_engine(database_url)


def main():
    with engine.begin() as connection:
        connection.execute(text("""
            ALTER TABLE orders
            ADD COLUMN IF NOT EXISTS quantity INTEGER NOT NULL DEFAULT 1
        """))

        connection.execute(text("""
            ALTER TABLE orders
            ADD COLUMN IF NOT EXISTS delivery_type VARCHAR(20)
            NOT NULL DEFAULT 'pickup'
        """))

    print("Order columns added successfully:")
    print("- quantity")
    print("- delivery_type")


if __name__ == "__main__":
    main()