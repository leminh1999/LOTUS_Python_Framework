#########################################################
# APPLICATION (KHÔNG DÙNG BROWSER (SELENIUM HAY GUI + LOTUS))
# 1. Load danh sách các video đang có trong vn_30_ready_list ở MySQL.
# 2. Vào thư mục chứa các video đã được duyệt để lấy danh sách các file .mp4 nằm trong thư mục này.
# 3. Xét từng file video trong thư mục này với file MySQL để xem file này đã được đưa lên MySQL chưa?
# 3.1 Nếu rồi thì xét file khác.
# 3.2 Nếu chưa thì:
# 3.2.1 Copy row dữ liệu của video này từ vn_20_scanned_list sang vn_30_ready_list
# 3.2.2 Cập nhật status của row này thành trạng thái mới tạo (status = "-999") và cập nhật lại TIMESTAMP.

import __init
print("==== START ====")
######################################
# Phần này giúp máy Devloper có thể chạy với các Args như Container được chỉ định.
import os, shutil
CHANNEL_NAME = "tik_vn_nancy_1"
if os.path.exists("D:/Database/SynologyDrive/Biz/RootManager1/data/channel_"+CHANNEL_NAME+"/0_AllTasks/task_3_args.py"):
  shutil.copy("D:/Database/SynologyDrive/Biz/RootManager1/data/channel_"+CHANNEL_NAME+"/0_AllTasks/task_3_args.py", "D:/Database/SynologyDrive/GIT/LOTUS_Python_Framework/task_args.py")
if os.path.exists("/HShare/0_AllTasks/task_3_args.py"):
  shutil.copy("/HShare/0_AllTasks/task_3_args.py", "/HShare/code/task_args.py")
######################################
from task_args import *
from time import sleep,time
from Conf.loggingSetup import *
from SystemManager.system_Wrap import SYS
# from Library.A1_PyAutoGUI.pyAutoGui_Wrap import pyAutoGui_Remap as GUI
from Library.A2_LOTUS.lotus_Wrap import lotus_Remap as LOTUS
# from Library.A3_Selenium.selenium_Wrap import Keys, WEB, seleniumIDE_Remap as IDE
# from Library.A4_SendInBlue.sendInBlue_Wrap import class_contentMode, mailConfig, sendInBlue_Wrapper as SIB
from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
from MyAPP.TiktopApp.GX.Components.tiktok_class import gxMysql,dataInfo, tiktok_Wrapper
from pprint import *

print("==== FINISH IMPORT ====")

TIK = tiktok_Wrapper()
READY_LIST_PATH = str(ARGS.READY_LIST_PATH) #Thư mục chứa các video đã được duyệt
if not os.path.exists(READY_LIST_PATH):            os.mkdir(READY_LIST_PATH)
if not os.path.exists(READY_LIST_PATH+"/ads"):     os.mkdir(READY_LIST_PATH+"/ads")
if not os.path.exists(READY_LIST_PATH+"/bind"):    os.mkdir(READY_LIST_PATH+"/bind")
if not os.path.exists(READY_LIST_PATH+"/approve"): os.mkdir(READY_LIST_PATH+"/approve")
################################################################################################
##############################      MAIN APPLICATION     #######################################
################################################################################################
try:
  
  #1.1 Kiểm tra tính tương đồng của video trong thư mục /HShare/0_AllTasks/0_scanned_list/bind và bảng vn_30_ready_list từ MySQL với key_type là bind và trạng thái status là Ready.
  #Chỉ giữ lại các video trong thư mục và dữ liệu từ bảng vn_30_ready_list nếu nó trùng nhau.
  #Nếu không trùng nhau thì xóa video trong thư mục và dữ liệu trong bảng vn_30_ready_list.
  TIK.checkSimilarity()
  
  #1. Load danh sách các video đang có trong vn_30_ready_list ở MySQL.
  queryString = "SELECT video_id FROM vn_30_ready_list;"
  gxMysql.myCursor.execute(queryString)
  readyListString = str(gxMysql.myCursor.fetchall())
  
  #2. Vào thư mục chứa các video đã được duyệt để lấy danh sách các file .mp4 nằm trong thư mục này.
  localListVideoFileName = LOTUS.others.listDir(READY_LIST_PATH+"/approve",returnFullPath=0)
  checkCounter = 0
  newVideoCounter = 0
  for file in localListVideoFileName:
    #1. Get file name only (also videoId)
    if ".mp4" in file:
      checkCounter += 1
      file = file.split(".mp4")[0]
      # print(file)
      viddeoId = file.split("_")[-1]

      
      #2. Check if videoId is in readyListString (if not, then add to MySQL/vn_30_ready_list)
      if str(viddeoId) in readyListString:
        # print("Video đã có trong ready list")
        continue
      else:
        logger.info("Video ID: "+str(viddeoId)+" chưa có trong vn_30_ready_list -> Add mới vào MySQL")
        newVideoCounter += 1
        #3. Copy entire a row from vn_20_scanned_list to vn_30_ready_list with videoId in gxMysql
        sql = "INSERT INTO vn_30_ready_list SELECT * FROM vn_20_scanned_list WHERE video_id='"+str(viddeoId)+"'"
        gxMysql.myCursor.execute(sql)
        gxMysql.myDb.commit()
        
        #4. Copy entire a row from vn_20_scanned_list to vn_30_ready_list with videoId in gxMysql
        updateString = "status = 'Ready', timestamp = CURRENT_TIMESTAMP"
        gxMysql.updateRow("vn_30_ready_list", updateString, whereCondition="video_id='"+str(viddeoId)+"'")
        
  logger.info("Đã xử lý cho "+str(checkCounter)+" file .mp4. Video mới: "+str(newVideoCounter))
  
except Exception as e:
  logger.error("Có lỗi Scanned List")
  logger.error(e)
finally:
  pass

TIK.clearContainerExeptLogs() #Chỉ xóa nếu không phải đang chạy Debug Mode
TIK.reqManKill(os.getenv("CONTAINER_NAME"))


