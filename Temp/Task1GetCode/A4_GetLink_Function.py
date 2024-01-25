import platform
# import urllib.request
import shutil
import mysql.connector
import re
import datetime
import time
from A1_GetLink_Define import *
from LotusLib_v1r2 import *
import pyperclip
from random import randint
from PIL import Image

pc_name_current = platform.uname()[1]

## Kết nối mySQL ##
myDb = mysql.connector.connect(
  host= MYSQL_IP,
  user= "tiktop_"+pc_name_current,
  password= "",
  database= MYSQL_DB, #Tên cơ sở dữ liệu
  autocommit=True #Tự động cập nhật bảng và dữ liệu đang chạy.
)
myCursor = myDb.cursor(dictionary=True) #=> Xuất dữ liệu dạng dictionary (Giống object)

myDbZalo = mysql.connector.connect(
  host= MYSQL_IP,
  user= 'tiktop_'+pc_name_current,
  password= '',
  database= 'zalo_bot', #Tên cơ sở dữ liệu
  autocommit=True #Tự động cập nhật bảng và dữ liệu đang chạy.
)
myCursorZalo = myDbZalo.cursor(dictionary=True) #=> Xuất dữ liệu dạng dictionary (Giống object)

blacklistUser = []

class devicePC:
  htmlErrCnt = 0 #Đếm số lần chạy lỗi vì không load được HTML
      
class curPostInfo:
  id               = ""
  video_id         = "1234567890"
  org_user         = ""
  cus_user         = ""
  post_date        = ""
  video_link       = DEFAULT_URL
  like_num         = ""
  comment_num      = ""
  share_num        = ""
  funny_num        = ""
  total_score      = ""
  task2_check_time = ""
  created_time     = ""
  Task1_PIC        = ""
  Task2_PIC        = ""
  video_source     = ""
  updated_time     = ""
  checking_retry   = 0
  funContenReport  = ""
  heart_check_flag = 0
  heart_click      = 0
  clip_caption     = ""

class tikTopConfig:
  id = ""
  task1_ena = ""
  task2_ena = ""
  max_hour_post = ""
  hs_like = ""
  hs_comment = ""
  hs_share = ""
  hs_funny = ""
  min_like = ""
  max_like = ""
  min_comment = ""
  max_comment = ""
  min_share = ""
  max_share = ""
  min_funny = ""
  max_funny = ""
  funny1_point = ""
  funny2_point = ""
  funny3_point = ""
  funny4_point = ""
  funny5_point = ""
  funny6_point = ""
  post_every_x_day  = ""
  last_post_day     = ""
  switch_task2_time = ""
  vol_num = ""
  fun_key = ""
  follow_min_score = ""
  download_min_score = ""

class tikTopTaskScheduler:
  id                   = "" # Số UID
  pc_name              = "" # Tên PC thực thiện task
  start_time           = "" # Thời gian bắt đầu
  end_time             = "" # Thời gian kết thúc
  start_action         = "" # Action:
                            #  + py_script: Chạy script python.
                            #  + restart: khởi động lại hệ thống.
                            #  + shutdown: Tắt máy
                            #  + nothing: Không làm gì cả.
  start_action_content = "" # Content ứng với action:
                            #  + py_script: đường dẫn đến file chạy.
                            #  + restart: NUL
                            #  + shutdown: NUL
                            #  + nothing: NUL
  end_action           = "" # Action:
                            #  + py_script: Chạy script python.
                            #  + restart: khởi động lại hệ thống.
                            #  + shutdown: Tắt máy
                            #  + nothing: Không làm gì cả.
  end_action_content   = "" # Content ứng với action:
                            #  + py_script: đường dẫn đến file chạy.
                            #  + restart: NUL
                            #  + shutdown: NUL
                            #  + nothing: NUL
  description          = "" # Mô tả task


class tikTopTaskMon:
  id                 = ""
  task1_running_flag = ""
  task2_running_flag = ""
  task3_running_flag = ""
  task4_running_flag = ""

#Lớp task2CheckCommnetInfo hiển thị thông tin của video sau cùng
class task2CheckCommnetInfo:
  likeFinal = ""
  commentFinal = ""
  shareFinal = ""
  htmlCode = ""
  funnyFinal = ""
  video_size = ""


