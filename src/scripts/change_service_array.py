import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv("src/.env")

database_url = os.environ.get("POSTGREE_DATABASE_URL")

if not database_url:
    raise RuntimeError("POSTGREE_DATABASE_URL not found")

engine = create_engine(database_url)

statements = [
    """
    ALTER TABLE public.services
    ALTER COLUMN supported_film_formats TYPE text[]
    USING CASE
        WHEN supported_film_formats IS NULL THEN NULL
        ELSE string_to_array(supported_film_formats, ',')
    END
    """,

    """
    ALTER TABLE public.services
    ALTER COLUMN processing_options TYPE text[]
    USING CASE
        WHEN processing_options IS NULL THEN NULL
        ELSE string_to_array(processing_options, ',')
    END
    """,

    """
    ALTER TABLE public.services
    ALTER COLUMN specialized_techniques TYPE text[]
    USING CASE
        WHEN specialized_techniques IS NULL THEN NULL
        ELSE string_to_array(specialized_techniques, ',')
    END
    """,

    """
    ALTER TABLE public.services
    ALTER COLUMN scanning_quality TYPE text[]
    USING CASE
        WHEN scanning_quality IS NULL THEN NULL
        ELSE string_to_array(scanning_quality, ',')
    END
    """,

    """
    ALTER TABLE public.services
    ALTER COLUMN printing_options TYPE text[]
    USING CASE
        WHEN printing_options IS NULL THEN NULL
        ELSE string_to_array(printing_options, ',')
    END
    """
]

with engine.begin() as connection:
    for i, statement in enumerate(statements, start=1):
        print(f"Changing column {i}/5...")
        connection.execute(text(statement))
        print("Done.")

print("\nAll 5 columns changed to text[] successfully!")