import __init
from Library.A9_MQTT.mqtt import mqttClass #pip install paho-mqtt
from Library.A6_Zabbix.Zabbix_Wrap import zabbix_Wrapper as ZABBIX_LIB
from pyzabbix import ZabbixMetric, ZabbixSender
# from pyzabbix.api import ZabbixAPI


# #### 2. Subcribe to a topic ###
import threading
import os
###############################################
broker = '128.199.200.17' #Broker IP
port = 1883
username = 'gocong'
password = 'fcj2018'
###############################################
client_id = f'TEST_MQTT_SUB_1'
MQTT_TOPIC = 'WSN_TOPIC_018F1A'


zabbix_server   = '157.65.24.169'
zabbix_port     =  10051
zabbix_user     = 'Admin'
zabbix_password = 'zabbix'
zabbix_url      = 'http://'+zabbix_server
zabbixLib = ZABBIX_LIB(zabbix_server, zabbix_port, zabbix_user, zabbix_password, zabbix_url)
#############################################################################
def mqttSubcribeFilter(msg):
    #1. Store data to log.txt
    if msg.topic == MQTT_TOPIC:
      os.system("echo "+str(msg.payload.decode())+" >> "+MQTT_TOPIC+"_log.txt")
    #2. Request upload data to Zabbix server
    if msg.topic == MQTT_TOPIC and "[SVR->Zabbix]" in msg.payload.decode():
      os.system("echo "+str(msg.payload.decode())+" >> "+MQTT_TOPIC+"_log.txt")
      zabbixData = msg.payload.decode().split("\'")
      hostName   = zabbixData[1]
      itemUidKey = zabbixData[3]
      itemValue  = zabbixData[5]
      message= hostName+"$$$"+itemUidKey+"$$$"+itemValue
      MQTT.publish(topic="ZABBIX_REQ", msg=message)   #Action 2
      
MQTT = mqttClass(broker, port, client_id, username, password)
MQTT.msgRcvFilter = mqttSubcribeFilter
MQTT.subscribe(MQTT_TOPIC)
threading.Thread(target=MQTT.listen).start()

#############################################################################
def zabbixSubcribeFilter(msg):
    #1. Request upload data to Zabbix server
    if msg.topic == "ZABBIX_REQ":
      message = msg.payload.decode().split("$$$")
      hostName   = message[0]
      itemUidKey = message[1]
      itemValue  = message[2]
      # zabbixLib.updateItemValue(hostName,itemUidKey,itemValue) #GATEWAY_UPLOAD
      metrics = [ZabbixMetric(hostName, itemUidKey, itemValue)]
      ZabbixSender(zabbix_server=zabbix_server, zabbix_port=zabbix_port).send(metrics)
      print("Upload to Zabbix")
      
ZABBIX = mqttClass(broker, port, "ZABBIX_"+client_id, username, password)
ZABBIX.msgRcvFilter = zabbixSubcribeFilter
ZABBIX.subscribe("ZABBIX_REQ")
threading.Thread(target=ZABBIX.listen).start()


