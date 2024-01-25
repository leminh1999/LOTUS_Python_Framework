# Các bước thực hiện:
#   1. Mở trình duyệt.
#   2. Đăng nhập vào tài khoản.
#   3. Thả tim cho từng comment trong clip (không phải tác giả)
#   4. Kiểm tra clip mới post trong danh dách các kênh theo dõi


#=======================================================================================
import time
import os
import random
### USER Declare ###
from Global.loggingSetup import *
# from LotusLib_v1r1 import *
from adsBotLib import *

adsBot = adsBotLib
pcRunResetCnt = 0
followNumPerLoopCnt = 0
followNumCnt = 0
      
THA_TIM_COMMENT     = 1    # 0 or 1
KIEM_TRA_NEW_POST   = 0    # 0 or 1
FORCE_NEW_POST_USER = ""   # "" or <follower>
TIM_COMMENT_SCROLL  = 25   # Không nên đổi. 25 tương ứng gần 100 comment đầu tiên.
                           # Đổi có thể làm thả tim cho các ngôn ngữ khác VPN đang chạy!!!
FOLLOW_NUM_PER_LOOP = 10

try:
  #Clear dummy png images at root folder
  for i in os.listdir("./"):
    if i.endswith('.png'):
      os.remove(i)
  followList = adsBot.loadMysqlFollowList(add_type='manual')
  
  ### STEP 1. Mở trình duyệt ###
  logger.info(">>>>> STEP 1: Mở trình duyệt <<<<<")
  logger.debug("--- Mở trình duyệt ---")
  adsBot.openChrome()
  LotusLib.delay(2000)

  ### STEP 2. Đăng nhập vào tài khooản ###
  logger.info(">>>>> STEP 2. Đăng nhập vào tài khooản <<<<<")

  while 1:
    logger.info("===========================================================================================================")
    logger.info("===== LOOP: "+str(pcRunResetCnt)+" ========================================================================================")
    logger.info("===========================================================================================================")
          
    ### STEP 3. Thả tim cho từng comment trong clip (không phải tác giả) ###
    if THA_TIM_COMMENT == 1:
      logger.info(">>>>> STEP 3. Thả tim cho từng comment trong clip (không phải tác giả) <<<<<")
      logger.info("--- 3.1 Lấy Video Link ---")
      adsBot.loadMysqlConf()
      adsBot.getMostCommentClip(tikTopConfig.vol_num)
      logger.info("--- 3.2 Vào trang Video Link ---")
      adsBot.openURL(curPostInfo.video_link)
      logger.info("--- 3.3 Mở cửa sổ xem code nếu chưa được mở từ trước ---")
      adsBot.openCodeWindow()
      logger.info("--- 3.4 Vào trang comment và đợi load xong ---")
      if adsBot.goToViewCommentPage() == True: # Đã load xong màn hình comment và các User
        print("ScrollNum3: = "+str(TIM_COMMENT_SCROLL))
        adsBot.heartClicking(scrollNum = TIM_COMMENT_SCROLL)
        adsBot.updateMysqlHeartClicking()
      else:
        curPostInfo.heart_check_flag = 1
        curPostInfo.heart_click = 0
        adsBot.updateMysqlHeartClicking()
      
    
    ### STEP 4. Kiểm tra clip mới post trong danh dách các kênh theo dõi ###
    if KIEM_TRA_NEW_POST == 1:
      followNumPerLoopCnt = 0
      while followNumPerLoopCnt < FOLLOW_NUM_PER_LOOP:
        logger.info(">>>>> STEP 4. Kiểm tra clip mới post trong danh dách các kênh theo dõi <<<<<")
        logger.info("--- 4.1 Lấy danh sách follow list ---")
        followNumPerLoopCnt += 1 #Loop tối đa FOLLOW_NUM_PER_LOOP thì chuyển qua thả tim comment
        
        follower =followList[followNumCnt]
        followNumCnt += 1
        if followNumCnt >= len(followList): exit() #Nếu đã chạy hết danh sach follower list thì reset máy một lần.
        
        if FORCE_NEW_POST_USER != "":
          follower = FORCE_NEW_POST_USER
        logger.info("\n=====> %s/%s. %s\n",str(followNumCnt),str(len(followList)),follower)
        
        logger.info("--- 4.2 Vào trang Video Link ---")
        adsBot.openCodeWindow()
        urlLink = "www.tiktok.com/@"+follower
        adsBot.openURLWithoutWait(urlLink)
        LotusLib.waitColor((700,700),rgb(247,247,248),10,20,500) # Images/53.png .Đợi màn hình load
        LotusLib.waitNotColor((700,700),rgb(247,247,248),10,60,500) # Images/52b.png .Đợi load xong
        logger.info("--- 4.3 Click vào video mới nhất ---")
        GUI.click(700,700)
        LotusLib.delay(1000)
        n = 1
        while n < 15:
          if LotusLib.checkColorWithCapture((30,1000),rgb(255,255,255),10,0) == True: #Vẫn chưa chuyển page
            GUI.click(700,700)
            LotusLib.delay(1000)
            # print("====>",n)
            n += 1
          else: #Đã chuyển sang page comment
            break
        LotusLib.waitColor((1060,1020),rgb(241,241,242),10,20,500) # Images/51s.png . Chờ ô bình luận hiện ra.
        logger.info("--- 4.4 Xem clip có phải mới đăng chưa đến 60ph hay không ---")
        videoLink,videoId,userAndTime = adsBot.checkNewPost()
        numCnt = str(followNumCnt)+"/"+str(len(followList))
        if videoLink != "Not_found":
          adsBot.sendZalo(numCnt,videoLink,videoId,userAndTime)
        if FORCE_NEW_POST_USER != "":
          logger.info("==== STOP: FORCE_NEW_POST_USER ====")
          adsBot.mySqlCloseConnection()
          exit()
        
    # Thoát chương trình sau 30 lần chạy
    pcRunResetCnt += 1
    if pcRunResetCnt > 30:
      logger.info("==== NORMAL RESET EVERY 30 TIMES RUNNING ====")
      adsBot.mySqlCloseConnection()
      exit()

except Exception as errMessage:
    logger.debug("!!!! ERROR !!!!")
    logger.error(errMessage)
finally:
    GUI.click(270,1064) #Vị trí VSCode
    adsBot.mySqlCloseConnection()
    exit()