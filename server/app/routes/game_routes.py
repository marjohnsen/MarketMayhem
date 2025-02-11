from flask import Blueprint, request, jsonify
from app.extensions import db

game_routes = Blueprint("game_routes", __name__)
