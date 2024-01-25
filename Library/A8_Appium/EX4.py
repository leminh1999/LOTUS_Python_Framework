import __init
from Library.A8_Appium.appium_Wrap import appium_Remap
import time,datetime

MOBI = appium_Remap()
MOBI.setup.begin(remoteAddr="localhost",remotePort=4723,deviceUUID="LHS7N18B29003666",implicitlyWait=10)


while True:
  print(datetime.datetime.now())
  MOBI.others.others_content_saveElementScreenshot('xpath=//*[@resource-id="com.ss.android.ugc.trill:id/e6m"]','abc.png')
  element = MOBI.others.others_content_getPosMidElement('xpath=//*[@resource-id="com.ss.android.ugc.trill:id/e6m"]')
  print(element)
  print(len(element))
  print(datetime.datetime.now())
  pass
  
  ###############################################################################################
  # RESULT: Library\A8_Appium\Components\PIC\EX4_saveElementScreenshot_and_FindElementPos.png   #
  #         Library\A8_Appium\Components\PIC\EX4_abc.png                                        #
  ###############################################################################################

