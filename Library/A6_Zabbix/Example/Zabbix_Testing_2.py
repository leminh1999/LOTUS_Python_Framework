import __init
from time import sleep
from Conf.loggingSetup import *
from pprint import *
from Library.A6_Zabbix.Zabbix_Wrap import zabbix_Wrapper as ZABBIX_LIB


################## TESTING #######################
# zabbix_server   = '157.65.24.169'
# zabbix_server   = '192.168.60.168'
# zabbix_server   = 'host.docker.internal' # Tuong duong voi localhost của host PC
zabbix_server   = 'lotus1104.synology.me'
zabbix_port     =  10051
zabbix_user     = 'Admin'
zabbix_password = 'zabbix'
zabbix_web_port =  82
zabbix_url      = 'http://'+zabbix_server+':'+str(zabbix_web_port)

hostGroupName   = "HostGroup_Test"
hostName        = "HostName_Test"
itemName        = "ItemName_Test"
itemUID         = "itemUID_Test" # CMEV, ABC_Customer, X, GW ID 0. Sensor ID 1. CH2.


#1. Khởi tạo Zabbix
zabbixLib = ZABBIX_LIB(zabbix_server, zabbix_port, zabbix_user, zabbix_password, zabbix_url)
#2. Tạo Hostgroup
zabbixLib.createHostgroup(hostGroupName)
#3. Tạo Host
zabbixLib.createHost(hostGroupName, hostName)
#4. Tạo Item
zabbixLib.createItem(hostName,itemUID,itemName)
# 5. Cập nhật giá trị cho Item
MAX_VALUE = 50
MIN_VALUE = 0
STEP = 10
DELAY_SEC = 1
value = 0
direction = "UP"
import math
while True:
  zabbixLib.updateItemValue (hostName, itemUID, value)
  if direction == "DOWN":
    value = value - STEP
  else:
    value = value + STEP
  if value < MIN_VALUE:
    direction = "UP"
    value = MIN_VALUE
  if value > MAX_VALUE:
    direction = "DOWN"
    value = MAX_VALUE
  sleep(DELAY_SEC)
  
# #5. Cập nhật giá trị cho Item
# MAX_VALUE = 180
# MIN_VALUE = 0
# STEP = 10
# DELAY_SEC = 1
# value = MIN_VALUE
# import math

# while True:
#   sinValue = math.sin(math.radians(value))*100
#   zabbixLib.updateItemValue (hostName, itemUID, sinValue)
#   value = value + STEP
#   if value == MAX_VALUE:
#     value = MIN_VALUE
#   sleep(DELAY_SEC)


zabbixLib.updateItemValue (hostName, itemUID, 20);sleep(1)
zabbixLib.updateItemValue (hostName, itemUID, 20);sleep(1)
zabbixLib.updateItemValue (hostName, itemUID, 20);sleep(1)
zabbixLib.updateItemValue (hostName, itemUID, 40);sleep(1)
zabbixLib.updateItemValue (hostName, itemUID, 40);sleep(1)
zabbixLib.updateItemValue (hostName, itemUID, 40);sleep(1)
zabbixLib.updateItemValue (hostName, itemUID, 50);sleep(1)
zabbixLib.updateItemValue (hostName, itemUID, 50);sleep(1)
zabbixLib.updateItemValue (hostName, itemUID, 50)



### RESULT ###
# ../Components/PIC/001.png

#6. Lấy giá trị HostGroupID
# hostGroupId = zabbixLib.getHostGroupID(hostGroupName)
# #7. Lấy giá trị HostID
# hostId = zabbixLib.getHostID(hostName)
# #8. Lấy giá trị ItemID
# itemId = zabbixLib.getItemID(hostName,itemName)
# #9. Truy xuất toàn bộ parameter của Item 
# itemParam1 = zabbixLib.getItemParam(hostName,itemName)
# pprint(itemParam1)
# #10. Cập nhật giá trị parameter cho Item
# zabbixLib.updateItemParam(hostName,itemName,{"units": "bpm"})
# #11. Truy xuất toàn bộ parameter của Item lần 2
# itemParam2 = zabbixLib.getItemParam(hostName,itemName)
# pprint(itemParam2)



