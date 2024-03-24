import paho.mqtt.subscribe as subscribe
import json
import sqlite3
from time import sleep
import datetime
import extract_db_data

id_inc = 1

def get_rpi_data(arg):
    msg = subscribe.simple("paho/test/topic", hostname="20.107.250.219")
    dekodet_besked = json.loads(msg.payload.decode())
    if arg == "type":
        return dekodet_besked['Strømtype']
    elif arg == "forbrug":
        return dekodet_besked['Strømforbrug']

def insert_strømforbrug_data_to_db():
    global id_inc
    antal_tabel_punkter = extract_db_data.get_ids("Strømforbrug")

    conn = sqlite3.connect("database/web_database.db")

    datetime_data = datetime.datetime.now()
    tidspunkt = datetime_data.strftime("%X")
    strømforbrug = round(float(get_rpi_data("forbrug")/1000), 2)
    
    if antal_tabel_punkter < 12:
        antal_tabel_punkter += 1
        query = """INSERT INTO Strømforbrug(Tidspunkt, Watt_pr_time) VALUES(?, ?)"""
        data = tidspunkt, strømforbrug
        try:
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()
        except sqlite3.Error as sql_e:
            print(f"sqlite error occured: {sql_e}")
            conn.rollback()
        except Exception as e:
            print(f"Error occured: {e}")

    query = f"""UPDATE Strømforbrug SET Tidspunkt = '{tidspunkt}', Watt_pr_time = {strømforbrug} WHERE ID == {id_inc};"""
    data = tidspunkt, strømforbrug
    try:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except sqlite3.Error as sql_e:
        print(f"sqlite error occured: {sql_e}")
        conn.rollback()
    except Exception as e:
        print(f"Error occured: {e}")

    if id_inc < 12:
        id_inc += 1
    elif id_inc >=12:
        id_inc = 1

def delete_data():
    try:
        conn = sqlite3.connect(database="database/web_database.db")
        query = """DELETE FROM Strømforbrug"""
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Could not insert! {e}")

def log():
    while True:
        insert_strømforbrug_data_to_db()
        sleep(280)
