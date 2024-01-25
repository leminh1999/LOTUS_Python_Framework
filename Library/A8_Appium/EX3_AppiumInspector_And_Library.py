import __init
from Library.A8_Appium.appium_Wrap import appium_Remap
import time,datetime

MOBI = appium_Remap()
MOBI.setup.begin(remoteAddr="localhost",remotePort=4723,deviceUUID="LHS7N18B29003666")


while True:
  element = MOBI.others.others_content_findFirstElement('xpath=//*[@resource-id="com.ss.android.ugc.trill:id/e6m"]')
  print(element)
  print(element.get_attribute('resource-id'))
  
  
  #############################################################################################
  # RESULT: Library\A8_Appium\Components\PIC\EX3_FindFirstElement_BaseOnAppiumInspector.png   #
  #############################################################################################

