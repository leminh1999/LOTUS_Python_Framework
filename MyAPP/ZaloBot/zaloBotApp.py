import __init
print("==== START ====")
from time import sleep,time
from Conf.loggingSetup import *
from SystemManager.system_Wrap import SYS
from Library.A1_PyAutoGUI.pyAutoGui_Wrap import pyAutoGui_Remap as GUI
from Library.A2_LOTUS.lotus_Wrap import lotus_Remap as LOTUS
from Library.A3_Selenium.selenium_Wrap import Keys, WEB, seleniumIDE_Remap as IDE
from Library.A4_SendInBlue.sendInBlue_Wrap import class_contentMode, mailConfig, sendInBlue_Wrapper as SIB
from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
# from Library.A6_Zabbix.Zabbix_Wrap import zabbix_Wrapper as ZABBIX
from Library.A7_Zalo.Zalo_Wrap import zalo_Wrapper as ZALO
# from Library.C1_Captcha.captcha_Wrap import captcha_Wrapper as CAPTCHA
# from pyngrok import ngrok, conf
from pprint import *
print("==== FINISH IMPORT ====")
logger.info(">>>>> STEP 0:  Initial for WDT <<<<<")

def hamGoiKhiWDT_Timeout():
  print("Hàm này được gọi khi Watchdog timeout")
  sleep(1)
  if SYS.pcInfo.pcName() != 'LOTUS-PC':
    os.system("shutdown -t 0 -r -f") #Restart PC nếu không phải là Lotus-PC
   
WDT = SYS.thread_WDT(threadID = 1, name = "watchDog", timeThresSec = 300, callbackFunc = hamGoiKhiWDT_Timeout)
WDT.start()  

logger.info(">>>>> STEP 1:  Mở trình duyệt, gửi mail, chờ đăng nhập vào Zalo <<<<<")  
#1. Mở trình duyệt, gửi mail, chờ đăng nhập vào Zalo
#PIC: Library\A7_Zalo\Components\PIC\001.png
ZALO.openChrome(headless=False)
IDE.others.others_clearReqWaitCmdFlg()
# IDE.others.others_browser_setBrowserPosition(1800,0)
# IDE.others.others_clearReqWaitCmdFlg()
IDE.others.others_browser_maximizeWindow()
IDE.others.others_clearReqWaitCmdFlg()
ZALO.sendMailQrcode()
#Chờ đến khi QR code không còn hiện (đã được đăng nhập) trong
#thời gian tối đa có thể hiển thị của nó (3 phút).
#Nếu vẫn còn hiển thị thì refresh rồi gửi lại.
while True:
  #Kiểm tra đăng nhập thành công.
  divTabIndicator =  IDE.others.others_content_findFirstElement("xpath=//div[@class='tab-indicator']","","",printCmd=False)
  if divTabIndicator != None: break
    
  #Kiểm tra mã quá hạn -> Gửi lại QR code mới và tiếp tục chờ.
  qrTimeOverErr = IDE.others.others_content_findFirstElement("xpath=//em[@class='error']","","",printCmd=False)
  if qrTimeOverErr != None:
    IDE.mouseKey.click("xpath=//a[text()='Lấy mã mới']")
    IDE.waitFor.waitForElementNotVisible("xpath=//em[@class='error']")
    ZALO.sendMailQrcode()


logger.info(">>>>> STEP 2:  Gửi Tin nhắn Welcome  <<<<<") 
#STEP 2.1. Nhảy vào contact và chờ message đến
ZALO.returnWaitScreen()
#STEP 2.2: Gửi tin nhắn Welcome Administrator
ZALO.welcomeToAdminMess()
#STEP 2.3: Vào màn hình chờ tin nhắn
#SEND DUMMY DATA TO TEST
# ZALO.dummyTxTest()

n = 0
WDT.refreshWDT()
logger.info(">>>>> STEP 3:  Kiểm tra tin nhắn đến và đi  <<<<<") 
while True:
  #3.1: Kiểm tra TX buffer gửi đi  
  ZALO.sendAllTxBuffer()
  WDT.refreshWDT()
  #3.2: Kiểm tra các tin nhắn nhận được
  ZALO.readMessToRxBuffer()
  #3.3: Refresh WDT. Trở về màn hình chờ sau khoảng 5 phút kiểm tra tin nhắn.
  WDT.refreshWDT()
  sleep(0.1)
  n += 1
  if n > 600:
    n=0
    logger.info ("Periodic return Wait Screen (~5mins)")
    # print(time())
    ZALO.returnWaitScreen() #Quay trở về màn hình chờ tin nhắn
    # zaloBot.dummyReadMySql() #Dummy read để tránh bị close session MySQL
  
  
  



# IDE.waitFor.waitForElementVisible("xpath=//div[@class='tab-indicator']","","Chờ tab-indicator hiện ra",printCmd=False)



    
  

while(1):
  pass

# IDE.setup.begin("Chrome",headless=False)
# sleep(3)
# # IDE.browser.open('https://chat.zalo.me/')
# response = WEB.driver.request('POST', 'https://democaptcha.com/demo-form-eng/recaptcha-2.html', data={"g-recaptcha-response": result})

# response = WEB.driver.request('POST', 'https://democaptcha.com/demo-form-eng/recaptcha-2.html', data={"g-recaptcha-response": result})
# sleep(3)
# print(response)