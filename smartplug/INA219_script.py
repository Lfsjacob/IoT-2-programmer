from ina219 import INA219
from ina219 import DeviceRangeError, logging
from time import sleep

SHUNT_OHMS = 0.1


def læs_ina():
    ina = INA219(SHUNT_OHMS, busnum=1, address=0x40)
    ina.configure()
    try:
        effekt = int(ina.power())
    except DeviceRangeError as e:
        print(e)
    return effekt
