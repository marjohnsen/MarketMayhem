import uuid
import enum
from app.extensions import db


class GameState(enum.Enum):
    PENDING = "pending"
    ONGOING = "ongoing"
    GAME_OVER = "game_over"


class PlayerState(enum.Enum):
    IN_LOBBY = "in_lobby"
    IN_GAME = "in_game"
    BANNED = "banned"


class ConnectionState(enum.Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(8), unique=True, nullable=False, default=lambda: uuid.uuid4().hex[:8])
    state = db.Column(db.Enum(GameState), nullable=False, default=GameState.PENDING)

    players = db.relationship("Player", backref="game", lazy=True, cascade="all, delete-orphan")


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    state = db.Column(db.Enum(PlayerState), nullable=False, default=PlayerState.IN_LOBBY)
    connection = db.Column(db.Enum(ConnectionState), nullable=False, default=ConnectionState.CONNECTED)
    gameplay_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=True, index=True)

    __table_args__ = (db.UniqueConstraint("name", "gameplay_id", name="uq_player_name_gameplay"),)
