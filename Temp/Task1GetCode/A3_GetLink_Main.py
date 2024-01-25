# Các bước thực hiện:
#   1. Mở trình duyệt.
#   2. Đăng nhập vào tài khooản.
#   3. Nhập vào URL sau: https://www.tiktok.com/@vangiau.07/video/6907176330987719937?lang=vi-VN
#   Sẽ xuất hiện 1 video hướng đến cái ta chọn và Tiktok sẽ tự động load thêm 28 video đề xuát dành cho bạn (Chú ý video đề xuất này sẽ không liên quan gì đến đường dẫn URL ta đã nhập).
#   4. Nhấn nút Page Down 20 lần. Mỗi lần cách nhau 0.5 giây.
#   5. Thực hiện lọc mã nguồn HTML để bắt dữ liệu và link video.
#   6. Link nào bắt được thỏa tiêu chí về số lượng like/comment/share tối thiểu và user không thuộc bảng blacklist thì đưa vào mySQL cho tác vụ 2 thực hiện rồi lại thực hiện lặp lại từ bước 3 đến 5.
# CHÚ Ý: Clip đưa vào mySQL có thể trùng. Trong trường hợp trùng thì nó sẽ cập nhật lại cột thời gian cập nhật, lượt tim, comment và share.
# Đườnng URL ở bước 3 được lấy bằng việc. Nhấn vào 1 video  bất kỳ. Sau khi màn hình mở ra video chế độ lớn thì copy URL đang có rồi nhập lại nhấn enter :)
#=======================================================================================
### Điều kiện chạy ###
# 1. Tỉ lệ màn hình 1920x1080
# 2. Vị trí chrome và của sổ code như hình. Images/9b.png
# 3. Cửa sổ chrome mặc định mở lên là maximize
# 3. Tỉ lệ màn hình Web là 1350x947 (phần còn lại của code) Images/8b.png
#    Mở phần xem code rồi click giữ cạnh biên để resize. Khi resize sẽ xuất hiện con số để canh tỉ lệ.
#=======================================================================================
### Standard Lib ###
import time
import os
import random
### USER Declare ###
from Global.loggingSetup import *
from A1_GetLink_Define import *
from LotusLib_v1r2 import *
from A4_GetLink_Function import *

task1GetLink = Task1GetLink
task2GetComment = Task2GetComment


runTime = 1
pcRunResetCnt = 1
taskScheduleRunning = 0
currentVpnWorking = ""

#Configure for Task Killer
nodeName = platform.uname()[1]
curDay  = datetime.datetime.now()
logPicName = 'Logs\Logfile_'+str(nodeName)+'_'+str(curDay.day)+str(curDay.strftime("%b"))+'_'+str(curDay.strftime("%H.%M.%S"))
LotusLib.taskKillerStart(threadID = 1, threadName = 'TaskKiller',logPathAndPrefixName = logPicName,pythonKillHotkey = 'shift+f12',vscodeKillHotkey = 'shift+f5')

