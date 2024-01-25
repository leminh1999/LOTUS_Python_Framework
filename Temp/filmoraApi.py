from Global.loggingSetup import *
import pyautogui
import mysql.connector
from LotusLib_v1r3 import *
import pyperclip
import re
from random import randint
from os import path
from pymediainfo import MediaInfo
from bs4 import BeautifulSoup
import shutil
import platform

### instance define ###
GUI = pyautogui
pc_name_current = platform.uname()[1]
MYSQL_IP = "192.168.68.200"
MYSQL_DB = "tiktop_vn"

## Kết nối mySQL ##
myDb = mysql.connector.connect(
  host= MYSQL_IP,
  user= "tiktop_"+pc_name_current,
  password= "",
  database= MYSQL_DB, #Tên cơ sở dữ liệu
  autocommit=True #Tự động cập nhật bảng và dữ liệu đang chạy.
)
myCursor = myDb.cursor(dictionary=True) #=> Xuất dữ liệu dạng dictionary (Giống object)

## Zalo MySQL init ###
myDbZalo = mysql.connector.connect(
  host= MYSQL_IP,
  user= 'tiktop_'+pc_name_current,
  password= '',
  database= 'zalo_bot', #Tên cơ sở dữ liệu
  autocommit=True #Tự động cập nhật bảng và dữ liệu đang chạy.
)
myCursorZalo = myDbZalo.cursor(dictionary=True) #=> Xuất dữ liệu dạng dictionary (Giống object)

class shortCfg ():
  runEna = 0
  runEveryMin = 60
  maxPostEachTime = 10
  delAfterDay = 3
  zaloInformEna = 0
  
