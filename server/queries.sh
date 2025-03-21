#!/bin/bash

usage() {
  echo "Usage: $0 -c  (to create/join/start game) or -p  (to get latest price)"
  exit 1
}

do_create=0
do_price=0

while getopts "cp" opt; do
  case $opt in
  c)
    do_create=1
    ;;
  p)
    do_price=1
    ;;
  *)
    usage
    ;;
  esac
done

# Ensure only one flag is provided.
if [ $do_create -eq 1 ] && [ $do_price -eq 1 ]; then
  echo "Please use only one flag: either -c or -p."
  usage
fi

if [ $do_create -eq 1 ]; then
  # Configuration for session creation and game start.
  ADMIN_KEY="123"
  SIMULATOR="GaussianMarketSimulator"
  EPOCHS=500
  TIMESTEP=1
  PLAYER_NAME="testing"

  # Create session.
  CREATE_RESPONSE=$(curl -s -X POST http://localhost:5000/create_session \
    -H "Content-Type: application/json" \
    -d "{\"admin_key\": \"$ADMIN_KEY\"}")
  SESSION_KEY=$(echo "$CREATE_RESPONSE" | jq -r '.session_key')
  echo "Session key: $SESSION_KEY"

  # Join session.
  JOIN_RESPONSE=$(curl -s -X POST http://localhost:5000/join_session \
    -H "Content-Type: application/json" \
    -d "{\"session_key\": \"$SESSION_KEY\", \"player_name\": \"$PLAYER_NAME\"}")
  PLAYER_KEY=$(echo "$JOIN_RESPONSE" | jq -r '.player_key')
  echo "Player key: $PLAYER_KEY"

  # Start game.
  START_RESPONSE=$(curl -s -X POST http://localhost:5000/start_game \
    -H "Content-Type: application/json" \
    -d "{\"admin_key\": \"$ADMIN_KEY\", \"session_key\": \"$SESSION_KEY\", \"simulator\": \"$SIMULATOR\", \"epochs\": $EPOCHS, \"timestep\": $TIMESTEP}")
  echo "Start game response: $START_RESPONSE"

elif [ $do_price -eq 1 ]; then
  # Get the latest price.
  PRICE_RESPONSE=$(curl -s -X POST http://localhost:5000/get_latest_price \
    -H "Content-Type: application/json")
  echo "Latest Price response: $PRICE_RESPONSE"
else
  usage
fi
