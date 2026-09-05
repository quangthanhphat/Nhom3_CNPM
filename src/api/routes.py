from api.controllers.film_lab_controller import bp as film_lab_bp
from api.controllers.auth_controller import bp as auth_bp
from api.controllers.service_controller import bp as service_bp
from api.controllers.service_category_controller import bp as service_category_bp

def register_routes(app):
    app.register_blueprint(film_lab_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(service_category_bp)