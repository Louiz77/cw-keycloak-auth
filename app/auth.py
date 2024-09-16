from . import keycloak_openid, keycloak_admin
from .utils import generate_token

class AuthCredentials:
    def __init__(self, email, password):
        self.email = email
        self.password = password

def login(credentials: AuthCredentials):
    token = keycloak_openid.token(credentials.email, credentials.password)
    userinfo = keycloak_openid.userinfo(token['access_token'])
    return "Logado com sucesso!"

def logout():
    keycloak_openid.logout(token['refresh_token'])
    return f"Usuário saiu."

def register(credentials: AuthCredentials):
    token_unico = generate_token()
    keycloak_admin.create_user({
        "email": credentials.email,
        "username": credentials.email,
        'attributes': {'token_unico': [token_unico]},
        "enabled": True,
        "credentials": [{"value": credentials.password, "type": "password"}]
    })
    return "Registrado com sucesso"

def update_password(credentials: AuthCredentials, token_recovery):
    user_id_dados = keycloak_admin.get_user_id(credentials.email)
    dados = keycloak_admin.get_user(user_id_dados)
    verify_token = dados.get('attributes', {}).get('token_unico', [])

    if token_recovery == verify_token[0]:
        keycloak_admin.set_user_password(user_id_dados, password=credentials.password, temporary=False)
        return "Usuário mudou de senha."
    else:
        return "Token informado está incorreto."
