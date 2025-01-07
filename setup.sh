#!/bin/bash

set -e

sudo apt-get install -y python3-smbus
sudo apt-get install -y i2c-tools
sudo apt-get install -y python-dev-is-python3
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cat > /etc/rc.local<< EOF 
#!/bin/sh -e

sudo /home/pi/hack-clock/run_server.sh &

exit 0
EOF
