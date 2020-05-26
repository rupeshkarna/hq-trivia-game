import uuid
from app.models import User, Game, GameState, Player
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


class GameService(object):
    MAX_PLAYER = 5

    @staticmethod
    def get_game() -> Game:
        game = Game.query.filter(Game.state == GameState.OPEN).first()
        if not game:
            game = Game(id=str(uuid.uuid4()),
                        state=GameState.OPEN)
            game.save()
            return game
        if len(game.players.all()) > GameService.MAX_PLAYER:
            game.state = GameState.IN_PROGRESS
            game.save()
            game = Game(id=str(uuid.uuid4()),
                        state=GameState.OPEN)
        return game

    @staticmethod
    def get_in_progress_games():
        return Game.query.filter(Game.state == GameState.IN_PROGRESS)

    def add_player_to_game(self, player_id: int, game: Game):
        player = Player(id=player_id, game_id=game.id)
        player.save()

    @staticmethod
    def find_game_by_id(id) -> Game:
        return Game.query.filter(Game.id == id).first()

    @staticmethod
    def get_open_game() -> Game:
        return Game.query.filter(Game.state == GameState.OPEN)
