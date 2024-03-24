from gpiozero import LED as relæ
from gpiozero import Button
from time import sleep
import threading
import api_data as database
import INA219_script
from log_data import data_func
import Neopixel_strøm


relæ_1 = relæ(4)
relæ_2 = relæ(6)
relæ_3 = relæ(26)
knap = Button(5)

relæ_1.on()
relæ_2.on()
relæ_3.on()

# data_func()

sort_lad = False

def kør_som_satan():
    global sort_lad
    if sort_lad == False:
        sort_lad = True
    elif sort_lad == True:
        sort_lad = False
    return sort_lad

def sorte_knap():
    knap.when_pressed = lambda : kør_som_satan()
    sleep(0.1)


def co2_stadier():
    sorte_knap()

    co2_udledning = database.opdater_strøm_stilling()

    # print(co2_udledning)
    effekt = INA219_script.læs_ina()

    co2_tærskel = 60
    # print(effekt)
    if co2_udledning <= co2_tærskel and effekt >= 500 and sort_lad == False:
        relæ_1.on()
        relæ_3.on()
        relæ_2.off()
        # print("lader USB enhed")
        status = 'Grøn Strøm'
        Neopixel_strøm.strøm_farve(Neopixel_strøm.farver["grøn"], False)
        sleep(1)
        return status, effekt
    elif co2_udledning <= co2_tærskel and effekt < 500 and sort_lad == False:
        relæ_2.on()
        relæ_3.off()
        relæ_1.off()
        # print("lader batteri")
        status = 'Grøn Strøm'
        Neopixel_strøm.strøm_farve(Neopixel_strøm.farver["grøn"], False)
        sleep(1)
        return status, effekt
    elif co2_udledning > co2_tærskel and sort_lad == False:
        relæ_1.on()
        relæ_2.on()
        relæ_3.off()
        # print("lader USB enhed fra batteri")
        status = 'Sort Strøm'
        Neopixel_strøm.strøm_farve(Neopixel_strøm.farver["rød"], False)
        sleep(1)
        return status, effekt
    elif sort_lad == True:
        relæ_1.on()
        relæ_3.on()
        relæ_2.off()
        # print("lader USB enhed med sort strøm")
        status = 'Sort Strøm'
        Neopixel_strøm.strøm_farve(Neopixel_strøm.farver["rød"], True)
        sleep(1)
        return status, effekt
    


def pls():
    sorte_knap()
    co2_stadier()



# while True:
#     pls()