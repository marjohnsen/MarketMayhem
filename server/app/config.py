import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///market_mayhem.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_KEY = os.environ.get("ADMIN_KEY")

    if not ADMIN_KEY:
        raise ValueError("ADMIN_KEY is not set!")
