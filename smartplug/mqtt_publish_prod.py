import paho.mqtt.publish as publish
import json
from time import sleep
import datetime
import threading
import log_data
import magi

def mqtt_publish():
    strøm_type, strømforbrug = magi.co2_stadier()
    # print(strøm_type)
    payload = {"Strømtype" : strøm_type,
                "Strømforbrug" : strømforbrug
    }
    publish.single("paho/test/topic", json.dumps(payload), hostname="20.107.250.219")
    # print(payload)
# print("Starter Publish")


x = threading.Thread(target=log_data.data_func)
x.start()
sleep(10)
while True:
    mqtt_publish()
    sleep(1)