import sqlite3
import time
import datetime
from scd30_i2c import SCD30

class SensorInterface(object):

    def __init__(self):
        self.scd30 = SCD30()
        self.scd30.set_measurement_interval(2)
        self.scd30.set_auto_self_calibration(active=True)
        time.sleep(5)
        self.scd30.start_periodic_measurement()
        time.sleep(2)

    def _write_to_db(self, temp: float, hum: float, co2: float):
        conn = sqlite3.connect("src/db/rguard_db.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO DHT_DATA values(datetime('now'), (?), (?), (?))", (temp, hum, co2))
        conn.commit()
        conn.close()

    def start_measurement(self):
        while True:
            if self.scd30.get_data_ready():
                measurement = self.scd30.read_measurement()
                if measurement is not None:
                    temp, hum, co2 = round(measurement[1],3), round(measurement[2],3), round(measurement[0],3)
                    print("[INFO]: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\t" + str(temp) + "\t" + str(hum) + "\t" + str(co2))
                    self._write_to_db(temp=temp, hum=hum, co2=co2)
            time.sleep(2)


if __name__ == "__main__":
    sensor = SensorInterface()
    sensor.start_measurement()
