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

echo "Now use rasp-config to enable I2C. See https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c for details"
