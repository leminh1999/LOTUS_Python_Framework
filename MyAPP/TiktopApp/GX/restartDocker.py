import __init
from Library.A2_LOTUS.lotus_Wrap import lotus_Remap as LOTUS
from time import sleep
import time
import threading

def openDockerAuto():
  while True:
    try:
      print("==> Openning Docker...")
      LOTUS.taskManager.programOpenJoinIn('C:\Program Files\Docker\Docker\Docker Desktop.exe')
      sleep(5)
    except:
      print("==> Docker was killed.")
      sleep(5)
threading.Thread(target=openDockerAuto).start()

def restartDocker():
  LOTUS.taskManager.taskKiller('"Docker Desktop.exe"')

while True:
  sleep(30)
  print("Kill Docker")  
  restartDocker()


