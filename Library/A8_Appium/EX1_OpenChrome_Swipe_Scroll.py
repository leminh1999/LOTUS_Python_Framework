import __init
from Library.A8_Appium.appium_Wrap import appium_Remap

MOBI = appium_Remap()
MOBI.setup.begin(remoteAddr="localhost",remotePort=4723,deviceUUID="LHS7N18B29003666")


while True:
  MOBI.button.home() # Ấn nút HOME
  MOBI.funcButton.openBrowserApp() # Mở ứng dụng Chrome
  
  #Mở trang web: https://www.google.com.vn
  MOBI.fingerKey.scrollUp() # Lăn lên để thấy thanh URL
  MOBI.others.others_clearReqWaitCmdFlg()
  MOBI.fingerKey.tap('id=com.android.chrome:id/url_bar') # Nhấn vào thanh URL để mở bàn phím
  MOBI.others.others_clearReqWaitCmdFlg()
  MOBI.fingerKey.type('id=com.android.chrome:id/url_bar','https://www.google.com.vn') # Nhập địa chỉ URL
  MOBI.others.others_clearReqWaitCmdFlg()
  MOBI.funcButton.enterKey() # Nhấn Enter để mở trang web
  MOBI.others.others_clearReqWaitCmdFlg()


  #Mở trang web: https://www.vnexpress.net
  MOBI.fingerKey.scrollUp() # Lăn lên để thấy thanh URL
  MOBI.others.others_clearReqWaitCmdFlg()
  MOBI.fingerKey.tap('id=com.android.chrome:id/url_bar') # Nhấn vào thanh URL để mở bàn phím
  MOBI.others.others_clearReqWaitCmdFlg()
  MOBI.fingerKey.type('id=com.android.chrome:id/url_bar','https://www.vnexpress.net') # Nhập địa chỉ URL
  MOBI.others.others_clearReqWaitCmdFlg()
  MOBI.funcButton.enterKey() # Nhấn Enter để mở trang web
  MOBI.others.others_clearReqWaitCmdFlg()



  


