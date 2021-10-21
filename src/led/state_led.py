import time
import RPi.GPIO as GPIO
import sqlite3

# src: https://sciencetaskforce.ch/en/policy-brief/on-the-use-of-co2-sensors-in-schools-and-other-indoor-environments/
UPPER_BOUND = 1000.0
MIDDLE_BOUND = 800.0

B_LED = 11
G_LED = 13
R_LED = 15


def get_average_co2_min() -> float:
    conn = sqlite3.connect("src/db/rguard_db.db")
    cursor = conn.cursor()
    co2, nb_entries = 0.0, 0
    for row in cursor.execute("SELECT * FROM DHT_DATA ORDER BY timestamp DESC LIMIT 60"):
        co2 += row[3]
        nb_entries += 1
    conn.close()
    co2 /= nb_entries
    return co2


# GPIO configuration
GPIO.setmode(GPIO.BOARD)
GPIO.setup(B_LED, GPIO.OUT)
GPIO.setup(G_LED, GPIO.OUT)
GPIO.setup(R_LED, GPIO.OUT)

GPIO.output(B_LED, GPIO.LOW)
GPIO.output(G_LED, GPIO.LOW)
GPIO.output(R_LED, GPIO.LOW)

# show state
while True:
    current_co2 = get_average_co2_min()
    # case too high
    if current_co2 >= UPPER_BOUND:
        GPIO.output(B_LED, GPIO.LOW)
        GPIO.output(G_LED, GPIO.LOW)
        GPIO.output(R_LED, GPIO.HIGH)
    elif UPPER_BOUND > current_co2 >= MIDDLE_BOUND:
        GPIO.output(B_LED, GPIO.HIGH)
        GPIO.output(G_LED, GPIO.LOW)
        GPIO.output(R_LED, GPIO.LOW)
    else:
        GPIO.output(B_LED, GPIO.LOW)
        GPIO.output(G_LED, GPIO.HIGH)
        GPIO.output(R_LED, GPIO.LOW)
    time.sleep(15.0)

GPIO.cleanup()
