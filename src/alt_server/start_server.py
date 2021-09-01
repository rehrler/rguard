from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd
import io
from flask import Flask, render_template, make_response
import sqlite3

app = Flask(__name__)


def get_data() -> tuple:
    conn = sqlite3.connect("src/db/rguard_db.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT * FROM DHT_DATA ORDER BY timestamp DESC LIMIT 1"):
        time = str(row[0])
        temp, hum, co2 = row[1], row[2], row[3]
    conn.close()
    return time, temp, hum, co2


def get_hist_data() -> tuple:
    conn = sqlite3.connect("src/db/rguard_db.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DHT_DATA ORDER BY timestamp DESC LIMIT 3600")
    data = cursor.fetchall()
    dates, temps, hums, co2s = [], [], [], []
    for row in reversed(data):
        dates.append(row[0])
        temps.append(row[1])
        hums.append(row[2])
        co2s.append(row[3])
    conn.close()
    return dates, temps, hums, co2s


@app.route("/")
def index():
    time, temp, hum, co2 = get_data()
    template_data = {
        'time': time,
        'temp': temp,
        'hum': hum,
        'co2': co2
    }
    return render_template("index.html", **template_data)


@app.route('/plot/all')
def plot_temp():
    dates, temps, hums, co2s = get_hist_data()
    temp = pd.Series(index=dates, data=temps)
    hum = pd.Series(index=dates, data=hums)
    co2 = pd.Series(index=dates, data=co2s)

    fig, axes = plt.subplots(figsize=(15, 5), nrows=1, ncols=3)
    co2.plot(kind="line", rot=90, ax=axes[2], title="CO2",
             linewidth=4.0, color='g', ylabel="CO2 [ppm]", grid=True)
    temp.plot(kind="line", rot=90, ax=axes[0], title="Temperature",
              linewidth=4.0, color='k', ylabel="Temperature [deg C]", grid=True)
    hum.plot(kind="line", rot=90, ax=axes[1], title="Humidity",
             linewidth=4.0, color='m', ylabel="Humidity [%]", grid=True)

    plt.tight_layout()

    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
