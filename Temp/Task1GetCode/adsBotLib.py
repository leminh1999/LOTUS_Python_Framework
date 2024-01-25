import platform
from Global.loggingSetup import *
import pyautogui
import mysql.connector
from os import path
from A4_GetLink_Function import *
from LotusLib_v1r1 import *
from random import randint

GUI = pyautogui

# myDb.close()

# #MySQL Database
# MYSQL_IP = "192.168.68.200"
# MYSQL_USER = "tiktop_vn"
# MYSQL_PASS = "ao!6ejM*7h8HtrgR"
# MYSQL_DB = "tiktop_vn"

# ## Kết nối mySQL ##
# myDb = mysql.connector.connect(
#   host= MYSQL_IP,
#   user= MYSQL_USER,
#   password= MYSQL_PASS,
#   database= MYSQL_DB, #Tên cơ sở dữ liệu
#   autocommit=True #Tự động cập nhật bảng và dữ liệu đang chạy.
# )
# myCursor = myDb.cursor(dictionary=True) #=> Xuất dữ liệu dạng dictionary (Giống object)

class adsBotLib(Task1GetLink,Task2GetComment):

  def findHeartAndClick(ignoreAuthor = 1,scrollNum = 20):
    print("ScrollNum1: = "+str(scrollNum))
    startPoint = [1305,500] #Tọa độ X là vị trí của đuôi tim Images/37s.png
    pageDownNum = 0
    heartClickNum = 0
    while pageDownNum < scrollNum:
    # while True: 
      capScreen = GUI.screenshot()
      clickHearOnPage = 0
      i = 0
      searchRange = 970 - 500
      while i < searchRange:
        timPos = [startPoint[0],startPoint[1]+i]
        if capScreen.getpixel((timPos[0]   ,timPos[1]   ))[0] < 145 and\
          capScreen.getpixel((timPos[0]- 7,timPos[1]- 9))[0] < 145 and\
          capScreen.getpixel((timPos[0]+ 8,timPos[1]- 9))[0] < 145 and\
          capScreen.getpixel((timPos[0]   ,timPos[1]-12))[0] < 145 : #Xác định có 1 trái tim qua 4 điểm: Đáy, trái, phải và trên Images/37s.png
          # print(startPoint[1]+i)
          kiemTraTacGia_Y = startPoint[1]+i-32
          if ignoreAuthor == 1: 
            if LotusLib.horFindColor(rgb(254,44,85),10,920,1280,6,kiemTraTacGia_Y) == False: #Không phải tác giả
              GUI.click(1305,startPoint[1]+i-8) #Click vào vị trí trái tim
              heartClickNum += 1
              clickHearOnPage += 1
              LotusLib.delay(randint(100,1000))
          else:
            GUI.click(1305,startPoint[1]+i-8) #Click vào vị trí trái tim
            heartClickNum += 1
            clickHearOnPage += 1
            LotusLib.delay(100)
          i += 80
        else:
          i += 1
      adsBotLib.commentPageDown()
      pageDownNum += 1
      if clickHearOnPage == 0: break #Nếu có trang nào đó mà không còn tim hay không còn click được nữa thì thoát ra
    logger.info("Heart clicked number = %d",heartClickNum)
    curPostInfo.heart_check_flag = 1
    curPostInfo.heart_click = heartClickNum

  def heartClicking(scrollNum = 20):
    print("ScrollNum2: = "+str(scrollNum))
    # Chờ load xong nội dung trang comment.
    logger.debug("Chờ load xong nội dung trang comment.")
    LotusLib.delay(1000)
    LotusLib.waitColor((1346,710),rgb(248,248,248),10,15,1000) # Images/48b.png Images/49b.png Khi đang load thì thanh cuộn dài. Load xong thì thanh cuộng ngắn.

    GUI.click(1330,950) #Click chọn phần nội dung comment để lát nữa nhấn nút pagedown để kéo comment xuống 40px
    adsBotLib.findHeartAndClick(ignoreAuthor = 1,scrollNum = scrollNum)
    
  def getMostCommentClip(volNum):
    #1. Lấy video link của clip được rando
    sql = "SELECT * from tiktop_vol"+str(volNum)+" WHERE comment_num NOT IN ('0','') AND heart_check_flag = '0' LIMIT 1"
    myCursor.execute(sql)
    configData = myCursor.fetchall()
    if len(configData) > 0: 
      print(configData[0])
      curPostInfo.video_id         = configData[0]['video_id']
      curPostInfo.video_link       = configData[0]['video_link']
      curPostInfo.heart_check_flag = configData[0]['heart_check_flag']
      curPostInfo.heart_click      = configData[0]['heart_click']
  
  def commentPageDown():
    # Tìm vị trí đỉnh thanh cuộn lần đầu tiên
    screenCapture = GUI.screenshot()
    i = 230 #Vị trí khởi điểm để tìm thanh cuộn
    while i < 950: # 950 là vì trí cuối cùng để tìm kiếm
      if 206 < screenCapture.getpixel((1346,i))[0] < 216 : # Màu của thanh cuộn là màu xám rgb(211,211,211)
        break;
      i = i + 1; #Bước nhảy
    scrollPos = [1346,i] #Vị trí đỉnh của thanh cuộn. Mỗi lần nhấn xuống thì thanh cuộn comment này sẽ trôi
    #Nhấn nút xuống và chờ thanh cuộn
    GUI.press('pagedown')
    scrollPos = adsBotLib.waitScrollDown(checkX=scrollPos[0],rangeYLow=scrollPos[1],rangeYHigh=950,timeout_s=5)
    print("ScrollPos2: ",scrollPos)
    LotusLib.delay(500)

  def updateMysqlHeartClicking():
    curPostInfo.Task1_PIC = platform.uname()[1]
    print(curPostInfo.Task1_PIC)
    # sql = "UPDATE tiktop_vol"+str(tikTopConfig.vol_num)+" SET heart_check_flag = "+str(curPostInfo.heart_check_flag)+",\
    #        heart_click = "+curPostInfo.heart_click+", TASK1_PIC = "+str(curPostInfo.Task1_PIC)+"  WHERE video_id = '"+str(curPostInfo.video_id)+"'"
    # myCursor.execute(sql)
    # myDb.commit()
    sql = "UPDATE tiktop_vol"+str(tikTopConfig.vol_num)+" SET heart_check_flag = %s, heart_click = %s, TASK1_PIC = %s WHERE video_id = %s"
    val = (str(curPostInfo.heart_check_flag),str(curPostInfo.heart_click),curPostInfo.Task1_PIC,curPostInfo.video_id)
    myCursor.execute(sql, val)
    myDb.commit()
    
  def checkNewPost():
    GUI.hotkey('ctrl','a')
    LotusLib.delay(500)
    GUI.hotkey('ctrl','c')
    LotusLib.delay(500)
    checkData = pyperclip.paste()
    checkData = checkData.replace('\n','Newline').replace('\r','Newline')
    logger.info(checkData)
    
    if "phút trước" in checkData:
      videoLink = checkData.split('https://')[1].split('?')[0]
      videoId = videoLink.split('/video/')[1]
      userAndTimeArr = checkData.split('phút trước')[0].split('Newline')
      userAndTime = userAndTimeArr[len(userAndTimeArr)-1]+"phút trước"

      # print("=== FOUND: NEW POST ===")
      # print(videoLink)
      # print(videoId)
      # print(userAndTimeArr)
      # print(userAndTime)
      return videoLink,videoId,userAndTime
    return "Not_found","Not_found","Not_found"
  
  def sendZalo(numCnt,videoLink,videoId,userAndTime):
    #Gửi Zalo
    sql = "SELECT * FROM tiktop_follow_new_post_send WHERE video_id ='"+videoId+"' LIMIT 1"
    myCursor.execute(sql)
    checkLastSent = myCursor.fetchall()
    
    if len(checkLastSent) == 0: #Nếu trước đó video chưa được gửi thì gửi.
      message = "= "+numCnt+". New Post =====\n"+userAndTime+"\n"+videoLink
      adsBotLib.sendToTxBufferQueue(send_to='0908549354',mess_type='text',mess_data=message,send_delay_sec=0,note='New Post (one hour)')
      # Đưa vào bảng MySQL danh sách gửi Zalo không trùng lập tiktop_follow_new_post_send
      sql = "INSERT INTO tiktop_follow_new_post_send (id,video_id) VALUES (%s,%s)"
      val = ("",videoId)
      myCursor.execute(sql, val)
      myDb.commit()
      logger.info(message)