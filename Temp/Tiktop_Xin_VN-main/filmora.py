from filmoraApi import *
from Global.loggingSetup import *
import time
import os
import sys
import subprocess
RUN_BY_HAND   = 1
RUN_BY_SCRIPT = 2
# NOT_APPROVED  = 3
# APPROVED_TO_PUBLISH = 4

filmora = filmoraApi() #Instant of class

#Xác định kiểu chạy khi gọi script python này
runMode = RUN_BY_SCRIPT
logger.info(sys.argv)
if (len(sys.argv) >= 2):
  if sys.argv[1] == 'RUN_BY_HAND':
    logger.info("RUN_BY_HAND")
    runMode = RUN_BY_HAND
    
# #Xác định 
# approveToPublish = NOT_APPROVED
# if (len(sys.argv) >= 3):
#   if sys.argv[2] == 'APPROVED_TO_PUBLISH':
#     logger.info("APPROVED_TO_PUBLISH")
#     approveToPublish = APPROVED_TO_PUBLISH
    
#Configure for Task Killer
nodeName = platform.uname()[1]
curDay  = datetime.datetime.now()
logPicName = 'Logs\Logfile_'+str(nodeName)+'_'+str(curDay.day)+str(curDay.strftime("%b"))+'_'+str(curDay.strftime("%H.%M.%S"))
LotusLib.taskKillerStart(threadID = 1, threadName = 'TaskKiller',logPathAndPrefixName = logPicName,pythonKillHotkey = 'shift+f12',vscodeKillHotkey = 'shift+f5')

