import __init
from Conf.loggingSetup import *
from Library.A9_MQTT.mqtt import mqttClass #pip install paho-mqtt

#### 1. Publish to a topic ####
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
# client_id = f'TEST_MQTT_PUB_1'
# username = 'not_required'
# password = 'not_required'
###############################################
GATEWAY_UID = "ABCDEF"
broker = 'lotus1104.synology.me' #Broker IP
port = 1883
client_id = f'WSN_CLIENT_'+GATEWAY_UID+"_"+str(random.randint(0, 1000))
# print("client_id: "+str(client_id))
username = 'mqtt_broker'
password = '!Da#ImU%VuF3V'
MQTT_TOPIC = 'WSN_TOPIC_'+GATEWAY_UID
MQTT_TOPIC = "WSN_TOPIC_01C821"
# print("TOPIC: "+str(TOPIC))

MQTT = mqttClass(broker, port, client_id, username, password)
# payload must be a string, bytearray, int, float or None.
while True:
    dataTime = time.strftime("%c")
    logger.info("[Topic_JUBEI_1] Publishing: "+str(dataTime))
    # MQTT.publish("Topic_JUBEI_1", dataTime)
    time.sleep(1)