try:
  #Delay from 0 to 2sec. Step 0.1 second.
  time.sleep(random.randint(0,20)/10)
  #Clear dummy png images at root folder
  for i in os.listdir("./"):
    if i.endswith('.png'):
      os.remove(i)

  ### STEP 1. Mở trình duyệt ###
  logger.info(">>>>> STEP 1: Mở trình duyệt <<<<<")
  task1GetLink.openChrome()
  LotusLib.delay(2000)
  # currentVpnWorking = task1GetLink.connectVpn(VPN_NATION)
  
  ### STEP 2. Đăng nhập vào tài khooản ###
  logger.info(">>>>> STEP 2. Đăng nhập vào tài khooản <<<<<")
  # ---> Gia sử tài khoản được đăng nhập tự động hoặc dùng các tài khoản tạm
  task1GetLink.loadMysqlBlacklist()
  followList = task1GetLink.loadMysqlFollowList(add_type='manual')
  
  while 1:
    task1GetLink.taskSchedulerChecking(taskScheduleRunning) #Kiểm tra task scheduler (Đi tiếp hay ngủ chờ task kế)
    taskScheduleRunning = 1
    logger.info(">>>>> Đọc config từ MySQL <<<<<")
    task1GetLink.loadMysqlConf()
    task1GetLink.loadMysqlTaskMon()

    if tikTopTaskMon.task1_running_flag == "1":
      myCursor.execute("create table IF NOT EXISTS tiktop_vol"+str(tikTopConfig.vol_num)+" (id INT AUTO_INCREMENT PRIMARY KEY) select * from tiktop_vol0_master")
      logger.info(">>>>> TASK 1 RUNNING <<<<<")
      logger.info("===========================================================================================================")
      logger.info("===== LOOP: "+str(runTime)+" ========================================================================================")
      logger.info("===========================================================================================================")
      watchDogCnt = 0 # Clear watchdog counter mỗi lần chạy
      
      ### STEP 3. Nhập vào URL ###
      logger.info(">>>>> STEP 3. Nhập vào URL <<<<<")
      task1GetLink.openURL(curPostInfo.video_link)
      task1GetLink.openCodeWindow()
      task1GetLink.loginGoogleAccAgain()
      
      ### STEP 4. Nhấn nút Page Down 30 lần. Mỗi lần cách nhau 0.5 giây ###
      logger.info(">>>>> STEP 4. Nhấn nút Page Down 60 lần. Mỗi lần cách nhau 0.5 giây <<<<<")
      task1GetLink.scrollLoadHTMLCode()

      ### STEP 5. Thực hiện lọc mã nguồn HTML để bắt dữ liệu và link video ###
      logger.info(">>>>> STEP 5. Thực hiện lọc mã nguồn HTML để bắt dữ liệu và link video <<<<<")
      htmlCode = task1GetLink.getCode() #Lấy HTML Code đưa vào biến
      # file = open("README.html", "r",encoding="utf8", errors="surrogateescape")
      # htmlCode = file.readline()
      
      logger.info(">>>>> STEP 5.1 Parsing dữ liệu từ web <<<<<")
      task1GetLink.parsingHTML_task1(str(htmlCode),minPost=2,followList=followList)
      # logger.info("============> DEBUG: END PARSING HTML CODE")
      task1GetLink.checkHalting(currentVpnWorking,logPicName)
      runTime += 1
 
      logger.info(">>>>> STEP 5.2 Kiểm tra chuyển sang task 2 <<<<<")
      now = datetime.datetime.now()
      curTime = now.hour*60 + now.minute
      if tikTopTaskMon.task1_running_flag == "1" and int(tikTopConfig.switch_task2_time) < curTime < int(tikTopConfig.switch_task2_time) + 30:
        runTime = 1
        task2GetComment.updateTaskMonTask1Task2(task1_flag=0,task2_flag=1) #Chuyển sang Task 2
      
