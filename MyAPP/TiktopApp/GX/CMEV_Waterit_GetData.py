#########################################################
# APPLICATION (SELENIUM Headless)
# 1. Load config để lấy các từ khóa từ vn_10_key_list từ MySQL về.
# 2. Lần lượt scan từng từ khóa (search/tag) trong vn_10_key_list bằng Selenium.
# 3. Với mỗi key sẽ có nhiều video quét được => Đưa các video này vào vn_02_scanned_list nếu nó chưa tồn tại trong MySQL.
# 4. Thread giải captcha và WDT song song.

import __init
print("==== START ====")
from task_args import *
import os
from time import sleep,time
from Conf.loggingSetup import *
from SystemManager.system_Wrap import SYS
from Library.A1_PyAutoGUI.pyAutoGui_Wrap import pyAutoGui_Remap as GUI
from Library.A2_LOTUS.lotus_Wrap import lotus_Remap as LOTUS
from Library.A3_Selenium.selenium_Wrap import Keys, WEB, seleniumIDE_Remap as IDE
# from Library.A4_SendInBlue.sendInBlue_Wrap import class_contentMode, mailConfig, sendInBlue_Wrapper as SIB
from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
from Library.A6_Zabbix.Zabbix_Wrap import zabbix_Wrapper as ZABBIX_LIB
from MyAPP.TiktopApp.GX.Components.tiktok_class import gxMysql,dataInfo, tiktok_Wrapper
from pprint import *
import threading
import re
print("==== FINISH IMPORT ====")

# logger.info(">>>>> STEP 0:  Initial for WDT <<<<<")
def hamGoiKhiWDT_Timeout():
  print("Hàm này được gọi khi Watchdog timeout")
  sleep(1)
  if SYS.pcInfo.pcName() != 'LOTUS-PC' and SYS.pcInfo.pcName() != 'LOTUS_S0':
    os.system("shutdown -t 0 -r -f") #Restart PC nếu không phải là Lotus-PC
WDT = SYS.thread_WDT(threadID = 1, name = "watchDog", timeThresSec = 300, callbackFunc = hamGoiKhiWDT_Timeout)
# WDT.start()
USERNAME = "ly.ra@cmengineering.com.vn"
USERPASS = "enyJnAFMHMJJ"
WEBPAGE = 'https://www.dms2.waterit.optex.net'
TIK = tiktok_Wrapper()

zabbix_server   = '157.65.24.169'
# zabbix_server   = '192.168.60.168'
# zabbix_server   = 'host.docker.internal' # Tuong duong voi localhost của host PC
zabbix_port     =  10051
zabbix_user     = 'Admin'
zabbix_password = 'zabbix'
zabbix_url      = 'http://'+zabbix_server
#1. Khởi tạo Zabbix
zabbixLib = ZABBIX_LIB(zabbix_server, zabbix_port, zabbix_user, zabbix_password, zabbix_url)


