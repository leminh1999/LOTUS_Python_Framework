#########################################################
# APPLICATION (SELENIUM Headless)
# 1. Load config để lấy các từ khóa từ vn_10_key_list từ MySQL về.
# 2. Lần lượt scan từng từ khóa (search/tag) trong vn_10_key_list bằng Selenium.
# 3. Với mỗi key sẽ có nhiều video quét được => Đưa các video này vào vn_02_scanned_list nếu nó chưa tồn tại trong MySQL.
# 4. Thread giải captcha và WDT song song.

import __init
print("==== START ====")
######################################
# Phần này giúp máy Devloper có thể chạy với các Args như Container được chỉ định. Một Containerr bất kỳ có thể chạy với task_args của các task khác.
import os, shutil
CHANNEL_NAME = "tik_vn_nancy_1"
if os.path.exists("D:/Database/SynologyDrive/Biz/RootManager1/data/channel_"+CHANNEL_NAME+"/0_AllTasks/task_1_args.py"):
  shutil.copy("D:/Database/SynologyDrive/Biz/RootManager1/data/channel_"+CHANNEL_NAME+"/0_AllTasks/task_1_args.py", "D:/Database/SynologyDrive/GIT/LOTUS_Python_Framework/task_args.py")
if os.path.exists("/HShare/0_AllTasks/task_1_args.py"):
  shutil.copy("/HShare/0_AllTasks/task_1_args.py", "/HShare/code/task_args.py")
######################################
from task_args import *
from time import sleep,time
from Conf.loggingSetup import *
from SystemManager.system_Wrap import SYS
from Library.A1_PyAutoGUI.pyAutoGui_Wrap import pyAutoGui_Remap as GUI
from Library.A2_LOTUS.lotus_Wrap import lotus_Remap as LOTUS
from Library.A3_Selenium.selenium_Wrap import Keys, WEB, seleniumIDE_Remap as IDE
# from Library.A4_SendInBlue.sendInBlue_Wrap import class_contentMode, mailConfig, sendInBlue_Wrapper as SIB
from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
from MyAPP.TiktopApp.GX.Components.tiktok_class import gxMysql,dataInfo, tiktok_Wrapper
from pprint import *
import threading
print("==== FINISH IMPORT ====")

USER_ACCOUNT = str(ARGS.USER_EMAIL)
CHROME_PROFILE = str(ARGS.CHROME_PROFILE)

if CHROME_PROFILE == "AUTOSEARCH":
  PROFILE_NAME = "tiktok_"+USER_ACCOUNT+".7z"
  os.system("rm -rf /root/.config/google-chrome")
  os.system("7z x -y /HShare/ChromeProfileMan/"+PROFILE_NAME+" -o/root/.config/google-chrome/")
elif ".7z" in  CHROME_PROFILE:
  PROFILE_NAME = CHROME_PROFILE
  os.system("rm -rf /root/.config/google-chrome")
  os.system("7z x -y /HShare/ChromeProfileMan/"+PROFILE_NAME+" -o/root/.config/google-chrome/")
else:
  PROFILE_NAME = ""

################################################################################################
##############################      MAIN APPLICATION     #######################################
################################################################################################
IGNORE_ACCOUNT_LIST = ["thebest202211"] #EX: IGNORE_ACCOUNT = ["user1","user2","user3"]

# logger.info(">>>>> STEP 0:  Initial for WDT <<<<<")
def hamGoiKhiWDT_Timeout():
  logger.warn("Watchdog timeout => Exit")
  TIK.clearContainerExeptLogs() #Chỉ xóa nếu không phải đang chạy Debug Mode
  TIK.reqManKill(os.getenv("CONTAINER_NAME"))
  exit()
WDT = SYS.thread_WDT(threadID = 1, name = "watchDog", timeThresSec = 300, callbackFunc = hamGoiKhiWDT_Timeout)
WDT.start()

TIK = tiktok_Wrapper()

logger.info(">>>>> STEP 1:  Mở trình duyệt <<<<<")
################################
#### Thread Captcha Solving ####
################################
thread_captchaSolvingStart = True
def thread_captcha_solving():
  while thread_captchaSolvingStart == True:
    #Print date time
    print("==> Time: %s" % time())
    TIK.captchaSolving()
    sleep(0.5)
################################

