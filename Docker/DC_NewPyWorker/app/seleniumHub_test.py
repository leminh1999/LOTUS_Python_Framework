import __init
import os
import pyautogui

########################################################################################
#https://abhishekvaid13.medium.com/pyautogui-headless-docker-mode-without-display-in-python-480480599fc4
DISPLAY_MODE = os.environ['DISPLAY_MODE']
if DISPLAY_MODE == 'XVFB_DISPLAY':
  print("XVFB_DISPLAY ON:", os.environ['DISPLAY'])
  import Xlib.display
  pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])
if DISPLAY_MODE == 'VNC_DISPLAY':
  print("VNC_DISPLAY ON:", os.environ['DISPLAY'])
  pass
########################################################################################

#



from time import sleep
from selenium import webdriver
from Library.A1_PyAutoGUI.pyAutoGui_Wrap import pyAutoGui_Remap as GUI
from Library.A3_Selenium.selenium_Wrap import Keys, WEB, seleniumIDE_Remap as IDE

print("1")
options = webdriver.ChromeOptions()
options.add_argument('disable-infobars')
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('start-maximized') #
# options.add_argument("--disable-extensions")
options.add_extension('/HShare/Library/A3_Selenium/Components/Jubei_Captcha_Auth.zip')
IDE.setup.begin("Chrome",headless=False,antiCaptcha=True)
IDE.browser.open('https://python.org')
IDE.others.others_clearReqWaitCmdFlg()
IDE.others.others_browser_maximizeWindow()
IDE.others.others_clearReqWaitCmdFlg()
print("2")
sleep(1)
GUI.screen.screenshot('screenshot.png')
print("3")
# IDE.setup.quit() #Kết thúc trình duyệt
