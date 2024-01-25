import os
import shutil

path_NV1 = "../../Tiktop_VB_Script_Running/Task1GetCode_NV1/"
path_NV2 = "../../Tiktop_VB_Script_Running/Task1GetCode_NV2/"
path_NV3 = "../../Tiktop_VB_Script_Running/Task1GetCode_NV3/"
path_NV4 = "../../Tiktop_VB_Script_Running/Task1GetCode_NV4/"
path_NV5 = "../../Tiktop_VB_Script_Running/Task1GetCode_NV5/"
path_NV6 = "../../Tiktop_VB_Script_Running/Task1GetCode_NV6/"
path_NV7 = "../../Tiktop_VB_Script_Running/Task1GetCode_NV7/"
path_NV8 = "../../Tiktop_VB_Script_Running/Task1GetCode_NV8/"
path_NV9 = "../../Tiktop_VB_Script_Running/Task1GetCode_NV9/"

def cleanAndCopy (path):
  # #Xóa các file logs
  # listFiles = os.listdir(path+"Logs/")
  # for i in listFiles:
  #   os.remove(path+"Logs/"+i)
  #Copy Images
  listFiles = os.listdir(path+"Images/")
  for i in listFiles:
    os.remove(path+"Images/"+i)
  
  #Copy code và Images
  shutil.copy("./A1_GetLink_Define.py",path) #copy A1
  shutil.copy("./A3_GetLink_Main.py",path) #copy A3
  shutil.copy("./A4_GetLink_Function.py",path) #copy A4
  shutil.copy("./A5_GetLink_PrimaryFunction.py",path) #copy A5
  shutil.copy("./adsBot.py",path)
  shutil.copy("./adsBotLib.py",path)
    
  listFiles = os.listdir("Images/")
  for i in listFiles:
    shutil.copy("Images/"+i,path+"Images/")

cleanAndCopy(path_NV1)
cleanAndCopy(path_NV2)
cleanAndCopy(path_NV3)
cleanAndCopy(path_NV4)
cleanAndCopy(path_NV5)
cleanAndCopy(path_NV6)
cleanAndCopy(path_NV7)
cleanAndCopy(path_NV8)
cleanAndCopy(path_NV9)
