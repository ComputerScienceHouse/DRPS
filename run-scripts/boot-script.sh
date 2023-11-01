#!/bin/sh
echo "_____ STARTING BOOT SCRIPT IN BACKGROUND ______"
screen -d -m /boot.sh

echo "_____ RUNNING API ______"
cd /app
python3 main.py
