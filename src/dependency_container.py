# Dependency Injection Container

from dependency_injector import containers, providers


# Import your services and repositories here
# from infrastructure.repositories import FilmLabRepository
# from services import FilmLabService


class Container(containers.DeclarativeContainer):
    # Define your providers
    # film_lab_repository = providers.Factory(FilmLabRepository)
    # film_lab_service = providers.Factory(
    #     FilmLabService,
    #     repository=film_lab_repository
    # )

    database = providers.Factory()