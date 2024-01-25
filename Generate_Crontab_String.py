# #Print contents of a yaml file
# import yaml #pip install pyyaml
# import pprint
# with open("Manager_config.yml") as f:
#     data = yaml.load(f, Loader=yaml.FullLoader)
#     pprint.pprint(data)
    
#Find a index of a key in a yaml file
import yaml #pip install pyyaml
import pprint
import json
import os
import time
import random

current_time = int(time.time())
random.seed(current_time)

os.system("rm -f mycron")
newCronFlag = True
with open("Manager_config.yml") as f:
  data = yaml.load(f, Loader=yaml.FullLoader)
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
        cronString = crontabTime.ljust(20) + " " + crontabSleep.ljust(10) + " " + crontabCommand.ljust(50) + " '" + str(crontabEnv) + "'\n"
        #write cronString to crontab
        f.write(cronString)


os.system("crontab mycron")
os.system("rm mycron")

    
    
    