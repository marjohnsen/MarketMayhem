import uuid
from app.db import db


class Game(db.Model):
    """
    The Game model represents a game session. It has a key to identify the game and a state to track the game's state.
    """

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(8), unique=True, nullable=False, default=lambda: uuid.uuid4().hex[:8])
    state = db.Column(db.String(20), nullable=False, default="lobby")
    players = db.relationship("Player", backref="game", lazy=True)


class Player(db.Model):
    """
    The player model represents a player in a game. It has a name and a reference to the game it is in.
    """

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(8), unique=True, nullable=False, default=lambda: uuid.uuid4().hex[:8])
    name = db.Column(db.String(80), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)
