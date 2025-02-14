from flask import Blueprint, request, jsonify
from app.db import db

game_routes = Blueprint("game_routes", __name__)