logger.info(">>>>> STEP 1:  Mở trình duyệt <<<<<")
################################################################################################
##############################      MAIN APPLICATION     #######################################
################################################################################################
while True:
  IDE.setup.begin("Chrome",headless=True)
  IDE.others.others_browser_maximizeWindow()
  IDE.others.others_clearReqWaitCmdFlg()
  try:
    #1. Login
    IDE.browser.open(WEBPAGE) #Login page
    IDE.waitFor.waitForElementVisible("id=MailAddress")
    IDE.mouseKey.type("id=MailAddress",USERNAME)
    IDE.waitFor.waitForAttr("id=MailAddress","value="+USERNAME)
    IDE.mouseKey.type("id=Password",USERPASS)
    IDE.waitFor.waitForAttr("id=Password","value="+USERPASS)
    IDE.mouseKey.click("id=Login")

    #2. Get data
    IDE.waitFor.waitForElementVisible("tag=tbody")
    IDE.waitFor.waitForElementVisible("xpath=//img[contains(@src,'ic_list.svg')]")
    IDE.waitFor.waitForElementVisible("xpath=//a[contains(@href,'WIA1501/Index03')]")
    IDE.mouseKey.click("xpath=//a[contains(@href,'WIA1501/Index03')]")
    # IDE.waitFor.waitForElementVisible("//td[contains(@class, 'odd')|//td[contains(@class, 'dataTables_empty')]") #Wait box of value appear
    IDE.waitFor.waitForElementVisible("class=odd") #Wait box of value appear
    noData = IDE.assertVerify.verifyText("class=odd","not found",printCmd=False)
    if noData == True:
      print("The data to view is not found.")
      IDE.setup.quit() #Kết thúc trình duyệt
      exit()
    IDE.waitFor.waitForElementVisible("id=Boxes") #Wait box of value appear

    #3. Print each row
    from bs4 import BeautifulSoup
    allRow = IDE.others.others_content_findAllElements("xpath=//tr[contains(@role, 'row')]")
    if len(allRow) < 2:
      print("The data to view is not found.")
      IDE.setup.quit() #Kết thúc trình duyệt
      exit()
    else:
      for row in allRow[1:]:
        # IDE.others.others_clearReqWaitCmdFlg()
        # sleep(1)
        # allTd = IDE.others.others_content_findAllElements("xpath=//td",element=row)
        # for td in allTd:
        #   print(td.text,end=" | ")
        
        #BS4
        bsElement = BeautifulSoup(row.get_attribute('innerHTML'), 'html.parser')
        allTd = bsElement.select("td")
        rowTime = allTd[1].text
        rowItem = allTd[2].text.replace("(","_").replace(")","_").replace(" ","_")
        rowItem = re.sub(r'[\(\) ]', '_', rowItem)
        rowValue = allTd[3].text
        rowUnit = allTd[4].text
        rowArea = allTd[5].text
        rowPoint = allTd[6].text
        rowSerial = allTd[11].text
        print(rowTime,rowItem,rowValue,rowUnit,rowArea,rowPoint,rowSerial)
        rowInfoString = rowTime+" "+rowItem+" "+rowValue+" "+rowUnit+" "+rowArea+" "+rowPoint+" "+rowSerial
        
        #Check rowInfoString in wateritRecord.txt file.
        # if rowInfoString in the file -> do nothing
        # if rowInfoString not in the file -> add rowInfoString to file and upload to Zabbix
        if os.path.isfile(".wateritRecord.txt") == False:
          print(".wateritRecord.txt file is not exist.")
          os.system("echo '' > .wateritRecord.txt")

        if rowInfoString in open(".wateritRecord.txt").read():
          print("=== FINISH. There is no new data to upload. ===")
          break 
        else:
          print("==> New data to upload.")

          #Upload to Zabbix
          HOSTGROUP_NAME   = "WaterIt_Device"
          HOST_NAME        = rowSerial
          ITEM_NAME        = rowItem
          ITEM_VALUE       = float(rowValue)
          ITEM_UUID         = HOST_NAME+"."+ITEM_NAME # CMEV, ABC_Customer, X, GW ID 0. Sensor ID 1. CH2.
          if zabbixLib.getItemID(HOST_NAME,ITEM_NAME) == False:
            zabbixLib.createHostgroup(HOSTGROUP_NAME)
            zabbixLib.createHost(HOSTGROUP_NAME, HOST_NAME)
            zabbixLib.createItem(HOST_NAME,ITEM_UUID,ITEM_NAME)
            zabbixLib.updateItemParam(HOST_NAME,ITEM_UUID,{"units": rowUnit})

          zabbixLib.updateItemValue (HOST_NAME, ITEM_UUID, ITEM_VALUE)
          # Add rowInfoString to file
          with open(".wateritRecord.txt", "a") as myfile:
            myfile.write(rowInfoString+"\n")
  except Exception as e:
    print("ERROR: ",e)
  finally:
    IDE.setup.quit() #Kết thúc trình duyệt
    sleep(60)

