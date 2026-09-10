from flask import Flask, jsonify
from flask_cors import CORS
import re


# =========================
# Controllers
# =========================

from api.controllers.auth_controller import bp as auth_bp
from api.controllers.film_lab_controller import bp as film_lab_bp
from api.controllers.service_controller import bp as service_bp
from api.controllers.service_category_controller import bp as service_category_bp
from api.controllers.order_result_controller import order_result_bp
from api.controllers.order_controller import bp as order_bp
from api.controllers.processing_workflow_controller import bp as processing_workflow_bp
from api.controllers.payment_controller import bp as payment_bp
from api.controllers.delivery_controller import bp as delivery_bp

from api.controllers.digital_film_archive_controller import bp as digital_film_archive_bp
from api.controllers.digital_scan_controller import bp as digital_scan_bp
from api.controllers.archive_item_controller import bp as archive_item_bp

from api.controllers.post_controller import bp as post_bp
from api.controllers.comment_controller import bp as comment_bp

from api.controllers.workshop_controller import bp as workshop_bp
from api.controllers.workshop_registration_controller import bp as workshop_registration_bp

from api.controllers.photowalk_controller import bp as photowalk_bp
from api.controllers.photowalk_registration_controller import bp as photowalk_registration_bp

from api.controllers.marketplace_listing_controller import bp as marketplace_listing_bp
from api.controllers.marketplace_transaction_controller import bp as marketplace_transaction_bp
from api.controllers.marketplace_message_controller import bp as marketplace_message_bp
from api.controllers.transaction_fee_controller import bp as transaction_fee_bp

from api.controllers.rating_controller import bp as rating_bp
from api.controllers.favorite_controller import bp as favorite_bp

from api.controllers.complaint_controller import bp as complaint_bp
from api.controllers.support_controller import bp as support_bp

from api.controllers.notification_controller import bp as notification_bp
from api.controllers.knowledge_base_controller import bp as knowledge_base_bp

from api.controllers.ai_recommendation_controller import bp as ai_recommendation_bp
from api.controllers.ai_photography_assistant_controller import bp as ai_photography_assistant_bp


# =========================
# Swagger
# =========================

from api.swagger import spec
from flask_swagger_ui import get_swaggerui_blueprint


# =========================
# Create Flask App
# =========================

app = Flask(__name__)

CORS(app)


# =========================
# Register API Blueprints
# =========================

app.register_blueprint(auth_bp)
app.register_blueprint(order_result_bp)
app.register_blueprint(film_lab_bp)
app.register_blueprint(service_bp)
app.register_blueprint(service_category_bp)

app.register_blueprint(order_bp)
app.register_blueprint(processing_workflow_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(delivery_bp)

app.register_blueprint(digital_film_archive_bp)
app.register_blueprint(digital_scan_bp)
app.register_blueprint(archive_item_bp)

app.register_blueprint(post_bp)
app.register_blueprint(comment_bp)

app.register_blueprint(workshop_bp)
app.register_blueprint(workshop_registration_bp)

app.register_blueprint(photowalk_bp)
app.register_blueprint(photowalk_registration_bp)

app.register_blueprint(marketplace_listing_bp)
app.register_blueprint(marketplace_transaction_bp)
app.register_blueprint(marketplace_message_bp)
app.register_blueprint(transaction_fee_bp)

app.register_blueprint(rating_bp)
app.register_blueprint(favorite_bp)

app.register_blueprint(complaint_bp)
app.register_blueprint(support_bp)

app.register_blueprint(notification_bp)
app.register_blueprint(knowledge_base_bp)

app.register_blueprint(ai_recommendation_bp)
app.register_blueprint(ai_photography_assistant_bp)


# =========================
# Swagger JSON
# =========================

@app.route('/swagger.json')
def swagger_json():
    return jsonify(spec.to_dict())


# =========================
# Swagger UI
# =========================

SWAGGER_URL = '/docs'
API_URL = '/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Film Lab API'
    }
)

app.register_blueprint(
    swaggerui_blueprint,
    url_prefix=SWAGGER_URL
)


# =========================
# Generate Swagger Paths
# =========================

with app.test_request_context():

    for rule in app.url_map.iter_rules():

        # ---------------------------------
        # Skip Swagger UI
        # ---------------------------------

        if rule.endpoint.startswith('swagger_ui.'):
            continue

        # ---------------------------------
        # Skip static files
        # ---------------------------------

        if rule.endpoint.startswith('static'):
            continue

        # ---------------------------------
        # Skip swagger.json
        # ---------------------------------

        if rule.endpoint == 'swagger_json':
            continue

        # ---------------------------------
        # Convert Flask route to OpenAPI
        #
        # Flask:
        # /film-labs/<uuid:film_lab_id>
        #
        # OpenAPI:
        # /film-labs/{film_lab_id}
        # ---------------------------------

        openapi_path = rule.rule

        openapi_path = re.sub(
            r'<(?:[^:<>]+:)?([^<>]+)>',
            r'{\1}',
            openapi_path
        )

        # ---------------------------------
        # Store operations
        # ---------------------------------

        operations = {}

        allowed_methods = {
            'GET',
            'POST',
            'PUT',
            'DELETE',
            'PATCH'
        }

        for method in rule.methods:

            if method not in allowed_methods:
                continue

            method_lower = method.lower()

            operation = {
                'summary': f'{method} {openapi_path}',

                'operationId': (
                    f'{method_lower}_'
                    f'{rule.endpoint.replace(".", "_")}'
                ),

                'responses': {
                    '200': {
                        'description': 'Successful response'
                    },
                    '201': {
                        'description': 'Created successfully'
                    },
                    '400': {
                        'description': 'Bad request'
                    },
                    '401': {
                        'description': 'Unauthorized'
                    },
                    '403': {
                        'description': 'Forbidden'
                    },
                    '404': {
                        'description': 'Not found'
                    }
                },

                'security': [
                    {
                        'BearerAuth': []
                    }
                ]
            }

            # ---------------------------------
            # Path Parameters
            # ---------------------------------

            parameters = []

            for argument in rule.arguments:

                parameters.append({
                    'name': argument,
                    'in': 'path',
                    'required': True,
                    'schema': {
                        'type': 'string'
                    }
                })

            if parameters:
                operation['parameters'] = parameters

            operations[method_lower] = operation

        # ---------------------------------
        # Add path to OpenAPI specification
        # ---------------------------------

        if operations:

            print(
                f'Adding Swagger path: {openapi_path}'
            )

            spec.path(
                path=openapi_path,
                operations=operations
            )


# =========================
# Home
# =========================

@app.route('/')
def home():

    return jsonify({
        'message': 'Film Lab API is running',
        'swagger': '/docs'
    })


# =========================
# Run Application
# =========================

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=9999,
        debug=True
    )