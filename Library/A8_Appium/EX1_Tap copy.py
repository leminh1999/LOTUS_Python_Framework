import __init
from Library.A8_Appium.appium_Wrap import appium_Remap

MOBI = appium_Remap()
MOBI.setup.begin(remoteAddr="localhost",remotePort=4723,deviceUUID="LHS7N18B29003666")

# MOBI2 = appium_Remap()
# MOBI2.SETUP.begin(remoteAddr="localhost",remotePort=4724,deviceUUID="LHS7N18B29003444")

# while True:
#     inputString = input("Enter your input: ")
#     print("Received input is: ", inputString)
#     APPIUM.driver.press_keycode(int(inputString)) # Ấn nút HOME

while True:
  # MOBI.button.home()
  # MOBI.button.back()
  # MOBI.button.volumeUp()
  # MOBI.button.volumeDown()
  # MOBI.button.volumeMute()
  # MOBI.button.power()
  # MOBI.button.power()
  
  # MOBI.fingerKey.longTap('xpath=//android.widget.TextView[@content-desc="Zalo"]')
  # MOBI.fingerKey.longTapDragDrop('xpath=//android.widget.TextView[@content-desc="Zalo"]',
  #                         'xpath=//android.widget.TextView[@content-desc="ZaloTạo 2 bản"]')
  
  # MOBI.fingerKey.scrollDown()
  # MOBI.others.others_clearReqWaitCmdFlg()
  # MOBI.fingerKey.scrollUp()
  # MOBI.others.others_clearReqWaitCmdFlg()
  # MOBI.fingerKey.swipeLeft()
  # MOBI.others.others_clearReqWaitCmdFlg()
  # MOBI.fingerKey.swipeRight()
  # MOBI.others.others_clearReqWaitCmdFlg()

  # video_options = {
  #     'timeLimit': '180',
  #     # 'bitRate': '4000000',
  #     # 'videoSize': '720x1280',
  #     # 'bugReport': 'true',
  #     # 'androidQuality': '20',
  #     # 'ignoreSilentMode': 'false',
  #     'remotePath': '/sdcard/Download/abc.mp4'
  # }
  # MOBI.logging.startRecordScreen()
  # APPIUM.driver.start_recording_screen(video_options)
  
  MOBI.fingerKey.scrollUp()
  MOBI.others.others_clearReqWaitCmdFlg()
  MOBI.fingerKey.tap('id=com.android.chrome:id/url_bar')
  MOBI.others.others_clearReqWaitCmdFlg()
  abc = MOBI.fingerKey.type('id=com.android.chrome:id/url_bar','https://www.google.com.vn')
  print(abc)
  MOBI.others.others_clearReqWaitCmdFlg()
  MOBI.funcButton.enterKey()
  MOBI.others.others_clearReqWaitCmdFlg()



  MOBI.fingerKey.scrollUp()
  MOBI.others.others_clearReqWaitCmdFlg()
  MOBI.fingerKey.tap('id=com.android.chrome:id/url_bar')
  MOBI.others.others_clearReqWaitCmdFlg()
  abc = MOBI.fingerKey.type('id=com.android.chrome:id/url_bar','https://www.vnexpress.net')
  print(abc)
  MOBI.others.others_clearReqWaitCmdFlg()
  MOBI.funcButton.enterKey()
  MOBI.others.others_clearReqWaitCmdFlg()

  # MOBI.logging.stopRecordScreen()


  


