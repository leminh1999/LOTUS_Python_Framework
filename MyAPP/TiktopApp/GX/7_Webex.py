import __init
print("==== START ====")
import os,threading
import math
from time import sleep,time,strftime,localtime
from datetime import timedelta
from Library.A3_Selenium.selenium_Wrap import Keys, WEB, seleniumIDE_Remap as IDE
from Library.A9_MQTT.mqtt import mqttClass #pip install requests==paho-mqtt1.6.1
print("==== FINISH IMPORT ====")
PROFILE_NAME = "tran.dung.webex.7z"
# os.system("rm -rf /root/.config/google-chrome")
# os.system("7z x -y /HShare/ChromeProfileMan/"+PROFILE_NAME+" -o/root/.config/google-chrome/")

FROM_TIME = math.ceil(time())
TO_TIME   = math.ceil(time())
CUR_TIME  = math.ceil(time())
WEB_STATUS = "0. INIT"
webOperatingFlag = False

def subcribeFilter(msg):
  global FROM_TIME, TO_TIME, WEB_STATUS
  try:
    if msg.topic == "WEBEX_HOST_RX" and msg.payload.decode() != "":
      message = str(msg.payload.decode())
      print("Received message: ",message)
      
      #Nếu message có dạng thời gian theo phút 30m, 1h, 2h,... thì tính toán thời gian FROM_TIME và TO_TIME
      if "m" in message or "h" in message:
        FROM_TIME = math.ceil(time())
        if "m" in message:
          TO_TIME = math.ceil(time()) + int(message.split("m")[0])*60
        elif "h" in message:
          TO_TIME = math.ceil(time()) + int(message.split("h")[0])*3600
        print("FROM_TIME: ",strftime('%H:%M:%S', localtime(FROM_TIME)))
        print("TO_TIME: ",strftime('%H:%M:%S', localtime(TO_TIME)))
        MQTT.publish(topic="WEBEX_HOST_TX", msg="👉✨⭐Receive Request!!!\nFROM: "+strftime('%H:%M:%S', localtime(FROM_TIME))+"\nTO: "+strftime('%H:%M:%S', localtime(TO_TIME)))
      
      #Nếu có 2 mốc thời gian trong message theo dạng 8h 14h30 thì tính toán thời gian FROM_TIME và TO_TIME
      if " " in message:
        #Tách phần FROM_TIME và TO_TIME
        fromTime = message.split(" ")[0]
        toTime = message.split(" ")[1]
        
        #Tách phần giờ và phút
        fromHour = int(fromTime.split("h")[0])
        fromMinute = int(fromTime.split("h")[1].split("m")[0])
        toHour = int(toTime.split("h")[0])
        toMinute = int(toTime.split("h")[1].split("m")[0])
        
        #Tính toán thời gian FROM_TIME và TO_TIME
        FROM_TIME = math.ceil(time()) + fromHour*3600 + fromMinute*60
        TO_TIME = math.ceil(time()) + toHour*3600 + toMinute*60
        print("FROM_TIME: ",strftime('%H:%M:%S', localtime(FROM_TIME)))
        print("TO_TIME: ",strftime('%H:%M:%S', localtime(TO_TIME)))
        MQTT.publish(topic="WEBEX_HOST_TX", msg="👉✨⭐Receive Request!!!\nFROM: "+strftime('%H:%M:%S', localtime(FROM_TIME))+"\nTO: "+strftime('%H:%M:%S', localtime(TO_TIME)))
      
      if "STOP" in message:
        FROM_TIME = math.ceil(time())
        TO_TIME = math.ceil(time())
        print("STOP!!!")
        MQTT.publish(topic="WEBEX_HOST_TX", msg="👉✨⭐Receive Request!!!\n⛔⛔⛔!!!")
        WEB_STATUS = "3. Waiting for Request..."
        MQTT.publish(topic="WEBEX_HOST_TX", msg=WEB_STATUS)
        
      if "STATUS" in message:
        MQTT.publish(topic="WEBEX_HOST_TX", msg=WEB_STATUS)
      
  except Exception as e:
    print("ERROR!!!")
    print(e)
      
