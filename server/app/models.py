from app import db, bcrypt
import enum


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),
                         index=False,
                         unique=True,
                         nullable=False)
    email = db.Column(db.String(80),
                      index=True,
                      unique=True,
                      nullable=False)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<User {self.username}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def generate_hash(password: str) -> str:
        return bcrypt.generate_password_hash(password)

    @staticmethod
    def compare_password_hash(password: str, password_hash: str) -> bool:
        return bcrypt.check_password_hash(password_hash, password)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def __repr__(self):
        return f'<Question {self.question}>'


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(80))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    correct = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Answer {self.answer}>'


class GameState(enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Game(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    state = db.Column(db.Enum(GameState))
    players = db.relationship("Player", backref="game", lazy="dynamic")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Game {self.id}>"


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(36), db.ForeignKey("game.id"))

    def save(self):
        db.session.add(self)
        db.session.commit()
