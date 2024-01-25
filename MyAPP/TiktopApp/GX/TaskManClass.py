##################################################################
# Vai trò:
#  - Quản lý và cập nhật danh sách khởi tạo các container theo thời gian như crontab.
#  - Kết nối vào gửi thông tin quản lý lên Zabbix Server. Bao gồm:
#    + Tên từng channel, số lượng following, like, video.
#    + Trạng thái hoạt động, lỗi, hình lỗi.
#  - Force chạy một task tức thì và xuất VNC nếu bật.
# Hoạt động:
#  - Kiểm tra Timestamp của bảng manager có bị cập nhật và enable có đang bật không? (Nếu enable là 0 thì thêm # và đầu contab)
#  - Force số lần chạy của mỗi task. 
#
import __init
import MyAPP.TiktopApp.GX.DynamicParamPC as PARAM
from Conf.loggingSetup import *
from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
from SystemManager.system_Wrap import SYS
import os
import time
import random
from crontab import CronTab
import datetime
import platform
import shutil

MYSQL_TABLE    = "channel_config"

#MySQL Configurations ############################################################
sql = MYSQL(hostAddress    = PARAM.MYSQL_HOST,       #Địa chỉ IP của MySQL server nội bộ tại nhà
            database       = "tik_0_man",
            username       = PARAM.MYSQL_USER,
            password       = PARAM.MYSQL_PASS)
##################################################################################
# rawMysqlDataList = [] #Fetch raw data from mysql (Including YAML config)
scheduleList = [] #Convert to [{nextRunTime:xxx, mysqlDataInJson:xxx},....]