MQTT = mqttClass("broker.emqx.io")
MQTT.msgRcvFilter = subcribeFilter
MQTT.subscribe("WEBEX_HOST_RX")
threading.Thread(target=MQTT.listen).start()

################################################################################################
##############################      MAIN APPLICATION     #######################################
################################################################################################

try:
  ############################################################################################################
  ############################################################################################################
  ############################################################################################################
  ### STEP 1. Mở trình duyệt ###
  print(">>>>> STEP 1: Mở trình duyệt <<<<<")
  WEB_STATUS = "1. Opening Browser..."
  MQTT.publish(topic="WEBEX_HOST_TX", msg=WEB_STATUS)
  webOperatingFlag = True
  IDE.setup.begin("Chrome",userProfilePath=PROFILE_NAME,headless=False,antiCaptcha=False,incognitoMode=False)
  IDE.others.others_browser_maximizeWindow()
  IDE.others.others_clearReqWaitCmdFlg()
  WEB_STATUS = "2. Login..."
  MQTT.publish(topic="WEBEX_HOST_TX", msg=WEB_STATUS)
  IDE.browser.open("https://web.webex.com/calls");sleep(15)
  IDE.waitFor.waitForElementVisible(target="xpath=//input[@data-test='people-search-input']")
  
  WEB_STATUS = "3. Waiting for Request..."
  MQTT.publish(topic="WEBEX_HOST_TX", msg=WEB_STATUS)
  
  while True:
    CUR_TIME = math.ceil(time())
    if FROM_TIME <= CUR_TIME <= TO_TIME:
      #PAST_TIME convert to string
      PAST_TIME_INT = CUR_TIME - FROM_TIME
      timeSplit = str(timedelta(seconds=PAST_TIME_INT)).split(":")
      if PAST_TIME_INT >= 3600:
        PAST_TIME_STR = timeSplit[0]+"h"+timeSplit[1]
      elif PAST_TIME_INT >= 60:
        PAST_TIME_STR = timeSplit[1]+"m"+timeSplit[2]
      else:
        PAST_TIME_STR = timeSplit[2]+"sec"
        
      #REMAIN_TIME convert to string
      REMAIN_TIME_INT = TO_TIME - CUR_TIME
      timeSplit = str(timedelta(seconds=REMAIN_TIME_INT)).split(":")
      if REMAIN_TIME_INT >= 3600:
        REMAIN_TIME_STR = timeSplit[0]+"h"+timeSplit[1]
      elif REMAIN_TIME_INT >= 60:
        REMAIN_TIME_STR = timeSplit[1]+"m"+timeSplit[2]
      else:
        REMAIN_TIME_STR = timeSplit[2]+"sec"
      WEB_STATUS = "4. In Schedule: "+PAST_TIME_STR+" | "+REMAIN_TIME_STR
      
      #Nếu thời gian time() chia hết cho 5s thì gửi thông báo WEB_STATUS
      if int(CUR_TIME-FROM_TIME)%5 == 0:
        MQTT.publish(topic="WEBEX_HOST_TX", msg=WEB_STATUS)
        #TOUCH WEBEX
        CUR_TIME = strftime('%H:%M:%S', localtime(CUR_TIME))
        IDE.mouseKey.click(target="xpath=//input[@data-test='people-search-input']")
        IDE.others.others_clearReqWaitCmdFlg()
        IDE.mouseKey.sendKeys("xpath=//input[@data-test='people-search-input']","${KEY_CONTROL}A")
        IDE.others.others_clearReqWaitCmdFlg()
        IDE.mouseKey.type(target="xpath=//input[@data-test='people-search-input']",value=str(CUR_TIME))
        IDE.others.others_clearReqWaitCmdFlg()
        
      sleep(1)
    
    else:
      WEB_STATUS = "3. Waiting for Request..."
      sleep(1)
    
    
    
    
    
  

    
except Exception as e:
  print("ERROR!!!")
  print(e)
finally:
  pass
