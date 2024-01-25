#########################################################
# Nhiệm vụ:
# - Xóa hết tất cả các video bị cũ hơn thời gian cho phép (CLIP_LIMIT_HOURS)
# - Xóa các clip Tiktok có nhưng không có ở MySQL và ngược lại.

import __init
print("==== START ====")
######################################
# Phần này giúp máy Devloper có thể chạy với các Args như Container được chỉ định.
import os, shutil
CHANNEL_NAME = "tik_vn_nancy_1"
if os.path.exists("D:/Database/SynologyDrive/Biz/RootManager1/data/channel_"+CHANNEL_NAME+"/0_AllTasks/task_5_args.py"):
  shutil.copy("D:/Database/SynologyDrive/Biz/RootManager1/data/channel_"+CHANNEL_NAME+"/0_AllTasks/task_5_args.py", "D:/Database/SynologyDrive/GIT/LOTUS_Python_Framework/task_args.py")
if os.path.exists("/HShare/0_AllTasks/task_5_args.py"):
  shutil.copy("/HShare/0_AllTasks/task_5_args.py", "/HShare/code/task_args.py")
######################################
from task_args import *
from time import sleep,time
import datetime
from Conf.loggingSetup import *
from SystemManager.system_Wrap import SYS
from Library.A1_PyAutoGUI.pyAutoGui_Wrap import pyAutoGui_Remap as GUI
from Library.A2_LOTUS.lotus_Wrap import rgb,lotus_Remap as LOTUS
from Library.A3_Selenium.selenium_Wrap import Keys, WEB, seleniumIDE_Remap as IDE
# from Library.A4_SendInBlue.sendInBlue_Wrap import class_contentMode, mailConfig, sendInBlue_Wrapper as SIB
from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
# from Library.A7_Zalo.Zalo_Wrap import botConfig,zalo_Wrapper as ZALO
from MyAPP.TiktopApp.GX.Components.tiktok_class import gxMysql,dataInfo, tiktok_Wrapper
from Conf.systemVar import *
from pprint import *
import threading
import random
import sys
import os
print("==== FINISH IMPORT ====")




bypassDelay = True
GOOGLE_USER = str(ARGS.GOOGLE_USER)
GOOGLE_PASS = str(ARGS.GOOGLE_PASS)
CLIP_LIMIT_HOURS = str(ARGS.CLIP_LIMIT_HOURS) #Giới hạn số giờ của clip. Nếu clip cũ hơn thời gian này thì sẽ bị xóa.
DEL_NOT_SYNC_CLIP = str(ARGS.DEL_NOT_SYNC_CLIP) #TRUE/FALSE. Xóa các clip Tiktok có nhưng không có ở MySQL và ngược lại.
PROFILE_NAME = str(ARGS.PROFILE_NAME) #Tên profile cần xóa clip cũ

# os.system("chmod 666 MyAPP/TiktopApp/GX/PIC/*") #Cho phép tất cả user đọc file ảnh
TIK  = tiktok_Wrapper()
print("==== FINISH IMPORT ====")
logger.info(">>>>> STEP 0:  Initial for WDT <<<<<")
def hamGoiKhiWDT_Timeout():
  print("Hàm này được gọi khi Watchdog timeout")
  sleep(1)
  if SYS.pcInfo.pcName() != 'LOTUS-PC':
    os.system("shutdown -t 0 -r -f") #Restart PC nếu không phải là Lotus-PC
WDT = SYS.thread_WDT(threadID = 1, name = "watchDog", timeThresSec = 600, callbackFunc = hamGoiKhiWDT_Timeout)
WDT.start()
################################################################################################
##############################      MAIN APPLICATION     #######################################
################################################################################################

