import __init
import socketio
from Library.A9_MQTT.mqtt import mqttClass #pip install paho-mqtt
import threading
import random
import json

############################################################
# USER CONFIGURATION                                       #
############################################################
SOCKETIO_EXPORT_LICENSE_TOPIC_LIST = list()  #Danh sách các TOPIC có giấy phép để publish đến mạng MQTT.
SOCKETIO_EXPORT_LICENSE_TOPIC_LIST.append("WSN_GW_01C823")  
MQTT_BROKER_IP = "lotus1104.synology.me"
MQTT_PORT = 1885
MQTT_USERNAME = "mqtt_broker"
MQTT_PASSWORD = "!Da#ImU%VuF3V"
MQTT_CLIENT_ID = f'MQTT_EXPORT_CONTROL_ID_'+str(random.randint(0, 10000))

SOCKETIO_URL = "http://lotus1104.synology.me:83" # EX: "http://lotus1104.synology.me:83"

############################################################
# 1. CONNECT TO MQTT BROKER                                #
############################################################
MQTT = mqttClass(MQTT_BROKER_IP, MQTT_PORT, MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD)
def subcribeFilter(msg):
  jsonData = eval(msg.payload.decode())
  #Check sender uid
  if "SIO_EXCTL" in jsonData["uid"]: return #SOCKETIO_EXPORT_CONTROL
  #CHECK LICENSE
  if msg.topic in SOCKETIO_EXPORT_LICENSE_TOPIC_LIST:
    #SEND TO SOCKETIO
    sio.emit('SOCKET', {"topic":msg.topic,"message":jsonData["message"]})
for subTopic in SOCKETIO_EXPORT_LICENSE_TOPIC_LIST: #Subcribe to all topic in SOCKETIO_EXPORT_LICENSE_TOPIC_LIST
  MQTT.subscribe(subTopic)
MQTT.msgRcvFilter = subcribeFilter
threading.Thread(target=MQTT.listen).start()
##############################################################

############################################################
# 2. CONNECT TO SOCKETIO BROKER                            #
############################################################
sio = socketio.Client()
sio.connect(SOCKETIO_URL)
@sio.event
def connect():
    print('Đã kết nối thành công đến SocketIO')