from A2_GetLink_ImportList import *
import shutil

#Lớp task2CheckCommnetInfo hiển thị thông tin của video sau cùng
class task2CheckCommnetInfo:
  likeFinal = ""
  commentFinal = ""
  shareFinal = ""
  htmlCode = ""
  funnyFinal = ""
  video_size = ""
      
class clipPostInfo:
  id = ""
  video_id = "0123456789"
  org_user = ""
  cus_user = ""
  post_date = ""
  video_link = ""
  like_num = ""
  comment_num = ""
  share_num = ""
  funny_num = ""
  total_score = ""
  video_local_name = ""
  comment_local_1 = ""
  comment_local_2 = ""
  comment_local_3 = ""
  comment_local_4 = ""
  comment_local_5 = ""
  comment_merge_name = ""
  video_pc_merge_name = ""
  video_mobile_merge_name = ""
  task2_check_time = ""
  update_time = ""

def debugPrintClipPostInfo():
  logger.debug("video_id   = %s",clipPostInfo.video_id)
  logger.debug("org_user   = %s",clipPostInfo.org_user)
  logger.debug("video_link = %s",clipPostInfo.video_link)

class Task2GetComment:
  avatar1stPos = ""
  avatarLastPos = ""
  
  def get999Post():
    sql = "SELECT * FROM tiktop_day WHERE task2_check_time = "+str(-999)+" LIMIT 1"
    mycursor.execute(sql)
    readData = mycursor.fetchall()[0] #Fetch là lấy dòng đầu tiên
    logger.info(readData)   
    clipPostInfo.id                      = readData[0]
    clipPostInfo.video_id                = readData[1]
    clipPostInfo.org_user                = readData[2]
    clipPostInfo.cus_user                = readData[3]
    clipPostInfo.post_date               = readData[4]
    clipPostInfo.video_link              = readData[5]
    clipPostInfo.like_num                = readData[6]
    clipPostInfo.comment_num             = readData[7]
    clipPostInfo.share_num               = readData[8]
    clipPostInfo.funny_num               = readData[9]
    clipPostInfo.total_score             = readData[10]
    clipPostInfo.video_local_name        = readData[11]
    clipPostInfo.comment_local_1         = readData[12]
    clipPostInfo.comment_local_2         = readData[13]
    clipPostInfo.comment_local_3         = readData[14]
    clipPostInfo.comment_local_4         = readData[15]
    clipPostInfo.comment_local_5         = readData[16]
    clipPostInfo.comment_merge_name      = readData[17]
    clipPostInfo.video_pc_merge_name     = readData[18]
    clipPostInfo.video_mobile_merge_name = readData[19]
    clipPostInfo.task2_check_time        = readData[20]
    clipPostInfo.update_time             = readData[21]
    if clipPostInfo.id == "": #Không còn video -999
      return 0
    else: #Còn video -999
      #Cập nhật trạng thái của dòng là đang checking
      sql = "UPDATE tiktop_day SET task2_check_time = %s,update_time = %s WHERE video_id = "+str(clipPostInfo.video_id)+""
      val = ("CHECKING",clipPostInfo.update_time)
      mycursor.execute(sql, val)
      mydb.commit()
      return 1



  def goToViewCommentPage():
    #Di chuyển mouse đến vị trí click
    GUI.click(600,500)  # Images/11b.png
    LotusLib.delay(500)
    GUI.click(600,500)  # Images/11b.png
    LotusLib.wait3Color((1341,240),(193,193,193),20,(1341,242),(193,193,193),20,(1341,244),(193,193,193),20,30) #Chờ màn hình load xong Images/12b.png
    allAvatarLoaded = 0
    checkTime = 0
    while checkTime < 30 and allAvatarLoaded == 0:
      for i in range (500,900):
        if LotusLib.getColor(857,i)[0] == 255:
          continue # Chưa load được các avatar
        else:
          allAvatarLoaded = 1
          break # Đã load xong các avatar
      checkTime += 1
      LotusLib.delay(100)

  #Chiến thuật bắt comment:
  # Images/13b.png
  # 1. Tìm vị trí comment đầu tiên
  # 2. Click nút xuống số 2 để cuộn avatar lên trên. Chú ý tính toán để avatar không vượt quá số 3. Mỗi lần cuộn sẽ trôi 40px.
  # 3. Từ vị trí số 4 đếm lên trên để tìm comment cuối cùng (Nếu phát hiện nữa avata cũng OK)
  # 4. Vùng bắt comment sẽ là từ vị trí comment đầu tiên đến comment gần cuối. Lưu hình này vào biến tạm chờ check điểm cười và các tiêu chí khác.
  def captureCommentPic():
    num2Pos = 1341,964 #Vị trí nút nhấn xuống comment. Mỗi lần nhấn trôi 40px
    num3Pos = 857,217  #Vị trí dòng comment sẽ bị ẩn khi cuộn xuống
    # 1. Tìm vị trí comment đầu tiên
    avatar1stPos = Task2GetComment.findCommentPos4(1)[0] #Nhận vị trí của first comment
    # 2. Click nút xuống số 2 để cuộn avatar lên trên. Chú ý tính toán để avatar không vượt quá số 3. Mỗi lần cuộn sẽ trôi 40px.
    print(avatar1stPos)
    if avatar1stPos != False: # Có phát hiện ra avatar thứ 1
      scrollPos = [1341,240]
      while avatar1stPos[1] - 40 > num3Pos[1]:
        avatar1stPos[1] -= 40
        GUI.click(num2Pos) #Nhấn nút chạy xuống 40px
        scrollPos = Task2GetComment.__waitScrollDown(checkX=scrollPos[0],rangeYLow=scrollPos[1],rangeYHigh=950,timeout_s=15)
        logger.info("Scrollbar Top Position: %s",scrollPos)
      logger.info("First comment pos: %s",avatar1stPos)
    # 3. Từ vị trí số 4 đếm lên trên để tìm comment cuối cùng (Nếu phát hiện nữa avata cũng OK)
    avatarLastPos = Task2GetComment.findCommentPos4(0)[1] #Nhận vị trí của last comment
    logger.info("Last comment pos: %s",avatarLastPos)
    # 4. Vùng bắt comment sẽ là từ vị trí comment đầu tiên đến comment gần cuối. Lưu hình này vào biến tạm chờ check điểm cười và các tiêu chí khác.
    logger.info("Save temp image tempComment.png")
    pyautogui.screenshot(region=(820,avatar1stPos[1], 500, avatarLastPos[1]-avatar1stPos[1]-1)).save(clipPostInfo.video_id+".png")
    Task2GetComment.avatar1stPos  = avatar1stPos
    Task2GetComment.avatarLastPos = avatarLastPos


  def checkFunnyPoint ():
    for i in range (0,50):
      GUI.click(1340,950)
      LotusLib.delay(100)
    
    htmlCode = Task1GetLink.getCode()
    GUI.move(1255,180) #Di chuyển chuột qua chỗ khác để tránh màn hình xanh
    x = htmlCode.split("comment-item")
    htmlCode100 = ""
    
    if len(x) <= 5:
      htmlCode100 = ""
    else:
      if len(x) >= 101:
        for i in range (1,102):
          htmlCode100 += x[i]
      else:
        for i in range (1,len(x)):
          htmlCode100 += x[i]
    
    funny_total_point = 0
    funny_total_point += htmlCode100.count("🤣") * int("50")
    funny_total_point += htmlCode100.count("😅") * int("30")
    funny_total_point += htmlCode100.count("😂") * int("30")
    funny_total_point += htmlCode100.count("😁") * int("20")
    funny_total_point += htmlCode100.count("😝") * int("20")
    funny_total_point += htmlCode100.count("😄") * int("20")
    logger.info("🤣 %s - 😅 %s - 😂 %s - 😁 %s - 😝 %s - 😄 %s",htmlCode100.count("🤣"),htmlCode100.count("😅"),htmlCode100.count("😂"),htmlCode100.count("😁"),htmlCode100.count("😝"),htmlCode100.count("😄"))
    logger.info("Comment num: %s - Funny Point: %s",len(x)-1,funny_total_point)
    clipPostInfo.funny_num = str(funny_total_point)
    return funny_total_point
    
  def calScoreAndUploadMySQL():
    like_num    = LotusLib.convertHumanNumToInt(clipPostInfo.like_num)
    comment_num = LotusLib.convertHumanNumToInt(clipPostInfo.comment_num)
    share_num   = LotusLib.convertHumanNumToInt(clipPostInfo.share_num)
    funny_num   = LotusLib.convertHumanNumToInt(clipPostInfo.funny_num)
    
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
    if int(clipPostInfo.funny_num) < int(tikTopConfig.min_funny):
      clipPostInfo.total_score = 0
      if os.path.exists(clipPostInfo.video_id+".png"):
        os.remove(clipPostInfo.video_id+".png")
    else:
      # Di chuyển file hình vào thư mục
      source = clipPostInfo.video_id+".png"
      dest = '../PostData/Vol'+tikTopConfig.vol_num
      shutil.move(source, dest)
      # Tính điểm tổng
      clipPostInfo.total_score = likeScore + commentScore + shareScore + funnyScore
      point1 = LotusLib.getColor(1200,162) # Images/15s.png . Màu chưa Follow (254,44,85) -> Nếu Follow (202,202,206)
      if point1[0] > 240 and point1[1] < 80 and point1[2] < 120: #Đang là nút Follow màu hồng -> Chưa follow
        logger.info("Click nút Follow - TotalScore: %s",clipPostInfo.total_score)
        GUI.click(1255,180) #Click vào nút Follow
    sql = "UPDATE tiktop_day SET funny_num = %s,total_score = %s WHERE video_id = "+str(clipPostInfo.video_id)+""
    val = (clipPostInfo.funny_num, clipPostInfo.total_score)
    mycursor.execute(sql, val)
    mydb.commit()
    
  def updateTaskMonTask1Task2(task1_flag=1, task2_flag=0):
    sql = "UPDATE tiktop_task_mon SET task1_running_flag = %s,task2_running_flag = %s WHERE id = '0'"
    val = (task1_flag,task2_flag)
    mycursor.execute(sql, val)
    mydb.commit()

  def updateTaskMonTask3Task4(task3_flag=1, task4_flag=0):
    sql = "UPDATE tiktop_task_mon SET task3_running_flag = %s,task4_running_flag = %s WHERE id = '0'"
    val = (task3_flag,task4_flag)
    mycursor.execute(sql, val)
    mydb.commit()

  def __waitScrollDown (checkX, rangeYLow, rangeYHigh,timeout_s):
    timeCnt = time.time();
    while (time.time() - timeCnt) < timeout_s: #Chưa hết thời gian time out
      # logger.info("DEBUG1: %s",(time.time() - timeCnt))
      for checkY in range (rangeYLow, rangeYHigh+1):
        # logger.info("DEBUG2: %s",checkY)
        if LotusLib.checkColorWithCapture((checkX,checkY),(192,192,192),10) == True: #Tìm đỉnh màu xám của scrollbar.
          if checkY != rangeYLow: #Chứng tỏ đã nhảy scrollbar -> Trả về vị trí scrollbar mới.
            # logger.info("DEBUG3: %s",checkY)
            return checkX,checkY
          else:
            # logger.info("DEBUG4: %s",checkY)
            LotusLib.delay(100)
            break
    # logger.info("-----------------: %s",checkY)
    return checkX,rangeYLow

  # def findCommentPos1 (fromPosY, toPosY): # Điều kiện: Tìm từ vị trí dưới lên -> fromPosY > toPosY
  #   capScreen = GUI.screenshot()
  #   i = 0
  #   searchRange = fromPosY - toPosY + 1
  #   while i < searchRange:
  #     pos = 857,fromPosY-i
  #     color = 255,255,255
  #     if LotusLib.checkColorWithoutCapture(capScreen,pos,color,5) == True: # Điểm kiểm tra là màu trắng của nền
  #       i += 1
  #     else: #Điểm kiểm tra có màu
  #       return [857,fromPosY-i-40]
  #   return False

  def findCommentPos4(findOnlyFirstCmt=0):
    startPoint = [1288,400]
    capScreen = GUI.screenshot()
    avatar1stPos = ""
    avatarLastPos = ""
    i = 0
    while i < 572:
      timPos = [startPoint[0],startPoint[1]+i]
      if capScreen.getpixel((timPos[0]   ,timPos[1]   ))[0] < 145 and\
         capScreen.getpixel((timPos[0]- 7,timPos[1]- 9))[0] < 145 and\
         capScreen.getpixel((timPos[0]+ 8,timPos[1]- 9))[0] < 145 and\
         capScreen.getpixel((timPos[0]   ,timPos[1]-12))[0] < 145: #Xác định có 1 trái tim qua 4 điểm: Đáy, trái, phải và trên Images/14s.png
        if avatar1stPos == "":
          avatar1stPos = [timPos[0],timPos[1]-40]
          if findOnlyFirstCmt == 1:
            return avatar1stPos,avatar1stPos
        avatarLastPos = [timPos[0],timPos[1]-40]
        i += 80
      else:
        i += 1
    if avatar1stPos != "" and avatarLastPos != "":
      return avatar1stPos,avatarLastPos
    else:
      logger.critical("KHÔNG TÌM ĐƯỢC COMMENT!!!")
      return exit()

  # def findCommentPos2 (fromPosY, toPosY): # Điều kiện: Tìm từ vị trí dưới lên -> fromPosY > toPosY
  #   firstPointRecorded = 0
  #   secondPointRecorded = 0
  #   capScreen = GUI.screenshot()
  #   i = 0
  #   searchRange = fromPosY - toPosY + 1
    
  #   if LotusLib.checkColorWithoutCapture(capScreen,(857,fromPosY),(255,255,255),5) == True: # Điểm kiểm tra là màu trắng của nền
  #     while i < searchRange:
  #       pos = 857,fromPosY-i
  #       color = 255,255,255
  #       if LotusLib.checkColorWithoutCapture(capScreen,pos,color,5) == True: # Điểm kiểm tra là màu trắng của nền
  #         i += 1
  #       else: #Điểm kiểm tra có màu
  #         return [857,fromPosY-i-40]
  #     return False
  #   else:
  #     while i < searchRange:
  #       pos = 857,fromPosY-i
  #       color = 255,255,255
  #       if LotusLib.checkColorWithoutCapture(capScreen,pos,color,5) == True: # Điểm kiểm tra là màu trắng của nền
  #         return [857,fromPosY-i-20+1] #Trừ 20 để tránh các avatar có hình trắng
  #       else:
  #         i+=1
  #   return False
          
          
  # def findCommentPos3 (fromPosY, toPosY): # Điều kiện: Tìm từ vị trí dưới lên -> fromPosY > toPosY
  #   firstPointRecorded = 0
  #   secondPointRecorded = 0
  #   capScreen = GUI.screenshot()
  #   i = 0
  #   searchRange = fromPosY - toPosY + 1
  #   while i < searchRange:
  #     pos = 857,fromPosY-i
  #     color = 255,255,255
  #     if LotusLib.checkColorWithoutCapture(capScreen,pos,color,5) == True: # Điểm kiểm tra là màu trắng của nền
  #       if secondPointRecorded == 1: #Avatar đã được bắt
  #         topAvatarPos = [857,fromPosY-i+1]
  #         return topAvatarPos
  #       else:
  #         i += 1
  #         firstPointRecorded = 0
  #         secondPointRecorded = 0
  #     else: #Điểm kiểm tra có màu
  #       if firstPointRecorded == 0: #Đây là điểm có màu đầu tiên
  #         i += 39
  #         firstPointRecorded = 1
  #       else: #Đây là điểm có màu thứ 2
  #         i +=1
  #         secondPointRecorded = 1
  #   return False
          
  #   # # 2. Click nút xuống số 2 để cuộn avatar lên trên. Chú ý tính toán để avatar không vượt quá số 3. Mỗi lần cuộn sẽ trôi 40px.
  #   # commentMovePosY = TopAvatarPos[1]
  #   # if commentMovePosY - 40 >= num3Pos[1]:
  #   #   commentMovePosY -= 40
  #   #   GUI.click(num2Pos) #Click nút xuống để đọc comment bên dưới.
      
        
      
    
    
    


