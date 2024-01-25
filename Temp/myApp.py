
#=======================================================================================
from JUBEI_Selenium import *
from SECKEY import *
from LotusLib_v1r2 import *

TASK1_SCROLL_DOWN = 2
COND_LIKE_COUNT = 1
COND_COMMENT_COUNT = 1
COND_SHARE_COUNT = 1
COND_POST_TIME = 100000

class myApp ():
  chrome = jubeiSelenium()
  def openChrome(self):
    #   1. Mở trình duyệt.
    self.chrome.begin()
    self.chrome.open("https://www.tiktok.com/@_lnah106_/video/7067914735512997147?")
    self.chrome.setWindowSize("1000x750")
    self.chrome.others_browser_setBrowserPosition(0,0)

  def loginAccount(self):
    # 2. Đăng nhập vào tài khooản.
    # 2.1 Click vào nút Login để đăng nhập
    self.chrome.click("xpath=//button[contains(.,'Log in')]","","Click vào nút Login để đăng nhập")
    # self.chrome.waitForElementPresent("xpath=//*[@id='verify-bar-close']",10000,"Chờ CAPCHA hiện ra tối đa trong 10s")
    time.sleep(4)
    # # GET_ELEMENT_SIZE
    # captchaVerifyImageElement = self.chrome.driver.find_element(By.XPATH,"//img[contains(@class,'captcha_verify_img')]")
    # try:
    #   print(captchaVerifyImageElement.size)
    # except:
    #   pass
    
    # try:
    #   print(captchaVerifyImageElement.location)
    # except:
    #   pass
    # captchaVerifyImageElement.screenshot('captcha_element1.png')
    # time.sleep(5000000)
    # self.chrome.click("xpath=//*[@id='verify-bar-close']","","Đóng cửa sổ CAPCHA")

    # 2.2 Chuyển qua cửa sổ popup iframe các kiểu login
    self.chrome.selectFrame("index=0")
    self.chrome.waitForElementPresent("xpath=//div[text()='Continue with LINE']")
    # 2.3 Click chọn kiểu đang nhập theo tài khoản LINE
    self.chrome.click("xpath=//div[text()='Continue with LINE']","","Click Continue with LINE")
    while self.chrome.browserTabNum == 1: #Chờ cửa sổ mới hiện ra
      time.sleep(1)
      self.chrome.refreshBrowserTabInfo()
    # 2.4 Chuyển sang của sổ nhập USER/PASS của LINE
    self.chrome.selectWindow("tab=1")
    self.chrome.waitForElementPresent("xpath=//input[@name='tid']")
    # 2.5 Nhập USER NAME
    self.chrome.type("xpath=//input[@name='tid']",LINE_USER)
    # while self.chrome.v=    
    # 2.6 Nhập PASSWORD
    self.chrome.type("xpath=//input[@name='tpasswd']",LINE_PASS)
    self.chrome.click("xpath=//button[@type='submit']")
    self.chrome.selectWindow("tab=0","","Trả về cửa sổ chính sau khi Login")
    #Chờ đóng web đóng hết các của sổ khác trong tối đa 20x1000ms = 20s.
    for i in range (0,20):
      if self.chrome.refreshBrowserTabNumOnly() == 1:
        self.chrome.pause(3000)
        break
      self.chrome.pause(1000)

  def scrollClipPost (self):
    #   3. Scroll down n lần. Mỗi lần cách nhau 1 giây.
    for i in range (0,TASK1_SCROLL_DOWN):
      self.chrome.runScript("window.scrollTo(0,2000000)")
      time.sleep(1)
  
  def checkClipPostCondition(self):
    #   5. Thực hiện lọc mã nguồn HTML để bắt dữ liệu và link video.
    self.elements = self.chrome.findElements("xpath=//div[contains(@data-e2e,'list-item-container')]")
    print(len(self.elements))
    self.task1ConditionPassedList = list()
    index = 0
    for clip in self.elements:
      userId       = clip.find_element(By.XPATH,"./child::*//*[contains(@data-e2e,'video-author-uniqueid')]").text
      userNickname = clip.find_element(By.XPATH,"./child::*//*[contains(@data-e2e,'video-author-nickname')]").text
      postTime     = clip.find_element(By.XPATH,"./child::*//*[contains(@class,'StyledAuthorAnchor')]").text.split("·")[1].strip()
      likeCount    = clip.find_element(By.XPATH,"./child::*//*[@data-e2e='like-count']").text
      commentCount = clip.find_element(By.XPATH,"./child::*//*[@data-e2e='comment-count']").text
      shareCount   = clip.find_element(By.XPATH,"./child::*//*[@data-e2e='share-count']").text
      
      print('-'*50)
      print("UserID  :",userId)
      print("Nickname:",userNickname)
      print("PostTime:",postTime)
      print("Like num:",likeCount)
      print("Commemt :",commentCount)
      print("Share   :",shareCount)
      print("")
  
      #Kiểm tra điều kiện
      likeCount    = LotusLib.convertHumanNumToInt(likeCount)
      commentCount = LotusLib.convertHumanNumToInt(commentCount)
      shareCount   = LotusLib.convertHumanNumToInt(shareCount)
      postTimeHour = LotusLib.convertToHour(postTime)
      if likeCount >= COND_LIKE_COUNT and commentCount >= COND_COMMENT_COUNT and shareCount >= COND_SHARE_COUNT and postTimeHour <= COND_POST_TIME:
        self.task1ConditionPassedList.append(index)
        print("===> Appended !!!")
      index += 1
  
  def authSlidePictureCaptcha(self):
    self.chrome.waitForElementPresent("xpath=//*[@id='verify-bar-close']",10000,"Chờ CAPCHA hiện ra tối đa trong 10s")
    # slideElement
    slideElement = self.chrome.driver.find_element(By.XPATH,"//img[contains(@class,'captcha_verify_img')]")
    try:
      print(slideElement.size)
    except:
      pass
    try:
      print(slideElement.location)
    except:
      pass
    slideElement.screenshot('captcha_element1.png')
    # # backgroundElement
    # slideElement = self.chrome.driver.find_element(By.XPATH,"//img[contains(@class,'captcha_verify_img')]")
    # try:
    #   print(slideElement.size)
    # except:
    #   pass
    # try:
    #   print(slideElement.location)
    # except:
    #   pass
    # slideElement.screenshot('captcha_element1.png')
    
    
    time.sleep(5000000)
    self.chrome.click("xpath=//*[@id='verify-bar-close']","","Đóng cửa sổ CAPCHA")