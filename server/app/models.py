import uuid
import enum
from app.db import db


class GameState(enum.Enum):
    LOBBY = "lobby"
    IN_PROGRESS = "active"
    FINISHED = "finished"


class PlayerState(enum.Enum):
    ACTIVE = "active"
    BANNED = "banned"


class Game(db.Model):
    """
    The Game model represents a game session. It has a key to identify the game and a state to track the game's state.
    """

    __tablename__ = "game"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(8), unique=True, nullable=False, default=lambda: uuid.uuid4().hex[:8])
    state = db.Column(db.Enum(GameState), nullable=False, default=GameState.LOBBY)

    players = db.relationship("Player", backref="game", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        player_count = db.session.query(Player).filter_by(game_id=self.id).count()
        return f"<Game (Key: {self.key}, State: {self.state}, Players: {player_count})>"


class Player(db.Model):
    """
    The Player model represents a player in a game. It has a name and a reference to the game it is in.
    """

    __tablename__ = "player"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(8), unique=True, nullable=False, default=lambda: uuid.uuid4().hex[:8])
    name = db.Column(db.String(20), nullable=False)
    state = db.Column(db.Enum(PlayerState), nullable=False, default=PlayerState.ACTIVE)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False, index=True)

    __table_args__ = db.UniqueConstraint("name", "game_id", name="uq_player_name_game")

    def __repr__(self):
        return f"<Player {self.name} (Key: {self.key}, State: {self.state})>"
