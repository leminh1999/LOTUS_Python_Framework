import __init
from Conf.loggingSetup import *
from SystemManager.system_Wrap import SYS
import platform
import mysql.connector
OS_SYSTEM = platform.system()
PC_NAME = SYS.pcInfo.pcName()
print("OS_SYSTEM = ",OS_SYSTEM)
print("PC_NAME = ",PC_NAME)

### Private Functions ###
def dynaConnectMysql(host:str="",database:str="mysql",username:str="bot",password:str="xI2@z63pa@"):
  try:
    mysql.connector.connect(
      host       = host,
      user       = username,
      password   = password,
      database   = database, #Tên cơ sở dữ liệu
      autocommit = True      #Tự động cập nhật bảng và dữ liệu đang chạy.
    )
    return True
  except:
    return False


def dynaPing(host:str):
  import subprocess
  param = '-n' if platform.system().lower()=='windows' else '-c'
  command = ['ping', param, '1', '-w', '1', host]
  return subprocess.call(command) == 0
###################################################################
REMOTE_NAS_IP = "lotus1104.synology.me"
LOCAL_HP1_IP = "192.168.68.119"
LOCAL_NAS_IP = "192.168.68.143"
LOCAL_LOTUS_S0 = "192.168.68.200"
LOCAL_INTERNAL_DOCKER = "200.200.200.1"
HOST_HOSTNAME = os.getenv("HOST_HOSTNAME") #Parent hostname của máy chủ chạy container
print("HOST_HOSTNAME = ",HOST_HOSTNAME)
#1. PC_NAME = LOTUS-PC
if PC_NAME == "LOTUS_S0" or HOST_HOSTNAME == "LOTUS_S0":
  FULL_CODE_DIR = "D:/Database/SynologyDrive/GIT/LOTUS_Python_Framework" #Chỉ dành cho máy DEV (CMEV-PC157)
  ROOT_MAN_DIR = "D:/Database/SynologyDrive/Biz/RootManager1"
  PATH_LAST_MAN_UPDATE = "D:/.lastManUpdate"
  if HOST_HOSTNAME == "LOTUS_S0":
    MYSQL_HOST = LOCAL_HP1_IP #Chạy từ Container của Docker. Chú ý: Container thuộc mạng nội bộ 200.200.200.x vẫn có thể truy xuất mạng LAN của máy host: 192.168.68.x
  else:
    MYSQL_HOST = LOCAL_HP1_IP #Chạy từ máy Dev
  logger.info("PC_NAME ("+PC_NAME+") will be connected to MySQL server ("+MYSQL_HOST+")...")
  
#2. PC_NAME = CMEV-PC157
elif PC_NAME == "CMEV-PC157" or HOST_HOSTNAME == "CMEV-PC157":
  if dynaPing(LOCAL_NAS_IP) == True and dynaConnectMysql(LOCAL_NAS_IP) == True:
    #HOME
    FULL_CODE_DIR = "D:/Database/SynologyDrive/GIT/LOTUS_Python_Framework"      #Full code. Get from Github.
    ROOT_MAN_DIR = "D:/Database/SynologyDrive/Biz/RootManager1"                          #Root Manager at Local PC.
    PATH_LAST_MAN_UPDATE = "D:/.lastManUpdate"                    #Path to save last update time of manager table.
    MYSQL_HOST = LOCAL_HP1_IP
    logger.info("PC_NAME ("+PC_NAME+") will be connected to MySQL server ("+MYSQL_HOST+")...")
  else:
    #OFFICE
    FULL_CODE_DIR = "D:/Database/SynologyDrive/GIT/LOTUS_Python_Framework"      #Full code. Get from Github.
    ROOT_MAN_DIR = "D:/Database/SynologyDrive/Biz/RootManager1"   #Root Manager at Local PC.
    PATH_LAST_MAN_UPDATE = "D:/.lastManUpdate"                    #Path to save last update time of manager table.
    MYSQL_HOST = "lotus1104.synology.me"                          #DDNS MySQL
    logger.info("PC_NAME ("+PC_NAME+") will be connected to MySQL server ("+MYSQL_HOST+")...")
  
elif PC_NAME == "lotushp1" or HOST_HOSTNAME == "lotushp1":
  if dynaPing(LOCAL_NAS_IP) == True and dynaConnectMysql(LOCAL_NAS_IP) == True:
    #HOME
    FULL_CODE_DIR = "/mnt/GIT/LOTUS_Python_Framework"      #Full code. Get from Github.
    ROOT_MAN_DIR = "/mnt/Biz/RootManager1"                          #Root Manager at Local PC.
    PATH_LAST_MAN_UPDATE = "/.lastManUpdate"                    #Path to save last update time of manager table.
    MYSQL_HOST = LOCAL_HP1_IP
    logger.info("PC_NAME ("+PC_NAME+") will be connected to MySQL server ("+MYSQL_HOST+")...")
  else:
    #OFFICE
    FULL_CODE_DIR = "/mnt/GIT/LOTUS_Python_Framework"      #Full code. Get from Github.
    ROOT_MAN_DIR = "/mnt/Biz/RootManager1"   #Root Manager at Local PC.
    PATH_LAST_MAN_UPDATE = "/.lastManUpdate"                    #Path to save last update time of manager table.
    MYSQL_HOST = "lotus1104.synology.me"                          #DDNS MySQL
    logger.info("PC_NAME ("+PC_NAME+") will be connected to MySQL server ("+MYSQL_HOST+")...")
    
#3. PC_NAME = Others
else:
  FULL_CODE_DIR = "-"
  ROOT_MAN_DIR = "-"
  PATH_LAST_MAN_UPDATE = "-"

##### Common #####
WORK_DIR = ROOT_MAN_DIR                                  #Work dir to run container.
MASTER_CODE_DIR = ROOT_MAN_DIR+"/code"  #Master code dir
MASTER_CODEGEN_DIR = ROOT_MAN_DIR+"/codeGenerating/MASTER_CODE"  #Master code dir
APP_DIR_S = FULL_CODE_DIR+"/MyAPP"     #Source App Dir
REQ_MAN_KILL = ROOT_MAN_DIR+"/data/0_AllChannels/0_ReqManKill.txt"
MYSQL_USER = "bot"
MYSQL_PASS = "xI2@z63pa@"



#### FINALLY ##############################################
connectStatus=dynaConnectMysql(host=MYSQL_HOST,database="mysql",username=MYSQL_USER,password=MYSQL_PASS)
if connectStatus == True:
  logger.info("=> MySQL server ("+MYSQL_HOST+") is connected successfully.")
else:
  logger.warning("=> MySQL server ("+MYSQL_HOST+") is NOT connected!!!")