#file.close()
    else:
      if tikTopTaskMon.task2_running_flag == "1":
        if os.path.exists("Y:/Post_Vol"+tikTopConfig.vol_num) == False:
          shutil.copytree("Y:/000_Post_Master","Y:/Post_Vol"+tikTopConfig.vol_num)
        logger.info(">>>>> TASK 2 RUNNING <<<<<")
        logger.info("===========================================================================================================")
        logger.info("===== LOOP: "+str(runTime)+" ========================================================================================")
        logger.info("===========================================================================================================")
        watchDogCnt = 0 # Clear watchdog counter mỗi lần chạy
        #   3. Load mẫu thông tin mẫu video từ mySQL:
        #     + Lấy video có thời gian cập nhật là -999 (Nếu hết -999 rồi thì kiểm tra xem còn cái này là CHECKING không? Nếu còn CHECKING thì kiểm tra lại tối đa là 4 lần (CHECKING_RETRY). Quá 4 lần cập nhật trạng thái là "NO_RESPOND".
        #     + Kiểm tra xem còn video vậy không. Nếu không còn thì cập nhật cờ task2_running_flag = 0 và cập nhật task1_running_flag = 1.
        logger.info(">>>>> STEP 3: Load mẫu thông tin mẫu video từ mySQL <<<<<")
        contTask2 = task2GetComment.get999Post() #Lấy video có thời gian cập nhật là -999 (Nếu hết -999 rồi thì kiểm tra xem còn cái này là CHECKING không? và cập nhật bảng Task Monitor (tikTop_task_mon)
        if contTask2 == 0: #Không còn tin 999 hoặc checking
          logger.info("----- Không còn tin 999 hoặc checking -----")
          #task2GetComment.waitAllFinishCHECKING() #Chờ cho tất cả các máy khác hoàn thành CHECKING của nó.
          runTime = 1
          #Cập nhật số thứ tự của Vol mới tại file config
          logger.info("----- Cập nhật số thứ tự của Vol mới tại bảng config -----")
          task2GetComment.updateVolNum()
          #Tạo thư mục lưu trữ Vol mới nếu chưa tồn tại.
          logger.info("----- Tạo thư mục lưu trữ Vol mới nếu chưa tồn tại. -----")
          if os.path.exists("Y:/Post_Vol"+tikTopConfig.vol_num) == False:
            shutil.copytree("Y:/000_Post_Master","Y:/Post_Vol"+tikTopConfig.vol_num)
          #Tạo bảng cho Vol mới
          logger.info("----- Tạo bảng mới cho Vol%s -----",tikTopConfig.vol_num)
          myCursor.execute("create table IF NOT EXISTS tiktop_vol"+str(tikTopConfig.vol_num)+" (id INT AUTO_INCREMENT PRIMARY KEY) select * from tiktop_vol0_master")
          #Cập nhật cờ tại bảng Task Monitor
          logger.info("----- Cập nhật cờ tại bảng Task Monitor -----")
          task2GetComment.updateTaskMonTask1Task2(task1_flag=1,task2_flag=0) #Chuyển công đoạn sang Task1
          task2GetComment.updateTaskMonTask3Task4(task3_flag=1,task4_flag=0) #Chuyển công đoạn sang Task3
          
          ##########################################
          # Chờ Task3 hoàn thành (Cờ Task3 bị xóa) #
          ##########################################
          # while True:
          #   sql = "SELECT * FROM tiktop_task_mon LIMIT 1"
          #   myCursor.execute(sql)
          #   readData = myCursor.fetchall()[0]
          #   if readData['task3_running_flag'] == '1': #Task 3 chưa hoàn thành
          #     delay(10000) #Delay 10 giây
          #   else: #Task3 đã hoàn thành
          #     break
          
        else:
          logger.info("Xử lý item ID: %s",curPostInfo.id)
          # 4. Truy cập video clip.
          #   a. Cập nhật lại điểm Like, Comment, Share.
          #   b. Đếm điểm cười.
          #     - Chụp hình nội dung comment nếu điểm cười lớn hơn điểm cười tối thiểu.
          #     - Nếu đạt điểm (total score) lớn hơn điểm cần có tối thiểu để follow kênh (tiktip_config->follow_min_score) mà kênh chưa được follow thì nhấn follow.
          logger.info(">>>>> STEP 4: Truy cập video clip - GetComment <<<<<")
          
          logger.info(">>>>> STEP 4.a: Cập nhật lại điểm Like, Comment, Share <<<<<")
          
          logger.info("----- Nhập vào URL -----")
          # print(curPostInfo.video_link)
          # curPostInfo.video_link = "https://www.tiktok.com/foryou?is_copy_url=1&is_from_webapp=v1&item_id=6983890608817491227#/@captv93/video/6983890608817491227" # <----------- FORCE
          task1GetLink.openURL(curPostInfo.video_link)
          task1GetLink.openCodeWindow()
          task1GetLink.loginGoogleAccAgain()
          logger.info("----- Thực hiện lọc mã nguồn HTML để bắt dữ liệu và link video -----")
          htmlCode = task1GetLink.getCode()
          logger.info("----- Parsing dữ liệu từ web & Update mySQL -----")
          updateData = task1GetLink.parsingHTML_task2(htmlCode,minPost=1)
          logger.info("like/comment/share: %s/%s/%s",updateData[0],updateData[1],updateData[2])
          if updateData[0] != "" and updateData[1] != "" and updateData[2] != "":
            
            logger.info(">>>>> STEP 4.b: Chụp hình nội dung comment nếu điểm cười lớn hơn điểm cười tối thiểu <<<<<")
            
            logger.info("----- Vào trang comment và đợi load nội dung -----")
            if task2GetComment.goToViewCommentPage() == True: # Đã load xong màn hình comment và các User
              logger.info("----- Chụp hình đoạn comment -----")
              task2GetComment.captureCommentPic()
              task2GetComment.addLogoWaterMarkInComment(alpha=6)
              logger.info("----- Đếm điểm cười và Follow nếu điểm cười đạt điểm ngưỡng. Lưu Video và cập nhật DONE -----")
              task2GetComment.checkFunnyPointEachComment()
              logger.info("DEBUG1")
              task2GetComment.calScoreAndUploadMySQL()
            
          
              
        #---------------------------------------------------------
        task1GetLink.checkHalting(currentVpnWorking,logPicName)
        runTime += 1

    # Thoát chương trình sau 30 lần chạy
    pcRunResetCnt += 1
    logger.info  ("==== NormalVideoDownload: %d ====",task2GetComment.normalVideoDownload)
    if pcRunResetCnt > 30:
      logger.info("==== NORMAL RESET EVERY 30 TIMES RUNNING ====")
      task2GetComment.mySqlCloseConnection()
      exit()
      
    # Thoát chương trình để debug
    # LOOPNUM = 1 #<--------------- USER nhập vào
    # if runTime > LOOPNUM:
    #   logger.info("==== LOOPNUM IS OVER -> EXIT PROGRAM ====")
    #   logger.info("normalVideoDownload: %d",task2GetComment.normalVideoDownload)
    #   exit()
    
except Exception as errMessage:
    logger.debug("!!!! ERROR !!!!")
    logger.error(errMessage)
    # task1GetLink.changeToNewVpnLocation(VPN_NATION,currentVpnWorking)
    GUI.screenshot().save(logPicName+"_ErrorTerminate_"+datetime.datetime.now().strftime("%d%b_%Hh%Mm%S")+".png")
finally:
    GUI.click(270,1064) #Vị trí VSCode
    task2GetComment.mySqlCloseConnection()
    LotusLib.taskKillerEnd()

