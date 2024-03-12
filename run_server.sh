#!/bin/sh

#export PYTHONPATH="$PYTHONPATH:$HOME/Projects/hack-clock/lib"
export PYTHONPATH="$PYTHONPATH:$HOME/hack-clock/lib"
cd srv/hackclock
#../../scripts/run_server.py --config "$HOME/Projects/hack-clock/tests/localsettings.conf"
../../scripts/run_server.py --config "$HOME/hack-clock/tests/localsettings.conf"
