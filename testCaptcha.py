import __init
print("==== START ====")
from time import sleep,time
from Conf.loggingSetup import *
from SystemManager.system_Wrap import SYS
from Library.A1_PyAutoGUI.pyAutoGui_Wrap import pyAutoGui_Remap as GUI
from Library.A2_LOTUS.lotus_Wrap import lotus_Remap as LOTUS
# from Library.A3_Selenium.selenium_Wrap import Keys, WEB, seleniumIDE_Remap as IDE
# from Library.A4_SendInBlue.sendInBlue_Wrap import class_contentMode, mailConfig, sendInBlue_Wrapper as SIB
# from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
# from Library.A6_Zabbix.Zabbix_Wrap import zabbix_Wrapper as ZABBIX
# from MyAPP.TiktopApp.GX.Components.tiktok_class import gxMysql,dataInfo, tiktok_Wrapper
# from Library.C1_Captcha.captcha_Wrap import captcha_Wrapper as CAPTCHA
# from pyngrok import ngrok, conf
# from pprint import *

print("==== FINISH IMPORT ====")
from urllib.request import urlopen
from PIL import Image
imageData = Image.open(urlopen('https://p19-captcha-sg.ibyteimg.com/tos-alisg-i-ovu2ybn2i4-sg/57942e928b8245cf81a2ccb8f765ef7e~tplv-ovu2ybn2i4-2.jpeg'))
imageWidth, imageHeight = imageData.size



brightColor = (230,230,230)
darkColor = (75,75,75)
deltaBrightColor = 30
deltaDarkColor = 75
checkFromX = 0
checkToX = imageWidth-20
checkFromY = 0
checkToY = imageHeight-20

detectSlidePos = False
for yLoc in range(checkFromY,checkToY):
  for xLoc in range(checkFromX,checkToX):
    # print("xLoc: ",xLoc,"yLoc: ",yLoc)
    if LOTUS.color.checkColorWithoutCapture(imageData,(xLoc,  yLoc   ),brightColor,deltaBrightColor,0) and\
       LOTUS.color.checkColorWithoutCapture(imageData,(xLoc,  yLoc+5 ),brightColor,deltaBrightColor,0) and\
       LOTUS.color.checkColorWithoutCapture(imageData,(xLoc,  yLoc+10),brightColor,deltaBrightColor,0) and\
       LOTUS.color.checkColorWithoutCapture(imageData,(xLoc+2,yLoc   ),darkColor,deltaDarkColor,0) and\
       LOTUS.color.checkColorWithoutCapture(imageData,(xLoc+2,yLoc+5 ),darkColor,deltaDarkColor,0) and\
       LOTUS.color.checkColorWithoutCapture(imageData,(xLoc+2,yLoc+10),darkColor,deltaDarkColor,0) :
      print(xLoc,yLoc)
      detectSlidePos = True
      break
  if detectSlidePos:
    break

       