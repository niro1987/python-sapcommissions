#!/usr/bin/env bash
# Setups the repository.

# Stop on errors
set -e

cd "$(dirname "$0")/.."

echo "Installing development dependencies..."
python3 -m pip install -r requirements.txt --upgrade
