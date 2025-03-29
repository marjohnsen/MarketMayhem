from typing import Any, Dict, Tuple

import numpy as np
from flask import Blueprint, Response, jsonify, request
from models import Player

from app.game import games
from app.validators import GameValidators

game_routes = Blueprint("game_routes", __name__)


@game_routes.route("/get_latest_price", methods=["POST"])
def get_latest_price() -> Tuple[Response, int]:
    data: Dict[str, Any] = request.get_json() or {}
    validators = GameValidators(data)

    (
        validators.require_fields(["session_key", "player_key"])
        .validate_session_key()
        .validate_player_key()
        .check_errors()
    )

    epoch, latest_price = games[data["session_key"]].exchange.get_latest_price()

    response: Dict[str, int | float] = {"epoch": epoch, "price": latest_price}
    return jsonify(response), 201


@game_routes.route("/trade", methods=["POST"])
def trade() -> Tuple[Response, int]:
    data: Dict[str, Any] = request.get_json() or {}
    validators = GameValidators(data)

    (
        validators.require_fields(["session_key", "player_key", "position"])
        .validate_session_key()
        .validate_player_key()
        .validate_game_running()
        .validate_position()
        .check_errors()
    )

    epoch, leverage = games[data["session_key"]].exchange.trade(data["player_key"], int(data["position"]))

    return jsonify({"epoch": epoch, "leverage": leverage}), 201


@game_routes.route("/get_scoreboard", methods=["POST"])
def get_scoreboard() -> Tuple[Response, int]:
    data: Dict[str, Any] = request.get_json() or {}
    validators = GameValidators(data)
    validators.require_fields(["session_key"]).validate_session_key().validate_game_stopped().check_errors()

    engine = games[data["session_key"]]
    accounts = engine.exchange.accounts
    market = engine.exchange.market
    log_returns = market.log_return
    start_price = engine.exchange.start_price

    price_series = np.exp(np.cumsum(log_returns)) * start_price

    def forward_fill(arr: np.ndarray) -> np.ndarray:
        mask = ~np.isnan(arr)
        idx = np.maximum.accumulate(np.where(mask, np.arange(len(arr)), 0))
        return arr[idx]

    scoreboard = {}

    for player_key, account in accounts.items():
        player = Player.query.filter_by(session_key=data["session_key"]).first()
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

    return jsonify(scoreboard), 200
