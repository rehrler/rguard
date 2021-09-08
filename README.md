# rguard :guardsman:

rguard is a *do it yourself* project with the aim to develop an opensource instruction for **building your own CO2
Sensor**. All instructions are here available including some CAD and STL files of a housing for 3d printing.

## Installation

### Raspberry Pi

1. Standard Installation of OS.

### Sensor Wiring

SCD30  | Raspberry Pi
--- | ---
VDD | 3V3 Power
GND | Ground
TX/SCL | GPIO 3 BCM 3 (SCL)
RX/SDA | GPIO 2 BCM 2 (SDA)
SEL | Ground

[source](https://pinout.xyz/pinout/i2c)

### rguard

1. Clone project on the raspberry pi

```shell
git clone https://github.com/rehrler/rguard.git --recursive
```

2. Install all dependencies and install the python packages

```shell
cd rguard && sudo apt-get update && sudo apt-get upgrade
sudo apt-get install -ylibgtk-3-dev build-essential gcc g++ pkg-config make hostapd python3-pip
pip3 install -r requirements.txt
```

3. Compile the rpi-i2c-timings

```shell
cd 3rdparty/rpi-i2c-timings && make
```

4. Setup the rpi-i2c-timings as a service at boot

```shell
sudo cp rpi-i2c /usr/bin/ && sudo cp rpi-i2c-timeout.service /etc/systemd/system/
sudo systemctl enable rpi-i2c-timeout.service
```

5. Setup the local access point and adjust the `/etc/create_ap.conf` with a SSID as your wifi name and a reasonable
   passphrase

```shell
cd ../linux-wifi-hotspot && make install-cli-only
sudo systemctl enable create_ap.service
```

6. Adjust paths and user in [src/services/rguard_sensor.service](src/services/rguard_sensor.service)
   , [src/services/rguard_server.service](src/services/rguard_server.service)
   and [src/services/rguard_led.service](src/services/rguard_led.service).

```text
WorkingDirectory=<path to rguard directory>
User=<your user>
ExecStart=<path to python exec> <path to capture_data.py/start_server.py/state_led.py>
```

7. Add rguard services to systemctl

```shell
cd ../../src/services/
sudo cp rguard_server.service /etc/systemd/system/ && sudo systemctl enable rguard_server.service
sudo cp rguard_sensor.service /etc/systemd/system/ && sudo systemctl enable rguard_sensor.service
sudo cp rguard_led.service /etc/systemd/system/ && sudo systemctl enable rguard_led.service
```

8. Reboot the raspberry pi, connect to the wifi with the given name and visit [10.0.0.1:5000](http://10.0.0.1:5000) and
   there you go!

## Notes

### CAD and STL File for 3d Printer

- top plate [cad/rguard_topplate.stl](cad/rguard_topplate.stl)
- base plate [cad/rguard_plate.stl](cad/rguard_plate.stl)

### Hardware

- Raspberry Pi 4 8gb [raspberrypi.org](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
- Sensirion
  SCD30 [sensirion.com](https://www.sensirion.com/en/environmental-sensors/carbon-dioxide-sensors/carbon-dioxide-sensors-scd30/)

## OS

- [Rapberry Pi OS Lite](https://www.raspberrypi.org/software/operating-systems/)

## Credits

- [SCD30 Python Interface](https://github.com/RequestForCoffee/scd30)
- [I2C timings](https://github.com/RequestForCoffee/rpi-i2c-timings)
- [Linux Wifi Hotspot](https://github.com/lakinduakash/linux-wifi-hotspot)