try:
  accumTimeMs = 5000
  lastSubcribeTimeMs = 0
  clipNumber = 0
  clipUserName = "Tiktok"

  #Xác định số vol number
  #1. Nếu là chạy bằng tay thì giá trị vol number bằng giá trị vol num của thư mục đang chạy. VD: /Post_Vol16
  #2. Nếu là chạy bằng script thì vol number sẽ bằng Vol_num - 1 từ MySQL
  if runMode == RUN_BY_HAND:
    Post_Vol = int(os.getcwd().split('Post_Vol')[1])
  else: # runMode == RUN_BY_SCRIPT:
    Post_Vol = filmora.task3GetVolNum()
  #Xác định các đường dẫn làm việc
  filmoraDir = 'G:\Biz\YoTu\TikTop\TikTop_Filmora\\'
  rootDir = "G:\Biz\YoTu\TikTop\TikTopData\PostData_VN\\"
  workingDir = rootDir+"Post_Vol"+str(Post_Vol)+"\\"
  inputDir = workingDir+"Input\\"
  outputDir = workingDir+"Output\\"
  
  if os.path.exists(rootDir+"Post_Vol"+str(Post_Vol)) == False:
    shutil.copytree(rootDir+"000_Post_Master",rootDir+"Post_Vol"+str(Post_Vol))
    logger.error("=== KHÔNG TỒN TẠI THƯ MỤC POST_VOL%s => TẠO MỚI RỒI THOÁT ===",str(Post_Vol))
    exit() # Go to Finally
  if len(os.listdir(inputDir)) == 0:
    logger.error("=== THƯ MỤC INPUT CỦA POST_VOL%s KHÔNG CÓ DỮ LIỆU ===",str(Post_Vol))
    exit() # Go to Finally
    
  ##############################
  # BẮT ĐẦU CHƯƠNG TRÌNH CHÍNH #
  ##############################
  #Tạm ngừng thay đổi VPN
  logger.info(">>>>> Tạm ngừng thay đổi VPN <<<<<")
  filmora.setVpnOper(0)
  # if approveToPublish == NOT_APPROVED:
  shutil.copy(rootDir+"000_Post_Master\\Video_Make.wfp",workingDir)
  #Gửi thông báo bắt đầu chạy Filmora qua Zalo
  logger.info(">>>>> Gửi thông báo bắt đầu chạy Filmora qua Zalo <<<<<")
  filmora.sendToTxBufferQueue(send_to='0908549354',mess_type='image',mess_data='Z:\ZaloBot\ZaloBot_running\Images\FilmoraStart.jpg',send_delay_sec=0,note='Filmora Start')
  #Bắt đầu chạy Filmora
  logger.info(">>>>> STEP 1: Mở cửa sổ Filmora <<<<<")
  app = "C:\Program Files\Wondershare\Filmora9\Wondershare Filmora9.exe"
  file = "G:\Biz\YoTu\TikTop\TikTopData\PostData_VN\Post_Vol"+str(Post_Vol)+"\Video_Make.wfp"
  logger.info(file)
  pid = subprocess.Popen([app, file]).pid

  #Kiểm tra chương trình đã mở và click vào
  posFilmoraIcon = LotusLib.horFindColor (rgb(81,224,191),10,50,1919,6,1062)
  LotusLib.waitColor((posFilmoraIcon[0],1079),rgb(255,114,0),20,40,500)
  GUI.click(posFilmoraIcon)
  LotusLib.waitColor((28,15),rgb(80,227,194),10,20,100) #Chờ icon chương trình trên góc TopLeft hiện ra.
  GUI.click(1160,545) # Images/32s.png .Click nút "NO" ở phần hỏi có chạy lại backup?
  delay(2000)
  #Kiểm tra xem có yêu cầu update không?
  GUI.click(1222,650) # Images/30s.png .Click nút bỏ qua cập nhật phiên bản mới.
  delay(1000)

  # if approveToPublish == NOT_APPROVED:
  logger.info("approveToPublish = NOT_APPROVED")
  logger.info(">>>>> STEP 2: Tiền xử lý khung view, lower third <<<<<")
  logger.info("----- 2.1: Zoom timeline level 6 -----")
  for i in range (0,10):
    GUI.click(1826,575) # Images/3s.png (1). Vị trí nút (+) tăng level của zoom timeline.
    LotusLib.delay(300)
  for i in range (0,4):
    GUI.click(1700,575) # Images/3s.png (2). Vị trí nút (-) tăng level của zoom timeline.
    LotusLib.delay(500)
  logger.info("----- 2.2: Vào thẻ Media>VideoPic -----")
  GUI.click(25,55)  # Images/4s.png .Vị trí nút Media.
  LotusLib.delay(1000)
  GUI.click(80,106) # Images/4s.png .Vị trí dòng VideoPic.  
  LotusLib.delay(500)
  logger.info("----- 2.3: Đưa cụm Lower Third vào clipboard -----")
  GUI.click(1915,1018) #Scroll thanh cuộn các lớp xuống dưới cùng
  LotusLib.delay(500)
  GUI.press('home')
  LotusLib.delay(500)
  GUI.press('down')
  LotusLib.delay(500)
  GUI.click(200,750) # Images/5s.png .Click chọn cụm Lower Third.
  LotusLib.delay(500)
  GUI.hotkey('ctrl','x') # Images/5s.png . Đưa cụm Lower Third vào clipboard.
  LotusLib.delay(500)
  # logger.info("----- 2.4: Đặt lại ngày tháng cho trang bìa -----")
  # dayPublish = datetime.datetime.now().strftime("%d/%m")
  # filmora.updateCoverPage(title=dayPublish)
  
  logger.info(">>>>> STEP 3: Đưa tất cả các clip vào <<<<<")
  logger.info("----- 3.1: Lấy danh sách các clip (.mp4) -----")
  listFile = filmora.getFileList(inputDir,'mp4')
  logger.info("Số file: %s",len(listFile))
  logger.info("----- 3.2: Đưa file vào timeline -----")
  descriptionFile = open(outputDir+"description.txt", "w", encoding="utf-8")
  for i in range(0,len(listFile)):
    GUI.click(1915,1018) #Scroll thanh cuộn các lớp xuống dưới cùng
    LotusLib.delay(200)
    logger.info("----- 3.2.1: Import video -----")
    # print(startClipPos)
    filmora.selectFilmoraLayer(layerSelect = 3)
    if filmora.importMedia(pathFile=listFile[i],replaceFileType='mp4') == True:
      filmora.insertMediaToTimeline()
      filmora.upKeyRepeat(time=1)
      filmora.deattachAudio()
      videoInfo = filmora.getVideoInfo(pathFile=listFile[i])
      videoDuration = filmora.filmoraGetClipDuration()
      pathCommentPic = listFile[i].replace('.mp4','.png')
      if path.exists(pathCommentPic) == True: #Nếu có file ảnh comment
        logger.info("----- 3.2.2: Scale video và dời vị trí clip -----")
        filmora.scaleAndMoveClip(videoInfo)
        logger.info("----- 3.2.3: Import comment -----")
        filmora.selectFilmoraLayer(layerSelect = 2)
        if filmora.importMedia(pathFile=listFile[i],replaceFileType='png') == True:
          filmora.insertMediaToTimeline()
          filmora.upKeyRepeat(time=1)
          filmora.extendDuration(videoDuration)
          logger.info("----- 3.2.4: Dời vị trí comment -----")
          filmora.moveComment()
      logger.info("----- 3.2.5: Chỉnh Lower Third -----")
      clipNumber += 1
      filmora.selectFilmoraLayer(layerSelect = 4)
      clipUserName,clipId,fileName = filmora.getUsernameFromMediaFile(listFile[i])
      lastSubcribeTimeMs = filmora.lowerThirdAdding(clipNumber,clipUserName,accumTimeMs,lastSubcribeTimeMs)
      logger.info("----- 3.2.6: Gán thông tin vào description file -----")
      # Ex: [ 1]  0:34 - minhsangst83           https://www.tiktok.com/@minhsangst83/...
      trackTime = filmora.calTrackTime(accumTimeMs)
      # link = "https://www.tiktok.com/@"+clipUserName+"/"+clipId
      descriptionFile.write("["+str(clipNumber).rjust(2)+"] "+trackTime.ljust(5)+" - "+clipUserName.ljust(27)+fileName+"\n")

      #Cộng dồn thời gian của video
      if videoInfo['durationMs'] < 8000: #Giây là thời gian tối thiểu để chạy Lower Third.
        accumTimeMs += 8000
      else:
        accumTimeMs += videoInfo['durationMs']
  descriptionFile.close()
  #Tạo backup Filmora và description
  shutil.copyfile(workingDir+'Video_Make.wfp', workingDir+'Video_Make_full.wfp')
  shutil.copyfile(outputDir+'description.txt', outputDir+'description_full.txt')
  # else: #approveToPublish = APPROVED_TO_PUBLISH
  #   logger.info("approveToPublish = APPROVED_TO_PUBLISH")

  ##################################
  ##### UPLOAD YOUTUBE TESTING #####
  ##################################
  while True:
    logger.info(">>>>> YOUTUBE UPLOAD TESTING <<<<<")
    videoName = "Video_Tong_Hop_"+str(Post_Vol)+".mp4"
    if os.path.exists(outputDir+videoName) == True:
      os.remove(outputDir+videoName)
        
    # 1. Export Video
    filmora.exportDraftVideo(outputDir,videoName)
    
    # 2. Upload Draft Video to Youtube
    userAccColor = rgb(236,66,123) # Images/15s.png .Account HaiNganTongHop
    filmora.openBrowser(userAccColor,url='https://studio.youtube.com/channel/UCHkipO9lRx4na1JYMSrYS7g')
    filmora.webUploadVideo(outputDir+videoName)

    listFaultVideoOrder = filmora.waitAndFindVideoFault(outputDir)
    if len(listFaultVideoOrder) != 0: #Có video vi phạm
      logger.info("Chuyển cửa sổ lại Filmora và xóa các clip bị vi phạm")
      posFilmoraIcon = LotusLib.horFindColor (rgb(81,224,191),10,50,1919,6,1062)
      GUI.click(posFilmoraIcon[0],posFilmoraIcon[1])
      LotusLib.waitColor((28,15),rgb(80,227,194),10,5,100)
      filmora.filmoraDelFaultClip(listFaultVideoOrder)
      filmora.remakeDescriptionAndMoveFaultVideo(workingDir,listFaultVideoOrder)
    else:
      break #Đã hết video vi phạm
  
  #Tạo backup Filmora và description
  shutil.copyfile(workingDir+'Video_Make.wfp', workingDir+'Video_Make_ok.wfp')
  shutil.copyfile(outputDir+'description.txt', outputDir+'description_ok.txt')
  
  #Minimize nhỏ cửa sổ Chrome lại
  logger.info("Đóng nhỏ cửa sổ Chrome lại")
  GUI.click(1806,16) #Minimize Chrome
  delay(1000)
  
  #Quay trở lại Filmora save rồi đóng lại
  logger.info("Quay trở lại Filmora save rồi đóng chương trình lại")
  GUI.hotkey('ctrl','s')
  delay(5000)
  GUI.click(1900,17) #close Filmora

  logger.info(">>>>> HOÀN THÀNH <<<<<")
  #Gửi thông báo báo qua zalo
  filmora.sendToTxBufferQueue(send_to='0908549354',mess_type='image',mess_data='Z:\ZaloBot\ZaloBot_running\Images\FilmoraFinish.png',send_delay_sec=0,note='Filmora Finish')