################################################################################################
##############################      MAIN APPLICATION     #######################################
################################################################################################
#1. Quét dữ liệu và cập nhật vào Scanned list
TIK.loadConfigGx()
for i in range(0,TIK.maxList):
  WDT.refreshWDT()
  logger.info("============= SEARCHING LIST {}/{} =============\n".format(i+1,TIK.maxList))
  try:
    #### Open browser and maximize window and start captcha solving thread
    try:
      IDE.setup.quit() #Kết thúc trình duyệt
    except:
      pass
    TIK.openChrome(userProfilePath=PROFILE_NAME,headless=False,antiCaptcha=True)
    IDE.others.others_browser_maximizeWindow()
    IDE.others.others_clearReqWaitCmdFlg()
    thread_Captcha = threading.Thread(target=thread_captcha_solving)
    thread_Captcha.start()
    
    ### Quét dữ liệu
    TIK.loadConfigGx() #Load các cấu hình của MySQL (bảng vn_10_key_list) dựa theo con trỏ của Row dữ liệu trong bảng vn_00 (key_check_num)
    if dataInfo.cur_key_type == "search":
      TIK.scanSearchList(keywords=dataInfo.cur_key_word)
      listClip = IDE.others.others_content_findAllElements("xpath=//div[contains(@class,'DivItemContainerForSearch')]","","Liệt kê toàn bộ clip vào list")
      dataInfo.cur_total_num = len(listClip)
      logger.info("Scan được %d clips\n", dataInfo.cur_total_num)
    elif dataInfo.cur_key_type == "tag":
      pass
    elif dataInfo.cur_key_type == "bind":
      TIK.scanBindList(keywords=dataInfo.cur_key_word)
      
      if gxMysql.myDb.is_connected() == False:
        logger.warning("MySQL connection was lost => Reconected")
        gxMysql.myDb.reconnect() #Tránh lỗi mất kết nối: "2013 (HY000): Lost connection to MySQL server during query"
      
      listClip = IDE.others.others_content_findAllElements("xpath=//div[contains(@class,'DivItemContainerV2')]","","Liệt kê toàn bộ clip vào list")
      dataInfo.cur_total_num = len(listClip)
      logger.info("Scan được %d clips\n", dataInfo.cur_total_num)
      #Xóa dữ liệu bind cũ
      TIK.delOldBindList(keywords=dataInfo.cur_key_word)
    else:
      continue

    i = 0
    for eachClip in listClip:
      print(i)
      i+=1
      # EX: https://www.tiktok.com/@cartoon_5_world/video/7013098852551052546
      clipLink = IDE.others.others_content_getAttribute("xpath=*//a[contains(@href,'video')]","href","Lấy URL của clip",False,eachClip)
      dataInfo.cur_video_link = clipLink
      dataInfo.cur_video_id = clipLink.split('/video/')[1]
      dataInfo.cur_video_user = clipLink.split('/')[-3].split('@')[1]
      print(dataInfo.cur_video_link)
      print(dataInfo.cur_video_id)
      print(dataInfo.cur_video_user)
      
      #Upload Scan list
      if dataInfo.cur_video_user not in IGNORE_ACCOUNT_LIST:
        TIK.appendScanList(dataInfo.cur_video_link,dataInfo.cur_video_id,dataInfo.cur_video_user)
    
  except Exception as e:
    logger.error("Có lỗi Scanned List")
    logger.error(e)
  finally:
    try:
      #Tăng giá trị scan trong table config
      checkNum = dataInfo.cfg00_key_check_num
      checkNum += 1
      if checkNum > TIK.maxList:
        checkNum = 1
      #Cập nhật MySQL: Config table
      sql = "UPDATE vn_00_config SET key_check_num = "+str(checkNum)+" WHERE id = 1"
      gxMysql.myCursor.execute(sql)
      gxMysql.myDb.commit()
      #Cập nhật MySQL: key_list table
      dataInfo.cur_scan_time += 1
      sql = "UPDATE vn_10_key_list SET scan_time = "+str(dataInfo.cur_scan_time)+", total_num = "+str(dataInfo.cur_total_num)+" WHERE id = "+str(dataInfo.cur_key_list_id)
      gxMysql.myCursor.execute(sql)
      gxMysql.myDb.commit()
    except Exception as e:
      logger.error("Có lỗi cập nhật MySQL")
      logger.error(e)
      break
    
##### STOP/KILL ALL THREAD #####
thread_captchaSolvingStart = False #Kết thúc thread captcha solving
WDT.stop()       #Kết thúc thread WDT
IDE.setup.quit() #Kết thúc trình duyệt
TIK.clearContainerExeptLogs() #Chỉ xóa nếu không phải đang chạy Debug Mode
TIK.reqManKill(os.getenv("CONTAINER_NAME"))