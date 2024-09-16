from flask import request
from .auth import login, logout, register, update_password, AuthCredentials

def init_routes(app):
    @app.route('/get_login', methods=['GET'])
    def login_rqst():
        if request.method == 'GET':
            try:
                credentials = AuthCredentials(
                    email=request.args.get("email"),
                    password=request.args.get("password")
                )
                return login(credentials)
            except Exception as e:
                return f"Error: {e}"

    @app.route('/get_reg', methods=['GET'])
    def register_rqst():
        if request.method == 'GET':
            try:
                credentials = AuthCredentials(
                    email=request.args.get("email"),
                    password=request.args.get("password")
                )
                return register(credentials)
            except Exception as e:
                return f"Error: {e}"

    @app.route('/get_unl', methods=['GET'])
    def logout_rqst():
        if request.method == 'GET':
            try:
                return logout()
            except Exception as e:
                return f"Error: {e}"

    @app.route('/get_upd', methods=['GET'])
    def update_rqst():
        if request.method == 'GET':
            try:
                credentials = AuthCredentials(
                    email=request.args.get("email"),
                    password=request.args.get("password")
                )
                token_recovery = request.args.get("token")
                return update_password(credentials, token_recovery)
            except Exception as e:
                return f"Error: {e}"
