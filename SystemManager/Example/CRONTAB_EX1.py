import __init
from time import sleep
from SystemManager.system_Wrap import *

def callback1():
  print('I am working on callback 1')

def callback2():
  print('I am working on callback 2')
  
#############################
# Example 1                 #
#############################
CRONTAB = SYS.thread_Crontab()
CRONTAB.start()
CRONTAB.debugPrintTime = True

#Register tasks
CRONTAB.registerCrontab('task 1', '0 * * * * * *', callback1,crontabExecMode.THREAD_CALLBACK)  #Every minute
CRONTAB.registerCrontab('task 2', '0 * * * * * *', callback2) #Every minute
CRONTAB.registerCrontab('task 3', '0 * * * * * *', "D:\Database\OneDrive - 5TB\Task_Managerment_Dung.xlsx",crontabExecMode.THREAD_WINRUN) #Every minute
#Show all tasklist
CRONTAB.showTasklist()

time.sleep(15)
CRONTAB.stop() #Stop crontab
print('CRONTAB STOPPED')

time.sleep(5)
CRONTAB.cont() #Continue
print('CRONTAB CONTINUE')
