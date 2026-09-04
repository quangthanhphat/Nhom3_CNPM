from abc import ABC, abstractmethod

from config import FactoryConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


class AbstractDatabase(ABC):
    def __init__(self):
        self.database_uri = FactoryConfig.get_config(
            "development"
        ).DATABASE_URI

        self.engine = create_engine(
            self.database_uri,
            poolclass=NullPool
        )

        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

        self.session = self.SessionLocal()

    @abstractmethod
    def init_database(self, app):
        pass