import sqlite3


def connect():
    conn = sqlite3.connect("./data/database.db")

    cursor = conn.cursor()

    return conn, cursor
