import json

from app import app


@app.route("/message")
def index():
    return {'message': "Hello from server"}
