#!/bin/bash
TITLE=$1
MESSAGE=$2
python3 core/discord_notifier.py "$TITLE" "$MESSAGE"
