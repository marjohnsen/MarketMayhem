import uuid
import enum
from app.db import db


class SessionState(enum.Enum):
    LOBBY = "lobby"
    PLAYING = "playing"
    ENDED = "ended"


class PlayerState(enum.Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    BANNED = "banned"


class Session(db.Model):
    __tablename__ = "sessions"

    key = db.Column(db.String(8), primary_key=True, unique=True, nullable=False, default=lambda: uuid.uuid4().hex[:8])
    state = db.Column(db.Enum(SessionState), nullable=False, default=SessionState.LOBBY)

    players = db.relationship("Player", backref="session", lazy=True, cascade="all, delete-orphan")


class Player(db.Model):
    __tablename__ = "players"

    key = db.Column(db.String(8), primary_key=True, unique=True, nullable=False, default=lambda: uuid.uuid4().hex[:8])
    name = db.Column(db.String(20), nullable=False)
    state = db.Column(db.Enum(PlayerState), nullable=False, default=PlayerState.CONNECTED)
    session_key = db.Column(db.String(8), db.ForeignKey("sessions.key"), nullable=False, index=True)

    __table_args__ = (db.UniqueConstraint("name", "session_key", name="uq_player_name_gameplay"),)
