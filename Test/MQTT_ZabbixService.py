import __init
from Library.A9_MQTT.mqtt import mqttClass #pip install paho-mqtt
from Library.A6_Zabbix.Zabbix_Wrap import zabbix_Wrapper as ZABBIX_LIB
from pyzabbix import ZabbixMetric, ZabbixSender
import random

# from pyzabbix.api import ZabbixAPI


# #### 2. Subcribe to a topic ###
import threading
import os
import datetime
##### MQTT BROKER ##########################################
broker = '128.199.200.17' #Broker IP
port = 1883
username = 'gocong'
password = 'fcj2018'
##### ZABBIX SERVER ########################################
zabbix_server   = '127.0.0.1'
zabbix_port     =  10051
zabbix_user     = 'Admin'
zabbix_password = 'zabbix'
zabbix_url      = 'http://'+zabbix_server
zabbixLib = ZABBIX_LIB(zabbix_server, zabbix_port, zabbix_user, zabbix_password, zabbix_url)
###############################################


#### GATEWAY NUMBER 1 ########################################
client_id = "MQTT_TOPIC_Server_Client_"+str(random.randint(1,10000))

#############################################################################
def zabbixSubcribeFilter(msg):
    #1. Request upload data to Zabbix server
    if msg.topic == "ZABBIX_REQ":
      message = msg.payload.decode().split("$$$")
      hostId   = message[0]
      itemUidKey = message[1]
      itemValue  = message[2]
      hostName = zabbixLib.getHostName(hostId)
      # zabbixLib.updateItemValue(hostName,itemUidKey,itemValue) #GATEWAY_UPLOAD
      metrics = [ZabbixMetric(hostName, itemUidKey, itemValue)]
      ZabbixSender(zabbix_server=zabbix_server, zabbix_port=zabbix_port).send(metrics)
      print("Upload to Zabbix")
      
ZABBIX = mqttClass(broker, port, "ZABBIX_"+client_id, username, password)
ZABBIX.msgRcvFilter = zabbixSubcribeFilter
ZABBIX.subscribe("ZABBIX_REQ")
threading.Thread(target=ZABBIX.listen).start()

######################################
print("MQTT Server is running...")