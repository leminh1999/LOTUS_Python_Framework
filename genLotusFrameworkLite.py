import os
import platform
import shutil

import __init

OS_SYSTEM = platform.system()
print( "OS_SYSTEM: ", OS_SYSTEM)
if OS_SYSTEM == "Windows":
    FULL_CODE_DIR = "D:/Database/GIT/LOTUS_Python_Framework"
    ROOT_MAN_DIR = "D:/Biz/RootManager1"
if OS_SYSTEM == "Linux" or OS_SYSTEM == "Darwin" :
    ROOT_MAN_DIR = ""
    FULL_CODE_DIR = ""

MASTER_CODE_DIR = ROOT_MAN_DIR+"/code/MASTER_CODE"
APP_DIR_S = FULL_CODE_DIR+"/MyAPP/TiktopApp/GX"

#Generate LOTUS_FRAMEWORK_LITE_MASTER
def genLotusFrameworkLite():
  '''
  Generate LOTUS_FRAMEWORK_LITE_MASTER from FULL_CODE_DIR
  ''''
  #0_Clean
  if os.path.exists(MASTER_CODE_DIR): shutil.rmtree(MASTER_CODE_DIR)
  os.mkdir(MASTER_CODE_DIR)

  #
  os.mkdir(MASTER_CODE_DIR+"/Conf")
  shutil.copyfile(FULL_CODE_DIR+"/Conf/loggingSetup.py", MASTER_CODE_DIR+"/Conf/loggingSetup.py")
  shutil.copyfile(FULL_CODE_DIR+"/Conf/systemDefine.py", MASTER_CODE_DIR+"/Conf/systemDefine.py")
  shutil.copyfile(FULL_CODE_DIR+"/Conf/systemVar.py", MASTER_CODE_DIR+"/Conf/systemVar.py")
  shutil.copytree(APP_DIR_S, MASTER_CODE_DIR+"/MY_APP")
  shutil.copyfile(FULL_CODE_DIR+"/__init.py", MASTER_CODE_DIR+"/__init.py")
  shutil.copyfile(FULL_CODE_DIR+"/main.py", MASTER_CODE_DIR+"/main.py")
  shutil.copytree(FULL_CODE_DIR+"/Library", MASTER_CODE_DIR+"/Library")

  #Find and delete all jpeg in a folder and sub folder in python
  delFileType = [".png", ".jpg", ".jpeg", ".gif"]
  delFileName = ["chromedriver"]
  delDirName  = ["__pycache__", "PIC", "Logs", "Doc", "Example"]
  for root, dirs, files in os.walk(MASTER_CODE_DIR):
      #Delete File and File Type
      for file in files:
          #Delete File
          for delFile in delFileName:
              if file == delFile:
                  os.remove(os.path.join(root, file))
          #Delete File Type
          for delType in delFileType:
              if file.endswith(delType):
                  os.remove(os.path.join(root, file))
      #Delete Dir
      for dir in dirs:
          for delDir in delDirName:
              if dir == delDir:
                  shutil.rmtree(os.path.join(root, dir))
              
  #Create Logs
  os.mkdir(MASTER_CODE_DIR+"/Logs")
  os.mkdir(MASTER_CODE_DIR+"/Logs/RotateLogs")

#Generate Data structure
def genDataStruct(rootManDir=ROOT_MAN_DIR, channelName="", taskId="", containerId="",masterCodeDir=MASTER_CODE_DIR):
  '''
  Generate Data structure at RootManager, Channel, Task, Container.
  Then copy to MASTER_CODE_DIR if masterCodeDir is exist.
  '''
  #At RootManager
  if rootManDir == "": return #Error
  if not os.path.exists(rootManDir+"/data"): os.mkdir(rootManDir+"/data")
  #At Channel
  if channelName != "":
    if not os.path.exists(rootManDir+"/data/0_AllChannels"): os.mkdir(rootManDir+"/data/0_AllChannels")
    if not os.path.exists(rootManDir+"/data/channel_"+channelName): os.mkdir(rootManDir+"/data/channel_"+channelName)
  #At Task
  if channelName != "" and taskId != "":
    if not os.path.exists(rootManDir+"/data/channel_"+channelName+"/0_AllTasks"): os.mkdir(rootManDir+"/data/channel_"+channelName+"/0_AllTasks")
    if not os.path.exists(rootManDir+"/data/channel_"+channelName+"/task_"+taskId) : os.mkdir(rootManDir+"/data/channel_"+channelName+"/task_"+taskId)
  #At Container
  if channelName != "" and taskId != "" and containerId != "":
    if not os.path.exists(rootManDir+"/data/channel_"+channelName+"/task_"+taskId+"/0_AllContainers"): os.mkdir(rootManDir+"/data/channel_"+channelName+"/task_"+taskId+"/0_AllContainers")
    if not os.path.exists(rootManDir+"/data/channel_"+channelName+"/task_"+taskId+"/taskContainer_"+containerId) :
      CONTAINTER_DIR = rootManDir+"/data/channel_"+channelName+"/task_"+taskId+"/taskContainer_"+containerId
      os.mkdir(CONTAINTER_DIR)
      if masterCodeDir != "":
        shutil.copytree(MASTER_CODE_DIR,CONTAINTER_DIR+"/code/")
      


# genDataStruct (rootManDir=ROOT_MAN_DIR, channelName="Tiktop", taskId="1", containerId="222", masterCodeDir=MASTER_CODE_DIR)

