#Scrip sẽ kiểm tra app có đang được chạy không? Nếu không thì bật nó
import os
import sys

def writeLog (log:str="", filename:str="/checkRunApp.log"):
  with open(filename, "a") as f:
    f.write(log+"\n")
    
# In các đối số dầu vào.
# os.system("echo '' > /checkRunApp.log")
# writeLog("Number of arguments: "+str(len(sys.argv))+" arguments.")
# writeLog("Argument 1: "+str(sys.argv[1]))
# writeLog("Argument 2: "+str(sys.argv[2]))

  

def checkAndOpenAppOneTime (checkKeyWord:str="",shOpenApp:str=""):
  # [Crontab -e] * * * * * python3 /root/1_HP1_MANAGER/00_DCP_TIK_PJ/TIK_PJ/checkRunApp.py 'Tik_Man.sh' 'screen -dmS Manager sh /root/Tik_Man.sh &' 
  # root      788986  0.0  0.0   2888   964 ?        Ss   16:16   0:00 /bin/sh -c python3 /root/1_HP1_MANAGER/00_DCP_TIK_PJ/TIK_PJ/checkRunApp.py 'Tik_Man.sh' 'screen -dmS Manager sh /root/Tik_Man.sh &' 
  # root      788988  0.0  0.0  17552  9892 ?        S    16:16   0:00 python3 /root/1_HP1_MANAGER/00_DCP_TIK_PJ/TIK_PJ/checkRunApp.py Tik_Man.sh screen -dmS Manager sh /root/Tik_Man.sh &
  numCnt = int(os.popen("ps aux | grep -v grep | grep "+checkKeyWord+" | wc -l").read())
  if numCnt <= 2: #Một khai báo bên Crontab sẽ tạo ra một tiến trình Session Leader (chạy sh) và một tiến trình con.
    print("\x1b[38;5;3mCheck: "+checkKeyWord+" is not running\x1b[0m")
    print("\x1b[38;5;3mExec: "+shOpenApp+"\x1b[0m")
    os.system(shOpenApp)
    

    
def checkAndOpenAppList (checkKeyWord:str="",shOpenApp:str=""):
  if int(os.popen("ps aux | grep -v grep | grep "+checkKeyWord+" | wc -l").read()) == 0:
    print("\x1b[38;5;3mCheck: "+checkKeyWord+" is not running\x1b[0m")
    print("\x1b[38;5;3mExec: "+shOpenApp+"\x1b[0m")
    os.system(shOpenApp)


if len(sys.argv) == 3:
  ############# CHECK AND OPEN APPLICATION ####################
  checkAndOpenAppOneTime (checkKeyWord=str(sys.argv[1]),shOpenApp=str(sys.argv[2]))
else:
  pass
  ############# LIST APPLICATION ####################
  # checkAndOpenAppList("MQTT_ZabbixService1","screen -dmS MQTT_ZABBIX python3 /home/ubuntu/Python/MQTT_TO_ZABBIX/MQTT_ZabbixService1.py &")
  # checkAndOpenAppList("MQTT_ZabbixService2","screen -dmS MQTT_ZABBIX python3 /home/ubuntu/Python/MQTT_TO_ZABBIX/MQTT_ZabbixService2.py &")
  # checkAndOpenAppList("MQTT_ZabbixService3","screen -dmS MQTT_ZABBIX python3 /home/ubuntu/Python/MQTT_TO_ZABBIX/MQTT_ZabbixService3.py &")