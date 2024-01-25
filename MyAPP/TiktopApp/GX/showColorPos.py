import pyautogui
import keyboard
import os
import sys
os.system("rm -f .screenshot*")

# import pyautogui
# pyautogui.displayMousePosition()
# pyautogui.mouseInfo()
try:
    while True:
        x, y = pyautogui.position()
        color = pyautogui.screenshot().getpixel((x, y))
        message = "("+str(x)+","+str(y)+"),rgb("+str(color[0]).rjust(3)+","+str(color[1]).rjust(3)+","+str(color[2]).rjust(3)+"),20"
        sys.stdout.write(message)
        sys.stdout.write("\n")
        # sys.stdout.write("\b" * len(message))
        sys.stdout.flush()
except KeyboardInterrupt:
    sys.stdout.write("\n")
    sys.stdout.flush()