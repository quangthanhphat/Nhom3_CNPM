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
        CREATE TABLE IF NOT EXISTS post_images (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            post_id UUID NOT NULL,
            image_path TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),

            CONSTRAINT fk_post_images_post
                FOREIGN KEY (post_id)
                REFERENCES posts(id)
                ON DELETE CASCADE
        );
    """)

    with engine.begin() as connection:
        connection.execute(sql)

    print("post_images table created successfully.")


if __name__ == "__main__":
    main()