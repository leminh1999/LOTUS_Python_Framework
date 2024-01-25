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

dockerClient = clientInfo(REMOVE_AFTER_RUN="YES",HOST_VNC_PORT="55902",RUN_CMD="TAIL_NOT_STOP")
# dockerClient = clientInfo(REMOVE_AFTER_RUN="YES",HOST_VNC_PORT="55902",RUN_CMD="python3 /HShare/MyAPP/TiktopApp/GX/1_SCAN_GX_APP.py")

# dockerClient = clientInfo(REMOVE_AFTER_RUN="YES",DISPLAY_MODE='VNC_DISPLAY',VNC_VIEW_ONLY="NO",RUN_CMD="python3 /HShare/MyAPP/TiktopApp/GX/2_DOWNLOAD_GX_APP.py")
# dockerClient = clientInfo(REMOVE_AFTER_RUN="YES",DISPLAY_MODE='XVFB_DISPLAY',VNC_VIEW_ONLY="YES",RUN_CMD="TAIL_NOT_STOP")
import os
os.system(dockerClient.genContainer())

##########################################################################################






