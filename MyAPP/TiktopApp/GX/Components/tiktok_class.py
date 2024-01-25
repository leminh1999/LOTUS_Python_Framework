import __init
import MyAPP.TiktopApp.GX.DynamicParamPC as PARAM
from task_args import *
from time import sleep,time
from Conf.loggingSetup import *
from Library.A1_PyAutoGUI.pyAutoGui_Wrap import pyAutoGui_Remap as GUI
from Library.A2_LOTUS.lotus_Wrap import rgb,lotus_Remap as LOTUS
from Library.A3_Selenium.selenium_Wrap import Keys, WEB, seleniumIDE_Remap as IDE
from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
from Library.C3_OmoCaptcha.omoCaptcha import omoCaptcha; OMO = omoCaptcha()
from SystemManager.system_Wrap import SYS
from pprint import *
import pyperclip
import re
import random
from os import path
import platform
import requests
from bs4 import BeautifulSoup as BS

#MySQL Configurations ##########################################
gxMysql = MYSQL(hostAddress    = PARAM.MYSQL_HOST,
                database       = ARGS.MYSQL_DB,
                username       = PARAM.MYSQL_USER,
                password       = PARAM.MYSQL_PASS)
################################################################

class dataInfo ():
  #Config
  cfg00_ena = 1
  cfg00_key_check_num = 0 
  '''Đây là contrỏ của key tìm kiếm trong vn_10_key_list'''
  
  #Key list
  key10_id        = 0
  key10_key_word  = ""
  key10_key_type  = ""
  key10_scan_time = 0
  key10_total_num = 0
  #Current process data
  cur_key_list_id = 0
  cur_key_word    = ""
  cur_key_type    = ""
  cur_scan_time   = 0
  cur_total_num   = 0
  cur_video_id    = ""
  cur_video_user  = ""
  cur_video_link  = ""
  cur_status      = ""

