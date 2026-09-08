import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

database_url = os.environ.get("POSTGREE_DATABASE_URL")

if not database_url:
    raise Exception("POSTGREE_DATABASE_URL not found")

database_url = database_url.replace(
    "postgresql+psycopg2://",
    "postgresql://"
)

connection = psycopg2.connect(database_url)

try:
    cursor = connection.cursor()

    # Remove the foreign key temporarily
    cursor.execute("""
        ALTER TABLE public.orders
        DROP CONSTRAINT IF EXISTS orders_service_id_fkey;
    """)

    # Remove old demo data related to orders.
    # CASCADE also removes data from tables that reference orders.
    cursor.execute("""
        TRUNCATE TABLE public.orders CASCADE;
    """)

    # Remove the old services table
    cursor.execute("""
        DROP TABLE IF EXISTS public.services;
    """)

    # Create the new services table
    cursor.execute("""
        CREATE TABLE public.services (
            id uuid NOT NULL DEFAULT gen_random_uuid(),

            film_lab_id uuid NOT NULL,
            category_id uuid NOT NULL,

            name varchar(150) NOT NULL,
            description text NULL,

            price numeric(10, 2) NOT NULL,

            turnaround_time_min integer NULL,
            turnaround_time_max integer NULL,

            processing_capacity integer NULL,

            supported_film_formats text NULL,

            processing_options text NULL,
            scanning_quality text NULL,
            printing_options text NULL,
            specialized_techniques text NULL,

            status varchar(20) NOT NULL DEFAULT 'active',
            created_at timestamp NOT NULL DEFAULT now(),
            updated_at timestamp NULL,

            CONSTRAINT services_pkey
                PRIMARY KEY (id),

            CONSTRAINT services_category_id_fkey
                FOREIGN KEY (category_id)
                REFERENCES public.service_categories (id),

            CONSTRAINT services_film_lab_id_fkey
                FOREIGN KEY (film_lab_id)
                REFERENCES public.film_labs (id)
        );
    """)

    # Restore the relationship from orders to services
    cursor.execute("""
        ALTER TABLE public.orders
        ADD CONSTRAINT orders_service_id_fkey
        FOREIGN KEY (service_id)
        REFERENCES public.services (id);
    """)

    connection.commit()

    print("Services table recreated successfully.")

except Exception as e:
    connection.rollback()
    print("ERROR:", e)

finally:
    cursor.close()
    connection.close()