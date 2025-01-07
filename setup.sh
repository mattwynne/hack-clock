#!/bin/bash

set -e

sudo apt-get install python-dev-is-python3 --yes
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

