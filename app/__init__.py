from flask import Flask
from keycloak import KeycloakAdmin, KeycloakOpenID
from .config import Config

# Configuração do Keycloak
keycloak_openid = KeycloakOpenID(
    server_url=Config.KEYCLOAK_SERVER_URL,
    client_id=Config.KEYCLOAK_CLIENT_ID,
    realm_name=Config.KEYCLOAK_REALM,
    client_secret_key=Config.KEYCLOAK_SECRET
)

keycloak_admin = KeycloakAdmin(
    server_url=Config.KEYCLOAK_SERVER_URL,
    username=Config.KEYCLOAK_ADMIN_USERNAME,
    password=Config.KEYCLOAK_ADMIN_PASSWORD,
    realm_name=Config.KEYCLOAK_REALM
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .routes import init_routes
    init_routes(app)

    return app
