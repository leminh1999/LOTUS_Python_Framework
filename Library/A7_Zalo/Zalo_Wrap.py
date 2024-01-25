import __init
from task_args import *
from time import sleep
from Conf.loggingSetup import *
from Library.A1_PyAutoGUI.pyAutoGui_Wrap import pyAutoGui_Remap as GUI
from Library.A2_LOTUS.lotus_Wrap import lotus_Remap as LOTUS
from Library.A3_Selenium.selenium_Wrap import Keys, WEB, seleniumIDE_Remap as IDE
from Library.A4_SendInBlue.sendInBlue_Wrap import class_contentMode, mailConfig, sendInBlue_Wrapper as SIB
from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
import MyAPP.TiktopApp.GX.DynamicParamPC as PARAM
from pprint import *
import pyperclip

import re
import random
from os import path
import platform


################################################################
## B. Khai báo trong Application ##
import platform
#MySQL Configurations ##########################################
zaloMysql = MYSQL(hostAddress    = PARAM.MYSQL_HOST,
                  database       = "zalo_bot",
                  username       = PARAM.MYSQL_USER,
                  password       = PARAM.MYSQL_PASS)
################################################################

### Zalo function define ###
class botConfig:
  ZALO_BOSS_PHONE = "0908549354"
  workingPathScreenShot = "Z:\\LOTUS_S0\\"

botDefaultConfig = botConfig
################################################################
class msgType:
  FILE     = "fileMessage"
  LOCATION = "locationMessage"
  TEXT     = "textMessage"
  PHOTO    = "photoMessage"
  GIF      = "gifMessage"
  STICKER  = "stickerMessage"
  LINK     = "linkMessage"
  OTHER    = "Others"
  
