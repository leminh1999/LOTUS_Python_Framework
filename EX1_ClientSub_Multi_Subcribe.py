import __init
from Library.A9_MQTT.mqtt import mqttClass #pip install paho-mqtt

# #### 2. Subcribe to a topic ###
import threading
import random
import time
###############################################
broker = 'broker.emqx.io' #Free broker
port = 1883
client_id = f'TEST_MQTT_SUB_1'
username = 'not_required'
password = 'not_required'
###############################################


def subcribeFilter(msg):
    pass
      
MQTT = mqttClass(broker, port, client_id, username, password)
MQTT.msgRcvFilter = subcribeFilter
MQTT.subscribe("Topic_JUBEI_1")
threading.Thread(target=MQTT.listen).start()
while True:
    print("Do something else")
    time.sleep(1)