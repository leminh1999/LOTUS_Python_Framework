import __init
from Library.A3_Selenium.Components.SeleniumIDE import *
from Library.A8_Appium.Components.Appium import *


APPIUM = AppiumLib()



#Import from Selenium IDE
class appium_Remap():
  class setup (): #==============================> Đã verify
    begin = APPIUM.begin
    quit  = APPIUM.quit

  class button (): #==============================> Đã verify #<---- Đã gán beautiful HTML LOG # Conf\htmlAsset\pressButton.png
    home                = APPIUM.buttonHome
    back                = APPIUM.buttonBack
    volumeUp            = APPIUM.buttonVolumeUp
    volumeDown          = APPIUM.buttonVolumeDown
    volumeMute          = APPIUM.buttonVolumeMute
    power               = APPIUM.buttonPower
    
  class funcButton (): #==============================> Đã verify #<---- Đã gán beautiful HTML LOG # Conf\htmlAsset\swFunc.png
    sleep               = APPIUM.funcSleep
    wakeUp              = APPIUM.funcWakeUp
    copy                = APPIUM.funcCopy
    paste               = APPIUM.funcPaste
    cut                 = APPIUM.funcCut
    pageDown            = APPIUM.funcPageDown
    pageUp              = APPIUM.funcPageUp
    enterKey            = APPIUM.funcEnterKey
    previous            = APPIUM.buttonBack
    forward             = APPIUM.buttonForward
    inputSearch         = APPIUM.funcInputSearch
    openCallApp         = APPIUM.funcOpenCallApp
    endCall             = APPIUM.funcEndCall
    openBrowserApp      = APPIUM.funcOpenBrowserApp
    openMailApp         = APPIUM.funcOpenMailApp
    appSwitch           = APPIUM.funcAppSwitch
    showAllApp          = APPIUM.funcShowAllApp
    brightnessUp        = APPIUM.funcBrightnessUp
    brightnessDown      = APPIUM.funcBrightnessDown
    openCalendarApp     = APPIUM.funcOpenCalendarApp
    openMusicApp        = APPIUM.funcOpenMusicApp
    openContactApp      = APPIUM.funcOpenContactApp
    cameraZoomIn        = APPIUM.funcCameraZoomIn
    cameraZoomOut       = APPIUM.funcCameraZoomOut
    cameraCaptureButton = APPIUM.funcCameraCaptureButton
    
  class fingerKey (): #==============================> Đã verify #<---- Đã gán beautiful HTML LOG # Conf\htmlAsset\ActionIcon.png
    wTap                = APPIUM.tap               # Wait then action.
    wTapPos             = APPIUM.tapPos            # Wait then action.
    wTapMultiPos        = APPIUM.tapMultiPos       # Wait then action.
    wDoubleTap          = APPIUM.doubleTap         # Wait then action.
    wLongTap            = APPIUM.longTap           # Wait then action.
    wDragDrop           = APPIUM.dragDrop          # Wait then action.
    wLongTapDragDrop    = APPIUM.longTapDragDrop   # Wait then action.
    scroll              = APPIUM.scroll
    scrollUp            = APPIUM.flickDown
    scrollDown          = APPIUM.flickUp
    swipeLeft           = APPIUM.swipeLeft
    swipeRight          = APPIUM.swipeRight
    flickUp             = APPIUM.flickUp
    flickDown           = APPIUM.flickDown
    wType               = APPIUM.type              # Wait then action.
    wSendKeys           = APPIUM.sendKeys          # Wait then action.
    sendKeyCode         = APPIUM.driver.press_keycode
    
  class waitFor (): #==============================> Đã verify #<---- Đã gán beautiful HTML LOG # Conf\htmlAsset\WaitIcon.png
    waitForElementPresent     = APPIUM.waitForElementPresent
    waitForElementNotPresent  = APPIUM.waitForElementNotPresent    #Cần chỉnh lại chỗ Wait. Đang bị sai.
    waitForElementVisible     = APPIUM.waitForElementVisible
    waitForElementNotVisible  = APPIUM.waitForElementNotVisible    #Cần chỉnh lại chỗ Wait. Đang bị sai.
    waitForElementEditable    = APPIUM.waitForElementEditable
    waitForElementNotEditable = APPIUM.waitForElementNotEditable  #Cần chỉnh lại chỗ Wait. Đang bị sai.
    waitForText               = APPIUM.waitForText
    waitForAttr               = APPIUM.waitForAttr
  
  
  
  class others ():
    others_content_findFirstElement      = APPIUM.others_content_findFirstElement #==============================> Đã verify
    others_content_findAllElements       = APPIUM.others_content_findAllElements #==============================> Đã verify
    others_content_findLastElement       = APPIUM.others_content_findLastElement #==============================> Đã verify
    others_content_getPageSourceCode     = APPIUM.others_content_getPageSourceCode #==============================> Đã verify
    others_keyMouse_hotkeys              = APPIUM.others_keyMouse_hotkeys
    others_content_getAttribute          = APPIUM.others_content_getAttribute #==============================> Đã verify
    others_content_getText               = APPIUM.others_content_getText
    others_debug_printComment            = APPIUM.others_debug_printComment #==============================> Đã verify
    others_clearReqWaitCmdFlg            = APPIUM.clearReqWaitCmdFlg #==============================> Đã verify
    others_clearExitOnExceptionFlg       = APPIUM.clearExitOnExceptionFlg 
    others_setExitOnExceptionFlg         = APPIUM.setExitOnExceptionFlg
    others_content_getPosSizeElement     = APPIUM.others_content_getPosSizeElement #==============================> Đã verify
    others_content_getPosMidElement      = APPIUM.others_content_getPosMidElement  #==============================> Đã verify
    others_content_saveElementScreenshot = APPIUM.others_content_saveElementScreenshot  #==============================> Đã verify
    
  class logging():
    startRecordScreen = APPIUM.startRecordScreen
    stopRecordScreen  = APPIUM.stopRecordScreen

  # class IDE (APPIUM.driver):
  #   pass














