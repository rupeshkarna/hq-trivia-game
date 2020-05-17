import json

from app import app
from flask import request
from app.service import UserService
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_raw_jwt
)


@app.route("/message")
@jwt_required
def index():
    return {'message': "Hello from server"}


@app.route("/registration", methods=["POST"])
def register():
    req = request.get_json()
    user_service = UserService(req)
    return user_service.register()


@app.route("/login", methods=["POST"])
def login():
    req = request.get_json()
    user_service = UserService(req)
    login = user_service.login()
    if login.status_code == 200:
        access_token = create_access_token(identity=req["username"])
        return dict(message=f"Logged in as {req['username']}",
                    access_token=access_token)
    return login
