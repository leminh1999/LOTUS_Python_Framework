import __init
print("==== START ====")
######################################
# Phần này giúp máy Devloper có thể chạy với các Args như Container được chỉ định.
import os, shutil
os.system("echo '==== START ====' >> /HShare/code/0_log.txt")

CHANNEL_NAME = "tik_vn_nancy_1"
if os.path.exists("D:/Database/SynologyDrive/Biz/RootManager1/data/channel_"+CHANNEL_NAME+"/0_AllTasks/task_4_args.py"):
  shutil.copy("D:/Database/SynologyDrive/Biz/RootManager1/data/channel_"+CHANNEL_NAME+"/0_AllTasks/task_4_args.py", "D:/Database/SynologyDrive/GIT/LOTUS_Python_Framework/task_args.py")
if os.path.exists("/HShare/0_AllTasks/task_4_args.py"):
  shutil.copy("/HShare/0_AllTasks/task_4_args.py", "/HShare/code/task_args.py")
######################################
from task_args import *
from time import sleep,time
from Conf.loggingSetup import *

os.system("echo DB1 >> /HShare/code/0_log.txt")

from Library.A1_PyAutoGUI.pyAutoGui_Wrap import pyAutoGui_Remap as GUI
os.system("echo DB2 >> /HShare/code/0_log.txt")

from Library.A3_Selenium.selenium_Wrap import Keys, WEB, seleniumIDE_Remap as IDE
os.system("echo DB3 >> /HShare/code/0_log.txt")

from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
os.system("echo DB4 >> /HShare/code/0_log.txt")

from MyAPP.TiktopApp.GX.Components.tiktok_class import gxMysql,dataInfo, tiktok_Wrapper; TIK = tiktok_Wrapper()
os.system("echo DB5 >> /HShare/code/0_log.txt")

TIK  = tiktok_Wrapper()
from Conf.systemVar import *
from pprint import *
import os

os.system("echo DB6 >> /HShare/code/0_log.txt")
print("==== FINISH IMPORT ====")

READY_LIST_PATH = str(ARGS.READY_LIST_PATH)
CLIP_CAPTION = str(ARGS.CLIP_CAPTION)
CLIP_HASHTAG = str(ARGS.CLIP_HASHTAG)
CLIP_MODE = str(ARGS.CLIP_MODE) #PRIVATE, PUBLIC (default)
USER_ACCOUNT = str(ARGS.USER_EMAIL)
USER_PASS = str(ARGS.USER_PASS)
CHROME_PROFILE = str(ARGS.CHROME_PROFILE)
os.system("echo DB7 >> /HShare/code/0_log.txt")

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
logger.info("PROFILE_NAME: "+PROFILE_NAME)
os.system("echo DB8 >> /HShare/code/0_log.txt")

################################################################################################
##############################      MAIN APPLICATION     #######################################
################################################################################################


try:
  ############################################################################################################
  ############################################################################################################
  ############################################################################################################
  ### STEP 0. Zalo to boss ###
  # ZALO.sendMessage(botConfig.ZALO_BOSS_PHONE,"text","Publishing...")
  ### STEP 1. Mở trình duyệt ###
  logger.info(">>>>> STEP 1: Mở trình duyệt <<<<<")
  IDE.setup.begin("Chrome",userProfilePath=PROFILE_NAME,headless=False,antiCaptcha=False,incognitoMode=False)
  IDE.others.others_browser_maximizeWindow()
  IDE.others.others_clearReqWaitCmdFlg()
  os.system("echo DB9 >> /HShare/code/0_log.txt")
  
    
  IDE.browser.open("https://www.tiktok.com")
  IDE.waitFor.waitForElementVisible(target="xpath=//a[@data-e2e='tiktok-logo']")
  sleep(2)
  os.system("echo DB10 >> /HShare/code/0_log.txt")
  
  ### STEP 3. Upload Video ###
  logger.info(">>>>> STEP 3. Upload Video <<<<<")
  gxMysql.checkConnectionToReconnect() #Tránh lỗi mất kết nối: "2013 (HY000): Lost connection to MySQL server during query"
  retryCount = 0
  while retryCount < 5:
    retryCount += 1
    logger.debug("=== STEP 3.1. Fetch Video ===")
    fetchDatabase = TIK.UPLOAD.fetchOneClipFromReadyListForPublishing()
    if fetchDatabase != None:
      try:
        logger.debug("=== STEP 3.2. Tạo video để upload ===")
        uploadFile = TIK.createUploadVideo(READY_LIST_PATH, fetchDatabase)
        logger.debug("=== STEP 3.3. Upload video lên ===")
        TIK.UPLOAD.seleUploadVideo(uploadFile,CLIP_CAPTION+" "+CLIP_HASHTAG,CLIP_MODE)
        logger.debug("=== STEP 3.4. Remove file video ở Processing và Ready Folder ===")
        # TIK.removeUploadVideo(uploadFile) #Xoá file upload ở Local (1_ready_list/Processing)
        os.system("rm -f "+READY_LIST_PATH+"/Processing/*") #Xoá các video ở 1_ready_list/Processing
        TIK.removeBindAdsVideo(READY_LIST_PATH, fetchDatabase)
      
        # ### STEP 4. Cập nhật vào Publish MySQL ###
        publishInfo = "SKIP_PUBLISH"
        # logger.info(">>>>> STEP 4. Cập nhật vào Publish MySQL <<<<<")
        # publishInfo = TIK.UPLOAD.seleGetLastPost() #Lấy thông tin video mới nhất
        # # print(publishInfo)
        # followingInfo = TIK.UPLOAD.getFollowingInfo() #Lấy thông tin video mới nhất
        # logger.debug(followingInfo)
      except Exception as e:
        logger.error(e)
        gxMysql.deleteRow("vn_30_ready_list", whereCondition="video_id = '"+str(fetchDatabase["video_id"])+"'")
        continue
      
      if publishInfo != None:
        # Cập nhật vn_40_publish_list MySQL
        # TIK.UPLOAD.updatePublishList(publishInfo,fetchDatabase["video_id"]) #Cập nhật vào Publish MySQL
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
          continue
          
        # ### STEP 5. Xóa video cũ ở tài khoản ###
        
        ### STEP 6. Zalo to boss ###
        # gxMysql.checkConnectionToReconnect() #Tránh lỗi mất kết nối: "2013 (HY000): Lost connection to MySQL server during query"
        # ZALO.sendMessage(botConfig.ZALO_BOSS_PHONE,"text",publishInfo["link"])

      logger.info("==== FINISH ====")
      break
    else:
      logger.warning("Không tìm được Video")
      continue
    
except Exception as e:
  logger.error("ERROR!!!")
  logger.error(e)
  # ZALO.sendMessage(botConfig.ZALO_BOSS_PHONE,"text","Publishing ERROR")
finally:
  pass


##### STOP/KILL ALL THREAD #####
thread_captchaSolvingStart = False #Kết thúc thread captcha solving
for i in range(1,10):
  GUI.key.hotkey('ctrl','w') #Đóng tất cả các tab
  sleep(0.1)
TIK.clearContainerExeptLogs() #Chỉ xóa nếu không phải đang chạy Debug Mode
TIK.reqManKill(os.getenv("CONTAINER_NAME"))