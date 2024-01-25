#########################################################
import __init
print("==== START ====")
######################################
# Phần này giúp máy Devloper có thể chạy với các Args như Container được chỉ định.
import os, shutil
CHANNEL_NAME = "tik_vn_nancy_1"
if os.path.exists("D:/Database/SynologyDrive/Biz/RootManager1/data/channel_"+CHANNEL_NAME+"/0_AllTasks/task_2_args.py"):
  shutil.copy("D:/Database/SynologyDrive/Biz/RootManager1/data/channel_"+CHANNEL_NAME+"/0_AllTasks/task_2_args.py", "D:/Database/SynologyDrive/GIT/LOTUS_Python_Framework/task_args.py")
if os.path.exists("/HShare/0_AllTasks/task_2_args.py"):
  shutil.copy("/HShare/0_AllTasks/task_2_args.py", "/HShare/code/task_args.py")
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
# logger.info(">>>>> STEP 0:  Initial for WDT <<<<<")
def hamGoiKhiWDT_Timeout():
  print("Hàm này được gọi khi Watchdog timeout")
  sleep(1)
  if SYS.pcInfo.pcName() != 'LOTUS-PC':
    # os.system("shutdown -t 0 -r -f") #Restart PC nếu không phải là Lotus-PC
    WDT.stop()
    TIK.clearContainerExeptLogs() #Chỉ xóa nếu không phải đang chạy Debug Mode
    TIK.reqManKill(os.getenv("CONTAINER_NAME"))
    exit()
WDT = SYS.thread_WDT(threadID = 1, name = "watchDog", timeThresSec = 300, callbackFunc = hamGoiKhiWDT_Timeout)
WDT.start()

#Load các tham số từ file task_args.py
SCANNED_LIST = str(ARGS.SCANNED_LIST) #Đường dẫn đến thư mục chứa video đã được download
READY_LIST_PATH = str(ARGS.READY_LIST_PATH) #Đường dẫn đến thư mục chứa video đã được duyệt
MAX_BIND_DOWNLOAD = int(ARGS.MAX_BIND_DOWNLOAD) #Số lượng video bind tối đa được download

if not os.path.exists(SCANNED_LIST): os.mkdir(SCANNED_LIST)

TIK = tiktok_Wrapper()

MAX_RETRY = 2 #Số lần download video bị lỗi

################################################################################################
##############################      MAIN APPLICATION     #######################################
################################################################################################
logger.info(">>>>> STEP 1:  Mở trình duyệt <<<<<")
TIK.UPLOAD.openBrowser("https://godownloader.com",incognito=False)
#Click tắt các bảng thông báo không cần thiết

sleep(1)
LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/0_CloudFlareAuth_2.png",confidence=0.7,timeout_sec=15,delayFinish_ms=0.5)
sleep(5)
LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/0_CloudFlareAuth_3.png",confidence=0.7,timeout_sec=15,delayFinish_ms=0.5)
GUI.mouse.click(535,360) # /MyAPP/TiktopApp/GX/PIC/0_CloudFlareAuth.png Click vào vị trí nút xác thực CloudFlare Auth.
sleep(0.1)
GUI.mouse.click(535,406) # /MyAPP/TiktopApp/GX/PIC/0_CloudFlareAuth.png Click vào vị trí nút xác thực CloudFlare Auth.

LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/0_GoDownload_finish_loaded.png",confidence=0.75,timeout_sec=15,delayFinish_ms=0.5)
# TIK.UPLOAD.tat_cac_thong_bao()

try:
  #1. Kiểm tra số lượng video bind trong vn_20_scanned_list có status là -999.
  #- Nếu 0 < số lượng <= 20 thì đổi trạng thái của các video với kiểy key_type là bind với trạng thái Downloaded thành -999.
  #- Đồng thời xóa hết các video với key_type là bind trong bảng vn_30_ready_list.
  TIK.checkBindVideo()
  
  retry = 0
  stopFetchBind = False
  clipInfo = None
  while True:
    WDT.refreshWDT()
    #1. Kiểm tra cờ dừng fetch video bind.
    #Nếu số lượng video trong thư mục 1_ready_list/bind < 20 thì tiếp tục fetch video bind.
    #Nếu số lượng video trong thư mục 1_ready_list/bind >= 20 thì dừng fetch video bind.
    if len(os.listdir(READY_LIST_PATH + "/bind")) < MAX_BIND_DOWNLOAD:
      stopFetchBind = False
    else:
      stopFetchBind = True
    
    #2. Fetch thông tin video. Thứ tự: ADS > BIND > SEARCH > TAG
    if retry == 0: #Fetch thông tin clip lần đầu tiên. Các lần retry sau không cần fetch lại.
      if gxMysql.myDb.is_connected() == False:
        logger.warning("MySQL connection was lost => Reconected")
        gxMysql.myDb.reconnect() #Tránh lỗi mất kết nối: "2013 (HY000): Lost connection to MySQL server during query"
      clipInfo = TIK.fetchNewClip(clipType="ads") #Tìm một clip ứng viên trong vn_20_scanned_list có status là -999
      TIK.videoLocation = READY_LIST_PATH + "/ads" #Đường dẫn đến thư mục chứa video
      if clipInfo == None:
        if stopFetchBind == False:
          clipInfo = TIK.fetchNewClip(clipType="bind",randQuery=True) #Dạng "bind" sẽ được load random.
          TIK.videoLocation = READY_LIST_PATH + "/bind" #Đường dẫn đến thư mục chứa video
        if clipInfo == None:
          clipInfo = TIK.fetchNewClip(clipType="search")
          TIK.videoLocation = SCANNED_LIST #Đường dẫn đến thư mục chứa video
          if clipInfo == None:
            clipInfo = TIK.fetchNewClip(clipType="tag")
            TIK.videoLocation = SCANNED_LIST #Đường dẫn đến thư mục chứa video
    
    #3. Download video
    if clipInfo != None:
      print(clipInfo)
      result = TIK.downloadNoWaterMarkVideoGui(clipInfo[2],clipInfo[1],clipInfo[3],clipInfo[4],clipInfo[5])
      #4. Cập nhật thẳng vào vn_30_ready_list nếu nó thuộc dạng 'bind' hay 'ads'
      if clipInfo[3] == 'bind' or clipInfo[3] == 'ads':
        viddeoId = clipInfo[1] #Lấy videoId của video vừa download
        TIK.UPLOAD.copyRowFromScannedListToReadyList(viddeoId) #Copy dòng dữ liệu của video vừa download vào bảng vn_30_ready_list
      #5. Cập nhật trạng thái của video vừa download vào vn_20_scanned_list
      if result == True:
        TIK.updateClipStatus(clipInfo[0],"Downloaded")
        retry = 0
      else:
        if (retry >= MAX_RETRY):
          TIK.updateClipStatus(clipInfo[0],"Failed")
          retry = 0
        else:
          retry += 1
    else:
      logger.info("=== Không còn clip mới/Đã đủ số lượng video bind ===")
      break
  
except Exception as e:
  print(e)
  print("Có lỗi Scanned List")
finally:
  pass


##### STOP/KILL ALL THREAD #####
thread_captchaSolvingStart = False #Kết thúc thread captcha solving
WDT.stop()
for i in range(1,10):
  GUI.key.hotkey('ctrl','w') #Đóng tất cả các tab
  sleep(0.1)
TIK.clearContainerExeptLogs() #Chỉ xóa nếu không phải đang chạy Debug Mode
TIK.reqManKill(os.getenv("CONTAINER_NAME"))