class Task1GetLink:
  htmlCode = ""
  
  #########################################################
  # Name: openChrome
  # Function: Mở trình duyệt Chrome ở góc trái màn hình và
  #           Maximize cửa sổ.
  # Parameter: None
  # Return: None
  #########################################################
  def openChrome ():
    
    logger.info("--- Mở trình duyệt ---")
    GUI.click(CHROME_POS)  #Click chọn mở Chrome từ taskbar
    logger.info("--- Chờ cửa sổ mở ra và Maximize cửa sổ ---")
    # LotusLib.waitImage("Images/1s.png",5) #Chờ nút của sổ mở ra tối đa 5s. Images/1b.png
    if LotusLib.wait3Color((1600,20),rgb(222,225,230),20,(1919,0),rgb(222,225,230),20,(0,0),rgb(222,225,230),20,10,DELAY100MS) == False: #Cửa sổ đang chuaw được Maximize
      LotusLib.delay(100)
      GUI.hotkey('alt','space') # Gọi bảng điều khiển cửa sổ.
      LotusLib.delay(600) #đợi 600ms
      GUI.press('x') #Maximize the window
      LotusLib.delay(1000) #đợi 600ms
      LotusLib.wait3Color((1600,20),rgb(222,225,230),20,(1919,0),rgb(222,225,230),20,(0,0),rgb(222,225,230),20,10,DELAY100MS) #Chờ cửa sổ maximize
    LotusLib.delay(1000) #đợi 1000ms
    GUI.click(1902,72)  #Click đóng cửa sổ yêu cầu phục hồi các task cũ
    

  #########################################################
  # Name: openURLWithoutWait
  # Function: Mở đường dẫn đến URL và không đợi trang load xong
  # Parameter: None
  # Return: None
  #########################################################
  def openURLWithoutWait(urlLink = curPostInfo.video_link):
    
    URL_LINK = urlLink
    logger.info("--- Truy cập URL: %s",URL_LINK)
    for i in range(0,8):
      logger.debug("--- Tắt các cửa sổ không cần thiết ---")
      if LotusLib.checkColorWithCapture((470,16),rgb(60,64,66),20):
        GUI.click(472,16) # Nhấn nút đóng các Tab thừa của Chrome.
        LotusLib.delay(1000)
      else:
        break
    GUI.click(ADDR_BAR)
    LotusLib.delay(500)
    GUI.hotkey('ctrl','a') #Chọn hết đường dẫn
    logger.debug("--- Nhập đường dẫn URL vào ---")
    pyperclip.copy(URL_LINK) #Copy nội dung tin nhắn vào clipboard
    LotusLib.delay(50)
    pyperclip.copy(URL_LINK) #Copy nội dung tin nhắn vào clipboard
    LotusLib.delay(50)
    pyperclip.copy(URL_LINK) #Copy nội dung tin nhắn vào clipboard
    LotusLib.delay(200)
    GUI.hotkey('ctrl','v') #Dán nội dung vào cửa sổ chat
    LotusLib.delay(500)
    GUI.press('enter')
    LotusLib.delay(500)
    GUI.click(ADDR_BAR)
    LotusLib.delay(500)
    GUI.press('enter')
    # LotusLib.wait3NotColor([22,11],rgb(6,6,6),20,[33,22],rgb(6,6,6),20,[16,20],rgb(255,255,255),20,90,DELAY100MS) #(Images/5s.png) Chờ Favicon thay đổi. Tối đa 90 giây. 
    
    
  #########################################################
  # Name: openURL
  # Function: Mở đường dẫn đến file video mặc định của meomay22
  # Parameter: None
  # Return: None
  #########################################################
  def openURL(urlLink):
    
    logger.info("--- Truy cập URL: %s",urlLink)
    for i in range(0,8):
      logger.debug("--- Tắt các cửa sổ không cần thiết ---")
      if LotusLib.checkColorWithCapture((470,16),rgb(60,64,66),20):
        GUI.click(472,16) # Nhấn nút đóng các Tab thừa của Chrome.
        LotusLib.delay(1000)
      else:
        break
    GUI.click(ADDR_BAR)
    LotusLib.delay(500)
    GUI.hotkey('ctrl','a') #Chọn hết đường dẫn
    logger.debug("--- Nhập đường dẫn URL vào ---")
    pyperclip.copy(urlLink) #Copy nội dung tin nhắn vào clipboard
    LotusLib.delay(50)
    pyperclip.copy(urlLink) #Copy nội dung tin nhắn vào clipboard
    LotusLib.delay(50)
    pyperclip.copy(urlLink) #Copy nội dung tin nhắn vào clipboard
    LotusLib.delay(200)
    GUI.hotkey('ctrl','v') #Dán nội dung vào cửa sổ chat
    LotusLib.delay(500)
    GUI.press('enter')
    LotusLib.delay(500)
    GUI.click(ADDR_BAR)
    LotusLib.delay(500)
    GUI.press('enter')
    LotusLib.wait3NotColor([22,11],rgb(6,6,6),20,[33,22],rgb(6,6,6),20,[16,20],rgb(255,255,255),20,2,DELAY100MS) #(Images/5s.png) Chờ Favicon thay đổi. Tối đa 90 giây. 
    # Kiểm tra đã load xong trang chưa
    i = 0
    while i < 90: #Chờ tối đa 1.5 phút
      i += 1 #Tăng biến đếm i
      if LotusLib.checkColorWithCapture([22,11],rgb(6,6,6),20,0) and \
         LotusLib.checkColorWithCapture([33,22],rgb(6,6,6),20,0) and \
         LotusLib.checkColorWithCapture([16,20],rgb(255,255,255),20,0) : # Đã load xong Favicon
        LotusLib.delay(500)
        break
      else:
        if LotusLib.checkColorWithCapture([666,560],rgb(26,115,232),5,0): # Màu rgb(26,115,232)
          GUI.click(666,560) # Images/34s.png  Click nút "Tải lại"s
        if LotusLib.checkColorWithCapture([720,570],rgb(26,115,232),5,0): # Màu rgb(26,115,232)
          GUI.click(720,570) # Images/34s.png  Click nút "Tải lại"
        if LotusLib.checkColorWithCapture([380,580],rgb(26,115,232),5,0): # Màu rgb(26,115,232)
          GUI.click(380,580) # Images/34s.png  Click nút "Tải lại"
        LotusLib.delay(500)
    

  #########################################################
  # Name: scrollLoadHTMLCode
  # Function: Cuộn nhấn pagedown 60 lần trong 30 giây để
  #           để load hết nội dung HTML.
  # Parameter: None
  # Return: None
  #########################################################
  def scrollLoadHTMLCode():
    
    GUI.click(15,120)
    for i in range(0,60):
      GUI.press("pagedown")
      LotusLib.delay(500)
    

  #########################################################
  # Name: openCodeWindow
  # Function: Kiểm tra và mở của sổ xem code.
  # Parameter: None
  # Return: None
  #########################################################
  def openCodeWindow():
    
    codeWindowColor = LotusLib.getColor(1836,114) # Images/6s.png vị trí số 1. Màu (243,243,243)
    if        codeWindowColor[0] <= 250 and\
              codeWindowColor[1] <= 250 and\
              codeWindowColor[2] <= 250 :
      LotusLib.delay(100)
    else:
      logger.info("--- Mở cửa sổ xem code ---")
      # Mở cửa sổ xem code
      GUI.hotkey('ctrl','shift','i') # Mở cửa sổ xem code
      LotusLib.delay(2000)
      LotusLib.waitColor([1836,114],rgb(243,243,243),5,60) # Images/33s.png số 1. Đợi cửa sổ code hiện ra
      LotusLib.delay(100)
      LotusLib.waitColor([1911,160],rgb(193,193,193),20,60) # Images/33s.png số 2. Đợi code được load xong
      LotusLib.delay(100) # Images/3b.png
    
    
  def loginGoogleAccAgain():
    
    if LotusLib.checkColorWithCapture((1108,121),rgb(254,44,85),10,1000) == True: # Images/54s.png .Nếu chưa đăng nhập.
      GUI.click(1108,121)
      LotusLib.waitColor((530,495),rgb(24,119,242),10,15,1000) # Images/55s.png (1). Dợi Icon Facebook hiện ra.
      GUI.click(684,557) # Images/55s.png (2). Click vào nút đăng nhập bằng Google.
      LotusLib.waitColor((957,404),rgb(32,12,28),20,15,1000) # Images/56b.png (1)
      GUI.click(965,572) # Images/56b.png (2)
      LotusLib.delay(15000)
    


  #########################################################
  # Name: getCode
  # Function: Kiểm tra mở của sổ xem code và load hết code
  #           rồi trả về code HTML
  # Parameter: None
  # Return: Trả về htmlCode dạng string
  #########################################################
  def getCode():
    GUI.click(1451,116) #Click vào tab Element. Images/7s.png
    LotusLib.delay(500)
    GUI.moveTo(1830,200) #Di chuyển chuột vào vùng code có thể cuộn chuột được.
    delay(200)
    GUI.scroll(2000) #Scroll lên trên cùng
    delay(500)
    logger.info("--- Mở ra cửa sổ copy element ---")
    GUI.click(1400,140) #Click vào vị trí thẻ <!DOCUMENT html>.
    LotusLib.waitColor((1700,140),rgb(207,232,252),20,15,0) # đợi dòng được chọn
    LotusLib.delay(300)
    GUI.press('down') #Xuống thẻ <html>
    LotusLib.delay(500)
    #Collapse children
    GUI.hotkey('shift','f10') # Images/58s.png Mở bẳng dropbox
    LotusLib.delay(1000)
    GUI.press('c')
    LotusLib.delay(500)
    GUI.press('c') 
    LotusLib.delay(500)
    GUI.press('c')
    LotusLib.delay(500)
    GUI.press('enter') #Chọn dòng Collapse children
    LotusLib.delay(1000)
    GUI.press('esc') # Images/58s.png .Thoát bảng dropbox nếu nó không tự tắt
    LotusLib.delay(500)
    #Copy nội dung html body
    GUI.press('down')
    LotusLib.delay(500)
    GUI.press('down')
    LotusLib.delay(500)
    GUI.hotkey('shift','f10') # Images/58s.png Mở bẳng dropbox
    LotusLib.delay(1000)
    GUI.press('c')
    LotusLib.delay(500)
    GUI.press('c')
    LotusLib.delay(500)
    GUI.press('enter')
    LotusLib.delay(500)
    GUI.press('enter') #Chọn "copy element"
    LotusLib.delay(500)
    GUI.press('up') #Tránh màn hình bị xanh do đang chọn code
    LotusLib.delay(1000)
    htmlCode = pyperclip.paste() #Gán html code từ clipboard vào biến
    htmlCode = htmlCode.replace('\n',' ')
    
    return htmlCode


  ## Kiểm tra trạng thái hoạt động của PC từ task scheduler ##
  # 1. Load Task Scheduler từ MySQL về.
  # 2. Kiểm tra và chọn một task scheduler ưu tiền từ trên xuống dưới
  # 3. Trả về các dạng kết quả:
  #      + "script" : Nếu đang trong khung thời gian Task Scheduler cài đặt.
  #      + "xx:xx"  : Nếu thời gian hiện tại không nằm trong khung thời gian nào thì
  #                   trả về thời gian dạng hh:mm cần đợi đến khung thời gian kế.
  def checkCurrentTaskScheduler():
    
    pc_name_current = platform.uname()[1]
    # logger.info("DEBUG: pc_name_current: %s\n",pc_name_current)
    #1. Load Task Scheduler từ MySQL về.
    sql = "SELECT * from tiktop_taskscheduler"
    myCursor.execute(sql)
    taskSchedulerArray = myCursor.fetchall()

    start_action         = ""
    start_action_content = ""
    end_action           = ""
    end_action_content   = ""
    procState = 'Out Schedule'
    waitNextSchedule_sec = 86400 #Thời gian chờ đến Task schedule tiếp theo
    
    #Tìm pc_name với tất cả các dòng của bảng Task Scheduler
    for i in range (0,len(taskSchedulerArray)):
      pc_name_mysql = taskSchedulerArray[i]['pc_name'];
      # logger.info("DEBUG: pc_name_mysql: %s\n",pc_name_mysql)
      patternRegex = re.compile(pc_name_mysql)
      compareMatch = patternRegex.search(pc_name_current) != None #Nếu match -> True

      # Kiểm tra khung thời gian khi tên pc_name đã khớp
      if compareMatch == True:
        start_time = str(taskSchedulerArray[i]['start_time'])
        end_time   = str(taskSchedulerArray[i]['end_time'])
        cur_time  = datetime.datetime.now().strftime("%H:%M") #Lấy thời gian hiện tại dạng hh:mm:ss
        
        #Chuyển đổi ra giây
        start_time = re.sub(r'0(\d)',r'\1',start_time)
        end_time   = re.sub(r'0(\d)',r'\1',end_time)
        cur_time   = re.sub(r'0(\d)',r'\1',cur_time)
        start_time = start_time.replace(":", '*60+')
        end_time   =   end_time.replace(":", '*60+')
        cur_time   =   cur_time.replace(":", '*60+')
        
        start_time_sec = eval('('+start_time+')*60') # Đổi sang giây
        end_time_sec   = eval('('+  end_time+')*60') # Đổi sang giây
        cur_time_sec   = eval('('+  cur_time+')*60') # Đổi sang giây
        # logger.info("DEBUG: start_time_sec: %d\n",start_time_sec)
        # logger.info("DEBUG: end_time_sec  : %d\n",end_time_sec)
        # logger.info("DEBUG: cur_time_sec  : %d\n",cur_time_sec)
        
        if start_time_sec <= cur_time_sec <= end_time_sec: #Khung thời gian không bao gồm móc 0h.
          procState = 'In Schedule'
        elif (start_time_sec > end_time_sec) and ((start_time_sec <= cur_time_sec) or (cur_time_sec <= end_time_sec)): #Khu thời gian chứa cả móc 0h
          procState = 'In Schedule'
        else: #Không thuộc khung thời gian xử lý
          procState = 'Out Schedule'
      
        if procState == 'In Schedule':
          start_action         = str(taskSchedulerArray[i]['start_action'])
          start_action_content = str(taskSchedulerArray[i]['start_action_content'])
          end_action           = str(taskSchedulerArray[i]['end_action'])
          end_action_content   = str(taskSchedulerArray[i]['end_action_content'])
          waitNextSchedule_sec = 0 #No need to wait in state "In Schedule"
          break #Thoát khỏi vòng lặp For nếu tìm được 1 In Schedule đầu tiên.
          
        if procState == 'Out Schedule':
          #Tính thời gian chờ đối với dòng task schedule đang check
          if cur_time_sec <= start_time_sec:
            waitNextSchedule_chk = start_time_sec - cur_time_sec;
          else:
            waitNextSchedule_chk = start_time_sec - cur_time_sec + 86400;
          #Cập nhật để lấy thời gian chờ đến task schedule gần nhất
          if waitNextSchedule_chk < waitNextSchedule_sec:
            waitNextSchedule_sec = waitNextSchedule_chk
            start_action         = str(taskSchedulerArray[i]['start_action'])
            start_action_content = str(taskSchedulerArray[i]['start_action_content'])
            end_action           = str(taskSchedulerArray[i]['end_action'])
            end_action_content   = str(taskSchedulerArray[i]['end_action_content'])
    
    return [procState,waitNextSchedule_sec,start_action,start_action_content,end_action,end_action_content]
    
    
  #########################################################
  # Name: loadMysqlConf
  # Function: Đọc về nôi dung của bảng config từ MySQL
  # Parameter: None
  # Return: None
  #########################################################
  def loadMysqlConf():
    
    sql = "SELECT * from tiktop_config"
    myCursor.execute(sql)
    configData = myCursor.fetchall()[0] #Fetch là lấy dòng đầu tiên
    if configData == "":
      logger.fatal("%s!!! ERROR !!!. Không kết nối được với MySQL")
      exit();
    logger.debug("%Chuỗi config đọc về từ mySQL:")
    logger.debug(configData)
    tikTopConfig.id                 = configData['id']
    tikTopConfig.task1_ena          = configData['task1_ena']
    tikTopConfig.task2_ena          = configData['task2_ena']
    tikTopConfig.max_hour_post      = configData['max_hour_post']
    tikTopConfig.hs_like            = configData['hs_like']
    tikTopConfig.hs_comment         = configData['hs_comment']
    tikTopConfig.hs_share           = configData['hs_share']
    tikTopConfig.hs_funny           = configData['hs_funny']
    tikTopConfig.min_like           = configData['min_like']
    tikTopConfig.max_like           = configData['max_like']
    tikTopConfig.min_comment        = configData['min_comment']
    tikTopConfig.max_comment        = configData['max_comment']
    tikTopConfig.min_share          = configData['min_share']
    tikTopConfig.max_share          = configData['max_share']
    tikTopConfig.min_funny          = configData['min_funny']
    tikTopConfig.max_funny          = configData['max_funny']
    tikTopConfig.funny1_point       = configData['funny1_point']
    tikTopConfig.funny2_point       = configData['funny2_point']
    tikTopConfig.funny3_point       = configData['funny3_point']
    tikTopConfig.funny4_point       = configData['funny4_point']
    tikTopConfig.funny5_point       = configData['funny5_point']
    tikTopConfig.funny6_point       = configData['funny6_point']
    tikTopConfig.post_every_x_day   = configData['post_every_x_day']
    tikTopConfig.last_post_day      = configData['last_post_day']
    tikTopConfig.switch_task2_time  = configData['switch_task2_time']
    tikTopConfig.vol_num            = configData['vol_num']
    tikTopConfig.fun_key            = configData['fun_key']
    tikTopConfig.follow_min_score   = configData['follow_min_score']
    tikTopConfig.download_min_score = configData['download_min_score']
    

  #########################################################
  # Name: loadMysqlTaskMon
  # Function: Đọc về nôi dung của bảng task monitor từ MySQL
  # Parameter: None
  # Return: None
  #########################################################
  def loadMysqlTaskMon():
    
    sql = "SELECT * from tiktop_task_mon"
    myCursor.execute(sql)
    readData = myCursor.fetchall()[0] #Fetch là lấy dòng đầu tiên
    if readData == "":
      logger.fatal("!!! ERROR !!!. Không kết nối được với MySQL")
      exit(); ##-> Reset lại máy VPS
    logger.debug("Chuỗi Task Monitor đọc về từ mySQL:")
    logger.debug(readData)
    tikTopTaskMon.id                 = readData['id']
    tikTopTaskMon.task1_running_flag = readData['task1_running_flag']
    tikTopTaskMon.task2_running_flag = readData['task2_running_flag']
    tikTopTaskMon.task3_running_flag = readData['task3_running_flag']
    tikTopTaskMon.task4_running_flag = readData['task4_running_flag']
    

  #########################################################
  # Name: loadMysqlBlacklist
  # Function: Đọc về nôi dung của bảng blacklist từ MySQL
  # Parameter: None
  # Return: None
  #########################################################
  def loadMysqlBlacklist():
    
    global blacklistUser
    sql = "SELECT * from tiktop_blacklist"
    myCursor.execute(sql)
    blacklistMysql = myCursor.fetchall()
    for i in range (0,len(blacklistMysql)):
      blacklistUser.append(blacklistMysql[i]['user_uid'])
    logger.debug("Blacklist: %s",blacklistUser)
    

  #########################################################
  # Name: loadMysqlFollowList
  # Function: Load danh sách các user đang theo dõi
  # Parameter: add_type = manual/script. Loại user được theo dõi.
  # Return: followList
  #########################################################
  def loadMysqlFollowList(add_type="manual"):
    
    followList = []
    sql = "SELECT * from tiktop_follow_list WHERE add_type = '"+add_type+"'"
    myCursor.execute(sql)
    followUser = myCursor.fetchall()
    for i in range (0,len(followUser)):
      followList.append(followUser[i]['org_user'])
    logger.debug("Follow List: %s",followList)
    
    return followList
    
  #########################################################
  # Name: parsingHTML_task1
  # Function: Tách dữ liệu từ code HTML nhập vào để tìm
  #           ra các thông tin cần thiết (Like, comment, share...)
  # Parameter:
  #  + htmlCode: Mã HTML code đầu vào.
  #  + minPost: Xác định số lượng clip post tối thiểu để chấp nhận
  #             code HTML đó.
  #  + debug: Cho chạy và in ở chế độ debug hoặc không in.
  # Return: None
  #########################################################
  def parsingHTML_task1 (htmlCode,minPost,followList,debug=0):
    
    # TỪ KHÓA: <h3 class="author-uniqueId jsx-2620806822" style="text-decoration: none;">hieuhoang20052005</h3></a><a href=
    # TỪ KHÓA: <strong title="like" class="jsx-1045706868 bar-item-text engagement-text-v23">8696</strong>
    # TỪ KHÓA: <strong title="comment" class="jsx-1045706868 bar-item-text engagement-text-v23">8696</strong>
    # TỪ KHÓA: <strong title="share" class="jsx-1045706868 bar-item-text engagement-text-v23">8696</strong>
    # TỪ KHÓA: <a href="https://www.tiktok.com/@vsorl0602/video/6891932365128600834" class="jsx-179939359 jsx-2715883145 item-video-card-wrapper">
    str(htmlCode)
    postPortionHTML = htmlCode.split('video-feed-item')
    numPost = len(postPortionHTML) - 1 #Bỏ 1 phần tử đầu và 1 phần tử cuối
    if debug == 1: print("DEBUG: numPost = ",numPost) #DEBUG1
    if numPost >= minPost: #Có video post cần lấy
      for i in range(1,numPost):
        logger.debug("")
        logger.debug("===== Parsing video post: "+str(i)+" =====")
        htmlParsing0 = postPortionHTML[i]
        # Check valid Post
        curPostInfo.post_date = re.sub(r'.*?author-nickname.*?span>(.*?)<.*',r'\1',htmlParsing0).strip() # ".*?" mean as few as possible
        postTimeRecord    = LotusLib.convertToHour(curPostInfo.post_date)
        if curPostInfo.post_date == "":
          logger.error("LOI POST DATE: "+curPostInfo.post_date)
          exit()
        # Kiểm tra và gửi Zalo nếu user thuộc danh sách follow và mới post chưa đầy 1h đồng hồ
        if postTimeRecord == 0:
          #Clip mới Post
          curPostInfo.org_user = re.sub(r'.*?author-uniqueId.*?\>(.*?)<.*',r'\1',htmlParsing0).strip() # ".*?" mean as few as possible
          if curPostInfo.org_user in followList:
            curPostInfo.video_link = re.sub(r'.*(www.tiktok.com/.*?)".*',r'\1',htmlParsing0).strip() # ".*?" mean as few as possible
            curPostInfo.video_id = curPostInfo.video_link.split("/video/")[1]
            curPostInfo.like_num = re.sub(r'.*?title="like">(.*?)<.*',r'\1',htmlParsing0).strip() # ".*?" mean as few as possible
            curPostInfo.comment_num = re.sub(r'.*?title="comment">(.*?)<.*',r'\1',htmlParsing0).strip() # ".*?" mean as few as possible
            curPostInfo.share_num = re.sub(r'.*?title="share">(.*?)<.*',r'\1',htmlParsing0).strip() # ".*?" mean as few as possible
            #Gửi Zalo
            sql = "SELECT * FROM tiktop_follow_new_post_send WHERE video_id ='"+curPostInfo.video_id+"' LIMIT 1"
            myCursor.execute(sql)
            checkLastSent = myCursor.fetchall()
            
            if len(checkLastSent) == 0: #Nếu trước đó video chưa được gửi thì gửi.
              message = f"""===== New Post =====
  {curPostInfo.video_link}
  + Post: {curPostInfo.post_date}
  + User: {curPostInfo.org_user}
  + Like/Comment/Share:
  {curPostInfo.like_num} / {curPostInfo.comment_num} / {curPostInfo.share_num}
  """
              Task2GetComment.sendToTxBufferQueue(send_to='0908549354',mess_type='text',mess_data=message,send_delay_sec=0,note='New Post (one hour)')
              # Đưa vào bảng MySQL danh sách gửi Zalo không trùng lập tiktop_follow_new_post_send
              sql = "INSERT INTO tiktop_follow_new_post_send (id,video_id) VALUES (%s,%s)"
              val = ("",curPostInfo.video_id)
              myCursor.execute(sql, val)
              myDb.commit()
            
        if postTimeRecord > int(tikTopConfig.max_hour_post):
          logger.info("==> Discard due to date: %s > max hour post",curPostInfo.post_date)
          continue
        # Check valid Share
        curPostInfo.share_num = re.sub(r'.*?title="share">(.*?)<.*',r'\1',htmlParsing0).strip() # ".*?" mean as few as possible
        postShareRecord   = LotusLib.convertHumanNumToInt(curPostInfo.share_num)
        if postShareRecord < int(tikTopConfig.min_share):
          logger.info("==> Discard due to Share: %s < min_share",curPostInfo.share_num)
          continue
        # Check valid Comment
        curPostInfo.comment_num = re.sub(r'.*?title="comment">(.*?)<.*',r'\1',htmlParsing0).strip() # ".*?" mean as few as possible
        postCommentRecord = LotusLib.convertHumanNumToInt(curPostInfo.comment_num)
        if postCommentRecord < int(tikTopConfig.min_comment):
          logger.info("==> Discard due to Comment: %s < min_comment",curPostInfo.comment_num)
          continue
        # Check valid Like
        curPostInfo.like_num = re.sub(r'.*?title="like">(.*?)<.*',r'\1',htmlParsing0).strip() # ".*?" mean as few as possible
        postLikeRecord    = LotusLib.convertHumanNumToInt(curPostInfo.like_num)
        if postLikeRecord < int(tikTopConfig.min_like):
          logger.info("==> Discard due to Like: %s < min_like",curPostInfo.like_num)
          continue
        
        # 2. Split by END String of keywords
        curPostInfo.org_user = re.sub(r'.*?author-uniqueId.*?\>(.*?)<.*',r'\1',htmlParsing0).strip() # ".*?" mean as few as possible
        logger.info("+ Tên Uniq User: "+str(curPostInfo.org_user))
        curPostInfo.cus_user = re.sub(r'.*?author-nickname.*?>(.*?)<.*',r'\1',htmlParsing0).strip() # ".*?" mean as few as possible
        logger.info("+ Tên Custom User: "+str(curPostInfo.cus_user))
        logger.info("+ Ngày post: "+str(curPostInfo.post_date))
        logger.info("+ Like num: "+str(curPostInfo.like_num))
        logger.info("+ Comment num: "+str(curPostInfo.comment_num))
        logger.info("+ Share num: "+str(curPostInfo.share_num))

        curPostInfo.video_link = re.sub(r'.*(www.tiktok.com/.*?)".*',r'\1',htmlParsing0).strip() # ".*?" mean as few as possible
        logger.info("+ Video link: "+str(curPostInfo.video_link))
        # logger.info("\n\n DEBUG:\n%s\n\n",htmlParsing0) #<------------- DEBUG
        
        curPostInfo.video_id = curPostInfo.video_link.split("/video/")[1]
        logger.info("+ VideoID: "+str(curPostInfo.video_id))
        
        # Get Task1 PIC
        curPostInfo.Task1_PIC = platform.uname()[1]

        # Get clip caption
        if "video-meta-caption" in htmlParsing0:
          curPostInfo.clip_caption = re.sub(r'.*video-meta-caption.*?<strong>(.*?)</strong>.*".*',r'\1',htmlParsing0).strip() # ".*?" mean as few as possible
          logger.info("+ Caption: "+str(curPostInfo.clip_caption))
          if ("Reply to" in curPostInfo.clip_caption) or \
             ("Trả lời"  in curPostInfo.clip_caption) or \
             ("#"        in curPostInfo.clip_caption) or \
             ("@"        in curPostInfo.clip_caption) :
            curPostInfo.clip_caption = ""
        else:
          curPostInfo.clip_caption = ""
            
        logger.debug("--- Kiểm tra User trong danh sách Blacklist ---")
        # logger.info("Org User: %s, Blacklist: %s",curPostInfo.org_user,blacklistUser)
        if curPostInfo.org_user in blacklistUser:
          logger.debug("!!! USER thuộc blacklist -> Bỏ qua !!!")
        else:
          logger.info("--- Cập nhật dòng dữ liệu lên MySQL ---")
          Task1GetLink.updateMysql()
      devicePC.htmlErrCnt = 0 #Xóa biến báo lỗi treo chương trình
    else: #Chương trình bị treo -> Thoát
      devicePC.htmlErrCnt += 1 #Cộng lỗi vào biến.
    
    return curPostInfo.like_num,curPostInfo.comment_num,curPostInfo.share_num
  
  #########################################################
  # Name: parsingHTML_task2
  # Function: Tách dữ liệu từ code HTML nhập vào để tìm
  #           ra các thông tin cần thiết (Like, comment, share...)
  # Parameter:
  #  + htmlCode: Mã HTML code đầu vào.
  #  + minPost: Xác định số lượng clip post tối thiểu để chấp nhận
  #             code HTML đó.
  #  + debug: Cho chạy và in ở chế độ debug hoặc không in.
  # Return: None
  #########################################################
  def parsingHTML_task2 (htmlCode,minPost,debug=0):
    # TỪ KHÓA: <h3 class="author-uniqueId jsx-2620806822" style="text-decoration: none;">hieuhoang20052005</h3></a><a href=
    # TỪ KHÓA: <strong title="like" class="jsx-1045706868 bar-item-text engagement-text-v23">8696</strong>
    # TỪ KHÓA: <strong title="comment" class="jsx-1045706868 bar-item-text engagement-text-v23">8696</strong>
    # TỪ KHÓA: <strong title="share" class="jsx-1045706868 bar-item-text engagement-text-v23">8696</strong>
    # TỪ KHÓA: <a href="https://www.tiktok.com/@vsorl0602/video/6891932365128600834" class="jsx-179939359 jsx-2715883145 item-video-card-wrapper">
    str(htmlCode)
    curPostInfo.video_source = ""
    postPortionHTML = htmlCode.split('video-feed-item')
    numPost = len(postPortionHTML) - 1 #Bỏ 1 phần tử đầu và 1 phần tử cuối
    if debug == 1: print("DEBUG: numPost = ",numPost) #DEBUG1
    if numPost >= minPost: #Có video post cần lấy
      logger.debug("\n===== Parsing video post: 1 =====")
      htmlParsing0 = postPortionHTML[1]
      
      # Check valid Like
      curPostInfo.like_num = re.sub(r'.*?title="like">(.*?)<.*',r'\1',htmlParsing0).strip() # ".*?" mean as few as possible
      logger.info("+ Like num: "+str(curPostInfo.like_num))
      ## Check valid Comment
      curPostInfo.comment_num = re.sub(r'.*?title="comment">(.*?)<.*',r'\1',htmlParsing0).strip() # ".*?" mean as few as possible
      logger.info("+ Comment num: "+str(curPostInfo.comment_num))
      # Check valid Share
      curPostInfo.share_num = re.sub(r'.*?title="share">(.*?)<.*',r'\1',htmlParsing0).strip() # ".*?" mean as few as possible
      logger.info("+ Share num: "+str(curPostInfo.share_num))
      
      # Nếu là task2 đang chạy sẽ có thêm phần video source
      videoSourceRaw = re.sub(r'.*?<video authorid.*?src="(.*?)".*',r'\1',htmlParsing0).strip() # ".*?" mean as few as possible
      curPostInfo.video_source = videoSourceRaw.replace('&amp;','&')
      logger.info("+ Video Source: "+str(curPostInfo.video_source))
      
      Task1GetLink.updateMysql_getComment_likeShare()
      devicePC.htmlErrCnt = 0 #Xóa biến báo lỗi treo chương trình
    else: #Chương trình bị treo -> Thoát
      devicePC.htmlErrCnt += 1 #Cộng lỗi vào biến.
    
    return curPostInfo.like_num,curPostInfo.comment_num,curPostInfo.share_num
  
  #########################################################
  # Name: checkHalting
  # Function: Kiểm tra chương trình có bị lỗi. Nếu lỗi 3 lần
  #           liên tiếp thì thoát khỏi chương trình
  # Parameter: None
  # Return: None
  #########################################################
  def checkHalting(currentVpnWorking,logPicName):
    
    if devicePC.htmlErrCnt >= 1:
      logger.error("#######################################################")
      logger.error("#### LỖI KHÔNG BẮT ĐƯỢC HTML CODE. LẦN: "+str(devicePC.htmlErrCnt)+" #############")
      logger.error("#######################################################")
    if devicePC.htmlErrCnt >= 3:
      logger.fatal("################# HỆ THỐNG SHUTDOWN ###################")
      # Task1GetLink.changeToNewVpnLocation(VPN_NATION,currentVpnWorking)
      GUI.screenshot().save(logPicName+"_ErrorTerminate_"+datetime.datetime.now().strftime("%d%b_%Hh%Mm%S")+".png")
      
      exit() #Thoát khỏi chương trình
    

  #########################################################
  # Name: updateMysql
  # Function: Cập nhật thông tin của clip lên MySQL. Nếu Chưa
  #           có thì tạo dòng dữ liệu mới.
  # Parameter: None
  # Return: None
  #########################################################
  def updateMysql():
    
    ### ĐẨY DATA lên mySQL ###
    #a. Kiểm tra điều kiện đây lên mySQL
    postTimeRecord    = LotusLib.convertToHour(curPostInfo.post_date)
    postLikeRecord    = LotusLib.convertHumanNumToInt(curPostInfo.like_num)
    postCommentRecord = LotusLib.convertHumanNumToInt(curPostInfo.comment_num)
    postShareRecord   = LotusLib.convertHumanNumToInt(curPostInfo.share_num)
    
    if postTimeRecord   <  int(tikTopConfig.max_hour_post) and \
      postLikeRecord    >= int(tikTopConfig.min_like) and \
      postCommentRecord >= int(tikTopConfig.min_comment) and \
      postShareRecord   >= int(tikTopConfig.min_share):
      # Chỉ cập nhật dữ liệu mySQL nếu thỏa tất cả điều kiện ở trên
      #b. Cập nhật dữ liệu. Nếu chưa tồn tại thì tạo thêm mới
      sql = "SELECT * from tiktop_vol"+str(tikTopConfig.vol_num)+" WHERE video_id = "+str(curPostInfo.video_id)+""
      myCursor.execute(sql)
      myCursor.fetchall()
  
      if myCursor.rowcount == 0: #Chưa có dữ liệu -> Thêm dữ liệu mới
        sql = "INSERT INTO tiktop_vol"+str(tikTopConfig.vol_num)+" (video_id,org_user,cus_user,post_date,video_link,like_num,comment_num,share_num,task2_check_time,Task1_PIC,clip_caption) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (curPostInfo.video_id,curPostInfo.org_user,curPostInfo.cus_user,curPostInfo.post_date,curPostInfo.video_link,curPostInfo.like_num,curPostInfo.comment_num,curPostInfo.share_num,"-999",curPostInfo.Task1_PIC,curPostInfo.clip_caption)
        myCursor.execute(sql, val)
        myDb.commit()
        logger.debug("*** MYSQL NEW ***")
      else: # Đã có thông tin dữ liệu -> Cập nhật dữ liệu    
        sql = "UPDATE tiktop_vol"+str(tikTopConfig.vol_num)+" SET updated_time = %s, post_date = %s,like_num = %s,comment_num = %s,share_num = %s,Task1_PIC = %s, clip_caption = %s WHERE video_id = "+str(curPostInfo.video_id)+""
        val = (LotusLib.getCurTime(),curPostInfo.post_date,curPostInfo.like_num,curPostInfo.comment_num,curPostInfo.share_num,curPostInfo.Task1_PIC,curPostInfo.clip_caption)
        myCursor.execute(sql, val)
        myDb.commit()
        logger.debug("*** MYSQL UPDATE ***")
      logger.debug("*** PostTime: %s, Like = %s, Comment = %s,Share = %s ***",postTimeRecord,postLikeRecord,postCommentRecord,postShareRecord)
    
    
  #########################################################
  # Name: updateMysql_getComment_likeShare
  # Function: Cập nhật thông tin của clip lên MySQL.
  # Parameter: None
  # Return: None
  #########################################################
  def updateMysql_getComment_likeShare():
    
    sql = "UPDATE tiktop_vol"+str(tikTopConfig.vol_num)+" SET like_num = %s,comment_num = %s,share_num = %s WHERE video_id = "+str(curPostInfo.video_id)+""
    val = (curPostInfo.like_num,curPostInfo.comment_num,curPostInfo.share_num)
    myCursor.execute(sql, val)
    myDb.commit()
    
      
  #########################################################
  # Name: taskSchedulerChecking
  # Function: Kiểm tra thời gian hoạt động của máy dựa 
  #           theo bảng Task Scheduler
  # Parameter: taskScheduleRunning
  # Return: None
  #########################################################
  def taskSchedulerChecking(taskScheduleRunning=0):
    
    #Kiểm tra thời gian hoạt động của máy dựa theo bảng Task Scheduler
    arr = Task1GetLink.checkCurrentTaskScheduler()
    if arr[0] == 'Out Schedule':
      #Khởi động lại nếu trước đó đang chạy task mà hết khoảng thời gian chạy
      if taskScheduleRunning == 1:
        logger.info(">>>> OUT SCHEDULE ===> RESTART!!!")
        exit() 
      # Đóng cửa sổ trình duyệt đang mở
      GUI.click(1900,15) #Vị trí nút đóng Chrome
      LotusLib.delay(1000)
      while arr[1] - 60 >= 0:
        time_min = int(arr[1])/60
        remain_hour = int(time_min/60)
        remain_min = int(time_min%60)
        if remain_hour > 0:
          print('Out Schedule => Hệ thống sẽ thức dậy sau '+str(remain_hour)+' giờ '+str(remain_min)+' phút nữa\n');
        else:
          print('Out Schedule => Hệ thống sẽ thức dậy sau '+str(remain_min)+' phút nữa\n');
        time.sleep(60) #Ngủ 60 giây
        arr[1] -=60 #Giảm 60 giây
      
      exit() #Exit chương trình và khởi động lại
    


  #########################################################
  # Name:   def surfSharkVPN(location):
  # Function: Kiểm tra và đăng nhập vào SurfSharkVPN
  # Parameter: location: Tên quốc gia muốn chuyển vùng
  # Return: None
  #########################################################
  def connectVpn(country):
    
    sql = "SELECT * FROM tiktop_config_vpn WHERE country = '"+str(country)+"' LIMIT 1"
    myCursor.execute(sql)
    readData = myCursor.fetchall()
    if len(readData) != 0: #Có dữ liệu
      Task1GetLink.surfSharkVPN(readData[0]['surfshark_working'])
      
      return readData[0]['surfshark_working']
    else:
      logger.error("NOT FOUND VPN WORKING COLUMN!!!")
    

  #########################################################
  # Name:   def surfSharkVPN(location):
  # Function: Kiểm tra và đăng nhập vào SurfSharkVPN
  # Parameter: location: Tên quốc gia muốn chuyển vùng
  # Return: None
  #########################################################
  def surfSharkVPN(location):
    
    #Kiểm tra location có đang mở không?
    if location == "vietnam":
      #Kiểm tra biểu tượng surfshark đang hoạt động ở location mong muốn.
      # Hình Images/40s.png
      #Group1: rgb(56,184,207) ,rgb(142,142,194),rgb(247,255,255)
      #Group2: rgb(142,212,238),rgb(226,191,147),rgb(142,212,238)
      if LotusLib.wait3Color((1800,50),rgb(56,184,207) ,10,\
                             (1803,58),rgb(142,142,194),10,\
                             (1802,62),rgb(247,255,255),10, 5,0) == True and \
         LotusLib.wait3Color((1806,60),rgb(142,212,238),10,\
                             (1809,58),rgb(226,191,147),10,\
                             (1810,63),rgb(142,212,238),10, 2,0) == True:
        logger.info("VPN's already activated")
        return "VPN's already activated"
      else:
        # Kích hoạt VPN theo location chỉ định
        logger.info("Kích hoạt VPN theo location chỉ định: %s",location)
        GUI.click(1800,50) #Vị trí nút surfshark
        LotusLib.wait3Color((1195,230),rgb(23,138,158),10,\
                            (1210,230),rgb(23,138,158),10,\
                            (1195,270),rgb(23,138,158),10,60,200) # Images/39b.png .Chờ màu rgb(23,138,158) trong 20 giây
        LotusLib.waitColor((1330,140),rgb(242,242,247),10,5,100)
        GUI.click(1232,135) # Images/41s.png .Click vị trí search
        LotusLib.delay(100)
        pyperclip.copy(str(location)) #Copy tên location vào clipboard
        LotusLib.delay(100)
        pyperclip.copy(str(location)) #Copy tên location vào clipboard
        LotusLib.delay(100)
        GUI.hotkey('ctrl','v')
        LotusLib.wait3NotColor((1195,225),rgb(23,138,158),10,\
                               (1203,226),rgb(240,248,249),10,\
                               (1210,225),rgb(23,138,158),10,300)
        GUI.click(1200,220) # Images/42b.png .Click chọn location hiện ra
        LotusLib.delay(300)
        GUI.click(1200,220) # Images/42b.png .Click chọn location hiện ra
        LotusLib.delay(300)
        LotusLib.waitColor((1800,50),rgb(56,184,207),20,30,200) # Images/40s.png .Chờ surfShartk kết nối thành công
        LotusLib.delay(300)
        GUI.click(1600,20) # Images/43b.png .Click ra ngoài để tắt cửa sổ.

    if location == "disconnect":
      #Kiểm tra biểu tượng surfshark đang hoạt động ở disconnect
      # Hình Images/46s.png
      if LotusLib.checkColorWithCapture((1800,50),rgb(134,134,140),20,100) == True:
        logger.info("VPN's already disconnected")
        return "VPN's already disconnected"
      else:
        # Disconnect VPN
        logger.info("Tiến hành disconnect VPN")
        GUI.click(1800,50) #Vị trí nút surfshark
        LotusLib.wait3Color((1195,230),rgb(23,138,158),10,\
                            (1210,230),rgb(23,138,158),10,\
                            (1195,270),rgb(23,138,158),10,60,200) # Images/39b.png .Chờ màu rgb(23,138,158) trong 20 giây
        LotusLib.delay(1000)
        GUI.click(1650,525) # Images/47s.png .Click vị trí nút Disconnect
        LotusLib.waitColor((1650,220),rgb(229,229,234),10,15,200) #  .Chờ surfShartk ngắt kết nối.
        LotusLib.delay(500)
        GUI.click(1600,20) # Images/43b.png .Click ra ngoài để tắt cửa sổ.
    

  #########################################################
  # Name: changeToNewVpnLocation
  # Function: Đổi sang một VPN location mới
  # Parameter: vpnNation: Tên quốc gia muốn chuyển vùng
  # Return: None
  #########################################################
  def changeToNewVpnLocation(vpnNation,currentVpnWorking):
    
    logger.info('========= CHANGE TO NEW VPN =========')
    logger.info('Current VPN: %s',currentVpnWorking)
    
    sql = "SELECT * FROM tiktop_config_vpn WHERE country = '"+str(vpnNation)+"' LIMIT 1"
    myCursor.execute(sql)
    readData = myCursor.fetchall()
    if len(readData) != 0: #Có dữ liệu
      locationList = readData[0]['surfshark_location_list'].split(',')
      workingLocation = readData[0]['surfshark_working']
      if workingLocation == currentVpnWorking: #Chưa bị ai đó đổi từ đầu chương trình tới giò => Đổi VPN mới
        # print(len(locationList))
        if len(locationList) != 1:
          nextLocationWorking = workingLocation
          while nextLocationWorking == workingLocation:
            nextLocationWorking = locationList[randint(0,len(locationList)-1)]
            logger.info('New VPN    : %s',nextLocationWorking)
          # Cập nhật location mới
          sql = "UPDATE tiktop_config_vpn SET country = %s, surfshark_working = %s WHERE country = '"+str(vpnNation)+"'"
          val = (str(vpnNation),nextLocationWorking)
          myCursor.execute(sql, val)
          myDb.commit()
          logger.info('=====================================')
    else:
      logger.error('CONFIG VPN FOR COUNTRY %s NOT FOUND!!!',str(vpnNation))
    
  
