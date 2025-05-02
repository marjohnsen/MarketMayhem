from typing import Any, Dict

import numpy as np
from flask import Blueprint, Response, jsonify, request

from app.db import db
from app.game import games
from app.models import Player
from app.validators import GameValidators

game_routes = Blueprint("game_routes", __name__)


@game_routes.route("/join_game", methods=["POST"])
def join_game() -> Response:
    data: Dict[str, Any] = request.get_json() or {}
    validators = GameValidators(data)

    (
        validators.require_fields(["game_key", "player_name"])
        .validate_game_key()
        .validate_new_player_name()
        .validate_state("waiting")
        .check_errors()
    )

    new_player = Player(name=data["player_name"], game_key=data["game_key"])  # type: ignore
    db.session.add(new_player)
    db.session.commit()

    return jsonify(
        {
            "message": f"Player {data['player_name']} has successfully joined the game.",
            "player_key": new_player.key,
        }
    )


@game_routes.route("/game_status", methods=["POST"])
def game_status() -> Response:
    data: Dict[str, Any] = request.get_json() or {}

    validators = GameValidators(data)

    if data["admin_key"]:
        (
            validators.require_fields(["game_key", "admin_key"])
            .validate_game_key()
            .validate_admin_key()
            .check_errors()
        )

    else:
        (
            validators.require_fields(["game_key", "player_key"])
            .validate_game_key()
            .validate_player_key()
            .check_errors()
        )

    return jsonify({"status": games[data["game_key"]].status})


@game_routes.route("/list_players", methods=["POST"])
def list_players() -> Response:
    data: Dict[str, Any] = request.get_json() or {}

    validators = GameValidators(data)

    if data["admin_key"]:
        (
            validators.require_fields(["game_key", "admin_key"])
            .validate_game_key()
            .validate_admin_key()
            .check_errors()
        )

    else:
        (
            validators.require_fields(["game_key", "player_key"])
            .validate_game_key()
            .validate_player_key()
            .check_errors()
        )

    players = db.session.query(Player).filter_by(game_key=data["game_key"]).all()
    player_names = [player.name for player in players]

    return jsonify({"players": player_names})


@game_routes.route("/get_latest_price", methods=["POST"])
def get_latest_price() -> Response:
    data: Dict[str, Any] = request.get_json() or {}
    validators = GameValidators(data)

    (
        validators.require_fields(["game_key", "player_key"])
        .validate_game_key()
        .validate_player_key()
        .check_errors()
    )

    epoch, latest_price = games[data["game_key"]].exchange.get_latest_price()

    response: Dict[str, int | float] = {"epoch": epoch, "price": latest_price}
    return jsonify(response)


@game_routes.route("/trade", methods=["POST"])
def trade() -> Response:
    data: Dict[str, Any] = request.get_json() or {}
    validators = GameValidators(data)

    (
        validators.require_fields(["game_key", "player_key", "position"])
        .validate_game_key()
        .validate_player_key()
        .validate_position()
        .check_errors()
    )

    epoch, leverage = games[data["game_key"]].exchange.trade(
        data["player_key"], int(data["position"])
    )

    return jsonify({"epoch": epoch, "leverage": leverage})


@game_routes.route("/get_scoreboard", methods=["POST"])
def get_scoreboard() -> Response:
    data: Dict[str, Any] = request.get_json() or {}
    validators = GameValidators(data)
    validators.require_fields(["game_key"]).validate_game_key().check_errors()

    engine = games[data["game_key"]]
    accounts = engine.exchange.accounts
    market = engine.exchange.market
    log_returns = market.log_return
    start_price = engine.exchange.start_price

    price_series = np.exp(np.cumsum(log_returns)) * start_price

    def forward_fill(arr: np.ndarray) -> np.ndarray:
        mask = ~np.isnan(arr)
        idx = np.maximum.accumulate(np.where(mask, np.arange(len(arr)), 0))
        return arr[idx]

    scoreboard: Dict[str, Any] = {}

    for player_key, account in accounts.items():
        player = Player.query.filter_by(game_key=data["game_key"]).first()
        player_name = player.name  # type: ignore
        position_changes = np.array(account["positions"])
        positions = forward_fill(np.cumsum(position_changes))
        portfolio = start_price * np.exp(np.cumsum(positions * log_returns))

        scoreboard[player_key] = {
            "positions": positions.tolist(),
            "portfolio": portfolio.tolist(),
            "score": portfolio[-1],
            "name": player_name,
        }

    scoreboard["price"] = {"series": price_series.tolist(), "start_price": start_price}

    return jsonify(scoreboard)
