from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin


# =========================
# Swagger / OpenAPI Spec
# =========================

spec = APISpec(
    title="Film Lab API",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[
        MarshmallowPlugin()
    ],
)


# =========================
# JWT Bearer Authentication
# =========================

spec.components.security_scheme(
    "BearerAuth",
    {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }
)


# =========================
# Default Security
# =========================

spec.options["security"] = [
    {
        "BearerAuth": []
    }
]