from flask import Flask, jsonify

from api.swagger import spec


from api.controllers.film_lab_controller import bp as film_lab_bp
from api.controllers.auth_controller import bp as auth_bp
from api.controllers.community_controller import bp as community_bp
from api.controllers.events_controller import bp as events_bp


from infrastructure.databases import init_db

from flasgger import Swagger
from flask_swagger_ui import get_swaggerui_blueprint


def create_app():
    app = Flask(__name__)

    Swagger(app)

    # Đăng ký blueprint
    app.register_blueprint(film_lab_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(community_bp)
    app.register_blueprint(events_bp)

    # Thêm Swagger UI blueprint
    SWAGGER_URL = '/docs'
    API_URL = '/swagger.json'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Film Lab API"}
    )

    app.register_blueprint(
        swaggerui_blueprint,
        url_prefix=SWAGGER_URL
    )

    try:
        init_db(app)
    except Exception as e:
        print(f"Error initializing database: {e}")



    # Register routes for Swagger
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint.startswith('film_lab.'):
                view_func = app.view_functions[rule.endpoint]
                print(f"Adding path: {rule.rule} -> {view_func}")
                spec.path(view=view_func)

    @app.route("/swagger.json")
    def swagger_json():
        return jsonify(spec.to_dict())

    return app


if __name__ == '__main__':
    app = create_app()

    app.run(
        host='0.0.0.0',
        port=9999,
        debug=True
    )