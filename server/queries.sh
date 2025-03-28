#!/bin/bash

# Configuration
ADMIN_KEY="123"
EPOCHS=60
TIMESTEP=1
PLAYER_NAME="testing"

if [ "$1" == "start" ]; then
  CREATE_RESPONSE=$(curl -s -X POST http://localhost:5000/create_session \
    -H "Content-Type: application/json" \
    -d "{\"admin_key\": \"$ADMIN_KEY\"}")
  SESSION_KEY=$(echo "$CREATE_RESPONSE" | jq -r '.session_key')
  echo "Session key: $SESSION_KEY"

  JOIN_RESPONSE=$(curl -s -X POST http://localhost:5000/join_session \
    -H "Content-Type: application/json" \
    -d "{\"session_key\": \"$SESSION_KEY\", \"player_name\": \"$PLAYER_NAME\"}")
  PLAYER_KEY=$(echo "$JOIN_RESPONSE" | jq -r '.player_key')
  echo "Player key: $PLAYER_KEY"

  START_RESPONSE=$(curl -s -X POST http://localhost:5000/start_game \
    -H "Content-Type: application/json" \
    -d "{\"admin_key\": \"$ADMIN_KEY\", \"session_key\": \"$SESSION_KEY\", \"epochs\": $EPOCHS, \"timestep\": $TIMESTEP}")
  echo "Start game response: $START_RESPONSE"
fi

if [ "$1" == "price" ]; then
  PRICE_RESPONSE=$(curl -s -X POST http://localhost:5000/get_latest_price \
    -H "Content-Type: application/json" \
    -d "{\"session_key\": \"$2\", \"player_key\": \"$3\"}")
  echo "$PRICE_RESPONSE"
fi

if [ "$1" == "trade" ]; then
  TRADE_RESPONSE=$(curl -s -X POST http://localhost:5000/trade \
    -H "Content-Type: application/json" \
    -d "{\"session_key\": \"$2\", \"player_key\": \"$3\", \"position\": \"$4\"}")
  echo "$TRADE_RESPONSE"
fi

if [ "$1" == "score" ]; then
  SCORE_RESPONSE=$(curl -s -X POST http://localhost:5000/get_scoreboard \
    -H "Content-Type: application/json" \
    -d "{\"session_key\": \"$2\"}")
  echo "$SCORE_RESPONSE"
fi
