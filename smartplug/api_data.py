import sqlite3
from datetime import datetime
from time import sleep, time

def hvornår_skal_der_opdateres():
    nu = datetime.now()

    nu_dato = str(nu).split(" ")
    nu_time = int(nu.strftime("%H"))
    nu_minut = int(nu.strftime("%M"))
    nu_sekunder = int(nu.strftime("%S"))
    nu_sekunder_sammenlagt = nu_time * 3600 + nu_minut * 60 + nu_sekunder
    x = 5 - (nu_minut % 5)
    y = nu_minut + x
    if nu_time == 0:
        if y != 60 and y >= 10:
            z = f"0{nu_time}:{y}"
        elif y != 60 and y <= 10:
            z = f"0{nu_time}:0{y}"
        else:
            z = f"0{nu_time + 1}:00"
        return z, nu_dato[0]
    else:
        if y != 60 and y >= 10:
            z = f"{nu_time}:{y}"
        elif y != 60 and y <= 10:
            z = f"{nu_time}:0{y}"
        else:
            z = f"{nu_time + 1}:00"
        return z, nu_dato[0]

def opdater_strøm_stilling():
    z, nu_dato = hvornår_skal_der_opdateres()
    # print(z)
    # print(nu_dato)
    # print(f"SELECT Tidspunkt, Dato, CO2_g_pr_kWh FROM CO2_Prognose WHERE Tidspunkt == '{z}' AND Dato == '{nu_dato}'")
    conn = sqlite3.connect(database="database/web_database.db")
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT Tidspunkt, Dato, CO2_g_pr_kWh FROM CO2_Prognose WHERE Tidspunkt == '{z}' AND Dato == '{nu_dato}'")
        rset = cur.fetchall()
        for row in rset:
            tidspunkt = row[0]
            dato = row[1]
            co2_udledning = row[2]
            tidspunkt_splittet = tidspunkt.split(":")
        
    except sqlite3.Error as e:
        print(f"Error calling SQL: '{e}'")
    finally:
        pass
        # conn.close()
        
    return co2_udledning

# hvornår_skal_der_opdateres()
opdater_strøm_stilling()