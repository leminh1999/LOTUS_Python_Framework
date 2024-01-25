import __init
from Library.A9_MQTT.mqtt import mqttClass #pip install paho-mqtt

# #### 2. Subcribe to a topic ###
import threading
import random
import time
###############################################
# broker = '128.199.200.17' #Broker IP
# port = 1883
# client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'gocong'
# password = 'fcj2018'
# print("client_id: "+str(client_id))
###############################################
# broker = 'broker.emqx.io' #Free broker
# port = 1883
# client_id = f'TEST_MQTT_SUB_1'
# username = 'not_required'
# password = 'not_required'
###############################################
broker = 'lotus1104.synology.me' #Broker IP
port = 1885
client_id = f'TEST_MQTT_SUB_1'
username = 'mqtt_broker'
password = '!Da#ImU%VuF3V'

def subcribeFilter(msg):
    if msg.topic == "WSN_GW_01C823" and msg.payload.decode() != "":
      print("Received:"+str(msg.payload.decode())) #Action 1
      
MQTT = mqttClass(broker, port, client_id, username, password)
MQTT.msgRcvFilter = subcribeFilter
MQTT.subscribe("WSN_GW_01C823")
# MQTT.subscribe("Topic_JUBEI_2")
# MQTT.subscribe("Topic_JUBEI_3")
threading.Thread(target=MQTT.listen).start()
while True:
    print("Do something else")
    time.sleep(1)