#############################################################################################
# MOBI = appium_Remap()
# MOBI.setup.begin(remoteAddr="localhost",remotePort=4723,deviceUUID="LHS7N18B29003666")

# MOBI2 = appium_Remap()
# MOBI2.SETUP.begin(remoteAddr="localhost",remotePort=4724,deviceUUID="LHS7N18B29003444")

# while True:
#     inputString = input("Enter your input: ")
#     print("Received input is: ", inputString)
#     APPIUM.driver.press_keycode(int(inputString)) # Ấn nút HOME

# while True:
#   # MOBI.button.home()
#   # MOBI.button.back()
#   # MOBI.button.volumeUp()
#   # MOBI.button.volumeDown()
#   # MOBI.button.volumeMute()
#   # MOBI.button.power()
#   # MOBI.button.power()
  
#   # MOBI.fingerKey.longTap('xpath=//android.widget.TextView[@content-desc="Zalo"]')
#   # MOBI.fingerKey.longTapDragDrop('xpath=//android.widget.TextView[@content-desc="Zalo"]',
#   #                         'xpath=//android.widget.TextView[@content-desc="ZaloTạo 2 bản"]')
  
#   # MOBI.fingerKey.scrollDown()
#   # MOBI.others.others_clearReqWaitCmdFlg()
#   # MOBI.fingerKey.scrollUp()
#   # MOBI.others.others_clearReqWaitCmdFlg()
#   # MOBI.fingerKey.swipeLeft()
#   # MOBI.others.others_clearReqWaitCmdFlg()
#   # MOBI.fingerKey.swipeRight()
#   # MOBI.others.others_clearReqWaitCmdFlg()

#   # video_options = {
#   #     'timeLimit': '180',
#   #     # 'bitRate': '4000000',
#   #     # 'videoSize': '720x1280',
#   #     # 'bugReport': 'true',
#   #     # 'androidQuality': '20',
#   #     # 'ignoreSilentMode': 'false',
#   #     'remotePath': '/sdcard/Download/abc.mp4'
#   # }
#   MOBI.logging.startRecordScreen()
#   # APPIUM.driver.start_recording_screen(video_options)
  
#   MOBI.fingerKey.scrollUp()
#   MOBI.others.others_clearReqWaitCmdFlg()
#   MOBI.fingerKey.tap('id=com.android.chrome:id/url_bar')
#   MOBI.others.others_clearReqWaitCmdFlg()
#   abc = MOBI.fingerKey.type('id=com.android.chrome:id/url_bar','https://www.google.com.vn')
#   print(abc)
#   MOBI.others.others_clearReqWaitCmdFlg()
#   MOBI.funcButton.enterKey()
#   MOBI.others.others_clearReqWaitCmdFlg()



#   MOBI.fingerKey.scrollUp()
#   MOBI.others.others_clearReqWaitCmdFlg()
#   MOBI.fingerKey.tap('id=com.android.chrome:id/url_bar')
#   MOBI.others.others_clearReqWaitCmdFlg()
#   abc = MOBI.fingerKey.type('id=com.android.chrome:id/url_bar','https://www.vnexpress.net')
#   print(abc)
#   MOBI.others.others_clearReqWaitCmdFlg()
#   MOBI.funcButton.enterKey()
#   MOBI.others.others_clearReqWaitCmdFlg()

#   MOBI.logging.stopRecordScreen()


  


