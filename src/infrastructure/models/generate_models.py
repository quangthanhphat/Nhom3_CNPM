import os
import subprocess
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect



load_dotenv()

database_url = os.environ.get("POSTGREE_DATABASE_URL")

if not database_url:
    raise RuntimeError("POSTGREE_DATABASE_URL not found")

# Connect to PostgreSQL and get all tables in public schema
engine = create_engine(database_url)
inspector = inspect(engine)

tables = inspector.get_table_names(schema="public")

if not tables:
    raise RuntimeError("No tables found in public schema")

tables_arg = ",".join(tables)

output_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "generated_models.py"
)

subprocess.run(
    [
        "sqlacodegen",
        "--generator",
        "declarative",
        "--schemas",
        "public",
        "--tables",
        tables_arg,
        database_url
    ],
    stdout=open(output_file, "w", encoding="utf-8"),
    check=True
)

# Make generated models use the project's shared Base
with open(output_file, "r", encoding="utf-8") as file:
    content = file.read()

content = content.replace(
    "from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship\n",
    "from sqlalchemy.orm import Mapped, mapped_column, relationship\n"
)

content = content.replace(
    "class Base(DeclarativeBase):\n    pass\n",
    "from infrastructure.databases.base import Base\n"
)

with open(output_file, "w", encoding="utf-8") as file:
    file.write(content)

print(f"Models generated successfully! ({len(tables)} public tables)")