#################################################################################################
#################################################################################################
#################################################################################################
class filmoraApi():
  def __init__(self):
    self.faultVideoNum = 0

  #########################################################
  # Name: getFileList
  # Function: Lấy danh sách các files ứng với loại filetype
  #           nhập vào.
  # Parameter:
  #   + path: đường dẫn đến thư mục tìm kiếm.
  #   + filetype: đuôi file tìm kiếm. Có thể nhập dạng list.
  # Return: List chứa danh danh các file được liệt kê.
  # Ex: listFileImage = getFileList(path='D:/Images/',filetype='jpg,bmp')
  #########################################################
  def getFileList(self,path="",fileType=""):
    accTime = 0
    clipNum = 0
    clipTimeMin = 0
    clipTimeSec = 0
    if path == "" or fileType == "":
      return ""
    else:
      outputList = list()
      fileTypeList = fileType.replace(' ','').split(',')
      for ftype in fileTypeList:
        print ("List for filetype: ",ftype)
        listFile = os.listdir(path)
        listFile.sort(reverse=True)
        for i in listFile:
          if i.endswith(ftype):
            # print("- File: ",path+i)
            outputList.append(path+i)
            # Extract duration
            media_info = MediaInfo.parse(path+i)
            for track in media_info.tracks:
              if track.track_type == 'Video':
                clipNum += 1
                durationMs = track.duration
                clipTime = int(durationMs/1000)
                clipTimeMin = int(clipTime/60)
                clipTimeSec = clipTime%60
                accTime += durationMs
                print("{}.Clip [{}:{}] {}".format(clipNum,clipTimeMin,clipTimeSec,path+i))
  
    accTimeHour = int(accTime/3600000)
    accTimeRemain = accTime%3600000
    accTimeMin = int(accTimeRemain/60000)
    accTimeRemain = accTimeRemain%60000
    accTimeSec = int(accTimeRemain/1000)
    accTimeRemain = accTimeRemain%1000
    accTimeMs = accTimeRemain
    print("Total Time: {}h{}m{}.{}s".format(accTimeHour,accTimeMin,accTimeSec,accTimeMs))
            
    return outputList
    
  #########################################################
  # Name: selectFilmoraLayer
  # Function: Chọn và kiểm tra lớp đã được chọn
  # Parameter: layerSelect: Lớp Filmora cần chọn. Images/1s.png
  # Return: None
  # Ex: selectFilmoraLayer(layerSelect = 3) #Layer dedicated for video
  #########################################################
  def selectFilmoraLayer(self,layerSelect=1):
    retry = 0
    checkPos = (5,980-32*layerSelect)
    selectedColor = rgb(18,22,28)
    GUI.click(630,575) #click để xõa con trỏ
    LotusLib.delay(100)
    GUI.click(1150,575) #click để xõa con trỏ
    LotusLib.delay(100)
    while retry < 3:
      getColor = LotusLib.getColor(checkPos[0],checkPos[1])
      if getColor == selectedColor:
        logger.info("Layer %s selected",layerSelect)
        return
      else:
        GUI.click(checkPos)
        if LotusLib.waitColor(checkPos,selectedColor,5,5,100) == True: #Chờ cho lớp được chọn
          logger.info("Layer %s selected",layerSelect)
          return
        else:
          GUI.click(630,575) #click để xõa con trỏ
          LotusLib.delay(300)
          GUI.click(1150,575) #click để xõa con trỏ
          LotusLib.delay(300)
          retry += 1
          logger.info("Layer %s không chọn được. Retry: %d",layerSelect,retry)
    logger.error("Layer %s không chọn được. Retry: %d => EXIT",layerSelect,retry)
    exit()
      
  #########################################################
  # Name: importMedia
  # Function: import file Media (video/pic) into Filmora
  # Parameter:
  #   + pathFile: Đường dẫn đến file cần lấy. pathFile
  #   + replaceFileType: Đuôi file cần lấy.
  # Return: True nếu file tồn tại, Fail nếu file không tồn tại.
  # Ex: importMedia("./Media/clip01.mp4","png") #Lấy file ảnh png
  #                              #Từ đường dẫn ./Media/clip01.png
  #########################################################
  def importMedia(self,pathFile="",replaceFileType=""):
    if pathFile == "" or replaceFileType == "":
      logger.error("Input của hàm chưa được nhập!!!")
      return False
    else:
      #Lấy loại bỏ đuôi đang có
      listParts = pathFile.split('.')
      lenParts = len(listParts)
      fileName = ""
      if lenParts <= 2:
        fileName = listParts[0]
      else:
        for i in range (0,lenParts-1):
          if i == 0:
            fileName += listParts[i]
          else:
            fileName += "."+listParts[i]
      pathFileNew = fileName+"."+replaceFileType
      winPath = pathFileNew.replace('/','\\')
      
      #Thực hiện import
      pyperclip.copy(winPath)
      LotusLib.delay(50)
      pyperclip.copy(winPath)
      LotusLib.delay(100)
      if path.exists(pathFileNew) == False:
        logger.error("NOT FOUND: %s",pathFileNew)
        return False
      else:
        #Tiến hành import
        logger.info("Tiến hành import: "+pathFileNew)
        GUI.hotkey('ctrl','i')
        LotusLib.delay(500)
        LotusLib.waitColor((1575,975),rgb(255,255,255),10,10,500)
        GUI.click(1575,975)
        LotusLib.delay(100)
        GUI.hotkey('ctrl','v')
        LotusLib.delay(100)
        GUI.press('enter')
        LotusLib.delay(200)
        LotusLib.waitNotColor((1575,975),rgb(255,255,255),10,10,200)
        #Kiểm tra file import có bị lỗi không
        if LotusLib.checkColorWithCapture((1199,606),rgb(74,222,208),10,200) == True:
          GUI.click(1209,606)
          return False
        #Chờ file được import và chọn nó
        print("Chờ file được import và chọn nó")
        GUI.click(350,125) # Images/9s.png (1). Vị trí nút Used
        LotusLib.delay(500)
        GUI.click(350,125) # Images/9s.png (1). Vị trí nút Used
        LotusLib.delay(500)
        arrow = LotusLib.getColor(338,129) # Images/10s.png .Vị trí mũi tên sort.
        n = 0
        while n < 10:
          # print("DEBUG: N = "+str(n))
          if LotusLib.checkColorWithCapture((347,154),rgb(255,255,255),10,0) == True: # Images/9s.png (2). Media chưa được load nếu vẫn là màu trắng.
            GUI.click(350,125) # Images/9s.png (1). Vị trí nút Used
            LotusLib.waitNotColor((338,129),arrow,10,5,0) #Chờ mũi tên xoay chiều
            arrow = LotusLib.getColor(338,129) # Images/10s.png .Vị trí mũi tên sort.
            LotusLib.delay(300)
            n += 1
            if n == 10:
              logger.error("ERROR: FILE không được import vào. n = 10.")
              exit()
          else:
            break
        GUI.click(347,154) #Click vào dòng media đầu tiên.
        LotusLib.waitColor((347,154),rgb(60,73,88),10,5,100) #Chờ cho dòng được chọn
        return True

  #########################################################
  # Name: insertMediaToTimeline
  # Function: Gán file Media đang chọn vào time line rồi
  #           nhấn 4 lần Up để lên đầu Media
  # Parameter: none
  # Return: none
  #########################################################
  def insertMediaToTimeline(self):
    GUI.hotkey('shift','i') #Đưa clip vừa gán từ Media vào Timeline
    LotusLib.delay(1000)
    GUI.click(1125,570) #Click xác nhận độ phân giải theo dự án.
    LotusLib.delay(1000)

  #########################################################
  # Name: upKeyRepeat
  # Function: Nhấn n lần phím Up
  # Parameter: time: số lần nhấn Up
  # Return: none
  #########################################################
  def upKeyRepeat(self,time=4):
    for j in range (0,time):
      GUI.press('up')
      LotusLib.delay(500)
    LotusLib.delay(1000)
  
  #########################################################
  # Name: getVideoInfo
  # Function: Trích xuất thông tin về độ phân giải và thời gian
  #           của video.
  # Parameter: pathFile: Đường dẫn đến file video cần giải mã.
  # Return: Trả về kiểu dictionary. width,height,duration_ms
  #########################################################
  def getVideoInfo(self,pathFile=""):
    media_info = MediaInfo.parse(pathFile)
    for track in media_info.tracks:
      if track.track_type == 'Video':
        durationMs = track.duration
        return {"width":track.width,"height":track.height,"durationMs":durationMs}

  #########################################################
  # Name: scaleAndMoveClip
  # Function: Kiểm tra clip đưa vào có cần scale và di chuyển không.
  #           Nếu có thì thực hiện.
  # Parameter: videoInfo: là 1 dictionary có chứa các thông Số
  #                       liên quan đến clip.
  # Return: none
  #########################################################
  def scaleAndMoveClip(self,videoInfo = dict()):
    #1. Convert video về theo dạng khung 1264x1080.
    #Tính kích thước khi scale chiều dọc 1080.
    widthWhenHeight1080 = int(videoInfo['width']*1080/videoInfo['height'])
    # print(widthWhenHeight1080)
    if widthWhenHeight1080 < 1264: #Không cần phải scale video.
      scale = 100 # Tức 100%
      moveX = -((widthWhenHeight1080-607)/2)*0.41927 #0.41927 là tỉ lệ 41.927% của cửa sổ Preview
      logger.debug("Không scale. Di chuyển trục X: %d",moveX)
    else: #Cần phải scale video
      scale = (1264/widthWhenHeight1080)*100 #Tỉ lệ % scale để đưa về dạng width = 1264.
      moveX = -((widthWhenHeight1080*scale/100-607)/2)*0.41927 #0.41927 là tỉ lệ 41.927% của cửa sổ Preview
      logger.debug("Scale = %f. Di chuyển trục X: %d",scale,moveX)
    
    #2. Thực hiện Scale và di chuyển X
    GUI.hotkey('alt','e')
    LotusLib.waitColor((870,530),rgb(97,222,208),20,5,100) # Images/2b.png (1). Đợi nút OK.
    GUI.click(50,50) #Vị trí nút Video
    LotusLib.delay(200)
    if LotusLib.checkColorWithCapture((100,100),rgb(34,41,49),5,100) == False: # Images/2b.png (2). Nút Transform đang đóng.
      GUI.click(22,81)
      LotusLib.waitColor((100,100),rgb(34,41,49),5,5,100) # Đợi dropdown
    GUI.click(100,100)
    LotusLib.delay(200)
    
    GUI.press('tab')
    LotusLib.delay(300)
    GUI.press('tab') # Vị trí Scale
    LotusLib.delay(300)
    if scale != 100:
      GUI.typewrite(str(scale))
      LotusLib.delay(300)
    GUI.press('tab') # Vị trí X
    LotusLib.delay(300)
    GUI.typewrite(str(moveX))
    LotusLib.delay(300)
    GUI.click(870,530) # Images/2b.png (1). Vị trí nút OK.
    LotusLib.waitNotColor((870,530),rgb(110,239,225),20,5,100) # Images/2b.png (1). Đợi nút OK mất.
    
  #########################################################
  # Name: moveComment
  # Function: Di chuyển comment sang bên phải.
  # Parameter: none
  # Return: none
  #########################################################
  def moveComment(self):
    moveX = ((1920-656)/2)*0.41927 #0.41927 là tỉ lệ 41.927% của cửa sổ Preview
    #1. Thực hiện Scale và di chuyển X
    GUI.hotkey('alt','e')
    LotusLib.waitColor((870,530),rgb(97,222,208),20,5,100) # Images/2b.png (1). Đợi nút OK.
    GUI.click(50,50) #Vị trí nút Video
    LotusLib.delay(200)
    if LotusLib.checkColorWithCapture((100,100),rgb(34,41,49),5,100) == False: # Images/2b.png (2). Nút Transform đang đóng.
      GUI.click(22,81)
      LotusLib.waitColor((100,100),rgb(34,41,49),5,5,100) # Đợi dropdown
    GUI.click(100,100)
    LotusLib.delay(200)
    
    GUI.press('tab')
    LotusLib.delay(300)
    GUI.press('tab') # Vị trí Scale
    LotusLib.delay(300)
    GUI.press('tab') # Vị trí X
    LotusLib.delay(300)
    GUI.typewrite(str(moveX))
    LotusLib.delay(300)
    GUI.click(870,530) # Images/2b.png (1). Vị trí nút OK.
    LotusLib.waitNotColor((870,530),rgb(110,239,225),20,5,100) # Images/2b.png (1). Đợi nút OK mất.

  def filmoraGetClipDuration(self):
    """
    \n#####################################################
    - Name: filmoraGetClipDuration
    - Function: Trích xuất thời gian thật tế của Video trong timeline.
    - Parameter: none
    - Return: videoDuration
    \n#####################################################
    """
    GUI.hotkey('ctrl','r') # Images/7s.png . Mở cửa sổ Custom speed.
    LotusLib.waitColor((1027,596),rgb(97,222,208),20,5,200) # Images/7s.png (2) . Đợi nút OK hiện ra.
    GUI.click(943,460) # Images/7s.png (1) . Chọn vị trí field thời gian.
    LotusLib.delay(300)
    GUI.hotkey('ctrl','a')
    LotusLib.delay(300)
    GUI.hotkey('ctrl','c')
    LotusLib.delay(200)
    GUI.hotkey('ctrl','c')
    LotusLib.delay(200)
    GUI.click(1027,590) # Images/7s.png (2) . Click nút OK hiện ra.
    LotusLib.delay(200)
    GUI.click(1027,590) # Images/7s.png (2) . Click nút OK hiện ra.
    videoDuration = pyperclip.paste()
    LotusLib.delay(100)
    return videoDuration

  def extendDuration(self,durationFilmoraFormat):
    """
    \n#####################################################
    - Name: extendDuration
    - Function: Kéo dài thời gian duration của đối tượng.
    - Parameter: durationFilmoraFormat: HH:MM:SS:FR
    - Return: none
    \n#####################################################
    """
    GUI.click(340,576) # Images/6b.png (1). Click chọn vị trí biểu tượng đồng hồ Duration.
    LotusLib.delay(300)
    GUI.click(340,576) # Images/6b.png (1). Click chọn vị trí biểu tượng đồng hồ Duration.
    LotusLib.waitColor((965,555),rgb(97,222,208),20,5,200) # Images/6b.png (3). Đợi nút OK xuất hiện.
    GUI.click(1010,460) # Images/6b.png (2). Click ô nhập thời gian Duration.
    LotusLib.delay(300)
    GUI.hotkey('ctrl','a')
    LotusLib.delay(300)
    GUI.typewrite(durationFilmoraFormat)
    LotusLib.delay(500)
    GUI.click(965,555) # Images/6b.png (3).Vị trí nút OK.
    LotusLib.delay(200)
    GUI.click(965,555) # Images/6b.png (3).Vị trí nút OK.
    LotusLib.waitNotColor((965,555),rgb(110,239,225),20,5,200) # Images/6b.png (3). Đợi nút OK biến mất.
    
  def lowerThirdAdding(self,clipNumber,clipUserName,accumTimeMs,lastSubcribeTimeMs):
    """
    \n#####################################################
    - Name: lowerThirdAdding
    - Function: Gán Lower Third vào clip và chỉnh lại thông tin.
    - Parameter:
        - clipNumber: Số thứ tự của clip trong video.
        - clipUserName: Tên của người post.
        - accumTimeMs: Thời gian tích tụ từ đầu video đến trước clip đang xét.
        - lastSubcribeTimeMs: Thời gian của lần hiển thị subcribe trước đó.
    - Return: lastSubcribeTimeMs
    \n#####################################################
    """
    LotusLib.delay(100)
    GUI.hotkey('ctrl','v') # Images/5s.png . Dán Lower Third vào timeline.
    LotusLib.delay(500)
    GUI.hotkey('ctrl','alt','g') # Images/5s.png . Un-group cụm Lower Third.
    LotusLib.delay(500)
    redCursor = LotusLib.horFindColor(findColor=rgb(255,83,73),deltaFindColor=5,xFrom=100,xEnd=1890,xStep=10,yPos=597)
    lowerThirdLayer10 = [redCursor[0]-70,660]
    lowerThirdLayer9  = [redCursor[0]-70,660+32*1]
    lowerThirdLayer8  = [redCursor[0]-70,660+32*2]
    lowerThirdLayer7  = [redCursor[0]-70,660+32*3]
    lowerThirdLayer6  = [redCursor[0]-70,660+32*4]
    lowerThirdLayer5  = [redCursor[0]-70,660+32*5]
    
    #Kiểm tra nút subcribe
    if accumTimeMs - lastSubcribeTimeMs >= 300000: #Đã lâu hơn 5 phút chưa được subcribe
      logger.info("----- Kiểm tra nút subcribe: Gán Subcribe -----")
      lastSubcribeTimeMs = accumTimeMs
    else:
      #Xóa subcribe
      logger.info("----- Kiểm tra nút subcribe: Xóa Subcribe -----")
      GUI.click(lowerThirdLayer10)
      LotusLib.delay(300)
      GUI.press('delete')
      LotusLib.delay(500)
      GUI.click(lowerThirdLayer9)
      LotusLib.delay(300)
      GUI.press('delete')
      LotusLib.delay(500)
      
    # Cập nhật clip number
    # logger.info("----- Cập nhật clip number -----")
    # GUI.click(lowerThirdLayer7)
    # LotusLib.delay(300)
    # GUI.hotkey('alt','e')
    # LotusLib.waitColor((868,527),rgb(97,222,208),20,5,100) # Images/8b.png (1). Chờ nút OK hiện ra.
    # GUI.click(865,280) # Images/8b.png (2). Click vào field nhập liệu.
    # LotusLib.delay(300)
    # GUI.hotkey('ctrl','a')
    # LotusLib.delay(500)
    # GUI.typewrite(str(clipNumber))
    # LotusLib.delay(300)
    # GUI.click(868,527) # Images/8b.png (1). Click nút OK hiện ra.
    # LotusLib.delay(300)
    
    logger.info("----- Cập nhật clip username -----")
    pyperclip.copy(clipUserName)
    LotusLib.delay(100)
    pyperclip.copy(clipUserName)
    LotusLib.delay(100)
    GUI.click(lowerThirdLayer8)
    LotusLib.delay(300)
    GUI.hotkey('alt','e')
    LotusLib.waitColor((868,527),rgb(97,222,208),20,5,100) # Images/8b.png (1). Chờ nút OK hiện ra.
    GUI.click(865,280) # Images/8b.png (2). Click vào field nhập liệu.
    LotusLib.delay(300)
    GUI.hotkey('ctrl','a')
    LotusLib.delay(500)
    GUI.hotkey('ctrl','v')
    LotusLib.delay(300)
    GUI.click(868,527) # Images/8b.png (1). Click nút OK hiện ra.
    LotusLib.delay(300)
    
    #Đi đến cuối video
    GUI.hotkey('end')
    LotusLib.delay(300)
    return lastSubcribeTimeMs

  def updateCoverPage(self,title):
    """
    \n#####################################################
    - Name: updateCoverPage
    - Function: Cập nhật cho tiêu đề của ảnh bìa của video
    - Parameter:
        - title: Tên title sẽ đưa vào ảnh bìa
    - Return: none
    \n#####################################################
    """
    # Cập nhật clip number
    logger.info("----- Cập nhật title trang cover: %s -----",title)
    GUI.click(145,693) #Vị trí track cover
    LotusLib.delay(300)
    GUI.hotkey('alt','e')
    LotusLib.waitColor((868,527),rgb(97,222,208),20,5,100) # Images/8b.png (1). Chờ nút OK hiện ra.
    GUI.click(865,280) # Images/8b.png (2). Click vào field nhập liệu.
    LotusLib.delay(300)
    GUI.hotkey('ctrl','a')
    LotusLib.delay(500)
    GUI.typewrite(str(title))
    LotusLib.delay(300)
    GUI.click(868,527) # Images/8b.png (1). Click nút OK hiện ra.
    LotusLib.delay(300)

  def getUsernameFromMediaFile(self,fullPath):
    """
    \n#####################################################
    - Name: getUsernameFromMediaFile
    - Function: Lấy tên username,videoId và tên file từ MediaFile
    - Parameter:
        - fullPath: Tên filename với đầy đủ đường dẫn
    - Return: username,videoId,fileName
    \n#####################################################
    """
    filenameSplit = fullPath.replace('\\','/').split('/')
    filename = filenameSplit[len(filenameSplit)-1]
    
    fileName = filename.split(".mp4")[0]
    listParts = fileName.split("_")
    videoId = listParts[1]
    lenParts = len(listParts)

    username = ""
    if lenParts <= 2:
      username = "Tiktok"
    else:
      for i in range (2,lenParts):
        if i == 2:
          username += listParts[i]
        else:
          username += "_"+listParts[i]
    return username,videoId,fileName
    
  def deattachAudio(self):
    """
    \n#####################################################
    - Name: deattachAudio
    - Function: Tách audio khỏi clip và chờ tách hoàn thành
    - Parameter: none
    - Return: none
    \n#####################################################
    """
    redCursor = LotusLib.horFindColor(findColor=rgb(255,83,73),deltaFindColor=5,xFrom=100,xEnd=1919,xStep=10,yPos=597)
    GUI.hotkey('ctrl','alt','d') #Deattach Audio
    LotusLib.delay(100)
    color = LotusLib.getColor(redCursor[0]+30,985)
    n = 0
    while n < 10:
      # print(n)
      if color[1] < 50:
        LotusLib.delay(100)
        color = LotusLib.getColor(redCursor[0]+20,985)
        n += 1
      else:
        break
    LotusLib.delay(100)
      
  def calTrackTime (self,accumTimeMs):
    """
    \n#####################################################
    - Name: calTrackTime
    - Function: Trả về thời gian của track trong phần description.
    - Parameter: accumTimeMs: Thời gian cộng dồn của video tính
                              tới đầu track.
    - Return: thời gian nhảy đến track dạng MM:SS
    \n#####################################################
    """
    trackHour = int(accumTimeMs/3600000)
    if trackHour == 0:
      trackHourString = "00"
    else:
      if trackHour < 10:
        trackHourString = "0"+str(trackHour)
      else:
        trackHourString = str(trackHour)
    
    remainTime = int(accumTimeMs%3600000)
    trackMin = int(remainTime/60000)
    if trackMin == 0:
      trackMinString = "00"
    else:
      if trackMin < 10:
        trackMinString = "0"+str(trackMin)
      else:
        trackMinString = str(trackMin)
    
    remainTime = int((remainTime%60000)/1000)
    trackSec = remainTime
    if trackSec == 0:
      trackSecString = "00"
    else:
      if trackSec < 10:
        trackSecString = "0"+str(trackSec)
      else:
        trackSecString = str(trackSec)
    
    if trackHour == 0:
      return trackMinString+":"+trackSecString
    else:
      return trackHourString+":"+trackMinString+":"+trackSecString
    

  def exportDraftVideo(self,videoPath,videoName):
    """
    \n#####################################################
    - Name: exportDraftVideo
    - Function: Export video MP4 và lưu ở thư mục máy.
    - Parameter:\n
      + videoPath: Đường dẫn đến thư mục lưu video.
      + videoName: Tên video kèm đuôi.
    - Return: thời gian nhảy đến track dạng MM:SS
    \n#####################################################
    """
    delay(1000)
    # 1. Chọn loại hình để xuất
    GUI.hotkey('ctrl','e') # Images/13b.png (1). Mở cửa sổ Export
    delay(2000)
    GUI.click(1085,585) # Images/27b.png .Click nút "Continue" nếu hiện ra.
    LotusLib.waitColor((1270,690),rgb(97,222,208),10,10,100) # Images/13b.png (6). Đợi màu tại vị trí số 6.
    GUI.click(540,280) # Images/13b.png (2). Click vào vị trí nút Local
    delay(30)
    GUI.click(550,360) # Images/13b.png (3). Click vào vị trí MP4
    delay(200)
    # 2. Nhập tên video
    videoNameNoExt = videoName.split('.mp4')[0]
    copyToClipboard(videoNameNoExt)
    GUI.click(1140,360) # Images/13b.png (4) . Vị trí nhập tên video.
    GUI.hotkey('ctrl','a')
    delay(100)
    pasteFromClipboard() #Dán tên file video vào field
    # 3. Chọn đường dẫn Lưu
    copyToClipboard(videoPath)
    GUI.click(1155,405) # Images/13b.png (5). Chọn vào biểu tượng thiết đặt thư mục lưu video
    LotusLib.waitColor((30,1000),rgb(240,240,240),10,10,1000) #Chờ cho cửa sổ bung ra
    pasteFromClipboard() #Dán đường dẫn vào field
    delay(200)
    GUI.press('enter')
    delay(1000)
    GUI.click(1740,1005)
    delay(200)
    LotusLib.waitColor((1270,690),rgb(97,222,208),10,10,100) # Images/13b.png (6). Đợi màu tại vị trí số 6.
    # 3. Xuất video
    GUI.click(1300,690) # Images/13b.png (5). Click vào nút Export.
    # 4. Chờ xuất xong video
    LotusLib.waitColor((660,600),rgb(97,222,208),10,1800,1000) # Images/14b.png (1). Đợi nút xanh hiện ra tối đa trong 30 phút.
    GUI.press('esc')
    delay(500)
    GUI.press('esc')
    delay(500)
    GUI.press('home')
    delay(500)

  def publishVideoByFilmora(self,videoCation):
    """
    \n#####################################################
    - Name: publishVideoByFilmora
    - Function: Xuất bản các video lên Youtube
    - Parameter:\n
      + videoCation: Caption (title) của video
    - Return: None
    \n#####################################################
    """
    delay(1000)
    GUI.hotkey('ctrl','e') # Images/11b.png (1). Mở cửa sổ Export
    LotusLib.waitColor((1270,690),rgb(97,222,208),10,10,100) # Images/11b.png (5). Đợi màu tại vị trí số 5.
    GUI.click(680,280) # Images/11b.png (2). Click vào vị trí nút Youtube
    LotusLib.waitColor((550,350),rgb(255,0,0),10,100) # Images/11b.png . Chờ biểu tượng Youtube hiện ra.
    
    # 1. Nhập tên video
    copyToClipboard(videoCation)
    GUI.click(980,375) # Images/11b.png . Vị trí nhập tên video.
    GUI.hotkey('ctrl','a')
    delay(200)
    pasteFromClipboard()
    delay(200)
    
    # 2. Chọn Private Video
    # GUI.click(1330,540) # Images/11b.png .Click vào nút chọn kiểu Public/Private
    # delay(500)
    # GUI.click(1330,585) # Click chọn kiểu Private hiện ra.
    # delay(500)
    
    # 3. Upload
    GUI.click(1300,690) # Images/11b.png (5). Click vào nút Export.

    # 4. Chờ xuất xong video
    LotusLib.waitColor((1012,537),rgb(97,222,208),20,300,500) # Đợi nút xanh hiện ra tối đa trong 5 phút.
    GUI.press('esc')
    delay(500)
    GUI.press('esc')
    delay(500)
    GUI.press('esc')
    delay(500)

  def openBrowser(self,userAccColor,url=""):
    """
    #####################################################\n
    - Name: openBrowser\n
    - Function:\n
      + Mở maximize chrome theo màu của tài khoản Google Account được đăng nhập từ trước.\n
      + Đóng các cửa sổ thừa đang mở nếu có.\n
      + Sau đó vào url chỉ định.\n
      
    - Parameter:\n
      + userAccColor: Màu của Google Account đã được đăng nhập.\n
      + url: Đường dẫn URL cần chạy\n
    - Return: None\n
    - Ex: filmora.openBrowser(userAccColor,url='https://www.youtube.com')\n
    #####################################################
    """
    #1. Click mở cửa sổ
    chromePosXY = LotusLib.horFindColor(userAccColor,5,45,1600,2,1066)
    if LotusLib.checkColorWithCapture((chromePosXY[0],1076),rgb(171,61,65),25,200) == False: # Images/16s.png (3). Màu nên của cửa sổ trên cùng đang làm việc.
      GUI.click(chromePosXY) # Images/16s.png (1). Click vào icon để mở ra.
      LotusLib.waitColor((chromePosXY[0],1079),rgb(255,178,178),10,10,100) # Images/16s.png (2). Chờ lằn trắng xuất hiện (Chương trình được mở)
      LotusLib.waitColor((chromePosXY[0],1076),rgb(171,61,65)  ,25,10,100) # Images/16s.png (3). Màu nên của cửa sổ trên cùng đang làm việc.
      delay(500)
    
    #2. Bung Maximize
    if LotusLib.checkColorWithCapture((0,0),rgb(120,187,123),10,0) == True: #Cửa sổ đang là Maximize
      pass
    else:
      GUI.hotkey('alt','space')
      delay(500)
      GUI.press('x')
      LotusLib.waitColor((0,0),rgb(120,187,123),10,10,100) #Chờ cửa sổ Maximize
      
    #3. Đóng các tab đang mở thừa
    for i in range (0,10):
      if LotusLib.checkColorWithCapture((470,17),rgb(32,33,36),10,0) == True: # Đang có Tab chưa đóng.
        GUI.click(470,17)
        delay(300)
      else:
        break
      
    #4. Mở liên kết URL
    copyToClipboard(url)
    GUI.click(1300,50)
    delay(200)
    GUI.hotkey('ctrl','a')
    delay(300)
    pasteFromClipboard()
    delay(300)
    GUI.press('enter')
    delay(2000)
    GUI.press('enter') #Gõ lần nữa để OK nếu bị hỏi reload lại trang web
    delay(1000)
    
    #5. Kiểm tra trang web được load xong
    LotusLib.wait3Color((23 ,17),rgb(255,1,1),10,
                        (79,135),rgb(255,1,1),10,
                        (10,135),rgb(255,255,255),10,15,100) # Images/17s.png
    
  def webUploadVideo(self,filePath): 
    """
    \n#####################################################\n
    - Name: webUploadVideo
    - Function: Tải video lên Youtube
    - Parameter: filePath: Đường dẫn đến file.
    - Return: None.
    \n#####################################################
    """
    #1. Mở của sổ view code.
    GUI.rightClick(8,112)
    delay(500)
    GUI.press('up')
    delay(300)
    GUI.press('enter')
    delay(500)
    LotusLib.waitColor((1353,115),rgb(241,243,244),5,20,500)
    
    #2. chọn nút upload
    GUI.click(1225,135) # Images/18s.png (1). Click nút Create
    LotusLib.waitColor((1270,175),rgb(255,255,255),2,10,100) # Images/18s.png (2). Chờ bảng hiện ra
    GUI.click(1270,175)
    delay(500)
    
    #3. Chờ cửa sổ popup để upload hiện ra
    LotusLib.wait3Color((1340,115),rgb(115,115,115),10,
                        (1100,550),rgb(255,255,255),10,
                        ( 680,700),rgb(  6,95 ,212),10,15,100) # Images/19b.png .Chờ cửa sổ popup hiện ra
    
    #4. Chọn file video upload
    copyToClipboard(filePath)
    GUI.click(677,688) # Images/19b.png (3)
    LotusLib.waitColor((30,1010),rgb(240,240,240),10,15,500)
    pasteFromClipboard()
    delay(500)
    GUI.press('enter')

    
  def waitAndFindVideoFault (self,outputPath):
    """
    \n#####################################################\n
    - Name: waitAndFindVideoFault
    - Function: Kiểm tra bản quyền và trả về list thứ tự video bị vi phạm
    - Parameter: outputPath: Đường dẫn đến thư mục output
    - Return: listFaultVideoOrder: list thứ tự video vi phạm bản quyền. Ex: [4, 11, 12, 13]
    \n#####################################################
    """
    CHECKING_WAIT = 1
    CHECKING_NG = 2
    CHECKING_OK = 3
    CHECKPOS = (788,271)
    
    #1. Chờ cho video được up xong và kiểm duyệt bản quyền hoàn tất.
    logger.info('#--- 1. Chờ cho video được up xong và kiểm duyệt bản quyền hoàn tất. ---')
    checkStatus = CHECKING_WAIT
    LotusLib.waitColor(CHECKPOS,rgb(204,204,204),10,15,1000) #Chờ cửa sổ popup check bản quyền hiện ra
    if LotusLib.waitNotColor(CHECKPOS,rgb(204,204,204),10,900,2000) != False: #Đợi dấu tròn xám biến mất trong 900.
      # GUI.screenshot().save("KetQuaKiemTra.png")
      LotusLib.waitNotColor(CHECKPOS,rgb(204,204,204),10,900,1000)
      LotusLib.waitNotColor(CHECKPOS,rgb(204,204,204),10,900,100)
      if LotusLib.checkColorWithCapture(CHECKPOS,rgb(7,96,212),10,0) == True: checkStatus = CHECKING_OK
      if LotusLib.checkColorWithCapture(CHECKPOS,rgb(204,1,1 ),10,0) == True: checkStatus = CHECKING_NG
    
    #2. Xử lý từng trường hợp lỗi
    if checkStatus == CHECKING_NG: # rgb(204,1,1 )
      self.faultVideoNum += 1
      logger.info('#--- 2. Video bị vi phạm bản quyền!!! ---')
      GUI.click(788,262) # Images/21s.png (1). Click vào nút báo vị trí báo lỗi bản quyền.
      LotusLib.waitColor((1057,367),rgb(255,255,255),1,3,100) # Images/21s.png (2). Chờ vị trí số xuất hiện.
      GUI.click(1061,421) # Images/21s.png (2). Click vào nút SEE DETAIL
      LotusLib.waitColor((1086,917),rgb(6,95,212),10,10,2000) # Images/22s.png (3). Chờ nút DONE hiện ra.
      GUI.screenshot().save(outputPath+"FaultVideoCapture_"+str(self.faultVideoNum)+".png")
      
      
      logger.info('#--- 2.1 Unfold các video bị cho là vi phạm ra ---')
      GUI.moveTo(1130,300) # Images/24s.png (1).Di chuyển chuột vào vùng có thể cuộn chuột được.
      delay(200)
      GUI.scroll(-2000) #Scroll xuống cuối cùng
      delay(500)
      
      # Unfold các video ẩn
      for i in range (0,5): #Lặp lại tối đa 5 lần.
        faultList = LotusLib.findAllImageOnScreen('G:/Biz/YoTu/TikTop/TikTop_Filmora/Images/23s.png')
        faultList.reverse() # Đảo ngược thứ tự để click chuột từ dưới lên trên
        if len(faultList) != 0: #Còn video vi phạm
          for faultPos in faultList:
            GUI.click(faultPos)
            delay(1000)
          GUI.scroll(500) #Scroll lên 500 đơn vị
        else:
          break
        
      logger.info('#--- 2.2 Copy HTML code ---')
      htmlCode = self.getCode()
      GUI.click(1114,920) #Click nút DONE của cửa sổ SEE DETAIL
      delay (200)
      GUI.press('esc') #Thoát cửa sổ SEE DETAIL
      
      logger.info('#--- 2.3 Xác định số thứ tự video lỗi ---')
      listFaultVideoOrder = self.htmlParserFindFaultVideo(htmlCode,outputPath)
      return listFaultVideoOrder
      
    if checkStatus == CHECKING_OK: # rgb(7,96,212)
      logger.info('#--- 2. Không có video bị vi phạm bản quyền. OK. ---')
      listFaultVideoOrder = list()
      return listFaultVideoOrder
    
    if checkStatus == CHECKING_WAIT: # rgb(204,204,204)
      logger.info('#--- 2. Timeout. Hết thời gian đợi check ---')
      listFaultVideoOrder = list()
      return listFaultVideoOrder
      
  #########################################################
  # Name: getCode
  # Function: Kiểm tra mở của sổ xem code và load hết code
  #           rồi trả về code HTML
  # Parameter: None
  # Return: Trả về htmlCode dạng string
  #########################################################
  def getCode(self):
    GUI.click(1451,116) #Click vào tab Element. Images/26s.png
    LotusLib.delay(300)
    GUI.moveTo(1830,200) #Di chuyển chuột vào vùng code có thể cuộn chuột được.
    delay(200)
    GUI.scroll(2000) #Scroll lên trên cùng
    delay(1000)
    logger.info("--- Mở ra cửa sổ copy element ---")
    GUI.click(1400,140) #Click vào vị trí thẻ <!DOCUMENT html>.
    LotusLib.waitColor((1700,140),rgb(207,232,252),20,15) # đợi dòng được chọn
    LotusLib.delay(500)
    GUI.press('down')
    LotusLib.delay(500)
    GUI.press('down')
    LotusLib.delay(500)
    GUI.press('down')
    LotusLib.delay(500)
    GUI.hotkey('shift','f10')
    LotusLib.delay(1000)
    GUI.press('c')
    LotusLib.delay(500)
    GUI.press('enter')
    LotusLib.delay(500)
    GUI.press('down') #Chọn nút copy
    LotusLib.delay(500)
    GUI.press('enter') #Chọn "copy element"
    LotusLib.delay(1000)
    htmlCode = pasteFromClipboardToVar() #Gán html code từ clipboard vào biến
    htmlCode = htmlCode.replace('\n',' ')
    return htmlCode
      
  def htmlParserFindFaultVideo(self,htmlCode,outputPath):
    soup = BeautifulSoup(htmlCode, 'html.parser')

    faultList = list()
    logger.info("Fault Time:")
    for eachPost in soup.select(".match-segment-detail"):
      timeRangeFault = re.sub(r"[\n\t\s\[a-z\]\[A-Z\]]*", "", eachPost.text)
      logger.info(timeRangeFault)
      
      #Xác định thời điểm
      timeMark = timeRangeFault.split('–')
      beginTime = timeMark[0].split(':')
      endTime = timeMark[1].split(':')
      if len(beginTime) == 3: beginTimeSec = int(beginTime[0])*3600 + int(beginTime[1])*60 + int(beginTime[2])
      if len(beginTime) == 2: beginTimeSec = int(beginTime[0])*60   + int(beginTime[1])
      if len(beginTime) == 1: beginTimeSec = int(beginTime[0])
      if len(endTime)   == 3: endTimeSec   = int(endTime[0])*3600 + int(endTime[1])*60 + int(endTime[2])
      if len(endTime)   == 2: endTimeSec   = int(endTime[0])*60   + int(endTime[1])
      if len(endTime)   == 1: endTimeSec   = int(endTime[0])
      midTimeSec = (beginTimeSec + endTimeSec)/2
      # print (beginTimeSec,endTimeSec,midTimeSec)
      faultList.append(midTimeSec)
    # print(faultList)
    # print('=======================================')
    descriptionFile = open(outputPath+"description.txt", "r", encoding="utf-8")
    descriptLines = descriptionFile.readlines()
    descriptionFile.close()
    descriptTimeList = list()
    for line in descriptLines:
      timeMark = line.split(']')[1].split(' ')[1].split(':')
      if len(timeMark) == 3: timeMarkSec = int(timeMark[0])*3600 + int(timeMark[1])*60 + int(timeMark[2])
      if len(timeMark) == 2: timeMarkSec = int(timeMark[0])*60   + int(timeMark[1])
      if len(timeMark) == 1: timeMarkSec = int(timeMark[0])
      descriptTimeList.append(timeMarkSec)
    # print (descriptTimeList)
    # print('=======================================')
    faultClipOrderList = list()
    for checkClip in faultList:
      number = 0
      for clipOrder in descriptTimeList:
        if checkClip >= clipOrder:
          number += 1
        else:
          break
      faultClipOrderList.append(number)
    # print (faultClipOrderList)
    faultClipOrderList.sort()
    logger.info("Fault Video Order: "+str(faultClipOrderList))
    return faultClipOrderList
    
  def filmoraDelFaultClip(self,listFaultVideoOrder):
    """
    \n#####################################################\n
    - Name: filmoraDelFaultClip
    - Function: Xóa các clip vi phạm trong Filmora.
    - Parameter: listFaultVideoOrder: Danh sách thứ tự các clip vi phạm.
    - Return: None
    \n#####################################################
    """
    #Trở về vị trí đầu video thứ nhất.
    logger.info("--- Trở về vị trí đầu clip thứ nhất. ---")
    GUI.press('esc')
    delay(500)
    GUI.press('esc')
    delay(500)
    GUI.click(45,1015)
    delay(100)
    GUI.hotkey('home')
    delay(1000)
    GUI.press('down')

    #Xóa các clip lỗi
    logger.info("--- Xóa các clip lỗi ---")
    curClipNum = 1
    for faultClipNum in listFaultVideoOrder:
      #Di chuyển con trỏ đến clip bị lỗi
      logger.debug("Clip Num: "+str(faultClipNum))
      # logger.debug("--- Di chuyển con trỏ đến clip bị lỗi ---")
      while curClipNum < faultClipNum:
        GUI.press('down')
        delay(500)
        GUI.press('down')
        delay(500)
        GUI.press('down')
        delay(500)
        GUI.press('down')
        delay(500)
        GUI.press('up')
        delay(500)
        curClipNum += 1
      #Xóa clip lỗi
      # logger.debug("--- Xóa clip lỗi ---")
      redCursor = LotusLib.horFindColor(findColor=rgb(255,83,73),deltaFindColor=5,xFrom=100,xEnd=1910,xStep=10,yPos=597)
      # print("Cursor: "+str(redCursor))
      for i in range (0,11):
        GUI.click(redCursor[0]+25,660+32*i)
        delay(250)
        GUI.click(redCursor[0]+25,652+32*i)
        delay(250)
        GUI.press('delete')
      curClipNum += 1
      
    #Trở về đầu timeline để tránh lỗi xóa file sau này
    delay(500)
    GUI.press('home')
    delay(500)
    
  def remakeDescriptionAndMoveFaultVideo(self,workingDir,listFaultVideoOrder=list()):
    logger.info("--- A. Tạo file description mới ---")
    outputDir = workingDir+"Output\\"
    descriptionFile = open(outputDir+"description.txt", "r", encoding="utf-8")
    #[ 1] 00:05 - ducminhts                  https://www.tiktok.com/@ducminhts/7004450018807598362
    #[ 2] 01:16 - vanthong_1999              https://www.tiktok.com/@vanthong_1999/7004405965470649626
    #[ 3] 01:32 - tiepnguyen0420             https://www.tiktok.com/@tiepnguyen0420/7004602056543587611
    #[ 4] 01:47 - thichlanhich0707           https://www.tiktok.com/@thichlanhich0707/7004495334894243099
    descAllLines = descriptionFile.readlines()
    descriptionFile.close()
    # print(descAllLines)
    videoTimeList     = list()
    videoIdList       = list()
    videoUserList     = list()
    videoFileNameList = list()
    logger.info("--- Parsing dữ liệu từ description cũ ---")
    for descLine in descAllLines:
      videoTime = re.sub(r'.*].(.*?) -.*',r'\1',descLine).strip()
      videoId = re.sub(r'.*/(.*)',r'\1',descLine).strip()
      videoUser = re.sub(r'.*- (.*) .*',r'\1',descLine).strip()
      videoFileName = re.sub(r'.* (.*)',r'\1',descLine).strip()
      videoTimeSplit = videoTime.split(':')
      if len(videoTimeSplit) == 3: videoTimeSecMark = int(videoTimeSplit[0])*3600+int(videoTimeSplit[1])*60+int(videoTimeSplit[2])
      if len(videoTimeSplit) == 2: videoTimeSecMark = int(videoTimeSplit[0])*60  +int(videoTimeSplit[1])
      videoTimeList.append(videoTimeSecMark)
      videoIdList.append(videoId)
      videoUserList.append(videoUser)
      videoFileNameList.append("https://"+videoFileName)
      
    # print (videoTimeList)
    # print (videoIdList)

    #Build new description file
    logger.info("--- Chỉnh sửa thông tin cho description mới ---")
    for faultId in listFaultVideoOrder:
      newVideoTimeList = list()
      shiftTime = 0
      videoFaultFlag = 0
      for i in range(0,len(videoTimeList)):
        # print (i)
        if i != faultId-1: #i không phải vị trí video lỗi
          if videoFaultFlag == 0:
            newVideoTimeList.append(videoTimeList[i])
          else:
            newVideoTimeList.append(videoTimeList[i]-shiftTime)
        else: #i đang là vị trí video lỗi
          videoFaultFlag = 1
          if i != len(videoTimeList)-1: shiftTime = videoTimeList[i+1]-videoTimeList[i]
          newVideoTimeList.append(videoTimeList[i])
      videoTimeList = newVideoTimeList
    #Loại bỏ các phần tử video lỗi trong list
    listFaultVideoOrder.reverse()
    for faultId in listFaultVideoOrder:
      videoTimeList.pop(faultId-1)
    # print (videoTimeList)
    listFaultVideoOrder.reverse()

    #Tạo list các videoId lỗi
    videoIdFaultList = list()
    for faultId in listFaultVideoOrder:
      videoIdFaultList.append(videoIdList[faultId-1])
    # print(videoIdFaultList)

    #Loại bỏ các phần tử video lỗi trong videoIdList,videoUserList,videoFileNameList
    listFaultVideoOrder.reverse()
    for faultId in listFaultVideoOrder:
      videoIdList.pop(faultId-1)
      videoUserList.pop(faultId-1)
      videoFileNameList.pop(faultId-1)
    # print(videoIdList)
    # print(videoUserList)
    # print(videoFileNameList)
    listFaultVideoOrder.reverse()

    #Convert videoTimeList to MM:SS
    videoTimeListMMSS = list()
    for videoTime in videoTimeList:
      videoTimeMMSS = self.calTrackTime(videoTime*1000)
      videoTimeListMMSS.append(videoTimeMMSS)
    # print (videoTimeListMMSS)

    #Make new description file
    logger.info("--- Tạo file description mới ---")
    if os.path.exists(outputDir+"description_"+str(self.faultVideoNum)+".txt"):
      os.remove(outputDir+"description_"+str(self.faultVideoNum)+".txt")
    os.rename(outputDir+"description.txt",outputDir+"description_"+str(self.faultVideoNum)+".txt")
    descriptionFile = open(outputDir+"description.txt", "w", encoding="utf-8")
    for i in range(0,len(videoIdList)):
      descriptionFile.write("["+str(i+1).rjust(2)+"] "+videoTimeListMMSS[i].ljust(5)+" - "+videoUserList[i].ljust(27)+videoFileNameList[i]+"\n")
    descriptionFile.close()
    #Di chuyển các video vi phạm vào thư mục Output/FaultVideo
    logger.info("--- B. Di chuyển các video lỗi vào thư mục Output\FaultVideo ---")
    #Kiểm tả file nếu co tồn tại thì di chuyển
    listFiles = os.listdir(workingDir+"Input\\")
    # print(listFiles)

    for faultVideoId in videoIdFaultList:
      for fileName in listFiles:
        if re.compile(faultVideoId).search(fileName) != None: #Có videoId tìm thấy trong list file
          #Di chuyển fileName nếu nó tồn tại
          print("Di chuyển file: "+fileName)
          if os.path.exists(workingDir+'Input\\'+fileName) == True:
            shutil.move(workingDir+'Input\\'+fileName, workingDir+'Output\FaultVideo\\'+fileName)
            
  def setVpnOper(self,vpnOper = 0):
    sql = "UPDATE tiktop_config_vpn SET vpn_enable = '"+str(vpnOper)+"'"
    myCursor.execute(sql)
    myDb.commit()
    
  #########################################################
  # Name: mySqlCloseConnection
  # Function: Đóng kết nối với MySQL
  # Parameter: none
  # Return: none
  #########################################################
  def mySqlCloseConnection(self):
    myDb.close()
    myDbZalo.close()

  #########################################################
  # Name: task3GetVolNum
  # Function: Trả về giá trị Vol num - 1 chỉ dành cho task3
  # Parameter: none
  # Return: Vol num - 1
  #########################################################
  def task3GetVolNum(self):
    sql = "SELECT * FROM tiktop_config LIMIT 1"
    myCursor.execute(sql)
    readData = myCursor.fetchall()[0] 
    return int(readData['vol_num'])-1

  #########################################################
  # Name: task3GetTaskEnable
  # Function: Trả về giá trị task enable của task 3
  # Parameter: none
  # Return: task3_ena
  #########################################################
  def task3GetTaskEnable(self):
    sql = "SELECT * FROM tiktop_config LIMIT 1"
    myCursor.execute(sql)
    readData = myCursor.fetchall()[0] 
    return int(readData['task3_ena'])
  
  #########################################################
  # Name: task3GetRunFlag
  # Function: Trả về cờ cho phép task3 hoạt động hay không.
  # Parameter: none
  # Return: task 3 running flag
  #########################################################
  def task3GetRunFlag(self):
    sql = "SELECT * FROM tiktop_task_mon LIMIT 1"
    myCursor.execute(sql)
    readData = myCursor.fetchall()[0] 
    return int(readData['task3_running_flag'])

  def task3ClearRunFlag(self):
    sql = "UPDATE tiktop_task_mon SET task3_running_flag = 0"
    myCursor.execute(sql)
    myDb.commit()
  
  def sendToTxBufferQueue(self,send_to,mess_type,mess_data,send_delay_sec=0,note='tiktop_vn_script'):
    send_timestamp_sec = int(datetime.datetime.now().timestamp() + send_delay_sec)
    send_schedule = datetime.datetime.fromtimestamp(send_timestamp_sec)
    # Register to Tx Buffer Queue
    sql = "INSERT INTO tx_buffer (send_to, uid, mess_type, mess_data,send_timestamp_sec,send_schedule,note) VALUES (%s, %s, %s, %s, %s, %s,%s)"
    val = (send_to, str(randint(0,1000000000)) ,mess_type,mess_data,str(send_timestamp_sec),str(send_schedule),note)
    myCursorZalo.execute(sql, val)
    myDbZalo.commit()
    
  #########################################################
  # Name: getVideoCaption
  # Function: 
  # Parameter: None
  # Return: None
  #########################################################
  def getVideoCaption (self,volNum, videoId):
    sql = "SELECT * FROM tiktop_vol"+str(volNum)+" WHERE video_id = '"+str(videoId)+"'"
    myCursor.execute(sql)
    readData = myCursor.fetchall()[0]
    return readData['clip_caption']
  
  
    
