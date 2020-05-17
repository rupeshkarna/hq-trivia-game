from app.models import User
from app.custom_response import CustomResponse
from app.schemas import UserSchema
from flask import jsonify


class UserService(object):

    def __init__(self, user):
        self.user = user

    def register(self):
        username = self.user.get("username")
        password = self.user.get("password")
        email = self.user.get("email")

        existing_user = User.query.filter(
            User.username == username or User.email == email).first()
        if existing_user:
            return jsonify(CustomResponse("User already registered", False)), 404

        user = User(username=username,
                    email=email,
                    password_hash=User.generate_hash(password))
        user.save()
        return UserSchema().jsonify(user)

    def login(self):
        username = self.user.get("username")
        password = self.user.get("password")

        existing_user = User.query.filter(User.username == username).first()
        if not existing_user:
            return jsonify(CustomResponse("User not found", False)), 404

        if not User.compare_password_hash(password, existing_user.password_hash):
            return jsonify(CustomResponse("Incorrect Password", False)), 404

        return jsonify(CustomResponse("Login Successful"))
