# FilmLabProject

AI-powered Platform Connecting Film Photography Enthusiasts with Film Processing Labs.

## Project Structure

```text
FilmLabProject/
├── docs/
├── src/
│   ├── api/
│   │   ├── controllers/
│   │   │   ├── auth_controller.py
│   │   │   └── film_lab_controller.py
│   │   ├── schemas/
│   │   │   └── auth.py
│   │   ├── middleware.py
│   │   ├── requests.py
│   │   ├── responses.py
│   │   ├── routes.py
│   │   └── swagger.py
│   │
│   ├── domain/
│   │   ├── models/
│   │   │   ├── auth.py
│   │   │   ├── iauth_repository.py
│   │   │   └── user.py
│   │   ├── constants.py
│   │   └── exceptions.py
│   │
│   ├── infrastructure/
│   │   ├── databases/
│   │   │   ├── abstract_database.py
│   │   │   ├── base.py
│   │   │   ├── database_postgres.py
│   │   │   └── factory_database.py
│   │   │
│   │   ├── models/
│   │   │   ├── user_model.py
│   │   │   └── generated_models.py
│   │   │
│   │   ├── repositories/
│   │   │   ├── auth_repository.py
│   │   │   ├── film_lab_repository.py
│   │   │   └── user_repository.py
│   │   │
│   │   └── services/
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   └── film_lab_service.py
│   │
│   ├── scripts/
│   │
│   ├── app_logging.py
│   ├── app.py
│   ├── config.py
│   ├── cors.py
│   ├── create_app.py
│   ├── dependency_container.py
│   ├── error_handler.py
│   ├── requirements.txt
│   └── swagger_config.json
│
├── .gitignore
└── README.md