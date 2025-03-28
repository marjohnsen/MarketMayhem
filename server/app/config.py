import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///market_mayhem.db"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    ADMIN_KEY: str = os.environ.get("ADMIN_KEY") or ""

    if not ADMIN_KEY:
        raise ValueError("ADMIN_KEY is not set!")
