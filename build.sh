#!/bin/bash
imageName=bot_logic

echo "Copying conn_string.txt to variables folder..."
cp conn_string.txt ./db/variables/conn_string.txt

echo Rebuilding $imageName...
docker-compose build --no-cache $imageName

echo Docker Composing down...
docker compose down

echo Docker Composing Up...
docker compose up
