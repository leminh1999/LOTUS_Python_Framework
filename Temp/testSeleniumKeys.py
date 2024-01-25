import __init
from time import sleep
from Conf.loggingSetup import *
from Library.A1_PyAutoGUI.pyAutoGui_Wrap import pyAutoGui_Remap as GUI
from Library.A2_LOTUS.lotus_Wrap import lotus_Remap as LOTUS
from Library.A3_Selenium.selenium_Wrap import Keys, WEB, seleniumIDE_Remap as IDE
from Library.A4_SendInBlue.sendInBlue_Wrap import class_contentMode, mailConfig, sendInBlue_Wrapper as SIB
from pyngrok import ngrok, conf



test = "1aaaa@2aaaaa@3aaaa@4aaaa"

a = test.split("@")

print(len(a))
print (a[-1])
print (test.split(a[-1])[0])