class zalo_Wrapper():
  userChoosing = "" #Người đang được chọn để gửi/nhận dữ liệu (Đang được hiển thị trên màn hình chat)
    
  def printHello():
    print("HELLO")
    
  def openChrome(headless):
    IDE.setup.begin("Chrome",headless=headless,antiCaptcha=False)
    IDE.browser.open('https://chat.zalo.me/')
    IDE.waitFor.waitForElementVisible("xpath=//a[contains(text(),'Với Mã QR')]")

  def sendMailQrcode ():
    #############################
    #1. Get QR code from Zalo
    IDE.waitFor.waitForElementVisible("xpath=//img[starts-with(@src,'data:image')]","","Đợi mã QR-Code được hiển thị")
    qrPicSource = IDE.others.others_content_getAttribute("xpath=//img[starts-with(@src,'data:image')]","src","")
    qrPic = qrPicSource[len("data:image/png;base64,"):]
    #############################
    #2. Store qrPic to PNG file
    # import base64
    # decodeit = open('QRCode.png', 'wb')
    # decodeit.write(base64.b64decode(qrPic))
    # decodeit.close()
    #############################
    #3. Send QR code to SIB
    mailConfig.subject = "Zalo QRCode"
    mailConfig.content_mode = class_contentMode.HTML_CONTENT
    mailConfig.html_content ="<!DOCTYPE html><html><body><h1>ABC</h1><img src='"+qrPicSource+"' alt='QR Code'></body></html>"
    mailConfig.attachment = [{'content':qrPic, 'name':'myAttachmentFromBase64.jpg'}]
    SIB.sendMail(mailConfig)
    
  def returnWaitScreen ():
    IDE.others.others_print_comment_only(">>> Nhảy vào MyCloud và chờ message đến <<<")
    IDE.mouseKey.click("xpath=//*[contains(@class,'fa-ic_mycloud_24')]","","Nhảy vào MyCloud chờ message đến",True)
    IDE.waitFor.waitForText("xpath=//*[contains(@class,'header-title')]","Cloud","Chờ của sổ 'Cloud của tôi' hiện ra",True)
    
    
    
  #########################################################
  # Name: welcomeToAdminMess
  # Function: Gửi tin nhắn Greeting đến Boss mỗi khi khởi động
  # Parameter: none
  # Return: none
  #########################################################
  def welcomeToAdminMess():
    send_timestamp_sec = int(datetime.datetime.now().timestamp())
    send_schedule = datetime.datetime.fromtimestamp(send_timestamp_sec)
    #Send Sticker
    sql = "INSERT INTO tx_buffer (send_to, uid, mess_type, mess_data,send_schedule,send_timestamp_sec,note) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (botConfig.ZALO_BOSS_PHONE, str(random.randint(0,1000000000)) , "sticker","Hey",str(send_schedule),str(send_timestamp_sec),'Zalo Manager')
    zaloMysql.myCursor.execute(sql, val)
    zaloMysql.myDb.commit()
    #Send screen
    # sql = "INSERT INTO tx_buffer (send_to, uid, mess_type, mess_data,send_schedule,send_timestamp_sec,note) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    # val = (botConfig.ZALO_BOSS_PHONE, str(random.randint(0,1000000000)) , "image",botConfig.workingPathScreenShot+'screenShot.png',str(send_schedule),str(send_timestamp_sec),'Zalo Manager')
    # zaloMysql.myCursor.execute(sql, val)
    # zaloMysql.myDb.commit()
    
  #########################################################
  # Name: sendAllTxBuffer
  # Function: Gửi hết toàn bộ TX message trong TX buffer
  #           hoặc dừng lại nếu đã gửi đi số message tối đa
  #           được thiết đặt cho một lần gửi đi.
  # Parameter: + maxSendNum: Số lượng tin nhắn tối đa trong
  #                          một lần gửi đi.
  # Return: None
  #########################################################
  def sendAllTxBuffer(maxSendNum=30):
    timeNowSec = datetime.datetime.now().timestamp()
    sql = "SELECT * FROM tx_buffer WHERE send_timestamp_sec < "+str(timeNowSec)
    zaloMysql.myCursor.execute(sql)
    readData = zaloMysql.myCursor.fetchall()

    if len(readData) != 0:
      logger.info("3.1.1 There is %s message in TX buffer reach schedule",len(readData))
      # Send all message
      logger.info("3.1.2 Send %s messages in TX buffer (MAX %s)-----",len(readData),maxSendNum)
      n=0
      while n<len(readData) and n<maxSendNum:
        sql = "SELECT * FROM tx_buffer WHERE send_timestamp_sec < "+str(timeNowSec)+" LIMIT 1"
        zaloMysql.myCursor.execute(sql)
        topMessage = zaloMysql.myCursor.fetchall()
        # print(sql)
        # print(topMessage)
        if zaloMysql.myCursor.rowcount != 0: #Có tin nhắn đến lịch gửi
          zalo_Wrapper.sendOneTopTxMess(topMessage)
          zalo_Wrapper.copyToTxBuffferDebug(topMessage[0]['uid'])
          zalo_Wrapper.clearUidTxMess(topMessage[0]['uid'])
        n+=1
      zalo_Wrapper.userChoosing = "" #clear
      #Quay trở về màn hình chờ tin nhắn
      logger.info("3.1.4 Send done -> Return wait screen")
      zalo_Wrapper.returnWaitScreen()
    else:
      # logger.debug("Tx Buffer: Không có tin nhắn gửi đi")
      pass

  #########################################################
  # Name: sendOneTopTxMess
  # Function: Gửi tin nhắn trên cùng của TX buffer
  # Parameter: None
  # Return: None
  #########################################################
  def sendOneTopTxMess(readData):
    if len(readData) == 0:
      logger.info("3.1.3.1 No message in TX buffer")
    else:
      logger.info("3.1.3.1 send %s message to %s ---",readData[0]['mess_type'],readData[0]['send_to'])
      # print("DEBUG:",readData[0]['send_to'],self.userChoosing)
      if readData[0]['send_to'] != zalo_Wrapper.userChoosing:
        zalo_Wrapper.userChoosing = readData[0]['send_to']
        IDE.mouseKey.type("id=contact-search-input",zalo_Wrapper.userChoosing,"Tìm kiếm người cần gửi message",True)
        IDE.waitFor.waitForAttr("id=contact-search-input",'value='+str(zalo_Wrapper.userChoosing),"",True)
        sleep(0.5)
        IDE.mouseKey.sendKeys("id=contact-search-input",Keys.ENTER,"",False)
        IDE.waitFor.waitForElementVisible("xpath=//i[contains(@class,'fa-outline-add-new-contact')]","30000","",True)
        IDE.waitFor.waitForElementEditable("id=input_line_0")
        
        
      #Kiểm tra loại tin nhắn
      # 1. mess_type = 'text'
      if readData[0]['mess_type'] == 'text':
        IDE.mouseKey.type("id=input_line_0",readData[0]['mess_data']+'\n',"Nhập nội dung message",True)
        IDE.others.others_clearReqWaitCmdFlg()
        sleep(1) #Chờ 1s để gửi xong dữ liệu

      # 2. mess_type = 'file'
      if readData[0]['mess_type'] == 'file':
        #Kiểm tra file có tồn tại trong máy không?
        if path.exists(readData[0]['mess_data']) == False:
          logger.error("NOT FOUND: %s",readData[0]['mess_data'])
          return 0 #Reject send message
        else:
          IDE.mouseKey.click("xpath=//div[@icon='chatbar-attach']","","Nhấn nút chọn file để gửi",True)
          IDE.waitFor.waitForElementVisible("xpath=//i[contains(@class,'fa-solid-files')]")
          IDE.mouseKey.click("xpath=//i[contains(@class,'fa-solid-files')]","","Nhấn nút chọn file để gửi",True)
          IDE.others.others_clearReqWaitCmdFlg()
          sleep(2)
          
          pyperclip.copy(readData[0]['mess_data'])
          sleep(0.2)
          pyperclip.copy(readData[0]['mess_data'])
          sleep(0.2)
          pyperclip.copy(readData[0]['mess_data'])
          sleep(0.2)
          GUI.key.hotkey('ctrl','v') #Dán nội dung vào cửa sổ chat
          sleep(0.2)
          GUI.key.press('enter')
          sleep(0.5)
          GUI.key.press('enter')
          sleep(0.5)

      # 3. mess_type = 'sticker'/'gif'
      if readData[0]['mess_type'] == 'sticker' or readData[0]['mess_type'] == 'gif':
        #PIC: Library\A7_Zalo\Components\PIC\003.png
        IDE.mouseKey.click("xpath=//div[@icon='chatbar-sticker']","","Nhấn vào nút gửi Sticker/Gif",True)
        IDE.waitFor.waitForElementVisible("xpath=//div[contains(@class,'media-dock')]","","Chờ mất bảng Media Dock hiện ra",True)
        
        if readData[0]['mess_type'] == 'sticker':
          IDE.mouseKey.type("xpath=//input[@placeholder='Tìm kiếm sticker']",readData[0]['mess_data'],"Nhập sticker cần tìm",True)
          sleep(1)
          IDE.waitFor.waitForElementVisible("xpath=//div[contains(@class,'sticker-zone-search')]")
          IDE.mouseKey.click("xpath=//div[contains(@class,'sticker-zone-search')]","","Chọn sticker đầu tiên hiện ra",True)
          
        elif readData[0]['mess_type'] == 'gif':
          IDE.mouseKey.click("xpath=//div[text()='GIF']","","Nhấn vào nút chọn loại GIF",True)
          IDE.waitFor.waitForElementVisible("xpath=//input[@placeholder='Tìm kiếm GIF']","","",True)
          IDE.mouseKey.type("xpath=//input[@placeholder='Tìm kiếm GIF']",readData[0]['mess_data'],"Nhập gif cần tìm",True)
          sleep(1)
          IDE.waitFor.waitForElementVisible("xpath=//div[contains(@class,'gif__thumb')]")
          IDE.mouseKey.click("xpath=//div[contains(@class,'gif__thumb')]","","Chọn GIF đầu tiên hiện ra",True)
          
        IDE.waitFor.waitForElementNotVisible("xpath=//div[contains(@class,'media-dock')]","","Chờ mất bảng Media Dock mất đóng",True)
        

      # 4. mess_type = 'location'
      #Ex: https://www.google.com/maps?q=10.8132583,106.712124&z=14&t=m
      if readData[0]['mess_type'] == 'location':
        locationPos = 'https://www.google.com/maps?q='+readData[0]['mess_data']+'&z=14&t=m'
        IDE.mouseKey.type("id=input_line_0",locationPos+'\n',"Nhập nội dung message",True)
        IDE.others.others_clearReqWaitCmdFlg()
        sleep(1) #Chờ 1s để gửi xong dữ liệu

      # 5. mess_type = 'image'
      if readData[0]['mess_type'] == 'image':
        #Kiểm tra file có tồn tại trong máy không?
        if path.exists(readData[0]['mess_data']) == False:
          logger.error("NOT FOUND: %s",readData[0]['mess_data'])
          return 0 #Reject send message
        else:
          IDE.mouseKey.click("xpath=//div[@icon='chatbar-photo']","","Nhấn nút chọn Image để gửi",True)
          IDE.others.others_clearReqWaitCmdFlg()
          sleep(2)
          pyperclip.copy(readData[0]['mess_data'])
          sleep(0.2)
          pyperclip.copy(readData[0]['mess_data'])
          sleep(0.2)
          pyperclip.copy(readData[0]['mess_data'])
          sleep(0.2)
          GUI.key.hotkey('ctrl','v') #Dán nội dung vào cửa sổ chat
          sleep(0.2)
          GUI.key.press('enter')
          sleep(0.5)
          GUI.key.press('enter')
          sleep(0.5)
          
  #########################################################
  # Name: clearUidTxMess
  # Function: Xóa tin nhắn với uid chỉ định
  # Parameter: +uid: giá trị unique ID của tin nhắn
  # Return: htmlCode
  #########################################################
  def clearUidTxMess(uid):
   sql = "DELETE FROM tx_buffer WHERE uid = "+str(uid)
   print(sql)
   zaloMysql.myCursor.execute(sql)
   zaloMysql.myDb.commit()
      
  #########################################################
  # Name: copyToTxBuffferDebug
  # Function: Copy dòng dữ liệu với UID xác định từ bảng
  #           tx_buffer sang tx_buffer_debug.
  # Parameter: uid: Giá trị Unique ID
  # Return: none
  #########################################################
  def copyToTxBuffferDebug(uid=''):
    try:
      sql = "INSERT INTO tx_buffer_debug SELECT * from tx_buffer WHERE uid = '"+str(uid)+"'"
      zaloMysql.myCursor.execute(sql)
      zaloMysql.myDb.commit()
    except:
      pass
      
  # #########################################################
  # # Name: readMessToRxBuffer
  # # Function: Đọc một loạt tin nhắn nhận được lưu vào buffer
  # # Parameter: None
  # # Return: None
  # #########################################################
  def readMessToRxBuffer():
    newMessageIndicator = IDE.others.others_content_findFirstElement("xpath=//i[contains(@class,'unread-red')]","","Kiểm tra có tin nhắn mới hay không?",False)
    if newMessageIndicator != None: #Có tin nhắn mới
      IDE.others.others_clearExitOnExceptionFlg() #Sẽ không thoát khỏi chương trình nếu gặp lỗi exception
      #Đọc tin nhắn mới
      logger.info("Có tin nhắn chưa được đọc")     
      IDE.mouseKey.click("xpath=//div[@title='Tin nhắn']","","Nhấn ICON tin nhắn",True)
      unreadButton = IDE.waitFor.waitForElementVisible("xpath=//div[text()='Chưa đọc']","","Chờ nút chưa đọc hiện ra",True)[1]
      unreadButton.click()
      sleep(0.5)
      IDE.waitFor.waitForElementVisible("xpath=//div[contains(@class,'msg-item')]","","",False)
      
      allReadMessages = IDE.others.others_content_findAllElements("xpath=//div[contains(@class,'msg-item')]","","Load tất cả các tin nhắn chưa đọc")
      for msg in allReadMessages:
        # IDE.others.others_browser_saveCurrentScreenshot("test.png","","","",msg)
        #1. Lấy thông tin của tin nhắn
        messAvatar = IDE.others.others_content_getAttribute("xpath=//img[contains(@src,'https')]","src","Lấy Avatar của message",False,msg)
        # print(messAvatar)
        messUserUid = re.sub(r'.*/(.*)\.jpg.*',r'\1',messAvatar.strip())
        print(messUserUid)
        messUsername = IDE.others.others_content_getText("xpath=//div[contains(@class,'conv-item-title__name')]/span",'',"Lấy tên của message",False,msg)
        # print(messUsername)
        #2. Mở tin nhắn
        msg.click()
        IDE.waitFor.waitForElementVisible("xpath=//img[contains(@class,'zl-avatar__photo') and contains(@src,'"+messAvatar+"')]","","Chờ Avatar được load",True)
        IDE.waitFor.waitForText("xpath=//div[contains(@class,'header-title')]",messUsername,"Chờ tên Username được load",True)
        
        #3. Lấy chat item cuối cùng. Nếu class có chữ "me" nghĩ là mình là người gửi cuối cùng thì không cần phải lấy nội dung.
        #   Nếu không thì lấy nội dung của tin nhắn
        lastChatItemElement = IDE.others.others_content_findLastElement("xpath=//div[contains(@class,'chat-item')]","","Truy cập last chat item group",True)
        lastChatItemClassAttr = lastChatItemElement.get_attribute("class")
        # print(">>>> lastChatItemClass: "+lastChatItemClassAttr)
        if "me" not in lastChatItemClassAttr: #Nếu không phải là tin nhắn của mình
          lastMsgElement = IDE.others.others_content_findLastElement("xpath=//div[contains(@class,'last-msg') and contains(@class,'card--')]","","Đọc tin nhắn cuối cùng của người gửi",True,lastChatItemElement)
          if lastMsgElement == None:
            lastMsgElement = IDE.others.others_content_findLastElement("xpath=//div[contains(@data-id,'div_LastReceivedMsg_Photo') and contains(@class,'img-msg-v2')]","","Đọc tin nhắn cuối cùng của người gửi",True,lastChatItemElement)
          if lastMsgElement == None:
            logger.warn("Không tìm thấy nội dung tin nhắn cuối cùng")
            zalo_Wrapper.userChoosing = "" #clear
            #Quay trở về màn hình chờ tin nhắn
            zalo_Wrapper.returnWaitScreen()
            return
          #4. Phân loại tin nhắn nhận được
          # print(lastMsgElement)
          lastMsgClass = lastMsgElement.get_attribute("class")
          # print(">>>> lastMsgClass: "+lastMsgClass)
          #File:     <div class="file-message card--file card  pin-react " data-id="div_ReceivedMsg_File"><div class="file-message__container"><div class="file-message__content-container" style="min-height: 49px;"><div class="file-tit-box file-tit-box--size-large file-message-icon file-message-icon--none"><div class="svg-icon svg-icon--size-large file-icon file-icon--size-large file-tit-box__icon file-message-icon__icon" style="background-image: url(&quot;assets/icon-file-empty.6796cfae2f36f6d44242f7af6104f2bb.svg&quot;);"><div class="file-icon__ext-text">WEB</div></div><div class="file-tick file-tick--status-none file-tick--size-large file-tit-box__tick file-message-icon__tick" style="background-image: url(&quot;assets/none.ec109d7e3fc260cd76687461867972b0.svg&quot;);"></div></div><div class="file-message__content"><div class="file-message__content-title" title="i-love-you-heart.webp"><div class="truncate">i-love-you-he</div><div>art.webp</div></div><div class="file-message__content-info-container"><div class="file-message__content-info"><span><span class="file-message__content-info-size" title="17.99 KB">17.99 KB</span><span class="file-message__content-info-preview-file truncate"><span data-translate-inner="STR_CLICK_TO_VIEW">Nhấn để xem trước</span></span><span class="file-message__content-info-preview-folder truncate"><span data-translate-inner="STR_VIEW_FOLDER">Click để xem thư mục</span></span></span></div><div class="file-message__content-actions flx-e none"><a class="clickable file-message__actions download" data-translate-title="STR_DOWNLOAD_FILE" title="Lưu về máy"><i class="fa fa-file-preview-download-icon file-message__actions-icon"></i></a></div></div></div></div></div><div class="file-message__others"><div class="flx" style="margin-top: 10px;"></div><div class="message-reaction-container  always-display "><div data-id="btn_ReceivedMsg_React" style="position: relative;"><div class="msg-reaction-icon"><div class="default-react-icon-thumb" style="background-image: url(&quot;https://res-zalo.zadn.vn/upload/media/2019/1/25/iconlike_1548389696575_103596.png&quot;);"></div></div><div class="emoji-list-wrapper  hide-elist"><div class="reaction-emoji-list "><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 82.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">/-strong</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 72.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">/-heart</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 82% 7.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:&gt;</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 20% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:o</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 2.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:-((</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:-h</span></div></div></div></div><div id="reaction-canvas-layer-03565817354043" class="react-effect "></div><div id="reaction-canvas-layer-13565817354043" class="react-effect "></div></div></div></div>
          #Photo:    <div class="img-msg-v2 -bg-v-1" data-id="div_ReceivedMsg_Photo" style="--thumb-cw:233px; --min-threshold:undefinedpx;"><div class="img-msg-v2__dn"></div><div class="img-msg-v2__bub"><div maxloss="0" class="ci-th -fit-scale-down fade-th-v2 msg-select-overlay img-msg-v2__th" style="width: 233px; height: 368px;"><div class="or-bx -ort-0 ci-th__thb ci-th-thumb-tr-enter-done" style="--or-bx-cw:233px; --or-bx-ch:368px; --or-bx-bw:233px; --or-bx-bh:368px;"><img class="ci-th__thumb" data-drag-src="https://f5.photo.talk.zdn.vn/8293979990283524806/cabf575d2716e548bc07.jpg" src="https://f5.photo.talk.zdn.vn/8293979990283524806/cabf575d2716e548bc07.jpg"></div></div><div class="qu-ba -hd"></div><div class="msg-select-overlay img-msg-v2__ft"><div class="img-msg-v2__rct"><div class="message-reaction-container  always-display  img-no-title "><div data-id="btn_ReceivedMsg_React" style="position: relative;"><div class="msg-reaction-icon"><div class="default-react-icon-thumb" style="background-image: url(&quot;https://res-zalo.zadn.vn/upload/media/2019/1/25/iconlike_1548389696575_103596.png&quot;);"></div></div><div class="emoji-list-wrapper  hide-elist"><div class="reaction-emoji-list "><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 82.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">/-strong</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 72.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">/-heart</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 82% 7.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:&gt;</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 20% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:o</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 2.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:-((</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:-h</span></div></div></div></div><div id="reaction-canvas-layer-03565816947687" class="react-effect "></div><div id="reaction-canvas-layer-13565816947687" class="react-effect "></div></div></div></div></div></div>
          #Sticker:  <div class="card  card--group-sticker card--sticker"><div class="flx flx-row"></div><div class="flx flx-row"><div class="card--group-sticker__row__item"><div class="card--group-sticker__row__item__sticker no-shadow-border"><div class="card  card--group-sticker card--sticker" data-id="div_ReceivedMsg_Sticker"><div style="position: relative;"><div class="card--sticker--container" data-id="div_StickerMenu_RecentItem"><div class="sticker sticker-message " style="width: 130px; height: 130px; background-image: url(&quot;https://zalo-api.zadn.vn/api/emoticon/sticker/webpc?eid=16503&amp;size=130&quot;);"></div></div></div></div></div></div></div></div>
          #Gif:      <div class="card  pin-react  card--picture  image-message -bg-v-1  "><div class="chat-message-picture__gif__wrapper" data-id="div_ReceivedMsg_GIF" style="height: 110px; width: 220px; background-color: transparent;"><img class="chat-message-picture chat-message-picture__gif" draggable="true" src="https://media-ten.z-cdn.me/images/41a9caeeb07c4b4374bf7bcd8393eea5/tenor.gif" crossorigin="Anonymous" style="height: 110px; width: 220px; background-color: transparent;"></div><div class="message-reaction-container  show-react-btn always-display  img-no-title "><div data-id="btn_ReceivedMsg_React" style="position: relative;"><div class="msg-reaction-icon"><div class="default-react-icon-thumb" style="background-image: url(&quot;https://res-zalo.zadn.vn/upload/media/2019/1/25/iconlike_1548389696575_103596.png&quot;);"></div></div><div class="emoji-list-wrapper  hide-elist"><div class="reaction-emoji-list "><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 82.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">/-strong</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 72.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">/-heart</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 82% 7.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:&gt;</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 20% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:o</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 2.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:-((</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:-h</span></div></div></div></div><div id="reaction-canvas-layer-03561603018628" class="react-effect "></div><div id="reaction-canvas-layer-13561603018628" class="react-effect "></div></div></div>
          #Location: <div class="card  pin-react  last-msg card--location"><div class="flx flx-center flx-al-s rel clickable"><div class="marker-icon"><div class="marker-icon__avatar" style="background-image: url(&quot;https://s120-ava-talk.zadn.vn/f/1/5/2/3/120/29de2616dda93c4949e4c70da66edafe.jpg&quot;);"></div></div><iframe width="100%" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?ll=10.7918024,106.6917251&amp;z=14&amp;output=embed" style="pointer-events: none;"></iframe></div><div class="card-send-time flx flx-al-c flx-1   "><span class="card-send-time__sendTime">12:37</span><div class="card-send-time__spacer"></div></div></div>
          #Text:     <div class="card  card--text" data-id="div_ReceivedMsg_Text"><div><span id="mtc-3565814133539"><span class="text">text ABC</span></span></div><div style="margin: 3px -5px 0px;"></div><div class="message-reaction-container "><div data-id="btn_ReceivedMsg_React" style="position: relative;"><div class="msg-reaction-icon"><div class="default-react-icon-thumb" style="background-image: url(&quot;https://res-zalo.zadn.vn/upload/media/2019/1/25/iconlike_1548389696575_103596.png&quot;);"></div></div><div class="emoji-list-wrapper  hide-elist"><div class="reaction-emoji-list "><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 82.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">/-strong</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 72.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">/-heart</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 82% 7.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:&gt;</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 20% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:o</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 2.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:-((</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:-h</span></div></div></div></div><div id="reaction-canvas-layer-03565814133539" class="react-effect "></div><div id="reaction-canvas-layer-13565814133539" class="react-effect "></div></div></div>
          #Link:     <div class="card  card--link has-big-thumb" data-id="div_ReceivedMsg_Link" style="max-width: calc(100% - 160px); min-width: 230px; width: 330px;"><div><div class="text" style="margin-bottom: 14px;"><span id="mtc-3565819797055"><a class="text-is-link" content="https://www.google.com/maps?q=10.8132583,106.712124&amp;z=14&amp;t=m&amp;utm_source=zalo&amp;utm_medium=zalo&amp;utm_campaign=zalo" target="_blank" rel="noopener noreferrer">https://www.google.com/maps?q=10.8132583,106.712124&amp;z=14&amp;t=m&amp;utm_source...ign=zalo</a></span></div><div><div class="flx flx-al-s card--link-content text-is-card-link clickable has-big-thumb"><div class="card--link-container"><img class="card--link-img" src="https://photo-link-talk.zadn.vn/photolinkv2/720/aHR0cHM6Ly9yZXMtemFsby56YWRuLnZuL3VwbG9hZC9tZWRpYS8yMDE4LzkvMjAvZGVmYXVsdF9nZW9jb2RlXzF4XzE1Mzc0MzIwNDA3MjJfMzExODMzLnBuZw==" crossorigin="Anonymous" style="max-width: 100%; width: 100%;"></div><div class="card-content"><span class="card-title on-hover">10°48`47.7"N 106°42`43.7"E</span><span class="card--link__sub clp clp--two">Tìm kiếm các doanh nghiệp địa phương, xem bản đồ và tìm chỉ đường trên Google Maps.</span><span class="card--link__src clp clp--one">www.google.com</span></div></div></div></div><div class="flx" style="margin-top: 10px;"></div><div class="message-reaction-container  show-react-btn"><div data-id="btn_ReceivedMsg_React" style="position: relative;"><div class="msg-reaction-icon"><div class="default-react-icon-thumb" style="background-image: url(&quot;https://res-zalo.zadn.vn/upload/media/2019/1/25/iconlike_1548389696575_103596.png&quot;);"></div></div><div class="emoji-list-wrapper  link-msg  hide-elist"><div class="reaction-emoji-list "><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 82.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">/-strong</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 72.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">/-heart</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 82% 7.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:&gt;</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 20% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:o</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 2.5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:-((</span></div><div class="reaction-emoji-icon"><span class="emoji-sizer emoji-outer " style="background: url(&quot;assets/emoji-md.6fa8afb705db684e87d22868d5d85557.png?v=20222710&quot;) 84% 5% / 5100%; -webkit-user-drag: none; margin: -1px; position: relative; top: 2px;">:-h</span></div></div></div></div><div id="reaction-canvas-layer-03565819797055" class="react-effect "></div><div id="reaction-canvas-layer-13565819797055" class="react-effect "></div></div></div>
          if   "card--file" in lastMsgClass: lastMsgType = msgType.FILE
          elif "card--location" in lastMsgClass: lastMsgType = msgType.LOCATION
          elif "card--text" in lastMsgClass: lastMsgType = msgType.TEXT
          elif "card--photo" in lastMsgClass or "card--image" in lastMsgClass or "img-msg-v2" in lastMsgClass: lastMsgType = msgType.PHOTO
          elif "card--picture" in lastMsgClass: lastMsgType = msgType.GIF
          elif "card--sticker" in lastMsgClass: lastMsgType = msgType.STICKER
          elif "card--link" in lastMsgClass: lastMsgType = msgType.LINK
          else: lastMsgType = msgType.OTHER
          
          #5. Lưu dữ liệu vào bảng tx_buffer
          #5.1. FILE MESSAGE
          if lastMsgType == msgType.FILE:
            fileName = IDE.others.others_content_getAttribute("xpath=//div[contains(@class,'file-message__content-title')]","title","Lấy Filename",False,lastMsgElement)
            uploadData = fileName
            zalo_Wrapper.pushMessToRxBuffer(messUserUid,messUsername,messAvatar,lastMsgType,uploadData)
          #5.2. LOCATION MESSAGE
          elif lastMsgType == msgType.LOCATION:
            #src="https://maps.google.com/maps?ll=10.7918024,106.6917251&amp;z=14&amp;output=embed"
            location = IDE.others.others_content_getAttribute("xpath=//iframe[contains(@src,'https')]","src","Lấy Location Link",False,lastMsgElement)
            latLon = re.sub(r'.*?\?ll=(.*?)\&.*',r'\1',location.strip())
            newLocation = 'https://www.google.com/maps?q='+latLon+'&z=14&t=m&mapclient=embed'
            uploadData = newLocation
            zalo_Wrapper.pushMessToRxBuffer(messUserUid,messUsername,messAvatar,lastMsgType,uploadData)
          #5.3. TEXT MESSAGE
          elif lastMsgType == msgType.TEXT:
            textMessage = IDE.others.others_content_getText("xpath=//span[contains(@id,'mtc')]/span","","Lấy Text Message",False,lastMsgElement)
            uploadData = textMessage
            zalo_Wrapper.pushMessToRxBuffer(messUserUid,messUsername,messAvatar,lastMsgType,uploadData)
          #5.4. PHOTO MESSAGE
          elif lastMsgType == msgType.PHOTO:
            photoUrl = IDE.others.others_content_getAttribute("xpath=//img[contains(@src,'https')]","src","Lấy Photo Link",False,lastMsgElement)
            uploadData = photoUrl
            zalo_Wrapper.pushMessToRxBuffer(messUserUid,messUsername,messAvatar,lastMsgType,uploadData)
          #5.5. GIF MESSAGE
          elif lastMsgType == msgType.GIF:
            gifUrl = IDE.others.others_content_getAttribute("xpath=//img[contains(@src,'https')]","src","Lấy GIF Link",False,lastMsgElement)
            uploadData = gifUrl
            zalo_Wrapper.pushMessToRxBuffer(messUserUid,messUsername,messAvatar,lastMsgType,uploadData)
          #5.6. STICKER MESSAGE
          elif lastMsgType == msgType.STICKER:
            stickerInStyle = IDE.others.others_content_getAttribute("xpath=//div[contains(@class,'sticker-message')]","style","Lấy Sticker Link",False,lastMsgElement)
            stickerUrl = re.sub(r'.*url\(\"(.*?)\"\).*',r'\1',stickerInStyle.strip())
            uploadData = stickerUrl
            zalo_Wrapper.pushMessToRxBuffer(messUserUid,messUsername,messAvatar,lastMsgType,uploadData)
          #5.7. LINK MESSAGE
          elif lastMsgType == msgType.LINK:
            linkUrl = IDE.others.others_content_getAttribute("xpath=//a[contains(@class,'text-is-link')]","content","Lấy Text Link",False,lastMsgElement)
            uploadData = linkUrl
            zalo_Wrapper.pushMessToRxBuffer(messUserUid,messUsername,messAvatar,lastMsgType,uploadData)
          #5.8. OTHER MESSAGE
          else:
            uploadData = ""
            pass
      # print(lastMsgType)
      # print(uploadData)
      IDE.others.others_setExitOnExceptionFlg() #Exit nếu có lỗi exception bên ngoài
      zalo_Wrapper.userChoosing = "" #clear
      #Quay trở về màn hình chờ tin nhắn
      zalo_Wrapper.returnWaitScreen()
      # while True:
      #   pass
      
    else: #Không có tin nhắn
      pass
            

  #########################################################
  # Name: welcomeToAdminMess
  # Function: Gửi tin nhắn Greeting đến Boss mỗi khi khởi động
  # Parameter: none
  # Return: none
  #########################################################
  def dummyTxTest():
    send_timestamp_sec = int(datetime.datetime.now().timestamp())
    send_schedule = datetime.datetime.fromtimestamp(send_timestamp_sec)
    sendTo = '0769807636'
    #Send Text
    sql = "INSERT INTO tx_buffer (send_to, uid, mess_type, mess_data,send_schedule,send_timestamp_sec,note) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (sendTo, str(random.randint(0,1000000000)) , "text","Xin chào bạn",str(send_schedule),str(send_timestamp_sec),'Zalo Manager')
    zaloMysql.myCursor.execute(sql, val)
    zaloMysql.myDb.commit()
    #Send file
    filePath = 'D:\\Database\\Local_GIT_WorkingDir\\LOTUS_Python_Framework\\Library\\A7_Zalo\\Components\\PIC\\001.png'
    sql = "INSERT INTO tx_buffer (send_to, uid, mess_type, mess_data,send_schedule,send_timestamp_sec,note) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (sendTo, str(random.randint(0,1000000000)) ,'file',str(filePath),str(send_schedule),str(send_timestamp_sec),'Zalo Manager')
    zaloMysql.myCursor.execute(sql, val)
    zaloMysql.myDb.commit()
    #Send Sticker
    sql = "INSERT INTO tx_buffer (send_to, uid, mess_type, mess_data,send_schedule,send_timestamp_sec,note) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (sendTo, str(random.randint(0,1000000000)) , "sticker","Hey",str(send_schedule),str(send_timestamp_sec),'Zalo Manager')
    zaloMysql.myCursor.execute(sql, val)
    zaloMysql.myDb.commit()
    #Send GIF
    sql = "INSERT INTO tx_buffer (send_to, uid, mess_type, mess_data,send_schedule,send_timestamp_sec,note) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (sendTo, str(random.randint(0,1000000000)) , "gif","Hey",str(send_schedule),str(send_timestamp_sec),'Zalo Manager')
    zaloMysql.myCursor.execute(sql, val)
    zaloMysql.myDb.commit()
    #Send Location
    locationPos = "10.8132583,106.712124" #Lat,Lon: https://www.google.com/maps?q=10.8132583,106.712124&z=14&t=m
    sql = "INSERT INTO tx_buffer (send_to, uid, mess_type, mess_data,send_schedule,send_timestamp_sec,note) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (sendTo, str(random.randint(0,1000000000)) , "location",locationPos,str(send_schedule),str(send_timestamp_sec),'Zalo Manager')
    zaloMysql.myCursor.execute(sql, val)
    zaloMysql.myDb.commit()
    #Send Image
    imagePath = 'D:\\Database\\Local_GIT_WorkingDir\\LOTUS_Python_Framework\\Library\\A7_Zalo\\Components\\PIC\\003.png'
    sql = "INSERT INTO tx_buffer (send_to, uid, mess_type, mess_data,send_schedule,send_timestamp_sec,note) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (sendTo, str(random.randint(0,1000000000)) , "image",imagePath,str(send_schedule),str(send_timestamp_sec),'Zalo Manager')
    zaloMysql.myCursor.execute(sql, val)
    zaloMysql.myDb.commit()

  #########################################################
  # Name: welcomeToAdminMess
  # Function: Gửi tin nhắn Greeting đến Boss mỗi khi khởi động
  # Parameter: none
  # Return: none
  #########################################################
  def sendMessage(sendTo=botConfig.ZALO_BOSS_PHONE,messType='text',messData='Hello',sendDelayInSec:int=0,note="Zalo Manager"):
    # print(sendTo)
    # print(messType)
    # print(messData)
    # print(sendDelayInSec)
    # print(note)
    send_timestamp_sec = int(datetime.datetime.now().timestamp())+int(sendDelayInSec)
    # print(send_timestamp_sec)
    send_schedule = datetime.datetime.fromtimestamp(send_timestamp_sec)
    # print(send_schedule)
    #Send Text
    sql = "INSERT INTO tx_buffer (send_to, uid, mess_type, mess_data,send_schedule,send_timestamp_sec,note) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (str(sendTo), str(random.randint(0,1000000000)), str(messType),str(messData),str(send_schedule),str(send_timestamp_sec),str(note))
    zaloMysql.myCursor.execute(sql, val)
    zaloMysql.myDb.commit()
    
  #########################################################
  # Name: pushMessToRxBuffer
  # Function: Push tin nhắn nhận được lên MySQL Rx Buffer.
  # Parameter:
  #  + username: Tên người gửi.
  #  + avatar: đường dẫn đến file hình avatar của người gửi
  #  + mess_type: loại tin nhắn (text,file,sticker,gif,image,location)
  #  + mess_data: Nội dung tin nhắn ứng với các loại trên.
  # Return: none
  #########################################################
  def pushMessToRxBuffer(userId,username,avatar,mess_type, mess_data):
    sql = "INSERT INTO rx_buffer (uid,userId,receive_from,avatar,mess_type, mess_data) VALUES (%s, %s, %s, %s, %s,%s)"
    val = (str(random.randint(0,1000000000)),str(userId),str(username),str(avatar),str(mess_type),str(mess_data))
    # print(sql)
    # print(val)
    zaloMysql.myCursor.execute(sql, val)
    zaloMysql.myDb.commit()
    
    