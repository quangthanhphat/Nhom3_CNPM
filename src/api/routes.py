from api.controllers.film_lab_controller import bp as film_lab_bp
from api.controllers.auth_controller import bp as auth_bp


def register_routes(app):
    app.register_blueprint(film_lab_bp)
    app.register_blueprint(auth_bp)