class youtubeShort():
  def __init__(self):
    self.faultVideoNum = 0

  #########################################################
  # Name: loadMysqlShortCfg
  # Function: Load dữ liệu config cho Short từ MySQL
  # Parameter: None
  # Return: None
  #########################################################
  def loadMysqlShortCfg (self):
    sql = "SELECT * FROM tiktop_config_short LIMIT 1"
    myCursor.execute(sql)
    readData = myCursor.fetchall()[0] 
    shortCfg.runEna = readData['run_ena']
    shortCfg.runEveryMin = readData['run_every_min']
    shortCfg.maxPostEachTime = readData['max_post_each_time']
    shortCfg.delAfterDay = readData['del_after_day']
    shortCfg.zaloInformEna = readData['zalo_inform_ena']

  def waitYoutubeChecking (self):
    """
    \n#####################################################\n
    - Name: waitYoutubeChecking\n
    - Function: Đợi Youtube kiểm tra bản quyền.\n
    - Parameter: None\n
    - Return:\n
      + True: nếu không có vi phạm
      + False: nếu vi phạm
    \n#####################################################
    """
    CHECKPOS = (788,271)
    #1. Chờ cho video được up xong và kiểm duyệt bản quyền hoàn tất.
    logger.info('#--- Chờ cho video được up xong và kiểm duyệt bản quyền hoàn tất. ---')
    checkStatus = False
    LotusLib.waitColor(CHECKPOS,rgb(204,204,204),10,15,1000) #Chờ cửa sổ popup check bản quyền hiện ra
    if LotusLib.waitNotColor(CHECKPOS,rgb(204,204,204),10,900,2000) != False: #Đợi dấu tròn xám biến mất trong 900.
      LotusLib.waitNotColor(CHECKPOS,rgb(204,204,204),10,900,1000)
      LotusLib.waitNotColor(CHECKPOS,rgb(204,204,204),10,900,100)
      if LotusLib.checkColorWithCapture(CHECKPOS,rgb(7,96,212),10,0) == True: checkStatus = True
      if LotusLib.checkColorWithCapture(CHECKPOS,rgb(204,1,1 ),10,0) == True: checkStatus = False
    return checkStatus
  
  def appendPublishVideoShort(self,videoID):
    """
    \n#####################################################\n
    - Name: appendPublishVideoShort
    - Function: Đưa video id của video được đăng tải vào danh sách MySQL.
    - Parameter: videoID cần đưa lên.
    - Return: None
    \n#####################################################
    """
    sql = "INSERT tiktop_short_published SET video_id = '"+str(videoID)+"'"
    myCursor.execute(sql)
    myDb.commit()
    
  def checkPublishVideoShort(self,videoID):
    """
    \n#####################################################\n
    - Name: checkPublishVideoShort
    - Function: Kiểm tra video id của video có trong danh sách
                đã publish trước đây hay chưa.
    - Parameter: videoID cần kiểm tra
    - Return:\n
      + True: Video đã được đăng trước đây.
      + False: Video chưa được đăng.
    \n#####################################################
    """
    sql = "SELECT * FROM tiktop_short_published WHERE video_id = '"+str(videoID)+"'"
    myCursor.execute(sql)
    readData = myCursor.fetchall()
    if len(readData) > 0:
      return True
    else:
      return False
    
  def genShortsReportImage(self,totalNum=0,publishedNum=0,saveFilePath=""):
    """
    \n#####################################################\n
    - Name: genShortsReportImage
    - Function: Tạo ra ảnh report về số lượng video xử lý và published.
    - Parameter:\n
      + totalNum: Tổng số clip cần xử lý.
      + publishedNum: Tổng số clip đã được xuất bản.
      + saveFilePath: Đường dẫn lưu file.
    - Return: None
    \n#####################################################
    """
    from PIL import Image, ImageDraw, ImageFont
    import os
    fontsFolder = 'C:\Windows\Fonts\\'
    # arialFont = ImageFont.truetype(os.path.join(fontsFolder, 'arial.ttf'), 210)
    comicFont = ImageFont.truetype(os.path.join(fontsFolder, 'comicbd.ttf'), 210)

    im = Image.open("Images/shortsReport.png")
    draw = ImageDraw.Draw(im)
    draw.text((530, -20), str(totalNum), fill='red', font=comicFont)
    draw.text((530,190), str(publishedNum), fill='red', font=comicFont)
    im.save(saveFilePath)