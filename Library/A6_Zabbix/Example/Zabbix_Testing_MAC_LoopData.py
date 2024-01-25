import __init
from time import sleep
from Conf.loggingSetup import *
from pprint import *
from Library.A6_Zabbix.Zabbix_Wrap import zabbix_Wrapper as ZABBIX_LIB


################## TESTING #######################
# zabbix_server   = '192.168.60.168'
zabbix_server   = 'host.docker.internal' # Tuong duong voi localhost của host PC
zabbix_port     =  10051
zabbix_user     = 'Admin'
zabbix_password = 'zabbix'
zabbix_web_port =  80
zabbix_url      = 'http://'+zabbix_server+':'+str(zabbix_web_port)

hostGroupName   = "HostGroup_Test" 
hostName        = "HostName_Test"
itemName        = "ItemName_Test"
itemUID         = "itemUID_Test" # CMEV, ABC_Customer, X, GW ID 0. Sensor ID 1. CH2.


#1. Khởi tạo Zabbix
zabbixLib = ZABBIX_LIB(zabbix_server, zabbix_port, zabbix_user, zabbix_password, zabbix_url)

#5. Cập nhật giá trị cho Item
import time
import numpy
import math
value = 0
sign = 1
while True:
  value = value + 30
  if value == 360: value = 0
  valuePi = value/180 * math.pi
  uploadValue=((numpy.sin(valuePi))+1)*50
  print("Upload value: ", uploadValue)
  zabbixLib.updateItemValue (hostName, itemUID, uploadValue)
  time.sleep(1)



 