################################################################################################
class TaskManager ():
  global scheduleList
  # global rawMysqlDataList
  
  #Generate LOTUS_FRAMEWORK_LITE_MASTER
  def genLotusFrameworkLite():
    '''
    Generate LOTUS_FRAMEWORK_LITE_MASTER from FULL_CODE_DIR
    '''
    #0_Clean
    if os.path.exists(PARAM.ROOT_MAN_DIR+"/codeGenerating"):
      shutil.rmtree(PARAM.ROOT_MAN_DIR+"/codeGenerating")
    os.mkdir(PARAM.ROOT_MAN_DIR+"/codeGenerating")
    if os.path.exists(PARAM.MASTER_CODEGEN_DIR): shutil.rmtree(PARAM.MASTER_CODEGEN_DIR)
    os.mkdir(PARAM.MASTER_CODEGEN_DIR)
    #
    shutil.copytree(PARAM.FULL_CODE_DIR+"/NasScripts", PARAM.MASTER_CODEGEN_DIR+"/NasScripts")
    shutil.copytree(PARAM.FULL_CODE_DIR+"/Conf", PARAM.MASTER_CODEGEN_DIR+"/Conf")
    shutil.copyfile(PARAM.FULL_CODE_DIR+"/__init.py", PARAM.MASTER_CODEGEN_DIR+"/__init.py")
    shutil.copyfile(PARAM.FULL_CODE_DIR+"/main.py", PARAM.MASTER_CODEGEN_DIR+"/main.py")
    shutil.copytree(PARAM.FULL_CODE_DIR+"/Library", PARAM.MASTER_CODEGEN_DIR+"/Library")
    shutil.copytree(PARAM.FULL_CODE_DIR+"/SystemManager", PARAM.MASTER_CODEGEN_DIR+"/SystemManager")

    #Find and delete all jpeg in a folder and sub folder in python
    delFileType = [".png", ".jpg", ".jpeg", ".gif"]
    delFileName = ["chromedriver"]
    delDirName  = ["__pycache__", "PIC", "Logs", "Doc", "Example"]
    for root, dirs, files in os.walk(PARAM.MASTER_CODEGEN_DIR):
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
                
    #Copy MyAPP
    shutil.copytree(PARAM.APP_DIR_S, PARAM.MASTER_CODEGEN_DIR+"/MyAPP")
    #Create Logs
    os.mkdir(PARAM.MASTER_CODEGEN_DIR+"/Logs")
    os.mkdir(PARAM.MASTER_CODEGEN_DIR+"/Logs/RotateLogs")
    shutil.make_archive(PARAM.MASTER_CODEGEN_DIR, 'gztar', PARAM.MASTER_CODEGEN_DIR)
    shutil.copyfile(PARAM.MASTER_CODEGEN_DIR+".tar.gz", PARAM.MASTER_CODE_DIR+"/MasterCode.tar.gz")
    now = datetime.datetime.now()
    date_time = now.strftime("%d.%b.%Y_%H.%M.%S")
    shutil.copyfile(PARAM.MASTER_CODEGEN_DIR+".tar.gz", PARAM.MASTER_CODE_DIR+"/History/MasterCode_"+str(date_time)+".tar.gz")
    shutil.rmtree(PARAM.ROOT_MAN_DIR+"/codeGenerating")
    
  def checkReqManKillFile(reqManKillFile=""):
    #Check reqManKillFile if exist
    if os.path.isfile(reqManKillFile):
      with open(reqManKillFile, 'r') as file:
          lines = file.readlines()
      if len(lines) > 0:
        try:
          # Remove the last line
          killTask = str(lines.pop()).strip()
          import subprocess
          command = 'docker ps --filter "status=running" --format "{{.ID}} {{.Names}} {{.Status}}"'
          output = subprocess.check_output(command, shell=True)
          for eachLine in output.decode('utf-8').splitlines():
            if killTask in eachLine:
              #Xóa container nếu nó vẫn còn đang chạy
              logger.info("Docker kill "+killTask)
              os.system("docker container rm -f "+killTask)
              with open(reqManKillFile, 'w') as file:
                  file.writelines(lines)
        except Exception as e:
          print(e)
          pass
        #Remove reqManKillFile file
        try:
          os.remove(reqManKillFile)
        except:
          pass
    

  def killLongTask(timeLimitSec=30*60, taskNameContain="_con_"):
    import subprocess
    command = 'docker ps --filter "status=running" --format "{{.ID}} {{.Names}} {{.Status}}"'
    try:
      output = subprocess.check_output(command, shell=True)
    except:
      logger.error("\n===================================================\nDocker Desktop/App chưa được chạy. Xin mở nó trước!\n===================================================\n")
    for eachLine in output.decode('utf-8').splitlines():
      if taskNameContain in eachLine:
        #1. Tính Runtime của container
        data = eachLine.split(" ")
        containerId = data[0]
        containerName = data[1]
        containerTime = data[3]
        containerUnit = data[4]
        if containerUnit == "seconds":
          runTimeSec = int(containerTime)
        elif containerUnit == "minutes":
          runTimeSec = int(containerTime) * 60
        elif containerUnit == "hours":
          runTimeSec = int(containerTime) * 60 * 60
        elif "day" in containerUnit :
          runTimeSec = int(containerTime) * 60 * 60 * 24
        elif containerUnit == "a":
          runTimeSec = 60
        else:
          runTimeSec = 0
        #2. So sánh với timeLimitSec
        if runTimeSec > timeLimitSec:
          logger.warning("Manager Kill Long Task: %s" % containerName)
          os.system("docker rm -f %s" % containerName)
        else:
          pass

  #Generate Data structure
  def genDataStruct(rootManDir=PARAM.ROOT_MAN_DIR, channelName="", taskName="", containerId="",masterCodeDir=PARAM.MASTER_CODE_DIR):
    '''
    Generate Data structure at RootManager, Channel, Task, Container.
    Then copy to MASTER_CODE_DIR if masterCodeDir is exist.
    '''
    #At RootManager
    if rootManDir == "": return #Error
    if not os.path.exists(rootManDir+"/data"): os.mkdir(rootManDir+"/data")
    if not os.path.exists(rootManDir+"/data/0_AllChannels"): os.mkdir(rootManDir+"/data/0_AllChannels")
    #At Channel
    if channelName != "":
      if not os.path.exists(rootManDir+"/data/channel_"+channelName): os.mkdir(rootManDir+"/data/channel_"+channelName)
      ALL_TASK_DIR = rootManDir+"/data/channel_"+channelName+"/0_AllTasks" 
      if not os.path.exists(ALL_TASK_DIR): os.mkdir(ALL_TASK_DIR)
      if not os.path.exists(ALL_TASK_DIR+"/0_scanned_list"): os.mkdir(ALL_TASK_DIR+"/0_scanned_list")
      if not os.path.exists(ALL_TASK_DIR+"/1_ready_list"): os.mkdir(ALL_TASK_DIR+"/1_ready_list")
      if not os.path.exists(ALL_TASK_DIR+"/1_ready_list/ads"): os.mkdir(ALL_TASK_DIR+"/1_ready_list/ads")
      if not os.path.exists(ALL_TASK_DIR+"/1_ready_list/bind"): os.mkdir(ALL_TASK_DIR+"/1_ready_list/bind")
      if not os.path.exists(ALL_TASK_DIR+"/1_ready_list/approve"): os.mkdir(ALL_TASK_DIR+"/1_ready_list/approve")
    #At Task
    if channelName != "" and taskName != "":
      if not os.path.exists(rootManDir+"/data/channel_"+channelName+"/"+taskName) : os.mkdir(rootManDir+"/data/channel_"+channelName+"/"+taskName)
      if not os.path.exists(rootManDir+"/data/channel_"+channelName+"/"+taskName+"/0_AllContainers"): os.mkdir(rootManDir+"/data/channel_"+channelName+"/"+taskName+"/0_AllContainers")
    #At Container
    if channelName != "" and taskName != "" and containerId != "":
      CONTAINTER_DIR = rootManDir+"/data/channel_"+channelName+"/"+taskName+"/taskContainer_"+str(containerId)
      if os.path.exists(CONTAINTER_DIR): shutil.rmtree(CONTAINTER_DIR)
      os.mkdir(CONTAINTER_DIR)
      if masterCodeDir != "":
        shutil.unpack_archive(PARAM.MASTER_CODE_DIR+"/MasterCode.tar.gz", CONTAINTER_DIR+"/code/")
        shutil.unpack_archive(CONTAINTER_DIR+"/code/MyAPP/TiktopApp/GX/startup.tar.gz", CONTAINTER_DIR+"/code/MyAPP/TiktopApp/GX")
        shutil.unpack_archive(CONTAINTER_DIR+"/code/MyAPP/TiktopApp/GX/vncPass.tar.gz", CONTAINTER_DIR+"/code/MyAPP/TiktopApp/GX")
        ARGS_FILE = rootManDir+"/data/channel_"+channelName+"/0_AllTasks/"+taskName+"_args.py"
        shutil.copyfile(ARGS_FILE,CONTAINTER_DIR+"/code/task_args.py")

  def __convertToScheduleList(channelConfig):
    global scheduleList
    import yaml #pip install pyyaml
    import json
    # Add random seed
    current_time = int(time.time())
    random.seed(current_time)
    #Check enable field
    if channelConfig['enable'] == 0:
      #Xóa scheduleList nếu có
      scheduleList = [x for x in scheduleList if x["channel"] != channelConfig['channel_name']]
      #Xóa trên mysql nếu có
      sql.deleteRow(table="schedule_list", whereCondition="channel = '"+channelConfig['channel_name']+"'")
      pass
      
      
      
      
      return None
    #Load YAML config
    yamlToJsonData = yaml.load(channelConfig['configuration'], Loader=yaml.FullLoader)
    channelConfig['configuration'] = yamlToJsonData
    #Get nextRunTime
    #  channelConfig  -> Tính thời gian cho mỗi task và gán vào list cụ thể để chạy container.
    #Init value
    commonArg = {}
    commonDocker = []
    taskDocker = []
    taskCrontab = {}
    taskCrontabTime = "0 0 * * *"
    taskCrontabSleep = "0"
    taskCrontabEnv = {}
    for confBlock in channelConfig['configuration']:
      if "common_arg" in confBlock:
        commonArg = channelConfig['configuration'][confBlock]
      # print("commonArg: ", commonArg)
      if "common_docker" in confBlock:
        commonDocker = channelConfig['configuration'][confBlock] 
      if "task_" in confBlock:
        taskNum = int(confBlock.split("_")[1])
        #################################
        # A. Collect all data in task_x #
        #################################
        taskConf = channelConfig['configuration'][confBlock]
        for taskConfBlock in taskConf:
          if "task_enable" in taskConfBlock and taskConf[taskConfBlock] == 0: continue #Skip task if task_enable = 0
          if "docker" in taskConfBlock: taskDocker = taskConf[taskConfBlock]
          if "crontab" in taskConfBlock: taskCrontab = taskConf[taskConfBlock]
          for crontabBlock in taskCrontab:
            if "time" in crontabBlock: taskCrontabTime = taskCrontab[crontabBlock]
            if "sleep" in crontabBlock: taskCrontabSleep = taskCrontab[crontabBlock]
            if "arg" in crontabBlock: taskCrontabEnv = taskCrontab[crontabBlock]
        
        ################################################
        # B. Calculate task_x then add to scheduleList #
        ################################################
        dockerArg = commonDocker.copy()
        # B1. Calculate Time
        if confBlock == "task_"+str(channelConfig['force_debug_task_num']):
          debugStatus = "DEBUG" #Force debug
          if SYS.pcInfo.pcName() == "CMEV-PC157":
            dockerArg.append("-v D:\Database\SynologyDrive\GIT\LOTUS_Python_Framework\.pc157DebugVscodeServer:/root/.vscode-server")
        else:
          debugStatus = "-" #Normal
          
        if confBlock == "task_"+str(channelConfig['force_task_num']):
          nextRunTime = round(datetime.datetime.now().timestamp() - 1)
          sleepTime = 0
          sleepTimeStr = "FIX(0)"
          #Clear force_task_num
          updateString = "force_task_num = 0"
          TaskManager.forceTaskRun(channelId=int(channelConfig['id']), taskNum=0, vncNum=0, debugNum=0)
        else:
          nextRunTime = round(CronTab(taskCrontabTime).next(delta=True,default_utc=False))
          if "RAN" in taskCrontabSleep:
            sleepTimeRan = taskCrontabSleep.split("(")[1].split(")")[0].strip()
            sleepTime = random.randint(0, int(sleepTimeRan))
            sleepTimeStr = "RAN("+str(sleepTimeRan)+")"
          else:
            sleepTime = int(taskCrontabSleep.strip())
            sleepTimeStr = "FIX("+str(sleepTime)+")"
          nextRunTime += sleepTime
          nextRunTime = round(datetime.datetime.now().timestamp() + nextRunTime)
        nextRunTime = datetime.datetime.fromtimestamp(nextRunTime)
        
        # B2. Calculate Script Arguments and Save to File
        scriptArgDict = commonArg.copy()
        scriptArgDict.update(taskCrontabEnv)
        # print("ScriptArg: ", scriptArg)
        TaskManager.genDataStruct(channelName=channelConfig['channel_name'])
        taskArgJsonFile = confBlock+"_args.json"
        taskArgParamFile = confBlock+"_args.py"
        with open(PARAM.ROOT_MAN_DIR+"/data/channel_"+channelConfig['channel_name']+"/0_AllTasks/"+taskArgJsonFile, "w", encoding="utf-8") as f:
          json.dump(scriptArgDict, f, indent=2)
        with open(PARAM.ROOT_MAN_DIR+"/data/channel_"+channelConfig['channel_name']+"/0_AllTasks/"+taskArgParamFile, "w", encoding="utf-8") as f:
          f.write("class ARGS: #Collect all ARGS of task (Transfer by Manager)\n")
          #Convert dict to each line
          for key in scriptArgDict:
            f.write("  "+key+" = \""+str(scriptArgDict[key])+"\"\n")
        
        # B3. Calculate Docker Arguments
        if int(channelConfig['force_vnc_task_num']) == taskNum: #Chỉ kết nối cổng 5901 ra ngoài khi VNC được yêu cầu
          dockerArg.append("-p 5901:5901")
          dockerArg.append("-e DISPLAY_MODE=VNC_DISPLAY")
        #Kiểm tra xem có yêu cầu debug không
        if int(channelConfig['force_debug_task_num']) == taskNum: #Chỉ kết nối cổng 5901 ra ngoài khi VNC được yêu cầu
          for i in range(0, len(taskDocker)):
            if "/bin/bash" in taskDocker[i]:
              taskDocker[i] = "/bin/bash -c \"tail -f /dev/null\"" #Để task chạy mãi mãi
              break
        else:
          pass
        dockerArg.extend(taskDocker)
        dockerArg = " ".join(dockerArg)
        # print("DockerArg: ", dockerArg)
        
        # B4. Add to scheduleList
        scheduleList.append({'time':nextRunTime,
                            'crontabTime':taskCrontabTime,
                            'sleepTime':sleepTimeStr,
                            'channel':channelConfig['channel_name'],
                            'task':confBlock,
                            'debugStatus': debugStatus,
                            'dockerRun':dockerArg})
        
        # Add to MySQL if not exist. If exist, update nextRunTime
        query = "SELECT * FROM schedule_list WHERE channel = '"+channelConfig['channel_name']+"' AND task = '"+confBlock+"'"
        result = sql.customSelect(query)
        if len(result) == 0:
          #Insert new data to MySQL table
          columnString = "time, crontabTime, sleepTime, channel, task, debugStatus, dockerRun"
          valueString  = "'"+str(nextRunTime)+"', '"+str(taskCrontabTime)+"', '"+str(sleepTimeStr)+"', '"+str(channelConfig['channel_name'])+"', '"+str(confBlock)+"', '"+str(debugStatus)+"', '"+str(dockerArg)+"'"
          sql.insertRow("schedule_list", columnString, valueString)
        else:
          #Update MySQL table
          updateString = "time = '"+str(nextRunTime)+"', crontabTime = '"+str(taskCrontabTime)+"', sleepTime = '"+str(sleepTimeStr)+"', debugStatus = '"+str(debugStatus)+"', dockerRun = '"+str(dockerArg)+"'"
          whereCondition = "channel = '"+str(channelConfig['channel_name'])+"' AND task = '"+str(confBlock)+"'"
          sql.updateRow("schedule_list", updateString, whereCondition)
          pass
          
           

  def __renewScheduleListForAllTasksOfAllChannels():
    # global rawMysqlDataList
    global scheduleList
    scheduleList = [] #Clear scheduleList
    query = "SELECT * FROM "+ MYSQL_TABLE
    allChannelConfig = sql.customSelect(query)
    for channelConf in allChannelConfig:
      try:
        # rawMysqlDataList.append(channelConf)
        TaskManager.__convertToScheduleList(channelConf)
      except Exception as e:
        print("Error: ", e)
        
  def __renewScheduleListForAllTasksChangedByHandInChannelConfigTable(changedChannelInChannelConfigTable=""):
    # global rawMysqlDataList
    global scheduleList
    scheduleList = [x for x in scheduleList if x["channel"] != changedChannelInChannelConfigTable] #Giữ lại các channel khác
    query = "SELECT * FROM "+ MYSQL_TABLE
    allChannelConfig = sql.customSelect(query)
    for channelConf in allChannelConfig:
      if channelConf['channel_name'] == changedChannelInChannelConfigTable: #Chỉ cập nhật lại cho channel bị thay đổi bằng tay.
        try:
          # rawMysqlDataList.append(channelConf)
          TaskManager.__convertToScheduleList(channelConf)
        except Exception as e:
          print("Error: ", e)

  def __clearScheduleListMySQL(mysqlTable):
    '''
    Xóa toàn bộ dữ liệu trong MySQL table'''
    #Clear MySQL table
    sql.deleteRow(mysqlTable, whereCondition="1=1")

  def __insertScheduleListMySQL(mysqlTable): #Update MySQL
    for i in range(0, len(scheduleList)):
      #Insert new data to MySQL table
      columnString = "time, crontabTime, sleepTime, channel, task, debugStatus, dockerRun"
      valueString  = "'"+str(scheduleList[i]['time'])+"', '"+str(scheduleList[i]['crontabTime'])+"', '"+str(scheduleList[i]['sleepTime'])+"', '"+str(scheduleList[i]['channel'])+"', '"+str(scheduleList[i]['task'])+"', '"+str(scheduleList[i]['debugStatus'])+"', '"+str(scheduleList[i]['dockerRun'])+"'" #+str(scheduleList[i]['dockerRun'])
      sql.insertRow(mysqlTable, columnString, valueString)

  def __updateScheduleListMySQL(mysqlTable): #Update MySQL
    #Update MySQL table
    updateString = "video_id = 'test2', key_word = 'test2', key_type = 'test2',\
                    status = 'test2', timestamp = CURRENT_TIMESTAMP"
    sql.updateRow("vn_20_scanned_list", updateString, whereCondition="id = 2")

  def checkChanelConfigTableChangedByHandToUpdateScheduleList():
    '''
    Kiểm tra MySQL table có thay đổi không.
    Update scheduleList nếu có thay đổi.
    '''
    #Get timestamp of lastest update
    query = "SELECT * FROM "+ MYSQL_TABLE + " ORDER BY timestamp DESC LIMIT 1"
    checkData =sql.customSelect(query)[0]
    timestamp = str(checkData['timestamp'])
    channel_name = str(checkData['channel_name'])

    #check if file PATH_LAST_MAN_UPDATE existed -> compare timestamp.
    #If timestamp is different -> update schedule list
    #If timestamp is same -> do nothing
    if os.path.isfile(PARAM.PATH_LAST_MAN_UPDATE):
      with open(PARAM.PATH_LAST_MAN_UPDATE, 'r', encoding="utf-8") as f:
        lastTimestamp = f.read()
      if lastTimestamp != timestamp:
        print(">>>> Update schedule list: ", timestamp)
        with open(PARAM.PATH_LAST_MAN_UPDATE, 'w', encoding="utf-8") as f:
          f.write(timestamp)
        TaskManager.__renewScheduleListForAllTasksChangedByHandInChannelConfigTable(channel_name) #Update crontab
      else:
        # print("No update schedule list: ", timestamp)
        pass
    else:
      print("Run first time after host reboot. Update schedule list: ", timestamp)
      with open(PARAM.PATH_LAST_MAN_UPDATE, 'w', encoding="utf-8") as f:
        f.write(timestamp)
      TaskManager.__renewScheduleListForAllTasksOfAllChannels() #First time run
      # TaskManager.__clearScheduleListMySQL(mysqlTable="schedule_list") #Clear MySQL
      # TaskManager.__insertScheduleListMySQL(mysqlTable="schedule_list") # Add new MySQL


  def checkTimeToRunInScheduleList():
    '''
    Kiểm tra xem có task nào cần chạy không.
    Nếu có thì chạy task đó.
    '''
    global scheduleList
    now = datetime.datetime.now()
    
    for task in scheduleList:
      if task['time'] <= now:
        logger.info("=== MATCHED TIME: "+str(now)+" ==================================")
        #get channel id from channel_config table
        query = "SELECT id FROM channel_config WHERE channel_name = '"+task['channel']+"'"
        channelId = sql.customSelect(query)[0]['id']
        logger.debug("[CID:"+str(channelId)+"]Channel: "+task['channel'])
        logger.debug("Task Num: "+task['task'])
        logger.debug("Schedule Time: "+str(task['time']))

        if task['debugStatus'] == "DEBUG":
          logger.warn("DEBUG MODE")
          debug_status = " -e FORCE_DEBUG_STATUS=True "
          #Next run time is 100 days later
          nextRunTime = round(datetime.datetime.now().timestamp() + 8640000) #Run after 100 days.
        else:
          debug_status = " -e FORCE_DEBUG_STATUS=False "
          nextRunTime = round(CronTab(task['crontabTime']).next(delta=True,default_utc=False))
          if "FIX(" in task['sleepTime']:
            sleepTime = int(task['sleepTime'].replace("FIX(","").replace(")",""))
          else:
            sleepNum = int(task['sleepTime'].replace("RAN(","").replace(")",""))
            sleepTime = random.randint(0, int(sleepNum))
          nextRunTime += sleepTime #Tính lại sleep time
          nextRunTime = round(datetime.datetime.now().timestamp() + nextRunTime)
        task['time'] = datetime.datetime.fromtimestamp(nextRunTime)
        logger.debug("Next Schedule: "+ str(task['time']))
        #1. Generate data structure and environment
        containerNum = int(time.time())
        containerName = task['channel']+"_"+task['task']+"_con_"+str(containerNum)
        dockerContainerName = "--name="+containerName+" --hostname=con_"+str(containerNum)
        TaskManager.genDataStruct(channelName=task['channel'], taskName=task['task'],containerId=containerNum)
        
        #2. REPLACE in docker
        REPLACED_CONTAINER_DIR = PARAM.ROOT_MAN_DIR+"/data/channel_"+task['channel']+"/"+task['task']+"/taskContainer_"+str(containerNum)
        REPLACED_HOSTNAME = SYS.pcInfo.pcName()
        REPLACED_CONTAINER_NAME = containerName
        REPLACED_ROOT_MAN_DIR = PARAM.ROOT_MAN_DIR
        REPLACED_LOCAL_CODE_DIR = "/HShare/data/channel_"+task['channel']+"/"+task['task']+"/taskContainer_"+str(containerNum)+"/code"
        REPLACED_IN_MANAGER = str(dockerContainerName) + str(debug_status)
        taskRun = task['dockerRun']
        taskRun = taskRun.replace("<REPLACED_CONTAINER_DIR>", REPLACED_CONTAINER_DIR)
        taskRun = taskRun.replace("<REPLACED_HOSTNAME>", REPLACED_HOSTNAME)
        taskRun = taskRun.replace("<REPLACED_CONTAINER_NAME>", REPLACED_CONTAINER_NAME)
        taskRun = taskRun.replace("<REPLACED_ROOT_MAN_DIR>", REPLACED_ROOT_MAN_DIR)
        taskRun = taskRun.replace("<REPLACED_LOCAL_CODE_DIR>", REPLACED_LOCAL_CODE_DIR)
        taskRun = taskRun.replace("<REPLACED_IN_MANAGER>", REPLACED_IN_MANAGER)
        
        logger.debug(taskRun.replace(" -", "\n-"))
        print("==== Run task ====")
        os.system(taskRun)

        #Update scheduleList on MySQL for the task reached time
        updateString = "time = '"+str(task['time'])+"'"
        sql.updateRow("schedule_list", updateString, whereCondition="channel = '"+str(task['channel'])+"' AND task = '"+str(task['task'])+"'")
        pass

  def forceTaskRun(channelId:int, taskNum:int, vncNum:int=0, debugNum:int=0):
    updateString = "force_task_num = "+str(taskNum)+", force_vnc_task_num = "+str(vncNum)+", force_debug_task_num = "+str(debugNum)
    sql.updateRow("channel_config", updateString, whereCondition="id = "+str(channelId))

