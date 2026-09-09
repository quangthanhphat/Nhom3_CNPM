import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()


def main():
    database_url = os.environ.get("POSTGREE_DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "POSTGREE_DATABASE_URL not found"
        )

    engine = create_engine(database_url)

    sql = text("""
        ALTER TABLE film_labs
        ADD COLUMN IF NOT EXISTS profile_image_path TEXT,
        ADD COLUMN IF NOT EXISTS cover_image_path TEXT;
    """)

    with engine.begin() as connection:
        connection.execute(sql)

    print("Film lab image columns added successfully.")


if __name__ == "__main__":
    main()