import json
from flask import Flask, render_template, make_response
import datetime
from time import time
import sqlite3

app = Flask(__name__)


def get_data() -> tuple:
    conn = sqlite3.connect("src/db/rguard_db.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT * FROM DHT_DATA ORDER BY timestamp DESC LIMIT 1"):
        time_stamp = row[0]
        temp, hum, co2 = row[1], row[2], row[3]
    conn.close()
    return time_stamp, temp, hum, co2


@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')


@app.route('/data', methods=["GET", "POST"])
def data():
    my_time, temp, hum, co2 = get_data()
    my_time_datetime = datetime.datetime.strptime(my_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=2)
    my_time_msecs = my_time_datetime.timestamp() * 1000
    new_data = [my_time_msecs, temp, hum, co2]

    response = make_response(json.dumps(new_data))

    response.content_type = 'application/json'

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
