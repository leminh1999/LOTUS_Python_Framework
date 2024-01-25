import __init
print("==== START ====")
######################################
# Phần này giúp máy Devloper có thể chạy với các Args như Container được chỉ định.
import os, shutil
CHANNEL_NAME = "tik_vn_nancy_1"
if os.path.exists("D:/Database/SynologyDrive/Biz/RootManager1/data/channel_"+CHANNEL_NAME+"/0_AllTasks/task_4_args.py"):
  shutil.copy("D:/Database/SynologyDrive/Biz/RootManager1/data/channel_"+CHANNEL_NAME+"/0_AllTasks/task_4_args.py", "D:/Database/SynologyDrive/GIT/LOTUS_Python_Framework/task_args.py")
if os.path.exists("/HShare/0_AllTasks/task_4_args.py"):
  shutil.copy("/HShare/0_AllTasks/task_4_args.py", "/HShare/code/task_args.py")
######################################
from task_args import *
from time import sleep,time
from Conf.loggingSetup import *
from Library.C3_OmoCaptcha.omoCaptcha import omoCaptcha; OMO = omoCaptcha()
from SystemManager.system_Wrap import SYS
from Library.A1_PyAutoGUI.pyAutoGui_Wrap import pyAutoGui_Remap as GUI
from Library.A2_LOTUS.lotus_Wrap import rgb,lotus_Remap as LOTUS
from Library.A3_Selenium.selenium_Wrap import Keys, WEB, seleniumIDE_Remap as IDE
# from Library.A4_SendInBlue.sendInBlue_Wrap import class_contentMode, mailConfig, sendInBlue_Wrapper as SIB
from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
from Library.A7_Zalo.Zalo_Wrap import botConfig,zalo_Wrapper as ZALO
from MyAPP.TiktopApp.GX.Components.tiktok_class import gxMysql,dataInfo, tiktok_Wrapper; TIK = tiktok_Wrapper()
TIK  = tiktok_Wrapper()
from Conf.systemVar import *
from pprint import *
import os
print("==== FINISH IMPORT ====")

bypassDelay = True
READY_LIST_PATH = str(ARGS.READY_LIST_PATH)
CLIP_CAPTION = str(ARGS.CLIP_CAPTION)
CLIP_HASHTAG = str(ARGS.CLIP_HASHTAG)
CLIP_MODE = str(ARGS.CLIP_MODE) #PRIVATE, PUBLIC (default)
USER_ACCOUNT = str(ARGS.GOOGLE_USER)
USER_PASS = str(ARGS.GOOGLE_PASS)

################################################################################################
##############################      MAIN APPLICATION     #######################################
################################################################################################


