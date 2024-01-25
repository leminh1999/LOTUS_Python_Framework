import __init
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
broker = 'lotus1104.synology.me' #Broker IP
port = 1885
client_id = f'TEST_MQTT_PUB_1'
username = 'mqtt_broker'
password = '!Da#ImU%VuF3V'

MQTT = mqttClass(broker, port, client_id, username, password)
# payload must be a string, bytearray, int, float or None.
stringMsg = 'Hello World!'
jsonData  = '{"name":"John", "age":30, "city":"New York"}'
listData  = '[1,2,3,4,5,6,7,8,9,10]'
while True:
    dataTime = time.strftime("%c")
    #print data and time
    print("[WSN_GW_01C823] Publishing: "+str(dataTime))
    sendMsg = '{"uid": "'+str(client_id)+'", "message": "'+str(dataTime)+'"}'
    # print(sendMsg)
    MQTT.publish("WSN_GW_01C823",sendMsg)
    time.sleep(1)
    # exit()