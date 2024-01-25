import __init
from Library.A8_Appium.appium_Wrap import appium_Remap

MOBI = appium_Remap()
MOBI.setup.begin(remoteAddr="localhost",remotePort=4723,deviceUUID="LHS7N18B29003666")


while True:
  MOBI.button.home()
  MOBI.button.back()
  MOBI.button.volumeUp()
  MOBI.button.volumeDown()
  MOBI.button.volumeMute()
  MOBI.button.power()
  MOBI.button.power()
  
  MOBI.fingerKey.longTap('xpath=//android.widget.TextView[@content-desc="Zalo"]')
  MOBI.fingerKey.longTapDragDrop('xpath=//android.widget.TextView[@content-desc="Zalo"]',
                          'xpath=//android.widget.TextView[@content-desc="ZaloTạo 2 bản"]')
  
  MOBI.fingerKey.scrollDown()
  MOBI.others.others_clearReqWaitCmdFlg()
  MOBI.fingerKey.scrollUp()
  MOBI.others.others_clearReqWaitCmdFlg()
  MOBI.fingerKey.swipeLeft()
  MOBI.others.others_clearReqWaitCmdFlg()
  MOBI.fingerKey.swipeRight()
  MOBI.others.others_clearReqWaitCmdFlg()


