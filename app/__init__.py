from flask import Flask
from flask_smorest import Api
from app.api.routes import blp as ChatBlueprint

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "super-secret-key"
    
    # OpenAPI / Swagger docs config
    app.config["API_TITLE"] = "Jarvish LLM API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    api = Api(app)
    api.register_blueprint(ChatBlueprint)

    return app