################################################################
################################################################
################################################################
class tiktok_upload():
  pass
  OPEN_BROWSER_CMD = "screen -dmS JUBEI google-chrome --no-sandbox --disable-infobars --window-position=0,0 --window-size=1920,1080"
  OPEN_BROWSER_NO_SHM_CMD = "screen -dmS JUBEI google-chrome --no-sandbox --disable-infobars --disable-dev-shm-usage --window-position=0,0 --window-size=1920,1080"
  
  def openBrowser(self,url,incognito=True,checkFirstOpen=True):
    if incognito == True:
      # browserPid = LOTUS.taskManager.programOpenParallel("C:\Program Files\Google\Chrome\Application\chrome.exe","--incognito")
      os.system(self.OPEN_BROWSER_CMD + " --incognito" + " " + url + " &")
      # if checkFirstOpen: LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_FirstOpenBrower.png",confidence=0.85,timeout_sec=15,delayFinish_ms=500,printLog=True) #Click vào nút đồng ý lần đầu tiên mở trình duyệt web.
      # LOTUS.color.waitColor((1638,20),rgb(32,33,36),20)
    else:
      # browserPid = LOTUS.taskManager.programOpenParallel("C:\Program Files\Google\Chrome\Application\chrome.exe","--maximize-window")
      os.system(self.OPEN_BROWSER_CMD + " " + url + " &")
      # if checkFirstOpen: LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_FirstOpenBrower.png",confidence=0.85,timeout_sec=15,delayFinish_ms=500,printLog=True) #Click vào nút đồng ý lần đầu tiên mở trình duyệt web.
      # LOTUS.color.waitColor((1638,20),rgb(222,225,230),20)
    sleep(1)
    GUI.mouse.click(1895,95,tween=GUI.mouse.effect.easeInOutBounce, duration=0.5) #Đóng thanh thông báo.
    
  def tat_cac_thong_bao(self):
    GUI.mouse.click(x=412,y=83);sleep(0.5)
    GUI.mouse.click(x=1893,y=84);sleep(0.5) 
    GUI.mouse.click(x=1894,y=94);sleep(0.5) 
    GUI.mouse.click(x=1868,y=716);sleep(0.5)
    GUI.mouse.click(x=1868,y=991);sleep(0.5)

  def gotoProfilePage(self,profileName:str):
    GUI.mouse.click(x=1400,y=50,tween=GUI.mouse.effect.easeInOutBounce, duration=0.5) #Vị trí thanh address bar
    sleep(0.1)
    GUI.key.hotkey("ctrl","a")
    sleep(0.1)
    LOTUS.clipboard.copyToClipboard("https://www.tiktok.com/@"+profileName)
    sleep(0.2)
    LOTUS.clipboard.pasteFromClipboard()
    sleep(0.2)
    GUI.key.press("enter")
    sleep(0.2)
    GUI.mouse.click(x=1400,y=50) #Vị trí thanh address bar
    sleep(0.2)
    GUI.key.press("enter")
    LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/0_ProfilePage.png",confidence=0.7,timeout_sec=30,delayFinish_ms=500)
    
    
  def loginTiktokGoogle(self):
    #Kiểm tra trạng thái đăng nhập
    if not GUI.screen.locateOnScreen(image="/MyAPP/TiktopApp/GX/PIC/0_loginIcon.png",confidence=0.7):
      logger.info("Tài khoản dã đăng nhập từ trước")
      return True
    else:
      LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_loginIcon.png",confidence=0.7,timeout_sec=60);sleep(2)
      if LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_GoogleAccountLogin.png",confidence=0.7,timeout_sec=60) == False:
        GUI.mouse.click(x=960,y=550,tween=GUI.mouse.effect.easeInOutBounce, duration=0.5); #Click vào nút đăng nhập bằng Google Account
        LOTUS.log.addClickPosToHtmlLog(960,550);sleep(0.5) 
      LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/0_TiktokLogin_Icon.png",confidence=0.7,timeout_sec=60)
      sleep(1)
      GUI.mouse.move(960,550,tween=GUI.mouse.effect.easeInOutBounce, duration=0.5)
      for i in range(0,2):
        GUI.mouse.click(960,550)
        LOTUS.log.addClickPosToHtmlLog(960,550)
        sleep(0.2) #Click vào nút đăng nhập bằng Google Account
      if LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/0_SendMessage.png",confidence=0.7,timeout_sec=90) != False:
        logger.info("Đăng nhập Tiktok thành công")
        return True
      else:
        logger.warn("Đăng nhập Tiktok thất bại !!!")
        return False

  def uploadVideo(self,videoPath,videoName="❤❤❤",publishMode="PUBLIC"):
    def __choseVideo():
      if LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_UploadFile_SelectFile.png",confidence=0.7,timeout_sec=60) == False:
        containerName = os.getenv("CONTAINER_NAME")
        os.system("echo "+containerName+" >> /HShare/0_AllChannels/0_ReqManKill.txt")
        exit()
      LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/0_OpenFileWindowAppear.png",confidence=0.7,timeout_sec=60)
      if LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/0_HomeAndVideoSelected.png",confidence=0.7,timeout_sec=60) != False:
        pass
      else:
        if LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_SelectHome.png",confidence=0.7,timeout_sec=60) == False:
          containerName = os.getenv("CONTAINER_NAME")
          os.system("echo "+containerName+" >> /HShare/0_AllChannels/0_ReqManKill.txt")
          exit()
      sleep(1)
      if LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_ClickOpen.png",confidence=0.7,timeout_sec=60) == False:
        containerName = os.getenv("CONTAINER_NAME")
        os.system("echo "+containerName+" >> /HShare/0_AllChannels/0_ReqManKill.txt")
        exit()
      
    
    ###Main code###
    if LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_UploadIcon.png",confidence=0.7,timeout_sec=60) == False:
      containerName = os.getenv("CONTAINER_NAME")
      os.system("echo "+containerName+" >> /HShare/0_AllChannels/0_ReqManKill.txt")
      exit()
    __choseVideo()
    for i in range (0,3):
      if LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/0_Edit_Video.png",confidence=0.7,timeout_sec=90) == False:
        logger.info("Chọn video thất bại. Thử lại lần thứ " + str(i+1))
        __choseVideo()
      else:
        break
    GUI.mouse.click(1306,169) #Click nút chấp nhận chính sách mới
    sleep(1)
    GUI.mouse.click(1306,169) #Click nút chấp nhận chính sách mới
    sleep(5)
    
    #Nhập Caption
    GUI.mouse.click(1200,440) #Vị trí nhập Caption
    LOTUS.log.addClickPosToHtmlLog(1200,440)
    GUI.key.hotkey('ctrl','a')
    LOTUS.clipboard.copyToClipboard(videoName);sleep(0.5)
    LOTUS.clipboard.pasteFromClipboard();sleep(0.5)

    
    #Chọn hình đại diện cho video
    ranPosX = random.randint(780,1440)
    for i in range(0,3):
      GUI.mouse.click(x=ranPosX,y=600) # ../PIC/011.png Số 2. Chọn hình đại diện cho video
      sleep(0.5)
    LOTUS.log.addClickPosToHtmlLog(ranPosX,600)
    
    #Publish mode
    if publishMode != "PUBLIC":
      if LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_PublicMode.png",confidence=0.7) == False:
        containerName = os.getenv("CONTAINER_NAME")
        os.system("echo "+containerName+" >> /HShare/0_AllChannels/0_ReqManKill.txt")
        exit()
      if LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_PrivateMode.png",confidence=0.7) == False:
        containerName = os.getenv("CONTAINER_NAME")
        os.system("echo "+containerName+" >> /HShare/0_AllChannels/0_ReqManKill.txt")
        exit()
      sleep(1)
    
    if LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_PostButton.png",confidence=0.7,timeout_sec=60) == False:
      containerName = os.getenv("CONTAINER_NAME")
      os.system("echo "+containerName+" >> /HShare/0_AllChannels/0_ReqManKill.txt")
      exit()
    sleep(200)
    GUI.mouse.click(1024, 1029) #Vị trí Click nút 0_PostButton
    if LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_ViewProfileButton.png",confidence=0.7,timeout_sec=90) == False:
      containerName = os.getenv("CONTAINER_NAME")
      os.system("echo "+containerName+" >> /HShare/0_AllChannels/0_ReqManKill.txt")
      exit()
      
  def seleUploadVideo(self,videoPath="",videoName="❤❤❤",publishMode="PUBLIC"):
    def __choseVideo():
      IDE.mouseKey.click("xpath=//div[contains(text(),'Select file')]") #Click nút Select files. /MyAPP/TiktopApp/GX/PIC/0_UploadFile_SelectFile.png
      LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/0_OpenFileWindowAppear.png",confidence=0.7,timeout_sec=60)
      if LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/0_HomeAndVideoSelected.png",confidence=0.7,timeout_sec=60) != False:
        pass
      else:
        if LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_SelectHome.png",confidence=0.7,timeout_sec=60) == False:
          containerName = os.getenv("CONTAINER_NAME")
          os.system("echo "+containerName+" >> /HShare/0_AllChannels/0_ReqManKill.txt")
          exit()
      sleep(1)
      if LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_ClickOpen.png",confidence=0.7,timeout_sec=60) == False:
        containerName = os.getenv("CONTAINER_NAME")
        os.system("echo "+containerName+" >> /HShare/0_AllChannels/0_ReqManKill.txt")
        exit()
      
    try:
      ###Main code###
      IDE.others.others_debug_printTabIframeInfo()
      iframeNum = IDE.others.others_content_getNumberOfIframes()
      IDE.waitFor.waitForElementVisible("xpath=//div[@data-e2e='upload-icon']")
      IDE.mouseKey.click("xpath=//div[@data-e2e='upload-icon']") #Click nút Upload video. /MyAPP/TiktopApp/GX/PIC/0_UploadIcon.png
      sleep(2)
      IDE.others.others_content_waitNewIframeOpen(iframeNum)
      IDE.webContent.selectFrame("index=0")
      IDE.waitFor.waitForElementVisible("xpath=//div[contains(text(),'Select file')]")
        
      __choseVideo()
      IDE.waitFor.waitForElementVisible("xpath=//div[contains(text(),'Edit video')]")
      
      #Nhập Caption
      sleep(2)
      IDE.mouseKey.click("xpath=//div[contains(@class,'public-DraftEditor-content')]")
      IDE.others.others_clearReqWaitCmdFlg()
      LOTUS.log.addClickPosToHtmlLog(1200,640)
      GUI.key.hotkey('ctrl','a')
      LOTUS.clipboard.copyToClipboard(videoName);sleep(0.5)
      LOTUS.clipboard.pasteFromClipboard();sleep(0.5)

      
      #Chọn hình đại diện cho video
      ranPosX = random.randint(780,1440)
      for i in range(0,3):
        GUI.mouse.click(x=ranPosX,y=650) # ../PIC/011.png Số 2. Chọn hình đại diện cho video
        sleep(0.5)
      LOTUS.log.addClickPosToHtmlLog(ranPosX,650)
      
      #Bỏ chọn tạo new_playlist cho video mới nếu có (Mặc định được chọn bởi Tiktok). ../PIC/0_Add_to_playlist.png
      if IDE.assertVerify.verifyElementPresent("xpath=//div[contains(@class,'tiktok-select-selector')]//div[contains(text(),'new_playlist')]") == True:
        IDE.mouseKey.click("xpath=//div[contains(@class,'tiktok-select-selector')]//div[contains(text(),'new_playlist')]")
        IDE.waitFor.waitForElementVisible("xpath=//div[contains(@class,'tiktok-select-dropdown')]//child::div[contains(@class,'css-mbgljv')]")
        IDE.mouseKey.click("xpath=//div[contains(@class,'tiktok-select-dropdown')]//child::div[contains(@class,'css-mbgljv')]//parent::*//child::input")
        IDE.waitFor.waitForElementNotVisible("xpath=//div[contains(@class,'tiktok-select-dropdown')]//child::div[contains(@class,'css-mbgljv')]")
        
      #Publish mode
      if publishMode != "PUBLIC":
        IDE.mouseKey.click("xpath=//div[contains(@class,'tiktok-select-selector')]//span[contains(text(),'Public')]")
        IDE.waitFor.waitForElementVisible("xpath=//span[text()='Private']")
        IDE.mouseKey.click("xpath=//span[text()='Private']")
        IDE.others.others_clearReqWaitCmdFlg()
        sleep(1)
      
      
      IDE.waitFor.waitForElementVisible("xpath=//div[contains(@class,'btn-post')]")
      IDE.mouseKey.click("xpath=//div[contains(@class,'btn-post')]") #Click Post. /MyAPP/TiktopApp/GX/PIC/0_PostButton.png
      
      IDE.waitFor.waitForElementVisible("xpath=//div[contains(text(),'Manage your posts')]") #Chờ trang Profile hiện ra. /MyAPP/TiktopApp/GX/PIC/0_Manage_your_posts.png
      IDE.mouseKey.click("xpath=//div[contains(text(),'Manage your posts')]")
      
      IDE.waitFor.waitForElementVisible("xpath=//*[contains(@data-tt,'IconTabHome')]") # /MyAPP/TiktopApp/GX/PIC/0_Profile_IconTabHome.png
      IDE.mouseKey.click("xpath=//*[contains(@data-tt,'IconTabHome')]")
    except Exception as e:
      logger.error(e)
      pass


  def seleGetLastPost(self):
    logger.debug("Đã vào trang cá nhân")
    sleep(2)
    # lastPostElement = IDE.others.others_content_findFirstElement("xpath=//div[contains(@class,'DivItemContainerV2')]")
    newClipLink = IDE.others.others_content_getAttribute(target="xpath=//div[contains(@class,'DivItemContainerV2')]//a[contains(@href,'tiktok')]",value="href")
    
    # GUI.mouse.middleClick(350,500) #Click chuột giữa vào video đầu tiên
    # LOTUS.log.addClickPosToHtmlLog(350,500,borderColor=(0,255,0));
    # sleep(2)
    # GUI.mouse.rightClick(350,500) #Click chuột phải vào video đầu tiên
    # LOTUS.log.addClickPosToHtmlLog(350,500,borderColor=(0,0,255));
    # sleep(1.5)
    # LOTUS.log.addClickPosToHtmlLog(390,630,borderColor=(0,0,255));
    # GUI.mouse.rightClick(390,630) #Click chuột phải vào ""Copy link address""
    # sleep(1)
    # newClipLink = LOTUS.clipboard.pasteFromClipboardToVar();sleep(0.2)
    # logger.debug("newClipLink: %s",newClipLink)
    newClipId = newClipLink.split("/")[-1]
    newClipUser = newClipLink.split("/")[-3].split("@")[-1]
    # logger.debug("newClipId: %s",newClipId)
    # logger.debug("newClipUser: %s",newClipUser)
    logger.debug("newClipLink: %s",newClipLink)
    return {"id":newClipId,"user":newClipUser,"link":newClipLink}
  
  def getLastPost(self):
    LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/0_ProfilePage.png",confidence=0.7,timeout_sec=90)
    logger.debug("Đã vào trang cá nhân")
    sleep(2)
    GUI.mouse.middleClick(350,500) #Click chuột giữa vào video đầu tiên
    LOTUS.log.addClickPosToHtmlLog(350,500,borderColor=(0,255,0));
    sleep(2)
    GUI.mouse.rightClick(350,500) #Click chuột phải vào video đầu tiên
    LOTUS.log.addClickPosToHtmlLog(350,500,borderColor=(0,0,255));
    sleep(1.5)
    LOTUS.log.addClickPosToHtmlLog(390,630,borderColor=(0,0,255));
    GUI.mouse.rightClick(390,630) #Click chuột phải vào ""Copy link address""
    sleep(1)
    newClipLink = LOTUS.clipboard.pasteFromClipboardToVar();sleep(0.2)
    # logger.debug("newClipLink: %s",newClipLink)
    newClipId = newClipLink.split("/")[-1]
    newClipUser = newClipLink.split("/")[-3].split("@")[-1]
    # logger.debug("newClipId: %s",newClipId)
    # logger.debug("newClipUser: %s",newClipUser)
    logger.debug("newClipLink: %s",newClipLink)
    return {"id":newClipId,"user":newClipUser,"link":newClipLink}

  def getFollowingInfo(self):
    GUI.key.hotkey('ctrl','a'); sleep(1)
    GUI.key.hotkey('ctrl','c'); sleep(0.5)
    dataInfo = LOTUS.clipboard.pasteFromClipboardToVar().split("\n");sleep(0.2)
    # logger.debug("dataInfo: ",dataInfo)

    lineNum = len(dataInfo)
    # print(lineNum)
    for line in reversed(dataInfo):
        lineNum -= 1
        if "Likes"     in line: likeNum = dataInfo[lineNum-1].strip()
        if "Followers" in line: followerNum = dataInfo[lineNum-1].strip()
        if "Following" in line:
          followNum = dataInfo[lineNum-1].strip()
          userCustomName = dataInfo[lineNum-2].strip()
          userUniqueName = dataInfo[lineNum-3].strip()
          break
          
    logger.debug("Likes number: " + likeNum)
    logger.debug("Followers number: " + followerNum)
    logger.debug("Following number: " + followNum)
    logger.debug("Custom name: " + userCustomName)
    logger.debug("Unique name: " + userUniqueName)
    
    return {"likeNum":likeNum,"followerNum":followerNum,"followNum":followNum,"userCustomName":userCustomName,"userUniqueName":userUniqueName}

  def updatePublishList(self,publishInfo,video_id:str):
    '''
    =============================================================================
    Function: Cập nhật thông tin về clip lên vn_40_publish_list
    Parameter: publishInfo
    Ruturn: None
    =============================================================================
    '''
    logger.debug("Cập nhật thông tin về clip lên vn_40_publish_list")
    gxMysql.checkConnectionToReconnect() #Tránh lỗi mất kết nối: "2013 (HY000): Lost connection to MySQL server during query"
    #Kiểm tra dữ liệu trên MySQL và INSERT nếu dòng chưa có
    sql = "SELECT * FROM vn_40_published_list WHERE org_video_id = '"+str(video_id)+"' LIMIT 1"
    gxMysql.myCursor.execute(sql)
    readData = gxMysql.myCursor.fetchall()
    print(readData)
    if len(readData) > 0: #Đã tồn tại
      #Xoá dữ liệu trên MySQL
      sql = "DELETE FROM vn_40_published_list WHERE org_video_id = '"+str(video_id)+"'"
      gxMysql.myCursor.execute(sql)
      gxMysql.myDb.commit()
    #MySQL -> INSERT
    sql = "INSERT INTO vn_40_published_list (video_id,video_link,org_video_id,status) VALUES (%s,%s,%s,%s)"
    val = (str(publishInfo["id"]),str(publishInfo["link"]),str(video_id),"Published")
    gxMysql.myCursor.execute(sql, val)
    gxMysql.myDb.commit()
    
    # columnString = "video_id, video_link, org_video_id, status"
    # valueString  = "'"+str(publishInfo["id"])+"','"+str(publishInfo["link"])+"','"+str(video_id)+"','"+"Published"+"'"
    # gxMysql.insertRow("vn_40_published_list", columnString, valueString)
    
  def copyRowFromScannedListToReadyList(sefl,viddeoId:str):
    #Xóa video_id trong vn_30_ready_list nếu nó tồn tại
    sql = "DELETE FROM vn_30_ready_list WHERE video_id = '"+str(viddeoId)+"'"
    gxMysql.myCursor.execute(sql)
    gxMysql.myDb.commit()
    #Copy video_id từ vn_20_scanned_list sang vn_30_ready_list
    sql = "INSERT INTO vn_30_ready_list SELECT * FROM vn_20_scanned_list WHERE video_id='"+str(viddeoId)+"'"
    gxMysql.myCursor.execute(sql)
    gxMysql.myDb.commit()
    #Cập nhật status của video_id trong vn_30_ready_list thành "Ready"
    sql = "UPDATE vn_30_ready_list SET status = 'Ready' WHERE video_id = '"+str(viddeoId)+"'"
    gxMysql.myCursor.execute(sql)
    gxMysql.myDb.commit()
    
  def fetchOneClipFromReadyListForPublishing(self):
    '''
    =============================================================================
    Function: Lấy 1 clip trong danh sách vn_30_ready_list để publish:
              + Ưu tiên lấy theo thứ tự: ADS > NON-ADS
              + Nếu có Ready thì random một kết quả rồi trả về.
    Parameter: None
    Ruturn: Thông tin row của database về clip hoặc None.\n
    =============================================================================
    '''
    RETRY_MAX = 10
    retryCounter = 0
    #Get ADS clip
    sql = "SELECT * FROM vn_30_ready_list WHERE status = 'Ready' AND key_type='ads' ORDER BY RAND() LIMIT 1"
    gxMysql.myCursor.execute(sql)
    vn30Read = gxMysql.myCursor.fetchall()
    if len(vn30Read) != 0:
      pass
    else: #Get NON-ADS clip
      sql = "SELECT * FROM vn_30_ready_list WHERE status = 'Ready' ORDER BY RAND() LIMIT 1"
      gxMysql.myCursor.execute(sql)
      vn30Read = gxMysql.myCursor.fetchall()
      
    if len(vn30Read) != 0:
      logger.debug("Lấy clip từ vn_30_ready_list thành công:")
      logger.debug(vn30Read[0])
      
      #In ra tất cả các row của vn_30_ready_list
      sql = "SELECT video_id FROM vn_30_ready_list"
      gxMysql.myCursor.execute(sql)
      vn30ReadAll = gxMysql.myCursor.fetchall()
      logger.debug("vn_30_ready_list (id):")
      logger.debug(vn30ReadAll)
      
      
      return vn30Read[0] #Trả về thông tin row của database với status = Ready
    
    else:
      return None #Trả về None nếu không có kết quả nào có status = Ready
  
  def getWebPublishedList(self):
    '''Lấy danh sách các video đã được đăng trên web'''
    #Scroll down to bottom
    for i in range(0,3):
      print("scrolling down...")
      GUI.mouse.scroll(-2000,1000,500)

    #Mở trang Inpect code
    GUI.key.press('f12') #Mở trang inspect code
    LOTUS.color.waitColor((1902,85),rgb(110,110,110),30,15,200) #Wait scrollbar appear
    #Lấy code HTML
    htmlCode = self.__getCode()
    #Lấy danh sách các video đã được đăng
    htmlElementCLipList = htmlCode.xpath("//a[contains(@href,'tiktok.com/@')]")
    clipList = []
    for clip in htmlElementCLipList:
      clipLink = (clip.attrib['href'])
      videoId = clipLink.split('/')[-1]
      #add videoId to clipList
      clipList.append(videoId)
      # print("Added: "+videoId)
    
    print("Number of video published: "+str(len(clipList)))
    # print(clipList)
    
    #Tắt trang inspect code
    GUI.key.press('f12') #Mở trang inspect code
    LOTUS.color.waitNotColor((1902,85),rgb(255,110,110),30,15,200,False) #Wait scrollbar disappear
    
    return clipList

    
    
      
  ###############################################################################
  #####################          PRIVATE             ############################
  ###############################################################################
  #########################################################
  # Name: getCode
  # Function: Kiểm tra mở của sổ xem code và load hết code
  #           rồi trả về code HTML
  # Parameter: None
  # Return: Trả về htmlCode dạng string
  #########################################################
  def __getCode(self):
    GUI.mouse.click(1451,85) #Click vào tab Element. Images/7s.png
    LOTUS.color.waitColor((1911,108),rgb(163,163,163),40,15,200) #Wait scrollbar appear
    GUI.mouse.moveTo(1830,200) #Di chuyển chuột vào vùng code có thể cuộn chuột được.
    sleep(0.2)
    GUI.mouse.scroll(500) #Scroll lên trên cùng
    sleep(0.5)
    GUI.mouse.click(1400,110) #Click vào vị trí thẻ <!DOCUMENT html>.
    sleep(1)
    GUI.mouse.click(1400,110) #Click vào vị trí thẻ <!DOCUMENT html>.
    LOTUS.color.waitColor((1700,110),rgb(207,232,252),20,15,0) # đợi dòng được chọn
    sleep(0.3)
    GUI.key.press('down') #Xuống thẻ <html>
    sleep(0.5)
    GUI.key.hotkey('shift','f10') # Images/58s.png Mở bẳng dropbox
    sleep(1)
    GUI.key.press('c')
    sleep(0.5)
    GUI.key.press('c')
    sleep(0.5)
    GUI.key.press('enter')
    sleep(0.5)
    GUI.key.press('enter') #Chọn "copy element"
    sleep(0.5)
    GUI.key.press('up') #Tránh màn hình bị xanh do đang chọn code
    sleep(1)

    import lxml.etree as etree
    htmlCode = LOTUS.clipboard.pasteFromClipboardToVarBigData()
    # htmlCode = htmlCode.replace('\n',' ')
    htmlCode = etree.HTML(str(htmlCode))
    
    return htmlCode