except Exception as errMessage:
    logger.debug("!!!!x ERROR !!!!")
    logger.error(errMessage)
    GUI.screenshot().save(logPicName+"_ErrorTerminate_"+datetime.datetime.now().strftime("%d%b_%Hh%Mm%S")+".png")
    #Gửi thông báo qua zalo
    filmora.sendToTxBufferQueue(send_to='0908549354',mess_type='image',mess_data='Z:\ZaloBot\ZaloBot_running\Images\FilmoraFinishFail.png',send_delay_sec=0,note='Filmora Finish Fail')
    filmora.sendToTxBufferQueue(send_to='0908549354',mess_type='image',mess_data='Z:\YoTu\TikTop\TikTop_Filmora\\'+logPicName+"_ErrorTerminate_"+datetime.datetime.now().strftime("%d%b_%Hh%Mm%S")+".png",send_delay_sec=0,note='Filmora Finish Fail')
finally:
    #Nếu VSCode đang mở thì click trả về VSCode
    vsCodePos = LotusLib.horFindColor(rgb(35,168,242),5,45,1600,5,1060)
    if vsCodePos != False:
      if LotusLib.checkColorWithCapture((vsCodePos[0],1079),rgb(255,178,178),10,100):
        GUI.click(vsCodePos) #Trả về VSCode đang mở.
    #Mở VPN Enable trở lại
    filmora.setVpnOper(1)
    #Đóng connection MySQL
    filmora.mySqlCloseConnection()
    LotusLib.taskKillerEnd()
