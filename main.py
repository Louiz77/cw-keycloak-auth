from keycloak import KeycloakAdmin
from keycloak import KeycloakOpenIDConnection
from keycloak import KeycloakOpenID
from flask import Flask, request
import secrets

app = Flask(__name__)
key = '214e6a96-3149-4df2-8846-2db1c1a9e4d3'

keycloak_connection = KeycloakOpenIDConnection(
                        server_url="http://localhost:8080/",
                        username='admin',
                        password='admin',
                        realm_name="master",
                        client_id="PythonClient",
                        client_secret_key=key,
                        verify=True)

keycloak_openid = KeycloakOpenID(server_url="http://localhost:8080/",
                                 client_id="PythonClient",
                                 realm_name="master",
                                 client_secret_key=key)

keycloak_admin = KeycloakAdmin(connection=keycloak_connection)

@app.route('/get_login', methods=['GET'])
def login_rqst():
    if request.method == 'GET':
        global password_sign
        global email_sign
        args = request.args
        password_sign = args.get("password")
        email_sign = args.get("email")
        try:
            login()
            return "Logado com sucesso!"
        except Exception as e:
            return f"Error: {e}"


@app.route('/get_reg', methods=['GET'])
def register_rqst():
    if request.method == 'GET':
        global password_create
        global email_create
        args = request.args
        password_create = args.get("password")
        email_create = args.get("email")
        try:
            register()
            return "Registrado com sucesso"
        except Exception as e:
            return f"Error: {e}"


@app.route('/get_unl', methods=['GET'])
def logout_rqst():
    if request.method == 'GET':
        try:
            logout()
            return f"Usuario {userinfo['email']} saiu."
        except Exception as e:
            return f"Error: {e}"

@app.route('/get_upd', methods=['GET'])
def update_rqst():
    if request.method == 'GET':
        global new_password
        global token_recovery
        global email_recovery
        args = request.args
        email_recovery = args.get("email")
        new_password = args.get("password")
        token_recovery = args.get("token")
        try:
            update_password()
            if response == 200:
                return "Usuario mudou de senha."
            elif response == 400:
                return "Token informado esta incorreto."
        except Exception as e:
            return f"Error: {e}"


def login():
    global token
    global userinfo
    token = keycloak_openid.token(email_sign, password_sign)
    userinfo = keycloak_openid.userinfo(token['access_token'])

def logout():
    keycloak_openid.logout(token['refresh_token'])

def register():
    token_unico = secrets.randbits(20)
    new_user = keycloak_admin.create_user({"email": email_create,
                                           "username": email_create,
                                           'attributes':
                                                {'token_unico': [token_unico]},
                                           "enabled": True,
                                           "credentials": [{"value": password_create,"type": "password",}]})

def update_password():
    global response
    user_id_dados = keycloak_admin.get_user_id(email_recovery)
    dados = keycloak_admin.get_user(user_id_dados)
    verify_token = dados.get('attributes', {}).get('token_unico', [])
    if token_recovery == verify_token[0]:
        response = 200
        get_id = dados.get('id')
        new_pass = keycloak_admin.set_user_password(get_id, password= new_password, temporary=False)
        token = ''
        userinfo = ''
    else:
        response = 400
