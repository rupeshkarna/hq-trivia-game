from app import db


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


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def __repr__(self):
        return f'<Question {self.question}'


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(80))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    correct = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Answer {self.answer}'
