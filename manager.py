##################################################################
# Vai trò:
#  - Quản lý và cập nhật crontab cho các task.
#  - Tạo ra các container cho các task dựa theo bảng crontab.
#  - Kết nối vào gửi thông tin quản lý lên Zabbix Server. Bao gồm:
#    + Tên từng channel, số lượng following, like, video.
#    + Trạng thái hoạt động, lỗi, hình lỗi.
#  - Force số lần chạy của mỗi task.
# Hoạt động:
#  - Kiểm tra Timestamp của bảng manager có bị cập nhật và enable có đang bật không? (Nếu enable là 0 thì thêm # và đầu contab)
#  - Force số lần chạy của mỗi task. 
#
import __init
from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
import os
import time
import random

MYSQL_HOST     = "200.200.200.1"
MYSQL_DATABASE = "tik_0_man"
MYSQL_USER     = "root"
MYSQL_PASS     = "admin"
MYSQL_TABLE    = "channel_config"
sql = MYSQL(MYSQL_HOST,MYSQL_USER,MYSQL_PASS,MYSQL_DATABASE)

def __genCrontabString(channelConfig):
  import yaml #pip install pyyaml
  import json

  # Add random seed
  current_time = int(time.time())
  random.seed(current_time)
  
  #endStatus = "" if channelConfig['enable'] == "1" else "#"
  endStatus = "" if channelConfig['enable'] == 1 else "#"
  data = yaml.load(channelConfig['configuration'], Loader=yaml.FullLoader)
  print(endStatus)
  # print(data)
  
  os.system("rm -f mycron")
  newCronFlag = True
  commonEnv = data['common_env']
  # pprint.pprint(commonEnv)

  for task, task_data in data.items():
    if task.startswith("task_"):
      with open("mycron", "a") as f:
        #For new crongroup
        if newCronFlag:
          newCronFlag = False
          f.write("\n##################################################################\n")
        #For new task
        f.write("#=== "+str(task).upper() +" ===\n")
        crontabInfo = task_data['crontab']
        # print(crontabInfo)

        #Generate crontab string
        crontabName:str = task
        crontabTime:str = crontabInfo['time']
        crontabSleep:str = crontabInfo['sleep']
        crontabCommand:str = crontabInfo['command']
        crontabEnv = crontabInfo['env']
        crontabEnv.update(commonEnv)
        
        #Calculate sleep time
        if crontabSleep == "0":
          crontabSleep = ""
        else:
          if crontabSleep.startswith("RAN"):
            sleepTime = crontabSleep.split("(")[1].split(")")[0].strip()
            sleepTime = str(random.randint(0, int(sleepTime)))
            crontabSleep = "sleep " + sleepTime + ";"
          else:
            sleepTime = crontabSleep.strip()
            crontabSleep = "sleep " + sleepTime + ";"
        crontabEnv = json.dumps(crontabEnv)
        #Generate crontab string
        cronString = endStatus + crontabTime.ljust(20) + " " + crontabSleep.ljust(10) + " " + crontabCommand.ljust(50) + " '" + str(crontabEnv) + "'\n"
        #write cronString to crontab
        f.write(cronString)
  os.system("crontab mycron")
  os.system("rm mycron")

def __updateCrontab():
  query = "SELECT * FROM "+ MYSQL_TABLE
  allChannelConfig = sql.customSelect(query)
  for channelConf in allChannelConfig:
    try:
      # print(channelConf)
      print("========================")
      __genCrontabString(channelConf)
    except Exception as e:
      print("Error: ", e)

def checkUpdateCrontab():
  #Get timestamp of lastest update
  query = "SELECT timestamp FROM "+ MYSQL_TABLE + " ORDER BY timestamp DESC LIMIT 1"
  timestamp = str(sql.customSelect(query)[0]['timestamp'])

  #check if file /.lastManUpdate existed -> compare timestamp.
  #If timestamp is different -> update crontab
  #If timestamp is same -> do nothing
  if os.path.isfile('/.lastManUpdate'):
    with open('/.lastManUpdate', 'r') as f:
      lastTimestamp = f.read()
    if lastTimestamp != timestamp:
      print("Update crontab: ", timestamp)
      with open('/.lastManUpdate', 'w') as f:
        f.write(timestamp)
      __updateCrontab() #Update crontab
    else:
      print("No update crontab: ", timestamp)
      pass
  else:
    print("First time run: ", timestamp)
    with open('/.lastManUpdate', 'w') as f:
      f.write(timestamp)
    __updateCrontab() #First time run

# while True:
#   checkUpdateCrontab()
#   time.sleep(1)


#Manager Node
managerNode = '''
docker run -tid --name manager -u root --privileged  --network newpyworker_network --ip 200.200.200.200 --hostname manager meomay22/dev_python:0.1 /bin/bash -l -c 'tail -f /dev/null'"
'''

import random
import time

