import sqlite3 as lite
import sys

con = lite.connect("src/db/rguard_db.db")

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS DHT_DATA")
    cur.execute("CREATE TABLE DHT_DATA(timestamp DATETIME, temp NUMERIC, hum NUMERIC, co2 NUMERIC)")

