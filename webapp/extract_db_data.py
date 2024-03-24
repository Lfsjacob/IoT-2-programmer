import sqlite3
from datetime import datetime
from time import sleep


def CO2_Prognose(number_of_rows):
    while True:
        query = """SELECT * FROM CO2_Prognose ORDER BY ID DESC;"""
        ids = []
        datoer = []
        tidspunkter = []
        co2 = []
        try:
            conn = sqlite3.connect("database/web_database.db")
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchmany(number_of_rows)
            inc = 0
            for i in range(number_of_rows):
                ids.append(rows[inc][0])
                datoer.append(rows[inc][1])
                tidspunkter.append(rows[inc][2])
                co2.append(rows[inc][3])
                inc += 1
            return ids, datoer, tidspunkter, co2
        except sqlite3.Error as sql_e:
            print(f"sqlite error occured: {sql_e}")
            conn.rollback()
        except Exception as e:
            print(f"Error occured: {e}")
        finally:
            conn.close()


def strømforbrug():
    while True:
        query = """SELECT * FROM Strømforbrug ORDER BY ID ASC;"""
        ids = []
        tidspunkter = []
        strømforbrug = []
        try:
            conn = sqlite3.connect("database/web_database.db")
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            inc = 0
            for i in range(len(rows)):
                ids.append(rows[inc][0])
                tidspunkter.append(rows[inc][1])
                strømforbrug.append(rows[inc][2])
                inc += 1
            return tidspunkter, strømforbrug
        except sqlite3.Error as sql_e:
            print(f"sqlite error occured: {sql_e}")
            conn.rollback()
        except Exception as e:
            print(f"Error occured: {e}")
        finally:
            conn.close()



def get_ids(table):
    query = f"""SELECT * FROM {table};"""
    ids = []
    try:
        conn = sqlite3.connect("database/web_database.db")
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        inc = 0
        for i in range(len(rows)):
            ids.append(rows[inc][0])
            inc += 1
    except sqlite3.Error as sql_e:
        print(f"sqlite error occured: {sql_e}")
        conn.rollback()
    except Exception as e:
        print(f"Error occured: {e}")
    finally:
        conn.close()
    return len(ids)