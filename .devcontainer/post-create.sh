#!/usr/bin/env bash
# Setups the repository.

# Stop on errors
set -e

cd "$(dirname "$0")/.."

python3 -m venv .venv
source .venv/bin/activate

git config --global --add safe.directory /workspaces/python-sapcommissions
pre-commit install
python3 -m pip install -e .
