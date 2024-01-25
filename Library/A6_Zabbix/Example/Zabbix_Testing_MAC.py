import __init
from time import sleep
from Conf.loggingSetup import *
from pprint import *
from Library.A6_Zabbix.Zabbix_Wrap import zabbix_Wrapper as ZABBIX_LIB


################## TESTING #######################
zabbix_server   = '192.168.60.168'
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
#2. Tạo Hostgroup
zabbixLib.createHostgroup(hostGroupName)
#3. Tạo Host
zabbixLib.createHost(hostGroupName, hostName)
#4. Tạo Item
zabbixLib.createItem(hostName,itemUID,itemName)
#5. Cập nhật giá trị cho Item
zabbixLib.updateItemValue (hostName, itemUID, 250)
### RESULT ###
# ../Components/PIC/001.png

#6. Lấy giá trị HostGroupID
hostGroupId = zabbixLib.getHostGroupID(hostGroupName)
#7. Lấy giá trị HostID
hostId = zabbixLib.getHostID(hostName)
#8. Lấy giá trị ItemID
itemId = zabbixLib.getItemID(hostName,itemName)
#9. Truy xuất toàn bộ parameter của Item 
itemParam1 = zabbixLib.getItemParam(hostName,itemName)
pprint(itemParam1)
#10. Cập nhật giá trị parameter cho Item
zabbixLib.updateItemParam(hostName,itemName,{"units": "bpm"})
#11. Truy xuất toàn bộ parameter của Item lần 2
itemParam2 = zabbixLib.getItemParam(hostName,itemName)
pprint(itemParam2)



