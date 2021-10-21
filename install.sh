#!/bin/bash

# update system and install necessary packages
echo "updating system..."
sudo apt-get update && sudo apt-get upgrade -y
echo "installing system requirements..."
sudo apt-get install -y libgtk-3-dev build-essential gcc g++ pkg-config make hostapd python3-pip dnsmasq git vim

# install pip requirements
echo "installing python requirements..."
cd ~/rguard
pip3 install -r requirements.txt

# create db
echo "creating db..."
cd ~/rguard
python3 src/db/create_db.py

# install rpi-i2c-timings
echo "installing rpi-i2c-timings..."
cd ~/rguard/3rdparty/rpi-i2c-timings
make
sudo cp rpi-i2c /usr/bin/

sudo cp rpi-i2c-timeout.service /etc/systemd/system/
sudo systemctl enable rpi-i2c-timeout.service

# enable hotspot
echo "installing access point..."
cd ~/rguard/linux-wifi-hotspot
make install-cli-only

sudo rm /etc/create_ap.conf
sudo cp ~/rguard/src/config/create_ap.conf /etc/

sudo systemctl enable create_ap.service

# enable all services
echo "installing system services..."
cd ~/rguard/src/services/

sudo cp rguard_server.service /etc/systemd/system/
sudo systemctl enable rguard_server.service

sudo cp rguard_sensor.service /etc/systemd/system/
sudo systemctl enable rguard_sensor.service

sudo cp rguard_led.service /etc/systemd/system/
sudo systemctl enable rguard_led.service

sudo cp rguard_cleardb.service /etc/systemd/system/
sudo systemctl enable rguard_cleardb.service

sudo cp rguard_virtualwlan.service /etc/systemd/system/
sudo systemctl enable rguard_virtualwlan.service

echo "done."

# reboot
echo "rebooting..."
sudo reboot now