class Task2GetComment:
  avatar1stPos = ""
  avatarLastPos = ""
  normalVideoDownload = 0

  def get999Post():
    rowStatus = "None"
    checkingNum = 0
    try:
      #Lấy tin -999 hoặc CHECKING (Nếu hết -999)
      sql = "SELECT * FROM tiktop_vol"+str(tikTopConfig.vol_num)+" WHERE task2_check_time = "+str(-999)+" LIMIT 1"
      myCursor.execute(sql)
      readData = myCursor.fetchall()
      if len(readData) != 0: #Có tin -999
        # logger.info("\n\nDEBUG: ===> -999 FOUND\n")
        rowStatus = "-999"
        checkingNum = 0
      else:
        sql = "SELECT * FROM tiktop_vol"+str(tikTopConfig.vol_num)+" WHERE task2_check_time = 'CHECKING'"
        #sql = "SELECT * FROM tiktop_vol"+str(tikTopConfig.vol_num)+" WHERE task2_check_time = 'CHECKING' and Task2_PIC = '"+str(platform.uname()[1])+"' LIMIT 1"
        myCursor.execute(sql)
        readData = myCursor.fetchall()
        if len(readData) != 0: #Có tin CHECKING
          # logger.info("\n\nDEBUG: ===> CHECKING FOUND\n")
          rowStatus = "CHECKING"
          checkingNum = randint(0,len(readData)-1)

      #Load thông tin về
      if rowStatus == "-999" or rowStatus == "CHECKING":
        readData = readData[checkingNum]
        logger.info("Read data: %s",readData)
        curPostInfo.id                 = readData['id']
        curPostInfo.video_id           = readData['video_id']
        curPostInfo.org_user           = readData['org_user']
        curPostInfo.cus_user           = readData['cus_user']
        curPostInfo.post_date          = readData['post_date']
        curPostInfo.video_link         = readData['video_link']
        curPostInfo.like_num           = readData['like_num']
        curPostInfo.comment_num        = readData['comment_num']
        curPostInfo.share_num          = readData['share_num']
        curPostInfo.funny_num          = readData['funny_num']
        curPostInfo.total_score        = readData['total_score']
        curPostInfo.task2_check_time   = readData['task2_check_time']
        curPostInfo.created_time       = readData['created_time']
        curPostInfo.Task1_PIC          = readData['Task1_PIC']
        curPostInfo.Task2_PIC          = readData['Task2_PIC']
        curPostInfo.video_source       = readData['video_source']
        curPostInfo.updated_time       = readData['updated_time']
        curPostInfo.checking_retry     = readData['checking_retry']
        curPostInfo.heart_check_flag   = readData['heart_check_flag']
        curPostInfo.heart_click        = readData['heart_click']
        curPostInfo.clip_caption       = readData['clip_caption']
      else:
        return 0 #NO_RESPOND
      
      if rowStatus == "-999":
        #Cập nhật trạng thái của dòng là đang checking
        sql = "UPDATE tiktop_vol"+str(tikTopConfig.vol_num)+" SET updated_time = %s, task2_check_time = %s, Task2_PIC = %s WHERE video_id = "+str(curPostInfo.video_id)
        val = (LotusLib.getCurTime(),"CHECKING",str(platform.uname()[1]))
        myCursor.execute(sql, val)
        myDb.commit()
        # logger.info("\n\nDEBUG: ===> UPDATED -999 to CHECKING\n")
        return 1

      if rowStatus == "CHECKING":
        curPostInfo.checking_retry += 1 #Tăng giá trị CHECKING_RETRY
        if curPostInfo.checking_retry <= 2:
          #Cập nhật trạng thái của dòng là đang checking
          sql = "UPDATE tiktop_vol"+str(tikTopConfig.vol_num)+" SET updated_time = %s, task2_check_time = %s, Task2_PIC = %s, checking_retry = %s WHERE video_id = "+str(curPostInfo.video_id)
          val = (LotusLib.getCurTime(),"CHECKING",str(platform.uname()[1]),str(curPostInfo.checking_retry))
          myCursor.execute(sql, val)
          myDb.commit()
          return 1
        else:
          #Cập nhật trạng thái của dòng là đang checking
          sql = "UPDATE tiktop_vol"+str(tikTopConfig.vol_num)+" SET updated_time = %s, task2_check_time = %s, Task2_PIC = %s WHERE video_id = "+str(curPostInfo.video_id)
          val = (LotusLib.getCurTime(),"NO_RESPOND",str(platform.uname()[1]))
          myCursor.execute(sql, val)
          myDb.commit()
          return 1
    
    except Exception as errMessage:
      logger.debug("!!!! ERROR !!!!")
      logger.error(errMessage)
      return 0

  def goToViewCommentPage():
    #Di chuyển mouse đến vị trí click
    GUI.click(650,450)
    if LotusLib.waitColor((1345,800),rgb(248,248,248),20,30) == False: # Images/36b.png .Chờ load xong chưa bao gồm load Avatar trong 30 giây
      return False
    allAvatarLoaded = 0
    checkTime = 0
    while checkTime < 20 and allAvatarLoaded < 2: # Đợi load comment tối đa 20 giây
      allAvatarLoaded = 0
      i = 500
      screen = GUI.screenshot()
      while i < 970:
        if 244 <= screen.getpixel((857,i))[0] <=  252: #Màu nền là (248,248,248)
          i +=1
        else:
          allAvatarLoaded +=1
          i += 40
          if allAvatarLoaded >= 2: #Tìm thấy 2 điểm khác màu nền trắng. Ít nhất load được 2 Avatar
            break # Đã load xong các avatar
      checkTime += 1
      LotusLib.delay(1000)
    LotusLib.delay(1000) #Chờ 1 giây để đảm bảo load xong toàn bộ Avatar
    if allAvatarLoaded >= 2:
      return True
    else:
      return False

  #Chiến thuật bắt comment:
  # Images/13b.png
  # 1. Tìm vị trí comment đầu tiên
  # 2. Click nút xuống số 2 để cuộn avatar lên trên. Chú ý tính toán để avatar không vượt quá số 3. Mỗi lần cuộn sẽ trôi 40px.
  # 3. Từ vị trí số 4 đếm lên trên để tìm comment cuối cùng (Nếu phát hiện nữa avata cũng OK)
  # 4. Vùng bắt comment sẽ là từ vị trí comment đầu tiên đến comment gần cuối. Lưu hình này vào biến tạm chờ check điểm cười và các tiêu chí khác.
  # def captureCommentPic():
  #   GUI.click(1330,950) #Click chọn phần nội dung comment để lát nữa nhấn nút down để kéo comment xuống 40px
  #   # 1. Tìm vị trí comment đầu tiên
  #   avatar1stPos = Task2GetComment.findCommentPos4(1)[0] #Nhận vị trí của first comment
  #   # 2. Click nút xuống số 2 để cuộn avatar lên trên. Chú ý tính toán để avatar không vượt quá số 3. Mỗi lần cuộn sẽ trôi 40px.
  #   # print(avatar1stPos)
  #   if avatar1stPos != False: # Có phát hiện ra avatar thứ 1
  #     #Tìm đỉnh của thanh cuộn comment
  #     screenCapture = GUI.screenshot()
  #     i = 230 #Vị trí khởi điểm để tìm thanh cuộn
  #     while i < 950: # 950 là vì trí cuối cùng để tìm kiếm
  #       if 206 < screenCapture.getpixel((1346,i))[0] < 216 : # Màu của thanh cuộn là màu xám rgb(211,211,211)
  #         break;
  #       i = i + 1; #Bước nhảy
  #     scrollPos = [1346,i] #Vị trí đỉnh của thanh cuộng. Mỗi lần nhấn xuống thì thanh cuộn comment này sẽ trôi
  #     num3Pos = 857,i  #Vị trí dòng comment sẽ bị ẩn khi cuộn xuống
  #     logger.info("===> DEBUG: scrollPos ="+str(scrollPos))
  #     avatar1stPos = scrollPos
  #     logger.debug("First comment pos: %s",avatar1stPos)
      
  #     # while avatar1stPos[1] - 40 > num3Pos[1]:
  #     #   avatar1stPos[1] -= 40
  #     #   GUI.press('down') #Nhấn nút chạy xuống 40px
  #     #   scrollPos = Task2GetComment.waitScrollDown(checkX=scrollPos[0],rangeYLow=scrollPos[1],rangeYHigh=950,timeout_s=15)
  #     #   logger.debug("Scrollbar Top Position: %s",scrollPos)
  #     # logger.debug("First comment pos: %s",avatar1stPos)
      
  #     # 3. Từ vị trí số 4 đếm lên trên để tìm comment cuối cùng (Nếu phát hiện nữa avata cũng OK)
  #     avatarLastPos = Task2GetComment.findCommentPos4(0)[1] #Nhận vị trí của last comment
  #     logger.debug("Last comment pos: %s",avatarLastPos)
  #     # 4. Vùng bắt comment sẽ là từ vị trí comment đầu tiên đến comment gần cuối. Lưu hình này vào biến tạm chờ check điểm cười và các tiêu chí khác.
  #     logger.debug("Save temp image")
  #     pyautogui.screenshot(region=(820,avatar1stPos[1], 510, avatarLastPos[1]-avatar1stPos[1]-1)).save(curPostInfo.video_id+".png")
  #     Task2GetComment.avatar1stPos  = avatar1stPos
  #     Task2GetComment.avatarLastPos = avatarLastPos
  #   else:
  #     return False

  #Chiến thuật đếm điểm cười trong từng comment:
  # 1. Tải các từ khóa cười từ MySQL\tiktop_config\fun_key về.
  # 2. Lọc lấy 100 comment đầu tiên.
  # 3. Tìm các từ khóa fun_key trong mỗi comment.
  # 4. Cứ mỗi một comment có key thì điểm số sẽ được tính 80 điểm. Tối đa cho điểm cười sẽ là 100*80 = 8000 điểm
  def checkFunnyPointEachComment():
    # 1. Tải các từ khóa cười từ MySQL\tiktop_config\fun_key về.
    # fun_icon_list = FUN_ICON.split(',')
    fun_key_list = tikTopConfig.fun_key.split(',')
    # fun_key_list += fun_icon_list
    
    # 2. Lọc lấy 100 comment đầu tiên.
    for i in range (0,50):
      GUI.press('pagedown')
      LotusLib.delay(100)
    
    htmlCode = Task1GetLink.getCode()
    GUI.move(1255,180) #Di chuyển chuột qua chỗ khác để tránh màn hình xanh
    x = htmlCode.split("comment-item")
    
    # 3. Tìm các từ khóa fun_key trong mỗi comment.
    # 4. Cứ mỗi một comment có key thì điểm số sẽ được tính 90 điểm. Tối đa cho điểm cười sẽ là 100*90 = 9000 điểm
    funny_total_point = 0
    fun_key_collect = ""
    totalFun = 0
    if len(x) <= 5:
      funny_total_point = 0
    else:
      if len(x) >= 101:
        findNumber = 101
      else:
        findNumber = len(x)
      for i in range (1,findNumber):
        for fun_key in fun_key_list:
          if fun_key in x[i]:
            funny_total_point += 90 # Cộng 90 điểm cho mỗi comment có key xuất hiện.
            fun_key_collect += fun_key
            break # Nhảy đến comment khác
    funDetail = ''
    curPostInfo.funContenReport = ""
    for fun_key in fun_key_list:
      num = fun_key_collect.count(fun_key)
      totalFun += num
      logger.info("%2.0d: %s",num,fun_key)
      if num < 10:
        if num != 0: funDetail += "  "+str(num)+": "+str(fun_key)+"\n"
      else:
        funDetail += str(num)+": "+str(fun_key)+"\n"
    scrollNum = len(x)-1
    logger.info("FunIn100: %s - TotalCommentScroll: %s - Funny Point: %s",totalFun,scrollNum,funny_total_point)
    curPostInfo.funny_num = str(funny_total_point)
    #Gán nội dung báo cáo Zalo
    # Get vol_num
    sql = "SELECT * from tiktop_config"
    myCursor.execute(sql)
    tiktopVnConfig = myCursor.fetchall()[0]
    tiktopVnVolNum = tiktopVnConfig['vol_num']
    num_999 = Task2GetComment.countInfoFromVolTable(tiktopVnVolNum, '-999')
    num_checking = Task2GetComment.countInfoFromVolTable(tiktopVnVolNum, 'CHECKING')
    num_done = Task2GetComment.countInfoFromVolTable(tiktopVnVolNum, 'DONE')
    num_no_respond = Task2GetComment.countInfoFromVolTable(tiktopVnVolNum, 'NO_RESPOND')
    num_total = num_999 + num_checking + num_done + num_no_respond
    
    curPostInfo.funContenReport = f"""\
{curPostInfo.video_link}

+ Like/Comment/Share:
{curPostInfo.like_num} / {curPostInfo.comment_num} / {curPostInfo.share_num}

+ Fun100/Scroll/FScore:
{totalFun} / {scrollNum} / {funny_total_point}

+ Thống kê:
{funDetail}

+ Vol{tiktopVnVolNum} Total: {num_total}
-999: {num_999}   -   CHECKING: {num_checking}
DONE: {num_done}   -   NO_RESPOND: {num_no_respond}
"""
    return funny_total_point
    
  def calScoreAndUploadMySQL():
    like_num    = LotusLib.convertHumanNumToInt(curPostInfo.like_num)
    comment_num = LotusLib.convertHumanNumToInt(curPostInfo.comment_num)
    share_num   = LotusLib.convertHumanNumToInt(curPostInfo.share_num)
    funny_num   = LotusLib.convertHumanNumToInt(curPostInfo.funny_num)
    
    #Tính điểm cho Like
    if int(like_num) < int(tikTopConfig.min_like):
      likeScore = 0
    else:
      if int(like_num) >= int(tikTopConfig.max_like):
        likeScore = int(tikTopConfig.max_like) * float(tikTopConfig.hs_like)
      else:
        likeScore = int(like_num) * float(tikTopConfig.hs_like)
    #Tính điểm cho Comment
    if int(comment_num) < int(tikTopConfig.min_comment):
      commentScore = 0
    else:
      if int(comment_num) >= int(tikTopConfig.max_comment):
        commentScore = int(tikTopConfig.max_comment) * float(tikTopConfig.hs_comment)
      else:
        commentScore = int(comment_num) * float(tikTopConfig.hs_comment)
    #Tính điểm cho Share
    if int(share_num) < int(tikTopConfig.min_share):
      shareScore = 0
    else:
      if int(share_num) >= int(tikTopConfig.max_share):
        shareScore = int(tikTopConfig.max_share) * float(tikTopConfig.hs_share)
      else:
        shareScore = int(share_num) * float(tikTopConfig.hs_share)
    #Tính điểm cho Funny
    if int(funny_num) < int(tikTopConfig.min_funny):
      funnyScore = 0
    else:
      if int(funny_num) >= int(tikTopConfig.max_funny):
        funnyScore = int(tikTopConfig.max_funny) * float(tikTopConfig.hs_funny)
      else:
        funnyScore = int(funny_num) * float(tikTopConfig.hs_funny)

    #Update lên MySQL
    if int(curPostInfo.funny_num) < int(tikTopConfig.min_funny):
      curPostInfo.total_score = 0
    else:
      # Tính điểm tổng
      curPostInfo.total_score = likeScore + commentScore + shareScore + funnyScore
      # Kiểm tra điều kiện để Follow
      if curPostInfo.total_score >= int(tikTopConfig.follow_min_score):
        point1 = LotusLib.getColor(1200,162) # Images/15s.png . Màu chưa Follow rgb(254,44,85) -> Nếu Follow rgb(226,227,228)
        if point1[0] > 240 and point1[1] < 80 and point1[2] < 120: # Images/38s.png . Đang là nút Follow màu hồng -> Chưa follow
          logger.info("Click nút Follow - TotalScore: %s",curPostInfo.total_score)
          GUI.click(1255,180) # Images/38s.png . Click vào nút Follow
      # Kiểm tra điều kiện để download
      if curPostInfo.total_score >= int(tikTopConfig.download_min_score):
        logger.info(">>> Video thỏa điều kiện tải xuống <<<")
        if os.path.exists("Y:\\Post_Vol"+tikTopConfig.vol_num) == False:
          shutil.copytree("Y:/000_Post_Master","Y:/Post_Vol"+tikTopConfig.vol_num)
        videoPath = 'Y:\\Post_Vol'+tikTopConfig.vol_num+'\\Input\\'+str(f'{int(curPostInfo.total_score):04.0f}')+'_'+str(curPostInfo.video_id)+'_'+str(curPostInfo.org_user)+'.mp4' #Tên file có dạng: P:/Vol<x>/<điểm>_<video_id>.mp4
        # Lưu video về máy
        videoPos = Task2GetComment.saveVideoClip_GUI(curPostInfo.video_source,str(videoPath))
        # Di chuyển file comment vào thư mục
        logger.info("Di chuyển file comment vào thư mục")
        if os.path.exists(curPostInfo.video_id+".png") and videoPos != 0:
          source = curPostInfo.video_id+".png"
          dest = 'Y:\\Post_Vol'+tikTopConfig.vol_num+'\\Input\\'+str(f'{int(curPostInfo.total_score):04.0f}')+'_'+str(curPostInfo.video_id)+'_'+str(curPostInfo.org_user)+'.png'
          shutil.move(source, dest)
          # Đăng ký gửi Zalo cho Boss duyệt clip
          send_zalo_num = Task2GetComment.getAndIncreseSendZaloNum()
          headTitle = "= "+str(f'{int(send_zalo_num):3d}')+"."+str(platform.uname()[1])+".SCORE: "+str(f'{int(curPostInfo.total_score):04.0f}')+" =====\n"
          resMess = headTitle + curPostInfo.funContenReport
          lastScheduleSendTime = Task2GetComment.getLastScheduleSendTime(note='tiktop_vn_script') #Nhận giá trị từ send_timestamp_sec
          if lastScheduleSendTime <= int(datetime.datetime.now().timestamp()):
            nextSendGap = 0 #Thời gian tính từ thời điểm hiện tại đến tin nhắn sẽ được gửi đi gần sau cùng.
          else:
            nextSendGap = lastScheduleSendTime - int(datetime.datetime.now().timestamp())
            
          # Chỉ gửi nếu video và image tồn tại
          # if os.path.exists(videoPath) and os.path.exists(dest):
          Task2GetComment.sendToTxBufferQueue(send_to='0908549354',mess_type='text',mess_data=resMess,send_delay_sec=nextSendGap+12,note='tiktop_vn_script')
          # Task2GetComment.sendToTxBufferQueue(send_to='0908549354',mess_type='file',mess_data=videoPath,send_delay_sec=nextSendGap+16,note='tiktop_vn_script')
          Task2GetComment.sendToTxBufferQueue(send_to='0908549354',mess_type='image',mess_data=dest,send_delay_sec=nextSendGap+20,note='tiktop_vn_script')
          
    logger.info("TotalScore: %s",curPostInfo.total_score)
    # Xóa file ảnh chụp comment nếu nó còn xót lại
    if os.path.exists(curPostInfo.video_id+".png"):
      os.remove(curPostInfo.video_id+".png")
    sql = "UPDATE tiktop_vol"+str(tikTopConfig.vol_num)+" SET updated_time = %s, funny_num = %s,total_score = %s, task2_check_time = %s WHERE video_id = "+str(curPostInfo.video_id)+""
    val = (LotusLib.getCurTime(),curPostInfo.funny_num, curPostInfo.total_score,"DONE")
    myCursor.execute(sql, val)
    myDb.commit()
    
  def updateTaskMonTask1Task2(task1_flag=1, task2_flag=0):
    # if task1_flag == 0 and task2_flag == 1:
    #  sql = "UPDATE tiktop_task_mon SET task1_running_flag = %s,task2_running_flag = %s,send_zalo_num = %s WHERE id = '0'"
    #  val = (task1_flag,task2_flag,"1")
    # else:
    #   sql = "UPDATE tiktop_task_mon SET task1_running_flag = %s,task2_running_flag = %s WHERE id = '0'"
    #   val = (task1_flag,task2_flag)
    sql = "UPDATE tiktop_task_mon SET task1_running_flag = %s,task2_running_flag = %s,send_zalo_num = %s WHERE id = '0'"
    val = (task1_flag,task2_flag,"1")
    myCursor.execute(sql, val)
    myDb.commit()

  def updateTaskMonTask3Task4(task3_flag=1, task4_flag=0):
    sql = "UPDATE tiktop_task_mon SET task3_running_flag = %s,task4_running_flag = %s WHERE id = '0'"
    val = (task3_flag,task4_flag)
    myCursor.execute(sql, val)
    myDb.commit()

  def updateVolNum():
    vol_num_str = str(eval(tikTopConfig.vol_num + "+ 1"))
    tikTopConfig.vol_num = vol_num_str
    # print(tikTopConfig.vol_num)
    sql = "UPDATE tiktop_config SET vol_num = %s, task1_ena = %s, task2_ena = %s WHERE id = '0'"
    val = (tikTopConfig.vol_num,"1","1")
    myCursor.execute(sql, val)
    myDb.commit()
    
  def waitScrollDown (checkX, rangeYLow, rangeYHigh,timeout_s):
    timeCnt = time.time();
    while (time.time() - timeCnt) < timeout_s: #Chưa hết thời gian time out
      # logger.info("DEBUG1: %s",(time.time() - timeCnt))
      checkY = rangeYLow
      screenCapture = GUI.screenshot()
      while checkY < (rangeYHigh+1):
        checkY += 5 
        # logger.info("DEBUG2: %s",checkY)
        if LotusLib.checkColorWithoutCapture(screenCapture,(checkX,checkY),rgb(211,211,211),10,0) == True: #Tìm đỉnh màu xám của scrollbar.
          if checkY != rangeYLow: #Chứng tỏ đã nhảy scrollbar -> Trả về vị trí scrollbar mới.
            # logger.info("DEBUG3: %s",checkY)
            return checkX,checkY
          else:
            # logger.info("DEBUG4: %s",checkY)
            LotusLib.delay(100)
            break
    # logger.info("-----------------: %s",checkY)
    return checkX,rangeYLow

  def findCommentPos4(findOnlyFirstCmt=0,ignoreFirstCommentFromAuthor = 0,maxHeight = 840,acceptHeartFromY = 425):
    # print("===> DEBUG: maxHeight: ",maxHeight)
    startPoint = [1305,acceptHeartFromY] #Tọa độ X là vị trí của đuôi tim Images/37s.png
    capScreen = GUI.screenshot()
    avatar1stPos = ""
    avatarLastPos = ""
    topCommentPos = ""
    i = 0
    searchRange = 970 - acceptHeartFromY
    while i < searchRange:
      timPos = [startPoint[0],startPoint[1]+i]
      if capScreen.getpixel((timPos[0]   ,timPos[1]   ))[0] < 145 and\
         capScreen.getpixel((timPos[0]- 7,timPos[1]- 9))[0] < 145 and\
         capScreen.getpixel((timPos[0]+ 8,timPos[1]- 9))[0] < 145 and\
         capScreen.getpixel((timPos[0]   ,timPos[1]-12))[0] < 145 : #Xác định có 1 trái tim qua 4 điểm: Đáy, trái, phải và trên Images/37s.png
        if topCommentPos == "":
          topCommentPos = [timPos[0],timPos[1]-40]

        if avatar1stPos == "":
          if ignoreFirstCommentFromAuthor == 1:
            if Task2GetComment.checkAuthorFirstComment([timPos[0],timPos[1]-40]) == True:
              i += 80
              continue
          avatar1stPos = [timPos[0],timPos[1]-40]
          if findOnlyFirstCmt == 1:
            logger.info("avatar1stPos: "+str(avatar1stPos))
            return avatar1stPos,avatar1stPos,topCommentPos
        if timPos[1]-40 - avatar1stPos[1] < maxHeight: #Kiểm tra độ dài tối đa của comment < max height
          avatarLastPos = [timPos[0],timPos[1]-40]
          i += 80
        else:
          break
      else:
        i += 1
    if avatar1stPos != "" and avatarLastPos != "":
      logger.info("avatar1stPos: "+str(avatar1stPos)+" - avatarLastPos: "+str(avatarLastPos))
      return avatar1stPos,avatarLastPos,topCommentPos
    else:
      logger.error("KHÔNG TÌM ĐƯỢC COMMENT!!!")
      return False

  # def saveVideoClip (videoURL,videoName):
  #   try:
  #     logger.info("Lưu Video: %s",videoName.split('\\')[-1])
  #     videoNameReplace = videoName.replace("\\","/")
  #     # logger.debug("videoNameReplace: %s",videoNameReplace)
  #     urllib.request.urlretrieve(videoURL, videoNameReplace+"_script.mp4")
  #   except Exception as errMessage:
  #     #Video bị cấm truy cập bởi lỗi HTTP 403
  #     logger.info(errMessage)
  #     Task2GetComment.saveVideoClip_GUI (videoURL,videoName)

  def saveVideoClip_GUI (videoURL,videoName):
    print(videoName)
    GUI.hotkey('ctrl','t')
    LotusLib.delay(200)
    LotusLib.waitColor((400,20),rgb(255,255,255),10,15) # Đợi màu trắng của tab mới hiện ra tại vị trí tab thứ 2
    LotusLib.delay(500)
    pyperclip.copy(str(videoURL)) #Copy đường link video vào clipboard
    LotusLib.delay(50)
    pyperclip.copy(str(videoURL)) #Copy đường link video vào clipboard
    LotusLib.delay(50)
    pyperclip.copy(str(videoURL)) #Copy đường link video vào clipboard
    LotusLib.delay(200)
    GUI.hotkey('ctrl','v')
    LotusLib.delay(200)
    GUI.press('enter')
    LotusLib.delay(500)
    #Chờ cho màn hình load được video (Màn hình sẽ không còn màu trắng của trang Blank page)
    LotusLib.waitNotColor((1850,950),rgb(255,255,255),10,15) #Chờ cho màu nền trắng của trang Blank page biến mất
    LotusLib.delay(500)
    #Chờ cho một trong 3 vị trí sau khác màu đen (Video đã đang phát)
    VIDEOPOS1 = 950,500
    VIDEOPOS2 = 810,400
    VIDEOPOS3 = 1125,590
    posVideo = LotusLib.wait3NotColor(VIDEOPOS1,rgb(0,0,0),10,VIDEOPOS2,rgb(0,0,0),10,VIDEOPOS3,rgb(0,0,0),10,60) #Chờ video xuất hiện trong 60s
    LotusLib.delay(300)
    # Click chọn save video
    # Images/21s.png
    # Click phải tại vị trí 1. Chờ màu của cửa sổ tại vị trí 2. Click save tại vị trí 3.
    if posVideo == 0:
      #Không tìm thấy video
      pass
    else:
      #Video đã fetch
      if posVideo == 1:
        GUI.rightClick(VIDEOPOS1)
        CLICKPOS = VIDEOPOS1
      if posVideo == 2:
        GUI.rightClick(VIDEOPOS2)
        CLICKPOS = VIDEOPOS2
      if posVideo == 3:
        GUI.rightClick(VIDEOPOS3)
        CLICKPOS = VIDEOPOS3
      LotusLib.delay(200)
      LotusLib.waitColor((CLICKPOS[0]+10,CLICKPOS[1]+10),rgb(255,255,255),30,10) # Images/21s.png Ví trí 2
      LotusLib.delay(1000)
      GUI.click(CLICKPOS[0]+50,CLICKPOS[1]+96) # Images/21s.png Vị trí 3
    LotusLib.delay(1000)
    LotusLib.waitColor((1860,900),rgb(255,255,255),10,60) #Chờ cho màu nền trắng của cửa sổ Save xuất hiện. Yêu cầu cửa sổ Save Maximize. Images/18b.png
    LotusLib.delay(1000)
    LotusLib.waitNotColor((193,138),rgb(255,255,255),20,5,300) # Images/45b.png .Chờ có dữ liệu được load ra rgb(72,76,82)
    pyperclip.copy(str(videoName)) #Copy tên video vào đường dẫn vào clipboard
    LotusLib.delay(50)
    pyperclip.copy(str(videoName)) #Copy tên video vào đường dẫn vào clipboard
    LotusLib.delay(50)
    pyperclip.copy(str(videoName)) #Copy tên video vào đường dẫn vào clipboard
    LotusLib.delay(2000) #Thời gian chờ cần có để hiện các dữ liệu trong thư mục save
    GUI.hotkey('ctrl','v')
    LotusLib.delay(1000)
    GUI.click(1805,945) #Click chọn vùng filename
    LotusLib.delay(500)
    GUI.hotkey('ctrl','a')
    LotusLib.delay(500)
    GUI.hotkey('ctrl','v')
    LotusLib.delay(500)
    GUI.press('enter') # Nhấn nút save
    LotusLib.delay(2000)
    GUI.hotkey('alt','y') #Nhấn nút YES ghi đề nếu file có lỡ tồn tại. Images/22s.png
    LotusLib.delay(1000)
    LotusLib.waitNotColor((1901,1021),rgb(0,0,0),10,15) #Chờ dòng trạng thái của nút tải video xuất hiện Images/19b.png
    LotusLib.delay(500)
    GUI.click(1901,1021) # Đóng dòng trạng thái tải video của Chrome Images/19b.png
    LotusLib.delay(100)
    GUI.click(1901,1021) # Đóng dòng trạng thái tải video của Chrome Images/19b.png
    LotusLib.delay(100)
    GUI.click(470,16) # Đóng Tab thứ 2
    LotusLib.delay(500)
    GUI.click(470,16) # Đóng Tab thứ 2
    Task2GetComment.normalVideoDownload += 1
    return posVideo
  
  def sendToTxBufferQueue(send_to,mess_type,mess_data,send_delay_sec=0,note='tiktop_vn_script'):
    send_timestamp_sec = int(datetime.datetime.now().timestamp() + send_delay_sec)
    send_schedule = datetime.datetime.fromtimestamp(send_timestamp_sec)
    # Register to Tx Buffer Queue
    sql = "INSERT INTO tx_buffer (send_to, uid, mess_type, mess_data,send_timestamp_sec,send_schedule,note) VALUES (%s, %s, %s, %s, %s, %s,%s)"
    val = (send_to, str(randint(0,1000000000)) ,mess_type,mess_data,str(send_timestamp_sec),str(send_schedule),note)
    myCursorZalo.execute(sql, val)
    myDbZalo.commit()
    
  def getLastScheduleSendTime(note='tiktop_vn_script'):
    sql = "SELECT * FROM tx_buffer WHERE note = '"+str(note)+"' ORDER BY send_timestamp_sec DESC LIMIT 1"
    myCursorZalo.execute(sql)
    readData = myCursorZalo.fetchall()
    if (len(readData)==0):
      return 0
    else:
      return int(readData[0]['send_timestamp_sec'])
    
  # Chờ cho tất cả cả máy khác đều hoàn thành xong phần CHECKING của mình
  def waitAllFinishCHECKING():
    n = 0
    while n < 2000:
      n+=1
      sql = "SELECT * FROM tiktop_vol"+str(tikTopConfig.vol_num)+" WHERE task2_check_time = 'CHECKING' LIMIT 1"
      myCursor.execute(sql)
      readData = myCursor.fetchall()
      if len(readData) != 0: #Có tin CHECKING
        LotusLib.delay(randint(1000,5000))
        
  def getAndIncreseSendZaloNum ():
    sql = "SELECT * FROM tiktop_task_mon"
    myCursor.execute(sql)
    readData = myCursor.fetchall()[0]
    send_zalo_num = int(readData['send_zalo_num'])
    sql = "UPDATE tiktop_task_mon SET send_zalo_num = '"+str(send_zalo_num + 1)+"'"
    myCursor.execute(sql)
    myDb.commit()
    return send_zalo_num
  
  def resetSendZaloNum():
    sql = "UPDATE tiktop_task_mon SET send_zalo_num = '1'"
    myCursor.execute(sql)
    myDb.commit()
    
  #########################################################
  # Name: mySqlCloseConnection
  # Function: Đóng kết nối với MySQL
  # Parameter: none
  # Return: none
  #########################################################
  def mySqlCloseConnection():
    myDb.close()
    myDbZalo.close()
    
  #########################################################
  # Name: captureCommentPic
  # Function: Bắt ảnh comment 510*840 pixel. Có Avartar.
  # Parameter: none
  # Return: none
  #########################################################
  def captureCommentParts(maxHeight = 0):
    GUI.click(1330,950) #Click chọn phần nội dung comment để lát nữa nhấn nút pagedown để kéo comment xuống 40px
    # 1. Lấy phần comment khúc đầu
    avatar1stPos,avatarLastPos,topCommentPos = Task2GetComment.findCommentPos4(findOnlyFirstCmt=0,ignoreFirstCommentFromAuthor=1,maxHeight=maxHeight,acceptHeartFromY=425) #Nhận vị trí của first comment
    firstCommentHeight = avatarLastPos[1]-avatar1stPos[1]
    if avatar1stPos != False:
      GUI.screenshot(region=(820,avatar1stPos[1], 510, firstCommentHeight)).save(curPostInfo.video_id+"_commentPart1.png")
    else:
      return False
    
    # 2. Nhấn Down xuống để cắt phần sau comment
    # Tìm vị trí đỉnh thanh cuộn lần đầu tiên
    screenCapture = GUI.screenshot()
    i = 230 #Vị trí khởi điểm để tìm thanh cuộn
    while i < 950: # 950 là vì trí cuối cùng để tìm kiếm
      if 206 < screenCapture.getpixel((1346,i))[0] < 216 : # Màu của thanh cuộn là màu xám rgb(211,211,211)
        break;
      i = i + 1; #Bước nhảy
    scrollPos = [1346,i] #Vị trí đỉnh của thanh cuộn. Mỗi lần nhấn xuống thì thanh cuộn comment này sẽ trôi
    #Nhấn nút xuống và chờ thanh cuộn
    print(scrollPos)
    GUI.press('pagedown')
    scrollPos = Task2GetComment.waitScrollDown(checkX=scrollPos[0],rangeYLow=scrollPos[1],rangeYHigh=950,timeout_s=15)
    LotusLib.delay(200)
    # 3. Lấy phần comment khúc sau
    # print(maxHeight," - ",firstCommentHeight," - ",topCommentPos)
    avatar1stPos,avatarLastPos,topCommentPos = Task2GetComment.findCommentPos4(findOnlyFirstCmt=0,ignoreFirstCommentFromAuthor=0,maxHeight=maxHeight-firstCommentHeight,acceptHeartFromY=topCommentPos[1]+39) #Nhận vị trí của first comment
    secondCommentHeight = avatarLastPos[1]-avatar1stPos[1]
    if avatar1stPos != False:
      GUI.screenshot(region=(820,avatar1stPos[1], 510, secondCommentHeight)).save(curPostInfo.video_id+"_commentPart2.png")
    else:
      return False
    
    # if avatar1stPos != False: # Có phát hiện ra avatar thứ 1
      # #Tìm đỉnh của thanh cuộn comment
      # screenCapture = GUI.screenshot()
      # i = 230 #Vị trí khởi điểm để tìm thanh cuộn
      # while i < 950: # 950 là vì trí cuối cùng để tìm kiếm
      #   if 206 < screenCapture.getpixel((1346,i))[0] < 216 : # Màu của thanh cuộn là màu xám rgb(211,211,211)
      #     break;
      #   i = i + 1; #Bước nhảy
      # scrollPos = [1346,i] #Vị trí đỉnh của thanh cuộng. Mỗi lần nhấn xuống thì thanh cuộn comment này sẽ trôi
      # num3Pos = 857,i  #Vị trí dòng comment sẽ bị ẩn khi cuộn xuống
      # # logger.info("===> DEBUG: scrollPos ="+str(scrollPos))
      # avatar1stPos = scrollPos
      # logger.debug("First comment pos: %s",avatar1stPos)
      
      # while avatar1stPos[1] - 40 > num3Pos[1]:
      #   avatar1stPos[1] -= 40
      #   GUI.press('down') #Nhấn nút chạy xuống 40px
      #   scrollPos = Task2GetComment.waitScrollDown(checkX=scrollPos[0],rangeYLow=scrollPos[1],rangeYHigh=950,timeout_s=15)
      #   logger.debug("Scrollbar Top Position: %s",scrollPos)
      # logger.debug("First comment pos: %s",avatar1stPos)
      
      # 3. Từ vị trí số 4 đếm lên trên để tìm comment cuối cùng (Nếu phát hiện nữa avata cũng OK)
      # avatarLastPos = Task2GetComment.findCommentPos4(0)[1] #Nhận vị trí của last comment
      # logger.debug("Last comment pos: %s",avatarLastPos)
      # 4. Vùng bắt comment sẽ là từ vị trí comment đầu tiên đến comment gần cuối. Lưu hình này vào biến tạm chờ check điểm cười và các tiêu chí khác.
      # logger.debug("Save temp image")
      # pyautogui.screenshot(region=(820,avatar1stPos[1], 510, avatarLastPos[1]-avatar1stPos[1]-1)).save(curPostInfo.video_id+".png")
      # Task2GetComment.avatar1stPos  = avatar1stPos
      # Task2GetComment.avatarLastPos = avatarLastPos
    # else:
    #   return False
    
  def checkAuthorFirstComment(avatar1stPos):
    if avatar1stPos != "":
      checkPosY = avatar1stPos[1] + 8
      print("CheckPosY: ",checkPosY)
      firstCheckPosX  = avatar1stPos[0] - 375
      secondCheckPosX = firstCheckPosX + 280
      print("CheckPosX_1: ",firstCheckPosX," - CheckPosX_2: ",secondCheckPosX)
      
      screen = GUI.screenshot()
      checkPosX = firstCheckPosX
      while checkPosX <= secondCheckPosX:
        checkPosX += 5
        if LotusLib.checkColorWithoutCapture(screen,(checkPosX,checkPosY),rgb(254,44,85),10,0) == True: #Đúng là tác giả => bỏ qua.
          print("FOUND Tac Gia: ",checkPosX,"-",checkPosY)
          return True #First comment là tác giả
      return False #First comment không phải tác giả
         
  def captureHeaderCommentPic():
    screen = GUI.screenshot()
    i = 230
    endPostHeader = 450
    while i < 450:
      if LotusLib.checkColorWithoutCapture(screen,(854,i),rgb(241,241,242),0,0) == True:
        endPostHeader = i - 7
        break
      else:
        i += 7
    print("endPostHeader: ",endPostHeader)
    GUI.screenshot(region=(820,140,510,endPostHeader-140)).save(curPostInfo.video_id+"_header.png")
    return endPostHeader-140
    
  def captureCommentPic():
    totalHeight = 840
    # Chờ load xong nội dung trang comment.
    logger.debug("Chờ load xong nội dung trang comment.")
    LotusLib.delay(1000)
    LotusLib.waitColor((1346,710),rgb(248,248,248),10,30,1000) # Images/48b.png Images/49b.png Khi đang load thì thanh cuộn dài. Load xong thì thanh cuộng ngắn.

    # Capture header and comment contents
    logger.debug("Capture header and comment content.")
    headerHeight = Task2GetComment.captureHeaderCommentPic()
    Task2GetComment.captureCommentParts(maxHeight=totalHeight-headerHeight)
    #Ghép comment image
    commentFullPic = Image.new('RGB',(510,840),(248,248,248)) #Màu nền rgb(248,248,248)
    if os.path.exists(curPostInfo.video_id+"_header.png") and\
      os.path.exists(curPostInfo.video_id+"_commentPart1.png") and\
      os.path.exists(curPostInfo.video_id+"_commentPart2.png"):
      headerPic    = Image.open(curPostInfo.video_id+"_header.png")
      dangFollow   = Image.open("Images/dangFollow.png")
      separateLine = Image.open("Images/commentSeparateLine.png")
      commentPic1  = Image.open(curPostInfo.video_id+"_commentPart1.png")
      commentPic2  = Image.open(curPostInfo.video_id+"_commentPart2.png")
      commentFullPic.paste(headerPic,(0,0))
      commentFullPic.paste(dangFollow,(364,12)) #Ghi đè lên nút Follow
      commentFullPic.paste(separateLine,(0,headerPic.size[1]-20))
      commentFullPic.paste(commentPic1,(0,headerPic.size[1]))
      commentFullPic.paste(commentPic2,(0,headerPic.size[1]+commentPic1.size[1]))
      # xóa các file tạm
      os.remove(curPostInfo.video_id+"_header.png")
      os.remove(curPostInfo.video_id+"_commentPart1.png")
      os.remove(curPostInfo.video_id+"_commentPart2.png")
    commentFullPic.save(curPostInfo.video_id+".png")
    
  def addLogoWaterMarkInComment(alpha=6):
    #1. Load and resize logo
    # print("DEBUG: #1. Load and resize logo")
    logoPath = './Images/Logo_625x625px.png'
    logoPic = Image.open(logoPath)
    logoResize = logoPic.resize((500,500))
    
    #2. Set logo transparent with alpla
    # print("DEBUG: #2. Set logo transparent with alpla")
    background = Image.new('RGB',(500,500),(248,248,248))
    background.paste(logoResize,(0,0),logoResize)
    background.putalpha(alpha)

    #3. Add to comment pic
    # print("DEBUG: #3. Add to comment pic")
    commentPic = Image.open(curPostInfo.video_id+".png")
    commentPic.paste(background,(10,200),background)
    commentPic.save(curPostInfo.video_id+".png")
  
  #########################################################
  # Name: countInfoFromVolTable
  # Function: Đếm số lượng các dòng thông tin từ bảng tiktop_volxx
  # Parameter:
  #    + vol_num: Sô vol cần truy xuất.
  #    + task2_check_time: loại tin cần đến ('-999','CHECKING',
  #                                         'DONE','NO_RESPOND')
  # Return: myCursor.rowcount: Số dòng đếm được.
  #########################################################
  def countInfoFromVolTable (vol_num = 1,task2_check_time = '-999'):
    sql = "SELECT * from tiktop_vol"+str(vol_num)+" WHERE task2_check_time = '"+str(task2_check_time)+"'"
    # print("DEBUG: 0.2 "+sql)
    myCursor.execute(sql)
    myCursor.fetchall()
    logger.info(myCursor.rowcount)
    return myCursor.rowcount