class clientInfo:
  def __init__(self, HOST_NAME:str="task",REMOVE_AFTER_RUN:str="YES",DISPLAY_MODE:str="XVFB_DISPLAY",
               HOST_VNC_PORT:str='55901',VNC_VIEW_ONLY:str='YES',SHARE_MEMORY:str='512M',
               NETWORK_NAME:str='newpyworker_network',RUN_CMD:str="TAIL_NOT_STOP"):
    random.seed(time.time())
    RAN_NUM = str(random.randint(1, 1000000))
    self.HOST_NAME = HOST_NAME+"_"+RAN_NUM
    self.REMOVE_AFTER_RUN = REMOVE_AFTER_RUN
    self.DISPLAY_MODE = DISPLAY_MODE
    self.HOST_VNC_PORT = HOST_VNC_PORT
    self.VNC_VIEW_ONLY = VNC_VIEW_ONLY
    self.SHARE_MEMORY = SHARE_MEMORY
    self.NETWORK_NAME = NETWORK_NAME
    if RUN_CMD == "TAIL_NOT_STOP":
      RUN_CMD = "tail -f /dev/null"
    self.RUN_CMD = RUN_CMD
    
  def genContainer(self):
    self.dockerClient  = "docker run -tid"                                                     #Create Container
    if self.REMOVE_AFTER_RUN == "YES":
      self.dockerClient += " --rm"                                                             #Remove Container when stop
    self.dockerClient += " --name="+self.HOST_NAME                                             #Container Name
    self.dockerClient += " --hostname="+self.HOST_NAME                                         #Container Hostname
    self.dockerClient += " --shm-size="+self.SHARE_MEMORY                                      #Shared Memory
    if self.DISPLAY_MODE == "VNC_DISPLAY":
      self.dockerClient += " -p "+self.HOST_VNC_PORT+":5901"                                   #VNC Port
    self.dockerClient += " -u root"                                                            #User
    self.dockerClient += " --privileged"                                                       #Privileged
    self.dockerClient += " -v D:/Database/GIT/LOTUS_Python_Framework/Docker/DC_NewPyWorker/worker/startup.sh:/etc/profile.d/startup.sh" #Startup Script
    self.dockerClient += " -v D:/Database/GIT/LOTUS_Python_Framework/Docker/DC_NewPyWorker/worker/vncPass:/root/.vnc/passwd" #VNC Password
    self.dockerClient += " -v D:/Database/GIT/LOTUS_Python_Framework:/HShare"                  #Host Share
    self.dockerClient += " -v D:/Biz/GX_DATA/vn_20_scanned_list:/vn_20_scanned_list"           #Scanned List
    self.dockerClient += " -v D:/Biz/GX_DATA/vn_30_ready_list:/vn_30_ready_list"               #Ready List
    self.dockerClient += " -v D:/Biz/GX_DATA/processing:/processing"                           #Processing List
    self.dockerClient += " -v D:/Database/GIT/LOTUS_Python_Framework/.bashrc:/root/.bashrc"    #Bashrc
    self.dockerClient += " -w /HShare/Docker/DC_NewPyWorker"                                   #Working Directory
    self.dockerClient += " --network="+self.NETWORK_NAME                                       #Network
    # self.dockerClient += " --ip 200.200.200.10"                                                #IP
    self.dockerClient += " -e DISPLAY_MODE="+self.DISPLAY_MODE                                 #Display Mode: VNC_DISPLAY/XVFB_DISPLAY
    self.dockerClient += " -e LOTUS_DISPLAY_VNC_VIEW_ONLY="+self.VNC_VIEW_ONLY                 #VNC View Only: YES/NO
    self.dockerClient += " -e USER=root"                                                       #User: root
    self.dockerClient += " -e LOTUS_DISPLAY_WIDTH=1920"                                        #Display Width
    self.dockerClient += " -e LOTUS_DISPLAY_HEIGHT=1080"                                       #Display Height
    self.dockerClient += " -e LOTUS_DISPLAY_DEPTH=24"                                          #Display Depth
    self.dockerClient += " --link=lotus_mysql"                                                 #Link to MySQL
    self.dockerClient += " newpyworker"                                                        #Image Name
    self.dockerClient += " /bin/bash -l -c \""+self.RUN_CMD+"\""                               #Run Command
    print(self.dockerClient)
    return self.dockerClient

# dockerClient = clientInfo(REMOVE_AFTER_RUN="YES",RUN_CMD="python3 /HShare/MyAPP/TiktopApp/GX/1_SCAN_GX_APP.py")
# dockerClient = clientInfo(REMOVE_AFTER_RUN="YES",DISPLAY_MODE='VNC_DISPLAY',VNC_VIEW_ONLY="NO",RUN_CMD="python3 /HShare/MyAPP/TiktopApp/GX/2_DOWNLOAD_GX_APP.py")
# dockerClient = clientInfo(REMOVE_AFTER_RUN="YES",DISPLAY_MODE='XVFB_DISPLAY',VNC_VIEW_ONLY="YES",RUN_CMD="TAIL_NOT_STOP")
# import os
# os.system(dockerClient.genContainer())

##########################################################################################






