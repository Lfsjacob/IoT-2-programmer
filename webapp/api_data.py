from datetime import datetime
import requests
from time import sleep, time
import sqlite3

def opdater_prognose_db():
    opdatering_tidspunkter_sek = [3*3600, 7*3600, 11*3600, 15*3600, 19*3600, 23*3600]
    opdatering_tidspunkter = {
        "Tre" : 3,
        "Syv" : 7,
        "Elleve" : 11,
        "Femten" : 15,
        "Nitten" : 19,
        "Treogtyve" : 23
    }
    nu_tid = datetime.now()
    nu_time = int(nu_tid.strftime("%H"))
    nu_minut = int(nu_tid.strftime("%M"))
    nu_sekund = int(nu_tid.strftime("%S"))
    nu_sammenlagt = nu_time * 3600 + nu_minut * 60 + nu_sekund
    # print(nu_sammenlagt)

    if nu_sammenlagt > opdatering_tidspunkter_sek[0] and nu_sammenlagt < opdatering_tidspunkter_sek[1]:
        sleep_tid = opdatering_tidspunkter_sek[1] - nu_sammenlagt
        # print(f"Sover i {sleep_tid} sekunder indtil kl. {int(opdatering_tidspunkter['Syv'])}:00")
        sleep(sleep_tid)
    elif nu_sammenlagt > opdatering_tidspunkter_sek[1] and nu_sammenlagt < opdatering_tidspunkter_sek[2]:
        sleep_tid = opdatering_tidspunkter_sek[2] - nu_sammenlagt
        # print(f"Sover i {sleep_tid} sekunder indtil kl. {int(opdatering_tidspunkter['Elleve'])}:00")
        sleep(sleep_tid)
    elif nu_sammenlagt > opdatering_tidspunkter_sek[2] and nu_sammenlagt < opdatering_tidspunkter_sek[3]:
        sleep_tid = opdatering_tidspunkter_sek[3] - nu_sammenlagt
        # print(f"Sover i {sleep_tid} sekunder indtil kl. {int(opdatering_tidspunkter['Femten'])}:00")
        sleep(sleep_tid)
    elif nu_sammenlagt > opdatering_tidspunkter_sek[3] and nu_sammenlagt < opdatering_tidspunkter_sek[4]:
        sleep_tid = opdatering_tidspunkter_sek[4] - nu_sammenlagt
        # print(f"Sover i {sleep_tid} sekunder indtil kl. {int(opdatering_tidspunkter['Nitten'])}:00")
        sleep(sleep_tid)
    elif nu_sammenlagt > opdatering_tidspunkter_sek[4] and nu_sammenlagt < opdatering_tidspunkter_sek[5]:
        sleep_tid = opdatering_tidspunkter_sek[5] - nu_sammenlagt
        # print(f"Sover i {sleep_tid} sekunder indtil kl. {int(opdatering_tidspunkter['Treogtyve'])}:00")
        sleep(sleep_tid)
    elif nu_sammenlagt > opdatering_tidspunkter_sek[5]:
        sleep_tid = ((24 * 3600) - nu_sammenlagt) + opdatering_tidspunkter_sek[0]
        # print(f"Sover i {sleep_tid} sekunder indtil kl. {int(opdatering_tidspunkter['Tre'])}:00")
        sleep(sleep_tid)
    elif nu_sammenlagt < opdatering_tidspunkter_sek[0]:
        sleep_tid = opdatering_tidspunkter_sek[0] - nu_sammenlagt
        # print(f"Sover i {sleep_tid} sekunder indtil kl. {int(opdatering_tidspunkter['Tre'])}:00")
        sleep(sleep_tid)


def request_API_data():
    limit = 396
    response = requests.get(url=f'https://api.energidataservice.dk/dataset/CO2EmisProg?columns=Minutes5DK,CO2Emission&offset=&sort=Minutes5UTC%20DESC&limit={limit*2}')
    result = response.json()
    records = result.get('records', [])
    sum = 0
    DK2_udledning = records[1::2]
    # print('Udledninger af CO2 øst for Storebælt i g/kWh:')

    for record in DK2_udledning:
        # print(' ', record)
        sum += record['CO2Emission']

    avg = int(sum / (limit))

    # print(f"\nGennemsnits udledning af CO2 øst for Storebælt i g/kWh: {avg}")
    return DK2_udledning


def insert_API_data_to_db(DK2_udledning):
    try:
        conn = sqlite3.connect(database="database/web_database.db")
        query = """DELETE FROM CO2_Prognose"""
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Could not insert! {e}")

    for record in DK2_udledning:
        dato_tidspunkt_splittet = record['Minutes5DK'].split("T")
        tidspunkt_splittet = dato_tidspunkt_splittet[1].split(":")
        tidspunkt_uden_sekunder = f"{tidspunkt_splittet[0]}:{tidspunkt_splittet[1]}"
        query = """INSERT INTO CO2_Prognose(Dato, Tidspunkt, CO2_g_pr_kWh) VALUES(?, ?, ?)"""
        data = dato_tidspunkt_splittet[0], tidspunkt_uden_sekunder, record['CO2Emission']

        try:
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()
        except sqlite3.Error as sql_e:
            print(f"sqlite error occured: {sql_e}")
            conn.rollback()
        except Exception as e:
            print(f"Error occured: {e}")
        finally:
            #conn.close()
            pass

def log():
    while True:
        insert_API_data_to_db(request_API_data())
        opdater_prognose_db()


