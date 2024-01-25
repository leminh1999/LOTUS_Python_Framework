import __init
from time import sleep
from Conf.loggingSetup import *
from Library.A1_PyAutoGUI.pyAutoGui_Wrap import pyAutoGui_Remap as GUI
from Library.A2_LOTUS.lotus_Wrap import lotus_Remap as LOTUS
from Library.A3_Selenium.selenium_Wrap import Keys, WEB, seleniumIDE_Remap as IDE
from Library.A4_SendInBlue.sendInBlue_Wrap import class_contentMode, mailConfig, sendInBlue_Wrapper as SIB
from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
from Library.A6_Zabbix.Zabbix_Wrap import zabbix_Wrap as ZABBIX
from pyngrok import ngrok, conf
from pprint import *


################## TESTING #######################
zabbix_server   = '128.199.153.250'
zabbix_port     =  10051
zabbix_user     = 'admin'
zabbix_password = 'CMEV12345'

hostGroupName   = "ABC_Customer" 
hostName        = "DaLat_Tanung_GW0"
itemName        = "CO2 sensor"
itemUID         = "201X0.1.2" # CMEV, ABC_Customer, X, GW ID 0. Sensor ID 1. CH2.

################## TESTING #######################
zabbix_server   = '128.199.153.250'
zabbix_port     =  10051
zabbix_user     = 'admin'
zabbix_password = 'CMEV12345'

hostGroupName   = "ABC_Customer" 
hostName        = "DaLat_Tanung_GW0"
itemName        = "CO2 sensor"
itemUID         = "201X0.1.2" # CMEV, ABC_Customer, X, GW ID 0. Sensor ID 1. CH2.

#1. Khởi tạo Zabbix
ZABBIX().__init__(zabbix_server, zabbix_port, zabbix_user, zabbix_password)
#2. Tạo Hostgroup
ZABBIX().createHostgroup(hostGroupName)
#3. Tạo Host
ZABBIX().createHost(hostGroupName, hostName)
#4. Tạo Item
ZABBIX().createItem(hostName,itemUID,itemName)
#5. Cập nhật giá trị cho Item
ZABBIX().updateItemValue (hostName, itemUID, 250)
### RESULT ###
# ../Components/PIC/001.png

#6. Lấy giá trị HostGroupID
hostGroupId = ZABBIX().getHostGroupID(hostGroupName)
#7. Lấy giá trị HostID
hostId = ZABBIX().getHostID(hostName)
#8. Lấy giá trị ItemID
itemId = ZABBIX().getItemID(hostName,itemName)
#9. Truy xuất toàn bộ parameter của Item 
itemParam1 = ZABBIX().getItemParam(hostName,itemName)
pprint(itemParam1)
#10. Cập nhật giá trị parameter cho Item
ZABBIX().updateItemParam(hostName,itemName,{"units": "bpm"})
#11. Truy xuất toàn bộ parameter của Item lần 2
itemParam2 = ZABBIX().getItemParam(hostName,itemName)
pprint(itemParam2)