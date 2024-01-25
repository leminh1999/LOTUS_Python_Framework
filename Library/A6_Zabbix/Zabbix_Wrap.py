import __init
from time import sleep
from Conf.loggingSetup import *
from pyzabbix import ZabbixMetric, ZabbixSender
from pyzabbix.api import ZabbixAPI
# from Library.A6_Zabbix.Components.ZabbixSender import ZabbixSender, ZabbixPacket

class zabbix_Wrapper:
  def __init__(self, zabbix_server = '128.199.153.250', zabbix_port = 10051 , zabbix_user = 'admin', zabbix_password = 'CMEV12345',zabbix_url="http://128.199.153.250/zabbix"):
    self.zabbix_server = zabbix_server
    self.zabbix_port = zabbix_port
    self.zabbix_user = zabbix_user
    self.zabbix_password = zabbix_password
    self.zabbix_api = ZabbixAPI(url=zabbix_url, user=self.zabbix_user, password=self.zabbix_password)
    
  def createHostgroup(self,zbx_hostgroup):
    '''
    - `name`: createHostgroup
    - `description`:  Tạo hostgroup trên Zabbix.
    - `parameters`:
      - `zbx_hostgroup`: Tên hostgroup.
    - `return`: None
    - `Example`:
        - createHostgroup('ABC_Customer')
    - `PIC`: ✨ Components/PIC/001.png
    '''
    try:
        result = self.zabbix_api.do_request('hostgroup.get', {'filter': {'name': [zbx_hostgroup]}})
        if [name['name'] for name in result['result']] == []:
            self.zabbix_api.hostgroup.create(name=zbx_hostgroup)
            logger.info(f'[Zabbix] Hostgroup created: {zbx_hostgroup} : {str(result)}')      # log hostgroup creation
    except Exception:
        logger.error('[Zabbix] Unable to request to server')

  def getHostGroupID (self,hostgroupName):
    '''
    - `name`: getHostGroupID
    - `description`:  Lấy ID của hostgroup.
    - `parameters`:
      - `hostgroupName`: Tên hostgroup.
    - `return`: ID của hostgroup.
    - `Example`:
      - getHostGroupID('ABC_Customer')
    '''
    try:
        result = self.zabbix_api.do_request('hostgroup.get', {'filter': {'name': [hostgroupName]}})
        if [name['name'] for name in result['result']] == []:
            return False
        else:
            return [name['groupid'] for name in result['result']][0]
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False

  def getHostGroupName(self,zbx_hostgroup_id):
    '''
    - `name`: getHostGroupName
    - `description`:  Lấy tên hostgroup.
    - `parameters`:
      - `zbx_hostgroup_id`: ID của hostgroup.
    - `return`: Tên hostgroup.
    - `Example`:
        - getHostGroupName('1')
    - `PIC`: ✨ Components/PIC/001.png
    '''
    try:
        result = self.zabbix_api.do_request('hostgroup.get', {'filter': {'groupid': [zbx_hostgroup_id]}})
        if [name['name'] for name in result['result']] == []:
            return False
        else:
            return [name['name'] for name in result['result']][0]
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False
      
  def renameHostgroup(self,zbx_hostgroup_id,zbx_hostgroup_new_name):
    '''
    - `name`: createHostgrenameHostgrouproup
    - `description`:  Đặt lại tên cho Hostgroup.
    - `parameters`:
      - `zbx_hostgroup_id`: ID của hostgroup.
      - `zbx_hostgroup_new_name`: Tên mới của hostgroup.
    - `return`: None
    - `Example`:
        - renameHostgroup('1', 'ABC_Customer')
    - `PIC`: ✨ Components/PIC/001.png
    '''
    try:
      self.zabbix_api.hostgroup.update(groupid=str(zbx_hostgroup_id),name=str(zbx_hostgroup_new_name))
      logger.info(f'[Zabbix] Hostgroup renamed: {zbx_hostgroup_new_name}')      # log hostgroup creation
    except Exception:
        logger.error('[Zabbix] Unable to request to server')

  def createHost(self,zbx_hostgroup, zbx_host):
    '''
    - `name`: createHost
    - `description`:  Tạo host trên Zabbix.
    - `parameters`:
      - `zbx_hostgroup`: Tên hostgroup.
      - `zbx_host`: Tên host.
    - `return`: None
    - `Example`:
        - createHost('ABC_Customer', 'DaLat_Tanung_GW0')
    - `PIC`: ✨ Components/PIC/001.png
    '''
    try:
        result = self.zabbix_api.do_request('host.get', {'filter':{'host':[zbx_host]}})
        if [host['host'] for host in result['result']] != []:
            return True
        else:
            result = self.zabbix_api.do_request('hostgroup.get', {'filter': {'name': [zbx_hostgroup]}})
            if [name['name'] for name in result['result']] == []:
                # HostGroup doesn't exist
                return False
            else:
                groupId = [name['groupid'] for name in result['result']][0]
                self.zabbix_api.do_request('host.create', {'host': zbx_host, 'interfaces': [{'type': 1, 'main': 1, 'useip': 1, 'ip': '127.0.0.1', 'dns': '', 'port': self.zabbix_port}], 'groups': [{'groupid': groupId}]})
                logger.info(f'[Zabbix] Host created: {zbx_host}')
                return True
    except Exception:
        logger.error('[Zabbix] Unable to request to server')

  def getHostID (self,hostName):
    '''
    - `name`: getHostID
    - `description`:  Lấy ID của host.
    - `parameters`:
      - `hostName`: Tên host.
    - `return`: ID của host.
    - `Example`:
      - getHostID('DaLat_Tanung_GW0')
    '''
    try:
        result = self.zabbix_api.do_request('host.get', {'filter': {'host': [hostName]}})
        if [host['host'] for host in result['result']] == []:
            return False
        else:
            return [host['hostid'] for host in result['result']][0]
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False

  def getHostName (self,hostID):
    '''
    - `name`: getHostName
    - `description`:  Lấy tên host.
    - `parameters`:
      - `hostID`: ID của host.
    - `return`: Tên host.
    - `Example`:
      - getHostName('10050')
    '''
    try:
        result = self.zabbix_api.do_request('host.get', {'filter': {'hostid': [hostID]}})
        if [host['hostid'] for host in result['result']] == []:
            return False
        else:
            return [host['host'] for host in result['result']][0]
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False

  def createItem(self,zbx_host, zbx_item_UID, zbx_item_name):
    '''
    - `name`: createItem
    - `description`:  Tạo item trên Zabbix.
    - `parameters`:
      - `zbx_host`: Tên host.
      - `zbx_item_UID`: UID của item. VD: 201X0.1.2 # CMEV, ABC_Customer, X, GW ID 0. Sensor ID 1. CH2.
      - `zbx_item_name`: Tên item.
    - `return`: None
    - `Example`:
        - createItem('DaLat_Tanung_GW0', '201X0.1.2', 'CH2')
    - `PIC`: ✨ Components/PIC/001.png
    '''
    try:
        result = self.zabbix_api.do_request('item.get', {'host': zbx_host, 'filter': {'key_':[zbx_item_UID]}})
        if [host['key_'] for host in result['result']] != []:
            return True
        else:
            result = self.zabbix_api.do_request('host.get', {'filter':{'host':[zbx_host]}})
            if [host['host'] for host in result['result']] == []:
                # Host doesn't exist
                return False
            else:
                hostId = [item['hostid'] for item in result['result']][0]
                self.zabbix_api.do_request('item.create', {'hostid': hostId, 'value_type': '0','type': '2', 'name': zbx_item_name, 'key_': zbx_item_UID})
                logger.info(f'[Zabbix] Item created: {zbx_item_name}')
                return True
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False

  def getItemID (self,hostName,itemKey):
    '''
    - `name`: getItemID
    - `description`:  Lấy ID của item.
    - `parameters`:
      - `hostName`: Tên host.
      - `itemKey`: item key.
    - `return`: ID của item.
    - `Example`:
      - getItemID('DaLat_Tanung_GW0',"201X0.1.2")
    '''
    try:
        result = self.zabbix_api.do_request('item.get', {'host': hostName, 'filter': {'key_': [itemKey]}})
        if [item['name'] for item in result['result']] == []:
            return False
        else:
            return [item['itemid'] for item in result['result']][0]
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False
      
  def updateItemValue (self,zbx_host, zbx_item_UID, zbx_item_value):
    '''
    - `name`: updateItemValue
    - `description`:  Tạo item trên Zabbix.
    - `parameters`:
      - `zbx_host`: Tên host.
      - `zbx_item_UID`: UID của item. VD: 201X0.1.2 # CMEV, ABC_Customer, X, GW ID 0. Sensor ID 1. CH2.
      - `zbx_item_value`: Giá trị item.
    - `return`: None
    - `Example`:
      - updateItemValue('DaLat_Tanung_GW0', '201X0.1.2', '250')
    - `PIC`: ✨ Components/PIC/001.png
    '''
    metrics = [ZabbixMetric(zbx_host, zbx_item_UID, zbx_item_value)]
    logger.debug(f'[Zabbix] {zbx_host} update item value: {zbx_item_UID} = {zbx_item_value}')
    ZabbixSender(zabbix_server=self.zabbix_server, zabbix_port=self.zabbix_port).send(metrics)
    
    # server = ZabbixSender(self.zabbix_server,self.zabbix_port)
    # packet = ZabbixPacket()
    # packet.add(zbx_host,zbx_item_UID,zbx_item_value)
    # server.send(packet)




  # def updateItemValue2 (self,zbx_itemid, zbx_item_value):
  #   try:
  #     self.zabbix_api.item.update(itemid=str(zbx_itemid),name=str(zbx_item_value))
  #     logger.info(f'[Zabbix] Hostgroup renamed: {zbx_hostgroup_new_name}')      # log hostgroup creation
  #   except Exception:
  #       logger.error('[Zabbix] Unable to request to server')
    

      

      

  


  def getHostParam (self,hostName):
    '''
    - `name`: getHostParam
    - `description`:  Lấy các tham số của host.
    - `parameters`:
      - `hostName`: Tên host.
    - `return`: Các tham số của host.
    - `Example`:
      - getHostParam('DaLat_Tanung_GW0')
    '''
    try:
        result = self.zabbix_api.do_request('host.get', {'filter': {'host': [hostName]}})
        if [host['host'] for host in result['result']] == []:
            return False
        else:
            return result['result'][0]
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False
      
  def getItemParam (self,hostName,itemName):
    '''
    - `name`: getItemValue
    - `description`:  Lấy giá trị của item.
    - `parameters`:
      - `hostName`: Tên host.
      - `itemName`: Tên item.
    - `return`: Giá trị của item. Dạng dictionary.
    - `Example`:
      - getItemValue('DaLat_Tanung_GW0', "201X0.1.2")
    '''
    try:
        result = self.zabbix_api.do_request('item.get', {'host': hostName, 'filter': {'name': [itemName]}})
        return result['result'][0]
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False

  def updateItemParam (self,hostName,itemKey, updateParamDict={}):
    '''
    - `name`: updateItemParam
    - `description`: Cập nhật tham số của item.
    - `parameters`:
      - `hostName`: Tên host.
      - `itemKey`: Tên item key.
      - `updateParamDict`: Danh sách tham số cần cập nhật dạng dict.\\
         Ex: {"units": "bpm"}\\
         Danh sách item's parameter: https://www.zabbix.com/documentation/6.0/en/manual/api/reference/item/object
    - `return`: None
    - `Example`:
      - updateItemParam("DaLat_Tanung_GW0","201X0.1.2",{"units": "bpm"})
    '''
    try:
        itemId = self.getItemID(hostName,itemKey)
        updateDict = {'itemid': itemId}
        updateDict.update(updateParamDict)
        self.zabbix_api.do_request('item.update',updateDict)
    except Exception:
        logger.error('[Zabbix] Unable to request to server')
        return False

################## TESTING #######################
# zabbix_server   = '157.65.24.169'
# zabbix_port     =  10051
# zabbix_user     = 'Admin'
# zabbix_password = 'zabbix'
# zabbix_url      = 'http://'+zabbix_server

# hostGroupName   = "HostGroup_Test" 
# hostName        = "HostName_Test"
# itemName        = "ItemName_Test"
# itemUID         = "itemUID_Test" # CMEV, ABC_Customer, X, GW ID 0. Sensor ID 1. CH2.

# zabbixLib = zabbix_Wrapper(zabbix_server, zabbix_port, zabbix_user, zabbix_password, zabbix_url)

# zabbixLib.__init__(zabbix_server, zabbix_port, zabbix_user, zabbix_password)
# zabbixLib.createHostgroup(hostGroupName)
# zabbixLib.createHost(hostGroupName, hostName)
# zabbixLib.createItem(hostName,itemUID,itemName)
# zabbixLib.updateItemValue (hostName, itemUID, 250)



