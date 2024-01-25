import __init
import os
os.environ['DISPLAY'] = '8702ba7a106e:1'
os.environ['XAUTHORITY']='/root/.Xauthority'

os.system("echo $DISPLAY")
os.system("echo $XAUTHORITY")

from Library.A1_PyAutoGUI.pyAutoGui_Wrap import pyAutoGui_Remap as GUI

print (os.getcwd())
GUI.screen.screenshot("test.png")