try:
  ############################################################################################################
  ############################################################################################################
  ############################################################################################################
  ### STEP 0. Zalo to boss ###
  ZALO.sendMessage(botConfig.ZALO_BOSS_PHONE,"text","Publishing...")
  ### STEP 1. Mở trình duyệt ###
  logger.info(">>>>> STEP 1: Mở trình duyệt <<<<<")
  IDE.setup.begin("Chrome",userProfilePath="ABC",headless=False,antiCaptcha=False,incognitoMode=False)
  IDE.others.others_browser_maximizeWindow()
  IDE.others.others_clearReqWaitCmdFlg()
  
  while True:
    sleep(1)
    
    
    
    
    
    
    
    
  # USER_ACCOUNT = "jackrose.2000@yahoo.com"
  # USER_PASS = "axn@HBO60"
  USER_ACCOUNT = "abcdef123456@getnada.com"
  USER_PASS = "H@@n24687"
  TIK.googleAccountLogin(user="tranhuudung1986@gmail.com",password="H@@n24687")
  
  #Login With Google Account on Web
  if "@gmail.com" in USER_ACCOUNT:
    TIK.googleAccountLogin(user=USER_ACCOUNT,password=USER_PASS)
    
  IDE.browser.open("https://www.tiktok.com")
  IDE.waitFor.waitForElementVisible(target="xpath=//a[@data-e2e='tiktok-logo']")
  sleep(2)
  
  ### STEP 2. Đăng nhập vào tài khooản Tiktok bằng tài khoản Google ###
  logger.info(">>>>> STEP 2. Đăng nhập vào tài khooản Tiktok bằng tài khoản Email <<<<<")
  if "@gmail.com" in USER_ACCOUNT:
    TIK.loginTiktokWithGoogleEmail(USER_ACCOUNT)
  else:
    TIK.loginTiktokWithOtherEmail(USER_ACCOUNT,USER_PASS)
  
  ### STEP 3. Upload Video ###
  logger.info(">>>>> STEP 3. Upload Video <<<<<")
  gxMysql.checkConnectionToReconnect() #Tránh lỗi mất kết nối: "2013 (HY000): Lost connection to MySQL server during query"
  fetchDatabase = TIK.UPLOAD.fetchOneClipFromReadyListForPublishing()
  if fetchDatabase != None:
    uploadFile = TIK.createUploadVideo(READY_LIST_PATH, fetchDatabase)
    TIK.UPLOAD.seleUploadVideo(uploadFile,CLIP_CAPTION+" "+CLIP_HASHTAG,CLIP_MODE)
    # TIK.removeUploadVideo(uploadFile) #Xoá file upload ở Local (1_ready_list/Processing)
    os.system("rm -f "+READY_LIST_PATH+"/Processing/*") #Xoá các video ở 1_ready_list/Processing
    TIK.removeBindAdsVideo(READY_LIST_PATH, fetchDatabase)
  
    ### STEP 4. Cập nhật vào Publish MySQL ###
    logger.info(">>>>> STEP 4. Cập nhật vào Publish MySQL <<<<<")
    publishInfo = TIK.UPLOAD.seleGetLastPost() #Lấy thông tin video mới nhất
    # print(publishInfo)
    followingInfo = TIK.UPLOAD.getFollowingInfo() #Lấy thông tin video mới nhất
    logger.debug(followingInfo)
    
    if publishInfo != None:
      # Cập nhật vn_40_publish_list MySQL
      TIK.UPLOAD.updatePublishList(publishInfo,fetchDatabase["video_id"]) #Cập nhật vào Publish MySQL
      # Cập nhật vn_30_ready_list MySQL
      # Nếu video có key_type là bind hay ads thì xóa vn_30_ready_list
      # Nếu video có key_type là dạng khách thì update Published  vào vn_30_ready_list
      try:
        if fetchDatabase["key_type"] == "bind" or fetchDatabase["key_type"] == "ads":
          gxMysql.deleteRow("vn_30_ready_list", whereCondition="video_id = '"+str(fetchDatabase["video_id"])+"'")
        else:
          gxMysql.updateRow("vn_30_ready_list", "status = 'Published'", whereCondition="video_id = '"+str(fetchDatabase["video_id"])+"'")
      except Exception as e:
        logger.error(e)
        
      # ### STEP 5. Xóa video cũ ở tài khoản ###
      
      ### STEP 6. Zalo to boss ###
      gxMysql.checkConnectionToReconnect() #Tránh lỗi mất kết nối: "2013 (HY000): Lost connection to MySQL server during query"
      ZALO.sendMessage(botConfig.ZALO_BOSS_PHONE,"text",publishInfo["link"])

    logger.info("==== FINISH ====")
  else:
    logger.warning("Không tìm được Video")
    
except Exception as e:
  logger.error("ERROR!!!")
  logger.error(e)
  ZALO.sendMessage(botConfig.ZALO_BOSS_PHONE,"text","Publishing ERROR")
finally:
  pass


##### STOP/KILL ALL THREAD #####
thread_captchaSolvingStart = False #Kết thúc thread captcha solving
for i in range(1,10):
  GUI.key.hotkey('ctrl','w') #Đóng tất cả các tab
  sleep(0.1)
TIK.clearContainerExeptLogs() #Chỉ xóa nếu không phải đang chạy Debug Mode
TIK.reqManKill(os.getenv("CONTAINER_NAME"))