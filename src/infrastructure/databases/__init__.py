from infrastructure.databases.factory_database import FactoryDatabase


def init_db(app):
    FactoryDatabase.get_database('POSTGREE').init_database(app)