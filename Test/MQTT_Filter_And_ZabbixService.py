import __init
import os
# WORK_PATH = "/root/python/wsnMqttZabbix/"
WORK_PATH = ""
# os.chdir(WORK_PATH)
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
zabbix_server   = '157.65.24.169'
zabbix_port     =  10051
zabbix_user     = 'Admin'
zabbix_password = 'zabbix'
zabbix_url      = 'http://'+zabbix_server
zabbixLib = ZABBIX_LIB(zabbix_server, zabbix_port, zabbix_user, zabbix_password, zabbix_url)
###############################################


#### GATEWAY NUMBER 1 ########################################
MQTT_FOLLOW_LIST = ["WSN_TOPIC_018F1A","WSN_TOPIC_01C821"]  #<-------------- Add topic to follow here & Restart


client_id = "MQTT_TOPIC_Server_Client_"+str(random.randint(1,1000))
def mqttSubcribeFilter(msg):
    #1. Store data to log.txt
    if msg.topic in MQTT_FOLLOW_LIST:
      # print("### WSN_TOPIC ##################################")
      DATETIME = datetime.datetime.now().strftime("%Y_%m_%d")
      STORE_PATH = WORK_PATH+str(msg.topic)+"_log_"+DATETIME+".txt"
      # STORE_PATH = str(msg.topic)+"_log_"+DATETIME+".txt"
      # os.system("echo '"+str(msg.payload.decode())+"' >> "+STORE_PATH)
      with open(STORE_PATH, "a") as myfile:
        myfile.write(str(msg.payload.decode())+"\n")
        
    #2. Request upload data to Zabbix server
    if msg.topic in MQTT_FOLLOW_LIST and "[SVR->Zabbix]" in msg.payload.decode():
      # print("### [SVR->Zabbix] ##############################")
      zabbixData = msg.payload.decode().split("\'")
      hostId   = zabbixData[1]
      itemUidKey = zabbixData[3]
      itemValue  = zabbixData[5]
      message= hostId+"$$$"+itemUidKey+"$$$"+itemValue
      MQTT.publish(topic="ZABBIX_REQ", msg=message)   #Action 2
      
MQTT = mqttClass(broker, port, client_id, username, password)
MQTT.msgRcvFilter = mqttSubcribeFilter
for subcribeMqtt in MQTT_FOLLOW_LIST:
  MQTT.subscribe(subcribeMqtt)
threading.Thread(target=MQTT.listen).start()

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