try:
  ############################################################################################################
  ############################################################################################################
  ############################################################################################################
  ### STEP 1. Mở trình duyệt ###
  TIK.loadConfigGx()
  logger.info(">>>>> STEP 1: Mở trình duyệt <<<<<")
  TIK.UPLOAD.openBrowser("www.tiktok.com",incognito=False) #Mở lại trình duyệt
  LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/0_Tiktok_loadpagefinished.png",confidence=0.7,timeout_sec=30,delayFinish_ms=500)
  
  ### STEP 2. Đăng nhập vào tài khooản ###
  logger.info(">>>>> STEP 2. Đăng nhập vào tài khooản Google <<<<<")
  result = TIK.googleAccountLogin(user=GOOGLE_USER,password=GOOGLE_PASS)
  if result == "LOGGED_IN":
    pass
  else: #NEW_LOGIN or RE_LOGIN
    #Đóng trình duyệt
    for i in range(0,10):
      GUI.key.hotkey("ctrl","w")
      sleep(0.1)
    #Mở lại trình duyệt vào trang profile
    TIK.UPLOAD.openBrowser("www.tiktok.com/",incognito=False,checkFirstOpen=False) #Mở lại trình duyệt
    LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/0_Tiktok_loadpagefinished.png",confidence=0.7,timeout_sec=30,delayFinish_ms=500)
  
  ### STEP 3. Đăng nhập vào tài khooản Tiktok bằng tài khoản Google ###
  logger.info(">>>>> STEP 3. Đăng nhập vào tài khoản Tiktok bằng tài khoản Google <<<<<")
  TIK.UPLOAD.loginTiktokGoogle()
  WDT.refreshWDT()
  TIK.UPLOAD.gotoProfilePage(PROFILE_NAME)
  
  ### STEP 4. Xác định danh sách video cần xóa ###
  logger.info(">>>>> STEP 4. Xác định danh sách video cần xóa <<<<<")
  if gxMysql.myDb.is_connected() == False:
    logger.warning("MySQL connection was lost => Reconected")
    gxMysql.myDb.reconnect() #Tránh lỗi mất kết nối: "2013 (HY000): Lost connection to MySQL server during query"
  #4.1 Xóa hết tất cả các video bị cũ hơn thời gian cho phép (CLIP_LIMIT_HOURS)
  if DEL_NOT_SYNC_CLIP == "FALSE":
    onlyMysqlPublishedList = list()
    onlyWebPublishedList = list()
    overTimePublishedList = list(TIK.getOverTimePublishedList(int(CLIP_LIMIT_HOURS)))
    delList = overTimePublishedList
    logger.debug("Các video cần xóa ["+str(len(delList))+"] = " + str(delList))
  else:
    mysqlPublishedList,orgVideoidList = list(TIK.getMysqlPublishedList())
    logger.debug("mysqlPublishedList ["+str(len(mysqlPublishedList))+"] = " + str(mysqlPublishedList))
    webPublishedList = list(TIK.UPLOAD.getWebPublishedList())
    logger.debug("webPublishedList ["+str(len(webPublishedList))+"] = " + str(webPublishedList))
    if len(webPublishedList) == 0:
      logger.warning("Không có/Load được danh sách video trên WEB (do lỗi???) => Ngừng quá trình xóa kiểm tra và xóa video để tránh rủi ro xóa nhầm")
      WDT.stop()
      TIK.clearContainerExeptLogs() #Chỉ xóa nếu không phải đang chạy Debug Mode
      TIK.reqManKill(os.getenv("CONTAINER_NAME"))
    onlyMysqlPublishedList = list(set(mysqlPublishedList) - set(webPublishedList))
    logger.debug("Các video chỉ có ở MySQL ["+str(len(onlyMysqlPublishedList))+"] = " + str(onlyMysqlPublishedList))
    bothMysqlAndWebPublishedList = list(set(mysqlPublishedList) & set(webPublishedList))
    logger.debug("Các video có cả MySQL+WEB ["+str(len(bothMysqlAndWebPublishedList))+"] = " + str(bothMysqlAndWebPublishedList))
    onlyWebPublishedList = list(set(webPublishedList) - set(mysqlPublishedList))
    logger.debug("Các video chỉ có ở WEB ["+str(len(onlyWebPublishedList))+"] = " + str(onlyWebPublishedList))
    overTimePublishedList = list(TIK.getOverTimePublishedList(int(CLIP_LIMIT_HOURS)))
    logger.debug("Các video quá thời gian tồn tại ["+str(len(overTimePublishedList))+"] = " + str(overTimePublishedList))
    delList = list(onlyMysqlPublishedList + onlyWebPublishedList + overTimePublishedList)
    logger.debug("Các video cần xóa ["+str(len(delList))+"] = " + str(delList))
    
  ### STEP 5. Xóa clip ###
  logger.info(">>>>> STEP 5. Xóa clip <<<<<")
  logger.debug("5.1 Xóa clip trên MySQL")
  #5.1 Xóa clip trên MySQL
  clearVn40MysqlList = onlyMysqlPublishedList + overTimePublishedList #CHÚ Ý: Các video thuộc bảng vn_40 đang dùng VideoID mới publish. Khác với bảng vn_30 đang dùng VideoID cũ.
  clearVn30MysqlList = TIK.convertNewVideoidToOldVideoid(clearVn40MysqlList)
  #5.1.1 Xóa clip trên bảng vn_40
  for i in range(0,len(clearVn40MysqlList)):
    TIK.deleteVideoidFromPublishedList(clearVn40MysqlList[i])
  #5.1.2 Xóa clip trên bảng vn_30
  for i in range(0,len(clearVn30MysqlList)):
    TIK.deleteVideoidFromReadyList(clearVn30MysqlList[i])
  #5.1.3 Xóa clip trên bảng vn_20 nếu nó thuộc dạng bind hay ads
  for i in range(0,len(clearVn30MysqlList)):
    TIK.deleteBindAdsVideoidFromScannedList(clearVn30MysqlList[i])

  #5.2 Xóa clip trên Web
  logger.debug("5.2 Xóa clip trên Web/Profile")
  clearWebList = onlyWebPublishedList + overTimePublishedList
  for i in range(0,len(clearWebList)):
    #Click vào thanh address bar và gõ địa chỉ
    logger.info("===== ["+str(i+1)+"] Delete Video "+str(clearWebList[i])+" From Profile =====")
    videoLink = "https://www.tiktok.com/@"+str(PROFILE_NAME)+"/video/"+clearWebList[i]
    TIK.deleteVideoFromProfile(videoLink)

  logger.info("==== FINISH ====")
    
except Exception as e:
  logger.error("ERROR!!!")
  logger.error(e)
finally:
  pass


##### STOP/KILL ALL THREAD #####
thread_captchaSolvingStart = False #Kết thúc thread captcha solving
for i in range(1,10):
  GUI.key.hotkey('ctrl','w') #Đóng tất cả các tab
  sleep(0.1)
WDT.stop()
TIK.clearContainerExeptLogs() #Chỉ xóa nếu không phải đang chạy Debug Mode
TIK.reqManKill(os.getenv("CONTAINER_NAME"))