################################################################
################################################################
################################################################
class tiktok_Wrapper():
  UPLOAD = tiktok_upload()
  videoLocation = "Z:\\Tmp"

  def __waitLoginStatus(self,timeout_sec:int=10):
    try:
      timeStart = time()
      while True:
        if IDE.assertVerify.verifyElementPresent("xpath=//a[@data-e2e='top-login-button']") == True:
          return "LOG_IN_BUTTON"
        elif IDE.assertVerify.verifyElementPresent("xpath=//a[@data-e2e='profile-icon']") == True:
          return "LOG_IN_ACCOUNT"
        elif IDE.assertVerify.verifyElementPresent("xpath=//p[text()='Continue with Google']") == True:
          return "LOG_IN_TABLE"
        elif time() - timeStart >= timeout_sec:
          return "TIMEOUT"
        sleep(0.1)
    except Exception as e:
      logger.error("Error: "+str(e))
      return "ERROR"
  
  def checkAndSolveCaptchaClick2SameImg(self):
    if IDE.assertVerify.verifyElementPresent("xpath=//div[contains(text(),'Select 2 objects that are the same')]") == True:
      logger.debug("Captcha Click 2 Same Img")
      imageUrl = IDE.others.others_content_getAttribute("xpath=//img[@draggable='false']","src")
      logger.debug("imageUrl: "+imageUrl)
      result = OMO.solveTiktokChoose2Same(imageUrl)
      IMAGE_POS = [0,0] #Vị trí x,y của hình Captcha
      if result[0] == True:
        posResult = result[1].split('|')
        GUI.mouse.click(IMAGE_POS[0]+int(posResult[0]),IMAGE_POS[1]+int(posResult[1])) #Click vào object 1
        sleep(200)
        GUI.mouse.click(IMAGE_POS[0]+int(posResult[2]),IMAGE_POS[1]+int(posResult[3])) #Click vào object 2
    
  def checkAndSolveCaptchaRotateImg(self):
    if IDE.assertVerify.verifyElementPresent("xpath=//div[contains(text(),'Drag the slider to fit the puzzle')]") == True:
      logger.debug("Captcha Rotate Img")
      imageUrlOutside = IDE.others.others_content_getAttribute("xpath=//img[@draggable='false'][1]","src")
      imageUrlInside  = IDE.others.others_content_getAttribute("xpath=//img[@draggable='false'][2]","src")
      logger.debug("imageUrlOutside: "+imageUrlOutside)
      logger.debug("imageUrlInside: " +imageUrlInside)
      result = OMO.solveTiktokRotateImage(imageInsidePathOrUrl=imageUrlInside,imageOutsidePathOrUrl=imageUrlOutside)
      if result[0] == True:
        angle = int(result[1])
        # SLIDER_POS = IDE.others.others_content_getPosMidElement("xpath=//div[@class='slider']")
        SLIDER_POS = [822,711] #Vị trí x,y của thanh slider
        GUI.mouse.move(SLIDER_POS[0],SLIDER_POS[1])
        sleep(0.2)
        GUI.mouse.dragRel(angle,0,0.5)

        
    
    
  def loginTiktokWithOtherEmail(self,USER_ACCOUNT:str="",USER_PASS:str=""):
    '''Login Tiktok with Other Email'''
    loginStatus = self.__waitLoginStatus()
    print("loginStatus: ",loginStatus)
    if loginStatus == "LOG_IN_BUTTON":
      IDE.mouseKey.click("xpath=//a[@data-e2e='top-login-button']")
      IDE.waitFor.waitForElementVisible("xpath=//p[text()='Continue with Google']")
      
    if loginStatus == "LOG_IN_BUTTON" or loginStatus == "LOG_IN_TABLE":
      IDE.mouseKey.click("xpath=//p[contains(text(),'email')]")
      IDE.waitFor.waitForElementVisible("xpath=//a[contains(text(),'Log in with email')]")
      sleep(0.5)
      IDE.mouseKey.click("xpath=//a[contains(text(),'Log in with email')]")
      IDE.waitFor.waitForElementVisible("xpath=//a[contains(text(),'Log in with phone')]")
      
      #Nhập email
      IDE.mouseKey.type("xpath=//input[@placeholder='Email or username']",USER_ACCOUNT)
      IDE.waitFor.waitForAttr("xpath=//input[@placeholder='Email or username']","value="+USER_ACCOUNT)
      
      #Nhập password
      # IDE.mouseKey.type("xpath=//input[@placeholder='Password']",USER_PASS)
      # IDE.others.others_clearReqWaitCmdFlg()
      # sleep(0.5)

      IDE.mouseKey.click("xpath=//input[@placeholder='Password']")
      IDE.others.others_clearReqWaitCmdFlg()
      sleep(0.5)
      LOTUS.clipboard.copyToClipboard(USER_PASS)
      sleep(0.2)
      LOTUS.clipboard.pasteFromClipboard()
      sleep(0.2)
      
      #Click vào nút đăng nhập
      loginCnt = 0
      while loginCnt < 100:
        loginCnt += 1
        try: #Quan trọng. Chỉ click nếu hình captcha chưa được mở.
          IDE.mouseKey.click("xpath=//button[@data-e2e='login-button']")
          IDE.others.others_clearReqWaitCmdFlg()
        except:
          pass
        sleep(1)
        if IDE.assertVerify.verifyElementPresent("id=captcha_container") == True:
          logger.info("Captcha appear")
          # self.checkAndSolveCaptchaClick2SameImg()
          # self.checkAndSolveCaptchaRotateImg()
          # checkAndSolveCaptchaSlideImg()
          # sleep(10)
          break
      
      
      
      
      

      pass
    
      
      
      

  def loginTiktokWithGoogleEmail(self,USER_ACCOUNT):
    '''Login Tiktok with Google Email'''
    loginStatus = self.__waitLoginStatus()
    print("loginStatus: ",loginStatus)
    if loginStatus == "LOG_IN_BUTTON":
      IDE.mouseKey.click("xpath=//a[@data-e2e='top-login-button']")
      IDE.waitFor.waitForElementVisible("xpath=//p[text()='Continue with Google']")
    
    if loginStatus == "LOG_IN_BUTTON" or loginStatus == "LOG_IN_TABLE":
      if "@gmail.com" in USER_ACCOUNT:
      #LOGIN WITH GOOGLE ACCOUNT
        IDE.mouseKey.click("xpath=//p[text()='Continue with Google']")
        LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/0_TiktokLogin_Icon.png",confidence=0.7,timeout_sec=60)
        sleep(1)
        GUI.mouse.click(x=960,y=550,tween=GUI.mouse.effect.easeInOutBounce, duration=0.5)
        sleep(0.2)
        GUI.mouse.click(960,550)
        sleep(0.3)
        GUI.mouse.click(960,550)
        LOTUS.log.addClickPosToHtmlLog(960,550)
        IDE.waitFor.waitForElementVisible("xpath=//div[@data-e2e='profile-icon']","60000")
      else:
      #LOGIN WITH OTHER ACCOUNT
        pass
    else:
    #Account logged in
      print("Account logged in")
    
  def reqManKill(self,containerName=""):
    os.system("echo "+containerName+" >> /HShare/0_AllChannels/0_ReqManKill.txt")
    
  def openChrome(self,userProfilePath="",headless=False,antiCaptcha=False):
    IDE.setup.begin("Chrome",userProfilePath=userProfilePath,headless=headless,antiCaptcha=antiCaptcha)
    # IDE.browser.open('https://www.tiktok.com/search?q=ABC')
    # IDE.waitFor.waitForElementVisible("xpath=//a[contains(@data-e2e,'tiktok-logo')]")
    
  def openTiktok(self):
    #1. Open homepage tiktok
    IDE.browser.open('https://www.tiktok.com/')
    IDE.waitFor.waitForElementVisible("xpath=//a[contains(@data-e2e,'tiktok-logo')]","","Đợi logo tiktok xuất hiện",False)

  def openGoDownloader(self):
    IDE.browser.open('https://godownloader.com/')
    IDE.waitFor.waitForElementVisible("id=goinput","","",False)
    
  def loadConfigGx(self):
    '''
    =============================================================================
    Function: Load các cấu hình của MySQL (Bảng vn_00 và vn_10) về class dataInfo.
    Parameter: None
    Ruturn: None
    =============================================================================
    '''
    #1. Load MySQL table config (00)
    sql = "SELECT * FROM vn_00_config LIMIT 1"
    gxMysql.myCursor.execute(sql)
    readData = gxMysql.myCursor.fetchall()
    dataInfo.cfg00_ena = readData[0]['ena']
    dataInfo.cfg00_key_check_num = readData[0]['key_check_num']

    #2. Load MySQL table key list (10)
    sql = "SELECT * FROM vn_10_key_list"
    gxMysql.myCursor.execute(sql)
    readData = gxMysql.myCursor.fetchall()
    
    self.maxList = len(readData)
    i = dataInfo.cfg00_key_check_num
    if i <= self.maxList:
      pass
    else:
      i = self.maxList
    dataInfo.key10_id        = dataInfo.cur_key_list_id = readData[i-1]['id']
    dataInfo.key10_key_word  = dataInfo.cur_key_word    = readData[i-1]['key_word']
    dataInfo.key10_key_type  = dataInfo.cur_key_type    = readData[i-1]['key_type']
    dataInfo.key10_scan_time = dataInfo.cur_scan_time   = readData[i-1]['scan_time']
    dataInfo.key10_total_num = dataInfo.cur_total_num   = readData[i-1]['total_num']
  
  def deleteVideoidFromPublishedList(self,video_id):
    '''Xóa video_id ra khỏi danh sách đã publish'''
    try:
      sql = "DELETE FROM vn_40_published_list WHERE video_id = '"+video_id+"'"
      gxMysql.myCursor.execute(sql)
      gxMysql.myDb.commit()
    except:
      pass
      
  def deleteVideoidFromReadyList(self,video_id):
    '''Xóa video_id ra khỏi danh sách đã publish'''
    try:
      sql = "DELETE FROM vn_30_ready_list WHERE video_id = '"+video_id+"'"
      gxMysql.myCursor.execute(sql)
      gxMysql.myDb.commit()
    except:
      pass
    
  def deleteBindAdsVideoidFromScannedList(self,video_id):
    '''Xóa video đó ở bảng vn_20 nếu nó thuộc dạng "bind" hoặc "ads".'''
    try:
      sql = "DELETE FROM vn_20_scanned_list WHERE video_id = '"+video_id+"' AND (video_type = 'bind' OR video_type = 'ads')"
      gxMysql.myCursor.execute(sql)
      gxMysql.myDb.commit()
    except:
      pass
  
  def getMysqlPublishedList(self):
    '''Lấy danh sách clip đã publish'''
    sql = "SELECT video_id,org_video_id FROM vn_40_published_list"
    gxMysql.myCursor.execute(sql)
    readData = gxMysql.myCursor.fetchall()
    video_id_list = []
    org_video_id_list = []
    for i in range(len(readData)):
      video_id_list.append(readData[i]['video_id'])
      org_video_id_list.append(readData[i]['org_video_id'])
    return video_id_list,org_video_id_list
  
  def getOverTimePublishedList(self,CLIP_LIMIT_HOURS:int):
    '''Lấy danh sách clip đã quá thời gian publish limit'''
    sql = "SELECT video_id FROM vn_40_published_list WHERE timestamp < DATE_SUB(NOW(), INTERVAL "+str(CLIP_LIMIT_HOURS)+" HOUR)"
    gxMysql.myCursor.execute(sql)
    readData = gxMysql.myCursor.fetchall()
    for i in range(len(readData)):
      readData[i] = readData[i]['video_id']
    return list(readData)
  
  def scanSearchList(self,keywords):
    '''
    =============================================================================
    Function: scanSearchList
    Description: scan từ khóa bằng việc nhập vào ô search rồi load hết nội dung.
    Parameter: keywords: từ khóa tìm kiếm.
    Ruturn: None
    =============================================================================
    '''
    IDE.browser.open("https://www.tiktok.com/search?q="+keywords)
    IDE.waitFor.waitForElementVisible("xpath=//a[contains(@data-e2e,'tiktok-logo')]")

    #Load đến khi nào hết nội dung tìm kiếm thì thôi
    lastClipNum = 0
    retryCnt = 0
    while True:
      try:
        waitReturn = IDE.waitFor.waitForElementVisible("xpath=//button[contains(@class,'ButtonMore')]","","Đợi nút Load More hiện ra",True)
        if waitReturn[0] == True: #Nếu có nút Load More thì click vào nút này
          #Kiểm tra clip load được nếu nút ButtonMore có xuất hiện nhưng không có clip nào thì thoát ra
          findResult = IDE.others.others_content_findAllElements("xpath=//div[contains(@class,'DivItemContainerForSearch')]","","",False)
          if findResult != None: 
            curClipNum = len(findResult)
            if curClipNum != lastClipNum:
              lastClipNum = curClipNum
            else:
              if retryCnt < 2:
                retryCnt += 1
              else:
                break #Thoát ra nếu không có clip nào mới được load khi nhấn nút Load More
          else:
            if retryCnt < 2:
              retryCnt += 1
            else:
              break #Thoát ra nếu không có clip nào mới được load khi nhấn nút Load More
          
          waitReturn[1].click()
          IDE.others.others_clearReqWaitCmdFlg()
          sleep(1)
        else:
          logger.info("Đã hết nội dung load Không có nút Load More")
          break
        self.checkAndWaitSlideCaptchaSolving()
      except Exception as errMessage:
        print(errMessage)
        print("Time out -> End Searching")
        break

  def delOldBindList (self,keywords:str):
    '''
    =============================================================================
    Function: delOldBindList
    Description: Nếu số lượng video chưa được Download (-999 và Failed) của từ khóa này:
      + Còn > 10 thì chỉ xóa các video -999 và Failed để cập nhật toàn bộ các video mới ở bước tiếp theo.
      + Nếu <= 10 thì toàn bộ video liên quan đến từ khóa này để cập nhật -999 toàn bộ.
    Parameter: keyWord: tên tài khoản kết nối đến.
    Ruturn: None
    =============================================================================
    '''
    #Kiểm tra dữ liệu trên MySQL và INSERT nếu dòng chưa có
    sql = "SELECT * FROM vn_20_scanned_list WHERE key_word = '"+keywords+"' AND key_type = 'bind' AND ( status = '-999' OR status = 'Failed') "
    gxMysql.myCursor.execute(sql)
    readData = gxMysql.myCursor.fetchall()
    
    if len(readData) > 10: #Số lượng video của từ khóa còn > 10 video chưa tải => Chỉ xóa các video -999 để ghi cái mới nhất.
      sql = "DELETE FROM vn_20_scanned_list WHERE key_word = '"+keywords+"' AND key_type = 'bind' AND ( status = '-999' OR status = 'Failed') "
      gxMysql.myCursor.execute(sql)
      gxMysql.myDb.commit()
    else: #Số lượng video của từ khóa còn <= 10. Xóa hết tất cả các video của từ khóa này và cập nhật lại -999 mới.
      sql = "DELETE FROM vn_20_scanned_list WHERE key_word = '"+keywords+"' AND key_type = 'bind'"
      gxMysql.myCursor.execute(sql)
      gxMysql.myDb.commit()

  def checkAndWaitSlideCaptchaSolving(self):
    if IDE.assertVerify.verifyElementPresent("class=captcha-disable-scroll") == True:
      IDE.waitFor.waitForElementNotPresent("class=captcha-disable-scroll") # /MyAPP/TiktopApp/GX/PIC/0_Captcha_Disable_Scroll.png
      sleep(2)
      
  def scanBindList(self,keywords:str):
    '''
    =============================================================================
    Function: scanBindList
    Description: scan từ khóa bằng việc kết nối với một tài khoản sẵn có nào đó và lấy video từ đó.
    Parameter: keywords: tên tài khoản kết nối đến.
    Ruturn: None
    =============================================================================
    '''
    IDE.browser.open("https://www.tiktok.com/search?q="+keywords)
    IDE.waitFor.waitForElementVisible("xpath=//a[contains(@data-e2e,'tiktok-logo')]") #Xuất hiện logo khi load xong.
    sleep(5) #Cần thiết để Tiktok ổn định hơn và cho load video nội dung (Nếu không sẽ dễ bị lỗi và chỉ cho phép 30 videos)
    self.checkAndWaitSlideCaptchaSolving()
    
    IDE.browser.open("https://www.tiktok.com/@"+keywords)
    IDE.waitFor.waitForElementVisible("xpath=//a[contains(@data-e2e,'tiktok-logo')]") #Xuất hiện logo khi load xong.
    sleep(5) #Cần thiết để Tiktok ổn định hơn và cho load video nội dung (Nếu không sẽ dễ bị lỗi và chỉ cho phép 30 videos)
    
    #Load đến khi nào hết nội dung tìm kiếm thì thôi
    lastClipNum = 0 #Số clip load được lần trước
    yPos = 0 #Scroll all clips
    i = 0 #Số lần scroll
    retryCnt = 0
    while True:
      try:
        findResult = IDE.others.others_content_findAllElements("xpath=//div[contains(@class,'DivItemContainerV2')]","","",False)
        if findResult != None: 
          curClipNum = len(findResult)
          if curClipNum != lastClipNum:
            lastClipNum = curClipNum
          else:
            if retryCnt < 2:
              retryCnt += 1
            else:
              break #Thoát ra nếu không có clip nào mới được load khi nhấn nút Load More
        else:
          if retryCnt < 2:
            retryCnt += 1
          else:
            break
        
        #Scroll to get more clips
        yPos += 5000
        i += 1
        print(i,"Scroll to: "+str(yPos))
        print("Current Clip Num: "+str(curClipNum))
        IDE.others.others_browser_scrollTo(0,yPos)
        IDE.others.others_clearReqWaitCmdFlg()
        self.checkAndWaitSlideCaptchaSolving()
        sleep(2)
      except Exception as errMessage:
        print(errMessage)
        print("Time out -> End Searching")
        break
      
  def appendScanList(self, videoLink, videoId,video_user):
    '''
    =============================================================================
    Function: Cập nhật lên scanList nếu thông tin về clip chưa tồn tại
    Parameter: None
    Ruturn: None
    =============================================================================
    '''
    #Kiểm tra dữ liệu trên MySQL và INSERT nếu dòng chưa có
    sql = "SELECT * FROM vn_20_scanned_list WHERE video_id = '"+str(videoId)+"' LIMIT 1"
    gxMysql.myCursor.execute(sql)
    readData = gxMysql.myCursor.fetchall()
    
    if len(readData) > 0: #Đã tồn tại
      pass
    else: #Chưa có trên MySQL -> INSERT
        sql = "INSERT INTO vn_20_scanned_list (video_id,video_user,video_link,key_word,key_type,status) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (str(videoId),str(video_user),str(videoLink),dataInfo.cur_key_word,dataInfo.cur_key_type,"-999")
        gxMysql.myCursor.execute(sql, val)
        gxMysql.myDb.commit()
  
  def captchaSolving(self):
    waitResult = IDE.assertVerify.verifyElementPresent("id=captcha-verify-image","","",False)
    if waitResult == True:
      print("==> Time1: %s" % time())
      # logger.debug("Captcha appeared !!!")
      captchaVerifyImageUrl = IDE.others.others_content_getAttribute("id=captcha-verify-image","src","",False)
      # print(captchaVerifyImageUrl)
      dragOffset = self.__calDragOffset(captchaVerifyImageUrl)
      # print(dragOffset)
      
      if dragOffset == None:
        return False
      else:
        print("==> Time2: %s" % time())
        IDE.mouseKey.dragAndDropToObjectOffset("xpath=//div[contains(@class,'captcha-drag-icon')]","",dragOffset,0)
        print("==> Time3: %s" % time())
        waitResult = IDE.waitFor.waitForElementNotVisible("id=captcha-verify-image",5000,"",False)
        if waitResult[0] == True:
          print("==> Time4: %s" % time())
          sleep(2)
        return True

  def getNewClip_1(self):
    '''
    =============================================================================
    Function: getNewClip
    Description: Tìm một clip ứng viên trong vn_20_clip_list chưa được đăng ở vn_40_clip_list, rồi trả về URL của nó:
      + Tìm trong vn_20_scanned_list có clip -999 hay không. Nếu có và clip này không tồn tại
        trong vn_40_clip_list thì trả về URL của clip này. Nêu có tồn tại thì chạy lại.
      + Nếu không có clip -999 trong vn_20_scanned_list thì tìm clip đã published trong vn_20_clip_list.
        Kiểm tra xem clip này có tồn tại trong vn_40_clip_list hay không. Nếu không thì trả về URL của clip này.
        Nếu có thì chạy lại.
      + Trả về None nếu sau 3 lần không tìm được đối tượng phù hợp.
    Parameter: None
    Ruturn:
      + (id,videoId,videoLink): nếu tìm được đối tượng.
      + None: nếu không tìm được đối tượng sau 3 lần tìm kiếm.
    =============================================================================
    '''
    #1. Tìm xem trong MySQL vn_20_scanned_list có clip nào có status = -999 hay không
    sql = "SELECT * FROM vn_20_scanned_list WHERE status = '-999' LIMIT 1"
    gxMysql.myCursor.execute(sql)
    readData = gxMysql.myCursor.fetchall()

    retry = 0
    while retry < 3: #Chạy lại tối đa 3 lần.
      retry += 1
      if len(readData) > 0: #Có clip nào có status = -999
        #2. Lấy clip này ra
        videoLink = readData[0]['video_link']
        videoId = readData[0]['video_id']
        id = readData[0]['id']
        #3. Cập nhật lại status = Published
        sql = "UPDATE vn_20_scanned_list SET status = 'Published' WHERE video_id = '"+str(videoId)+"'"
        gxMysql.myCursor.execute(sql)
        gxMysql.myDb.commit()
        #4. Kiểm tra nế clip id này có trong list vn_40_published_list hay không
        sql = "SELECT * FROM vn_40_published_list WHERE org_video_id = '"+str(videoId)+"' LIMIT 1"
        gxMysql.myCursor.execute(sql)
        readData = gxMysql.myCursor.fetchall()
        if len(readData) > 0: #Đã có trong list vn_40_published_list -> Tìm clip khác
          continue 
        else: #Chưa có trong list vn_40_published_list -> Return clip này
          return id,videoId,videoLink
      else:
        #5.Random a Published clip if there is no status -999
        sql = "SELECT * FROM vn_20_scanned_list WHERE status = 'Published' ORDER BY RAND() LIMIT 1"
        gxMysql.myCursor.execute(sql)
        readData = gxMysql.myCursor.fetchall()
        if len(readData) > 0:
          videoLink = readData[0]['video_link']
          videoId = readData[0]['video_id']
          id = readData[0]['id']
        #6. Kiểm tra nế clip id này có trong list vn_40_published_list hay không
        sql = "SELECT * FROM vn_40_published_list WHERE org_video_id = '"+str(videoId)+"' LIMIT 1"
        gxMysql.myCursor.execute(sql)
        readData = gxMysql.myCursor.fetchall()
        if len(readData) > 0: #Đã có trong list vn_40_published_list -> Tìm clip khác
          continue 
        else: #Chưa có trong list vn_40_published_list -> Return clip này
          return id,videoId,videoLink
    return None

  #Kiểm tra số lượng video bind trong vn_20_scanned_list có status là -999. Nếu số lượng < 20 thì đổi trạng thái của các video với kiểy key_type là bind với trạng thái Downloaded thành -999.
  def checkBindVideo(self):
    '''
     Kiểm tra số lượng video bind trong vn_20_scanned_list có status là -999.
     - Nếu 0 < số lượng <= 20 thì đổi trạng thái của các video với kiểy key_type là bind với trạng thái Downloaded thành -999.
     - Đồng thời xóa hết các video với key_type là bind trong bảng vn_30_ready_list.
    '''
    
    sql = "SELECT * FROM vn_20_scanned_list WHERE status = '-999' AND key_type = 'bind'"
    gxMysql.myCursor.execute(sql)
    readData = gxMysql.myCursor.fetchall()
    # logger.debug("DEBUG 1: checkBindVideo: len(readData) = %d",len(readData))
    if 0 < len(readData) <= 20:
      #Nếu số lượng <= 20 thì đổi trạng thái của các video với kiểy key_type là bind với trạng thái Downloaded thành -999
      sql = "UPDATE vn_20_scanned_list SET status = '-999' WHERE status = 'Downloaded' AND key_type = 'bind'"
      # logger.debug("DEBUG 2: checkBindVideo: sql = ",sql)
      gxMysql.myCursor.execute(sql)
      gxMysql.myDb.commit()
      #Đồng thời xóa hết các video với key_type là bind trong bảng vn_30_ready_list.
      sql = "DELETE FROM vn_30_ready_list WHERE key_type = 'bind'"
      # logger.debug("DEBUG 3: checkBindVideo: sql = ",sql)
      gxMysql.myCursor.execute(sql)
      gxMysql.myDb.commit()
    

  def checkSimilarity(self):
    '''
    Kiểm tra tính tương đồng của video trong thư mục /HShare/0_AllTasks/1_ready_list/bind và bảng vn_30_ready_list từ MySQL với key_type là bind và trạng thái status là Ready.
    - Chỉ giữ lại các video trong thư mục và dữ liệu từ bảng vn_30_ready_list nếu nó trùng nhau.
    - Nếu không trùng nhau thì xóa video trong thư mục và dữ liệu trong bảng vn_30_ready_list.
    '''
    #1. Lấy danh sách các video trong thư mục 0_scnned_list\bind
    videoList = os.listdir('/HShare/0_AllTasks/1_ready_list/bind')
    print("Video list: ",videoList)
    #2. Lấy danh sách các video trong bảng vn_30_ready_list
    sql = "SELECT * FROM vn_30_ready_list WHERE key_type = 'bind' AND status = 'Ready'"
    gxMysql.myCursor.execute(sql)
    readData = gxMysql.myCursor.fetchall()
    print("Read data: ",readData)
    #3. So sánh 2 danh sách này
    matchList = []
    unmatchedVideoList = []
    unmatchedMysqlList = []
    for video in videoList:
      videoId = video.split(".mp4")[0].split("_")[-1]
      for row in readData:
        print("Video id: ",videoId, " - Row video id: ",row['video_id'])
        if videoId == row['video_id']:
          matchList = matchList + [videoId]
    print("Match list: ",matchList)
    #4. Tìm ra những video không có trong bảng vn_30_ready_list
    unmatchedVideoList = [video for video in videoList if video.split(".mp4")[0].split("_")[-1] not in matchList]
    unmatchedMysqlList = [row['video_id'] for row in readData if row['video_id'] not in matchList]
    print("Unmatched video list: ",unmatchedVideoList)
    print("Unmatched mysql list: ",unmatchedMysqlList)
    #5. Xóa những video không có trong bảng vn_30_ready_list
    for video in unmatchedVideoList:
      os.remove('/HShare/0_AllTasks/1_ready_list/bind/'+video)
    #6. Xóa những video không có trong MySQL
    for videoId in unmatchedMysqlList:
      sql = "DELETE FROM vn_30_ready_list WHERE video_id = '"+str(videoId)+"'"
      gxMysql.myCursor.execute(sql)
      gxMysql.myDb.commit()

    

  def fetchNewClip(self,clipType:str="search",status:str="-999",randQuery:bool=False):
    '''
    =============================================================================
    Function: fetchNewClip
    Description: Tìm một clip ứng viên trong vn_20_scanned_list có status là -999, rồi trả về video_id và video_link của nó.
    Parameter:
      + clipType: Loại clip cần tìm. Có các giá trị: search, tag, bind .Default = search.
      + status: Trạng thái của clip cần tìm. Có các giá trị: -999, Downloaded.
      + randQuery: Nếu là True thì sẽ random một clip trong danh sách. Nếu là False thì sẽ lấy clip đầu tiên trong danh sách.
    Ruturn:
      + (id,videoId,videoLink): nếu tìm được đối tượng.
      + None: nếu không tìm được đối tượng.
    '''
    if randQuery == True:
      randQueryReq = "ORDER BY RAND() "
    else:
      randQueryReq = ""
    #Query data
    sql = "SELECT * FROM vn_20_scanned_list WHERE key_type='"+clipType+"' AND status = '"+status+"' "+randQueryReq+" LIMIT 1"
    gxMysql.myCursor.execute(sql)
    readData = gxMysql.myCursor.fetchall()
    if len(readData) > 0:
      videoLink = readData[0]['video_link']
      videoId = readData[0]['video_id']
      id = readData[0]['id']
      keyWord = readData[0]['key_word']
      keyType = readData[0]['key_type']
      videoUser = readData[0]['video_user']
      return (id,videoId,videoLink,keyType,keyWord,videoUser)
    else:
      return None
    
  def downloadNoWaterMarkVideoGui(self,videoLink:str,videoId,keyType:str,keyWord:str,videoUser:str):
    '''
    =============================================================================
    Function: downloadNoWaterMarkVideo
    Description: Download video không có watermark.
    Parameter:
      + videoLink: link của video.
      + videoId: id của video.
      + keyType: loại từ khóa.
      + keyWord: từ khóa.
    Return:
      + True: nếu download thành công.
      + False: nếu download thất bại.
    =============================================================================
    '''
    maxRetry = 1
    retryDownload = 0
    keyWord = keyWord.replace(" ","_")
    os.system("rm /root/Downloads/*.mp4") #Xóa các file video cũ
    while retryDownload <= maxRetry:
      downPath = "/root/Downloads"
      os.system("rm -rdf "+downPath+"/*")
      #1. Input video link
      #https://www.tiktok.com/@thaohiepchau/video/7095925670290722074
      #https://godownloader.com/#link=https%3A%2F%2Fwww.tiktok.com%2F%40thaohiepchau%2Fvideo%2F7095925670290722074
      videoLinkDecode = videoLink
      videoLinkDecode = videoLinkDecode.replace(":","%3A")
      videoLinkDecode = videoLinkDecode.replace("/","%2F")
      videoLinkDecode = videoLinkDecode.replace("@","%40")
      videoLinkDecode = "https://godownloader.com/#link="+videoLinkDecode
      logger.info("VIDEO: "+videoLinkDecode)

      GUI.mouse.click(1500,50) #Click vào thanh địa chỉ
      LOTUS.clipboard.copyToClipboard(videoLinkDecode); sleep(0.1)
      
      GUI.key.hotkey("ctrl","v"); sleep(0.1)
      GUI.key.press("enter"); sleep(0.3)
      GUI.mouse.click(1500,50) #Click vào thanh địa chỉ
      GUI.key.press("enter"); sleep(1)
      #Wait and click to download video
      sleep(10) #Chờ 10 giây để chuyển trang.
      LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/0_DownloadVideoNoWatermark.png",confidence=0.7,timeout_sec=60)
      sleep(3) #Chờ để hình ảnh được nhảy lên đầu trang (Do lỗi của web)
      LOTUS.log.addRectScreenCaptureToHtmlLog(region_xyxy=(740,80,1170,350))
      LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_DownloadVideoNoWatermark.png",confidence=0.7,timeout_sec=30)
      print(datetime.datetime.now())
      sleep(1)
      
      #Chờ video được tải xong trong tối đa 2 phút. Sau đó, đổi tên và di chuyển video.
      #1. Kiểm tra file tồn tại
      curPathWildCard = downPath+"/*"+videoId+"*com.mp4"
      downloadingPath = curPathWildCard+".crdownload"
      newPath = self.videoLocation+"/"+keyType+"_"+keyWord+"_"+videoUser+"_"+videoId+".mp4"
      checkDownloadingStatus = str(os.system("ls "+downloadingPath))
      print("Check status: "+checkDownloadingStatus)
      
      #Wait 60s for download video
      import time
      WAIT_TIME_SECONDS = 180
      startDownloadTime = time.time()
      while time.time() - startDownloadTime < WAIT_TIME_SECONDS:
        if checkDownloadingStatus != '0': #File *.crdownload không tồn tại nữa => File đã tải xong.
          try:
            #Kiểm tra file có tồn tại không
            if str(os.system("ls "+curPathWildCard)) != '0':
              logger.warn(">>>>> File tải về bị lỗi, không tồn tại => Tải lại")
              return False
            else:
              os.system("mv -f "+curPathWildCard+" "+newPath)
              #Kiểm tra kích thuớc file. Nếu file có kích thước nhỏ hơn 1MB => File tải về bị lỗi.
              fileSize = os.path.getsize(newPath)
              if fileSize < 100*1024: #<100KB
                logger.warn(">>>>> File tải về bị lỗi, kích thước nhỏ hơn 100KB => Tải lại")
                os.system("rm -f "+newPath)
                return False
              logger.debug(">>>>> File đã tải xong: "+newPath)
              LOTUS.log.addRectScreenCaptureToHtmlLog(caption="Download Status",textColor=(0,0,255),region_xyxy=(0,1020,1890,1079))
              return True
          except Exception as e:  
            print(e)
        else:
          print(">>>>> File chưa tải xong. Thời gia chờ còn lại: "+str(int(WAIT_TIME_SECONDS - (time.time() - startDownloadTime)))+" giây")
          sleep(1)
          checkDownloadingStatus = str(os.system("ls "+downloadingPath))
          print("Check status: "+checkDownloadingStatus)
      logger.warn(">>>>> File chưa tải xong sau 3 phút")
      LOTUS.log.addRectScreenCaptureToHtmlLog(caption="Download Status",textColor=(0,0,255),region_xyxy=(0,1020,1890,1079))
      if retryDownload < maxRetry:
        retryDownload += 1 #Retry lại 1 lần nữa.
        continue
      else:
        return False
        
  def downloadNoWaterMarkVideoSele(self,videoLink:str,videoId,keyType:str,keyWord:str,videoUser:str):
    '''
    =============================================================================
    Function: downloadNoWaterMarkVideo
    Description: Download video không có watermark.
    Parameter:
      + videoLink: link của video.
      + videoId: id của video.
      + keyType: loại từ khóa.
      + keyWord: từ khóa.
    Return:
      + True: nếu download thành công.
      + False: nếu download thất bại.
    =============================================================================
    '''
    maxRetry = 1
    retryDownload = 0
    while retryDownload <= maxRetry:
      #1. Input video link
      #https://www.tiktok.com/@thaohiepchau/video/7095925670290722074
      #https://godownloader.com/#link=https%3A%2F%2Fwww.tiktok.com%2F%40thaohiepchau%2Fvideo%2F7095925670290722074
      videoLinkDecode = videoLink
      videoLinkDecode = videoLinkDecode.replace(":","%3A")
      videoLinkDecode = videoLinkDecode.replace("/","%2F")
      videoLinkDecode = videoLinkDecode.replace("@","%40")
      videoLinkDecode = "https://godownloader.com/#link="+videoLinkDecode
      print(videoLinkDecode)
      
      IDE.browser.open("https://www.google.com")
      waitResult = IDE.waitFor.waitForElementVisible("xpath=//img[@alt='Google']","","Đợi logo Google hiện ra",True)
      IDE.browser.open(videoLinkDecode)
      waitResult = IDE.waitFor.waitForElementVisible("xpath=//a[contains(text(),'Video No Watermark')]","","Đợi link tải Video No Watermark xuất hiện",True)

      if waitResult[0] == True:
        videoDownloadLink = IDE.others.others_content_getAttribute("xpath=//a[contains(text(),'Video No Watermark')]","href","hrefNoWaterMark",False)
        print(videoDownloadLink)
        #2. Download video
        try:
          kwargs = {'allow_redirects': True}
          r = requests.get(videoDownloadLink, **kwargs)
          keyType = keyType.replace(" ","")
          keyWord = keyWord.replace(" ","")
          
          videoSavePath = self.videoLocation+"/"+keyType+"_"+keyWord+"_"+videoUser+"_"+str(videoId)+".mp4"
          with open(f'{videoSavePath}', "wb",encoding="utf-8") as f:
              f.write(r.content) #Lưu video lại nếu có cửa sổ video mở ra.
          retryDownload = 0
          return True
        except: 
          if retryDownload < maxRetry:
            retryDownload += 1 #Retry lại 1 lần nữa.
            continue
          else:
            return False
      else:
        if retryDownload < maxRetry:
          retryDownload += 1 #Retry lại 1 lần nữa.
          continue
        else:
          return False

  #Update status của clip trong mysql vn_20_scanned_list
  def updateClipStatus(self,id,status):
    '''
    =============================================================================
    Function: updateClipStatus
    Description: Update status của clip trong mysql vn_20_scanned_list.
    Parameter:
      + id: id của clip.
      + status: status của clip.
    Return: None
    =============================================================================
    '''
    sql = "UPDATE vn_20_scanned_list SET status = '"+str(status)+"' WHERE id = '"+str(id)+"'"
    gxMysql.myCursor.execute(sql)
    gxMysql.myDb.commit()

  def loginLineAccount(self,username,password):
    '''
    =============================================================================
    Function: uploadVideoToTiktok
    Description: Upload video vào tiktok.
    Parameter:
      + videoLink: link của video.
      + videoId: id của video.
    Return:
      + True: nếu upload thành công.
      + False: nếu upload thất bại.
    =============================================================================
    '''
    #1. Click button Đăng nhập
    IDE.mouseKey.click("xpath=//button[contains(@data-e2e,'top-login-button')]","","Click button Đăng nhập")
    #2. Đợi mở popup login
    IDE.waitFor.waitForElementVisible("xpath=//div[text()='Continue with LINE']","","Đợi button Continue with LINE xuất hiện",True)
    #3. Click button Continue with LINE
    IDE.mouseKey.click("xpath=//div[text()='Continue with LINE']","","Click button Continue with LINE")
    while WEB.browserTabNum == 1: #Chờ cửa sổ mới hiện ra
      sleep(1)
      WEB.refreshBrowserTabInfo()
    IDE.others.others_clearReqWaitCmdFlg()
    #4. Chuyển sang của sổ nhập USER/PASS của LINE
    IDE.browser.selectWindow("tab=1")
    IDE.waitFor.waitForElementVisible("xpath=//input[@name='tid']")
    #5. Nhập USER NAME/PASSWORD
    IDE.mouseKey.type("xpath=//input[@name='tid']",username,"Nhập USER NAME")
    IDE.others.others_clearReqWaitCmdFlg()
    IDE.mouseKey.type("xpath=//input[@name='tpasswd']",password,"Nhập PASSWORD")
    IDE.others.others_clearReqWaitCmdFlg()
    IDE.mouseKey.click("xpath=//button[@type='submit']","","Click button Đăng nhập")
    IDE.others.others_clearReqWaitCmdFlg()
    IDE.browser.selectWindow("tab=0","","Trả về cửa sổ chính sau khi Login")
    IDE.others.others_clearReqWaitCmdFlg()
    #6. Chờ đóng web đóng hết các của sổ khác trong tối đa 20x1000ms = 20s.
    for i in range (0,20):
      if WEB.refreshBrowserTabNumOnly() == 1:
        sleep(3)
        break
      sleep(1)
    
  def _inputPassword(self,password:str=""):
    '''
    =============================================================================
    Function: _inputPassword
    Description: Input password vào màn hình password khi đăng nhập tài khoản Gmail
    Parameter:
      + password: password của tài khoản Gmail.
    Return: None
    =============================================================================
    '''
    #Click store password
    # GUI.mouse.click(x=787,y=610) #Vị trí nút ghi nhớ Password
    # sleep(0.5)
    if LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_PassInput.png",confidence=0.7,timeout_sec=10) == False:
      GUI.mouse.doubleClick(x=830,y=575) #Vị trí Password
    sleep(0.5)
    LOTUS.clipboard.copyToClipboard(password)
    sleep(0.1)
    LOTUS.clipboard.pasteFromClipboard()
    sleep(0.1)
    GUI.key.press("enter")
        
    #Chờ đăng nhập thành công
    loginSuccess = LOTUS.wait.waitNotImage("/MyAPP/TiktopApp/GX/PIC/0_BrowerAccountLoginStatus.png",0.8,15,2)

    if loginSuccess == False:
      logger.error("Đăng nhập không thành công -> EXIT")
      containerName = os.getenv("CONTAINER_NAME")
      os.system("echo "+containerName+" >> /HShare/0_AllChannels/0_ReqManKill.txt")
      exit()
    else:
      logger.info("Đăng nhập thành công: %s","googleUser")

  def googleAccountLogin(self,user:str="",password:str=""):
    '''Kiểm tra xem có đang đăng nhập tài khoản google từ trước không?
    1. Nếu có thì tiếp tục.
    2. Nếu không có thì đăng nhập.'''
    
    if len(LOTUS.imageAction.findAllImageOnScreen("/MyAPP/TiktopApp/GX/PIC/0_BrowerAccountLoginStatus.png",0.8)) > 0:
      AccLoginStatus = False #Chưa đăng nhập tài khoản Google
    else:
      AccLoginStatus = True #Đã đăng nhập tài khoản Google
    
    if AccLoginStatus == True:
      logger.info("Đã đăng nhập tài khoản Google")
      return "LOGGED_IN"
    else:
      logger.info("Chưa đăng nhập tài khoản Google")
      # GUI.mouse.click(x=1400,y=50,tween=GUI.mouse.effect.easeInOutBounce, duration=0.5) #Vị trí thanh address bar
      GUI.mouse.click(x=1400,y=50)
      sleep(0.1)
      GUI.key.hotkey("ctrl","a")
      sleep(0.1)
      LOTUS.clipboard.copyToClipboard("https://accounts.google.com")
      sleep(0.2)
      LOTUS.clipboard.pasteFromClipboard()
      sleep(0.2)
      GUI.key.press("enter")
      sleep(0.5)
      #Chờ màn hình chuyển
      result = LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/022.png",confidence=0.7,timeout_sec=30)
      print("result = ",result)
      #Kiểm tra trạng thái đăng nhập
      #1. Login mới.
      #2. Login lại.
      loginStatus = "UNKNOWN"
      loginStatus = LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/0_NewLogin.png",confidence=0.7,timeout_sec=2)
      if loginStatus != False:
        loginStatus = "NEW_LOGIN" # PIC/019.png
      else:
        loginStatus = "RE_LOGIN"
      
      if loginStatus == "NEW_LOGIN":
        logger.info("NEW_LOGIN")
        self.__inputUserName(user)
        #Chờ màn hình password hiện ra
        for i in range (0,4):
          waitImage = LOTUS.wait.waitImage('/MyAPP/TiktopApp/GX/PIC/0_passwordScreenAppear.png',confidence=0.7) # PIC/0_passwordScreenAppear.png
          if waitImage == False:
            if i == 3: #Nếu chưa hiện màn hình password sau 3 lần thì exit
              containerName = os.getenv("CONTAINER_NAME")
              os.system("echo "+containerName+" >> /HShare/0_AllChannels/0_ReqManKill.txt")
              exit()
            logger.info("Chưa hiện màn hình password. Nhấn nút BACK rồi Retry lần: "+str(i+1))
            GUI.mouse.click(22,52,tween=GUI.mouse.effect.easeInOutBounce, duration=0.5) #Nhấn vào nút BACK của Browser
            sleep(3)
            self.__inputUserName(user)
          else:
            break
        self._inputPassword(password)
        return "NEW_LOGIN"
                          
      if loginStatus == "RE_LOGIN":
        GUI.mouse.click(x=1000,y=500,tween=GUI.mouse.effect.easeInOutBounce, duration=0.5) #Vị trí tài khoản
        sleep(0.5)
        GUI.mouse.click(x=1000,y=500,tween=GUI.mouse.effect.easeInOutBounce, duration=0.5) #Vị trí tài khoản
        LOTUS.log.addClickPosToHtmlLog(1000,500)
        logger.info("LOGIN AGAIN")
        self._inputPassword(password)
        return "RE_LOGIN"


  def __inputUserName(self, user):
      if LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_EmailInput.png",confidence=0.7,timeout_sec=10) == False:
        GUI.mouse.doubleClick(x=830,y=520,tween=GUI.mouse.effect.easeInOutBounce, duration=0.5) #Vị trí Email
        LOTUS.log.addClickPosToHtmlLog(830,520)
      sleep(0.1)
      LOTUS.clipboard.copyToClipboard(user)
      sleep(0.2)
      LOTUS.clipboard.pasteFromClipboard()
      sleep(0.2)
      GUI.key.press("enter")

  def removeUploadVideo(self,uploadFile:str):
    #Delete all video
    fileName = uploadFile.split("/")[-1]
    delAllVideoPath = uploadFile.replace(fileName,SYS.pcInfo.pcName()+"*")
    print("delAllVideoPath = ",delAllVideoPath)
    os.system("rm -f "+delAllVideoPath)
    logger.info("Remove: %s",delAllVideoPath)

  def createUploadVideo(self,READY_LIST_PATH, fetchDatabase):
    keyType   = fetchDatabase["key_type"].replace(" ","_")
    keyWord   = fetchDatabase["key_word"].replace(" ","_")
    videoUser = fetchDatabase["video_user"]
    videoId   = fetchDatabase["video_id"]
    #Set sub location
    if keyType == "ads":
      subLocation = "/ads"
    elif keyType == "bind":
      subLocation = "/bind"
    elif keyType == "search":
      subLocation = "/approve"
    elif keyType == "tag":
      subLocation = "/approve"
    else:
      subLocation = "/approve"
    #Create upload file
    clipLocation = READY_LIST_PATH+subLocation+"/"+keyType+"_"+keyWord+"_"+videoUser+"_"+str(videoId)+".mp4"
    ranNum = random.randrange(1111,9999,1)
    if not os.path.exists(READY_LIST_PATH+"/processing"):
      os.system("mkdir -p "+READY_LIST_PATH+"/processing")
    uploadFile = READY_LIST_PATH+"/processing/"+SYS.pcInfo.pcName()+"_SONY_video_capture_"+str(ranNum)+".mp4"
    import shutil
    shutil.copyfile(clipLocation, uploadFile)
    os.system("rm -f /root/*.mp4")
    os.system("ln -sf "+uploadFile+" /root/uploadFile.mp4")
    logger.info("Upload file: %s",uploadFile)
    return uploadFile

  def removeBindAdsVideo(self,READY_LIST_PATH, fetchDatabase):
    keyType   = fetchDatabase["key_type"].replace(" ","_")
    videoId   = fetchDatabase["video_id"]
    if keyType == "bind":
      subLocation = "/bind"
    elif keyType == "ads":
      subLocation = "/ads"
    else:
      return None
    
    #Xóa file có chứa videoId trong thư mục READY_LIST_PATH
    delVideoPath = READY_LIST_PATH+subLocation+"/*"+str(videoId)+".mp4"
    try:
      os.system("rm -f "+delVideoPath)
      logger.info("Remove Bind Video: %s",delVideoPath)
    except:
      logger.error("Remove Bind Video: %s",delVideoPath)
    
  def convertNewVideoidToOldVideoid(self,clearVn40MysqlList:list):
    '''Đổi video_id (video mới đăng) của bảng vn_40 thành video_id (video gốc) của bảng vn_30'''
    org_video_id_list = list()
    for newVideoId in clearVn40MysqlList:
      #Lấy org_video_id (video gốc) của bảng vn_40_published_list
      sql = "SELECT org_video_id FROM vn_40_published_list WHERE video_id = '"+str(newVideoId)+"'"
      gxMysql.myCursor.execute(sql)
      readData = gxMysql.myCursor.fetchall()
      
      if len(readData) > 0:
        org_video_id_list.append(readData[0]["org_video_id"])
      else:
        continue
      
    return org_video_id_list
    
  def clearContainerExeptLogs(self):
    FORCE_DEBUG_STATUS = os.getenv('FORCE_DEBUG_STATUS')
    CUR_WORKDIR = os.getcwd()
    logger.info("FORCE_DEBUG_STATUS: "+str(FORCE_DEBUG_STATUS))
    logger.info("CUR_WORKDIR: "+CUR_WORKDIR)
    if "/HShare/" in CUR_WORKDIR and "/code" in CUR_WORKDIR and FORCE_DEBUG_STATUS!="True" and FORCE_DEBUG_STATUS!="None": #Container: /HShare/data/channel_tik_vn_gx_1/task_3/taskContainer_1678106382/code
      logger.info("### Clear Container Exept Logs ###")
      logger.info("Clear Done! "+CUR_WORKDIR)
      os.system("rm *")
      os.system("rm -rf ./Conf")
      os.system("rm -rf ./Library")
      os.system("rm -rf ./NasScripts")
      os.system("rm -rf ./SystemManager")
      os.system("rm -rf ./MyAPP")
      os.system("rm -rf ./__pycache__")
    

  ###############################################################################
  #####################          PRIVATE             ############################
  ###############################################################################
  def __calDragOffset(self,imageUrl=""):
    '''
    =============================================================================
    Function: Tính toán offset cần rê của slide để giải captcha
    Parameter: imageUrl: đường dẫn đến file ảnh
    Ruturn:
      + Nếu có: slideOffset
      + Nếu không tính đượC: None
    =============================================================================
    '''
    holePos = self.__findHoleOfDragIcon(imageUrl)
    # print(holePos)
    if holePos != None:
      xPos = holePos[2]
      return int(xPos*271/454)
    else:
      return None

  def __findHoleOfDragIcon(self, imageUrl=""):
    '''
    =============================================================================
    Function: Tìm vị trí lỗ của drag icon trong ảnh.
    Parameter: imageUrl: đường dẫn đến file ảnh
    Ruturn:
      + Tìm thấy: (<imageWidth>,<imageHeight>,<dragPosX>,<dragPosY>)
      + Không tìm thấy: None
    Ex: findHoleOfDragIcon("https://p19-captcha-sg.ibyteimg.com/tos-alisg-i-ovu2ybn2i4-sg/57942e928b8245cf81a2ccb8f765ef7e~tplv-ovu2ybn2i4-2.jpeg")
        => Return: (552,344,364,71)
        PIC: MyAPP/TiktopApp/GX/PIC/002.jpeg
        RESULT: MyAPP/TiktopApp/GX/PIC/003.png
    =============================================================================
    '''
    from urllib.request import urlopen
    from PIL import Image
    imageData = Image.open(urlopen(imageUrl))
    imageWidth, imageHeight = imageData.size

    brightColor = (230,230,230)
    darkColor = (75,75,75)
    deltaBrightColor = 30
    deltaDarkColor = 75
    checkFromX = 5 + 86 + int(86/2) #86 là kích thước của cục drag icon
    checkToX = imageWidth -86 - int(86/2) #86 là kích thước của cục drag icon
    checkFromY = 5 + int(86/2) #86 là kích thước của cục drag icon
    checkToY = imageHeight -86 #86 là kích thước của cục drag icon

    for yLoc in range(checkFromY,checkToY):
      for xLoc in range(checkFromX,checkToX):
        # if LOTUS.color.checkColorWithoutCapture(imageData,(xLoc,   yLoc   ),brightColor,deltaBrightColor,0) and\
        #    LOTUS.color.checkColorWithoutCapture(imageData,(xLoc,   yLoc+5 ),brightColor,deltaBrightColor,0) and\
        #    LOTUS.color.checkColorWithoutCapture(imageData,(xLoc,   yLoc+10),brightColor,deltaBrightColor,0) and\
        #    LOTUS.color.checkColorWithoutCapture(imageData,(xLoc+5 ,yLoc-1 ),brightColor,deltaBrightColor,0) and\
        #    LOTUS.color.checkColorWithoutCapture(imageData,(xLoc+10,yLoc-1 ),brightColor,deltaBrightColor,0) and\
        #    LOTUS.color.checkColorWithoutCapture(imageData,(xLoc+2 ,yLoc   ),darkColor,deltaDarkColor,0) and\
        #    LOTUS.color.checkColorWithoutCapture(imageData,(xLoc+2 ,yLoc+5 ),darkColor,deltaDarkColor,0) and\
        #    LOTUS.color.checkColorWithoutCapture(imageData,(xLoc+2 ,yLoc+10),darkColor,deltaDarkColor,0) and\
        #    LOTUS.color.checkColorWithoutCapture(imageData,(xLoc+5 ,yLoc   ),darkColor,deltaDarkColor,0) and\
        #    LOTUS.color.checkColorWithoutCapture(imageData,(xLoc+10,yLoc   ),darkColor,deltaDarkColor,0) :
        #    return (imageWidth,imageHeight,xLoc,yLoc)
        
        if LOTUS.color.checkColorWithoutCapture(imageData,(xLoc,   yLoc   ),brightColor,deltaBrightColor,0) and\
           LOTUS.color.checkColorWithoutCapture(imageData,(xLoc,   yLoc+5 ),brightColor,deltaBrightColor,0) and\
           LOTUS.color.checkColorWithoutCapture(imageData,(xLoc+5 ,yLoc-1 ),brightColor,deltaBrightColor,0) and\
           LOTUS.color.checkColorWithoutCapture(imageData,(xLoc+10,yLoc-1 ),brightColor,deltaBrightColor,0) and\
           LOTUS.color.checkColorWithoutCapture(imageData,(xLoc+2 ,yLoc+5 ),darkColor,deltaDarkColor,0) and\
           LOTUS.color.checkColorWithoutCapture(imageData,(xLoc+2 ,yLoc+10),darkColor,deltaDarkColor,0) and\
           LOTUS.color.checkColorWithoutCapture(imageData,(xLoc+10,yLoc   ),darkColor,deltaDarkColor,0) :
           return (imageWidth,imageHeight,xLoc,yLoc)
    return None

  def deleteVideoFromProfile(self,videoLink):
    '''
    =============================================================================
    Function: Xóa video khỏi profile
    Parameter: videoId: id của video cần xóa
    Ruturn: True/False
    =============================================================================
    '''
    #Click vào thanh address bar và gõ địa chỉ
    LOTUS.clipboard.copyToClipboard(videoLink);sleep(0.1)
    GUI.mouse.click(1600,50);sleep(1)
    LOTUS.clipboard.pasteFromClipboard();sleep(0.1)
    GUI.key.press("enter");sleep(0.5)
    GUI.mouse.click(1600,50);sleep(0.5)
    GUI.key.press("enter")
    LOTUS.wait.waitImage("/MyAPP/TiktopApp/GX/PIC/0_WebLoad_Done.png",confidence=0.7,timeout_sec=5,delayFinish_ms=500,printLog=False)
    #Chờ đến khi video hiện ra
    LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_Video_3_dots.png",confidence=0.7,timeout_sec=15,delayFinish_ms=500,printLog=True)
    sleep(2)
    LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_DeleteVideo_button.png",confidence=0.7,timeout_sec=15,delayFinish_ms=500,printLog=True)
    sleep(2)
    LOTUS.imageAction.clickImage("/MyAPP/TiktopApp/GX/PIC/0_ConfirmDel_Video.png",confidence=0.7,timeout_sec=15,delayFinish_ms=500,printLog=True)
    sleep(3)

    















