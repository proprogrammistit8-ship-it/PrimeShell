#!/usr/bin/env bash

FLAKE_PATH="$HOME/.config/primeshell"

nix develop "$FLAKE_PATH" --command python3 "$FLAKE_PATH/main.py"