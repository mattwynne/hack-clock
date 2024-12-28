#!/bin/bash

set -e

src=$(realpath "$(dirname "$0")")

export PYTHONPATH="$PYTHONPATH:$src/lib"
export PORT=8080
source "$src/venv/bin/activate"
cd "$src/srv/hackclock"
"$src/scripts/run_server.py" --config "$src/tests/localsettings.conf"
