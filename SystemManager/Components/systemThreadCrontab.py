import __init
import time
from Conf.loggingSetup import *
from datetime import datetime
from crontab import CronTab
import threading
import subprocess


# CHÚ Ý: kiểu khai báo của crontab được ghi ở đây:
# https://pypi.org/project/crontab/

crontabTaskList = list() # List of crontab task
crontabInfoDict = dict() # Dictionary of crontab info

class crontabExecMode ():
  '''Cài đặt chế độ chạy của crontab:
  - THREAD_CALLBACK: Mở một thread mới để chạy hàm callback được nhập vào trước đó.
  - THREAD_WINRUN: Mở một thread mới để chạy Window Run với Command đã nhập vào.
  '''
  THREAD_CALLBACK = 'thread_callback'
  THREAD_WINRUN = 'thread_winrun'
  
class threadCrontab (threading.Thread):
  '''`Giới Thiệu`: Thread contab được sử dụng để quản lý sự thực thi các task con. Cơ chế hoạt động giống như Crontab của Linux.
  `Cơ chế hoạt động`: Thread contab sẽ được chạy như một luồng độc lập với Thread main. Các task sẽ được chạy theo thời gian đã được định nghĩa trong crontab.\\
  Khi đến thời gian thì một Thread con mới sẽ được chạy để thực thi task con đó.\\
  Mỗi task con khi đến thời gian sẽ có một luồng riêng sử lý. Luồng này sẽ tắt khi task con kết thúc.\\
  |__Thread Main\\
  |__Thread Crontab Manager\\
      |__Thread Task 1\\
      |__Thread Task 2
        
  `Các bước sử dụng:`
  - Chuẩn bị một hàm callback sẵn.
  - Đăng ký một task: `threadCrontab.registerCrontab(taskName, taskTime, taskCallback)`
  - Xóa một task: `threadCrontab.deleteCrontab(taskName)`
  - Chạy các task: `threadCrontab.start()`
  - Dừng các task: `threadCrontab.stop()`
  - Tiếp tục các task: `threadCrontab.cont()`
  - Hiển thị các task đang chạy: `threadCrontab.showTaskList()`

      
  '''
  def __init__(self):
    threading.Thread.__init__(self)
    self.run_flag = True
    self.debugPrintTime = False

  #register a crontab entry
  def registerCrontab(self,taskName, taskTime, taskCallback, class_crontabExecMode = crontabExecMode.THREAD_CALLBACK):
    if taskName in crontabTaskList:
      logger.info('>>> Task name('+taskName+') already registered!!!')
      return False

    #Register to dictionary
    crontabInfoDict[taskName+'_name']       = taskName
    crontabInfoDict[taskName+'_time']       = taskTime
    crontabInfoDict[taskName+'_callback']   = taskCallback
    crontabInfoDict[taskName+'_execMode']   = class_crontabExecMode
    crontabInfoDict[taskName+'_nextRunSec'] = CronTab(taskTime).next()
    crontabInfoDict[taskName+'_execFlag']   = 0
    #Register to List
    crontabTaskList.append(taskName)
  
  #delete a crontab entry
  def deleteCrontab(self,taskName):
    #Remove from List
    crontabTaskList.remove(taskName)
    #Remove from Dictionary
    crontabInfoDict.pop(taskName+'_name')
    crontabInfoDict.pop(taskName+'_time')
    crontabInfoDict.pop(taskName+'_callback')
    crontabInfoDict.pop(taskName+'_execMode')
    crontabInfoDict.pop(taskName+'_nextRunSec')
    crontabInfoDict.pop(taskName+'_execFlag')
  
  def run(self):
    logger.info (">>>> Crontab Manager is running <<<<")
    self.run_flag = True
    while (1):
      if self.run_flag == True: self.__checkTaskAndExec()
      time.sleep(1)
      
  def stop(self):
    self.run_flag = False
    
  def cont (self):
    self.run_flag = True
    
  def showTasklist(self):
    #Show task list
    print('-'*100)
    print('{n:<8}{t:<20}{s:<30}{m:<12}{c:<}'.format(n = 'Num',t = 'TaskName', s = 'Schedule Time', m = 'Mode',c = 'Callback/Command' ))
    print('-'*100)
    
    num = 0
    for i in crontabTaskList:
      num += 1
      print('{n:<8}{t:<20}{s:<30}{m:<12}{c:<}'.format( \
        n = num, \
        t = crontabInfoDict[i+'_name'], \
        s = crontabInfoDict[i+'_time'], \
        # m = crontabInfoDict[i+'_execMode'], \
        m = 'CALLBACK' if crontabInfoDict[i+'_execMode'] == 'thread_callback' else 'WINRUN' , \
        c = str(crontabInfoDict[i+'_callback']) \
      ))
    print('-'*100+'\n')
  
  def __refreshInfoDict(self):
    '''Refresh thời gian chạy tiếp theo của các task trong crontab và trạng thái cờ task_execFlag'''
    for i in crontabTaskList:
      nextRunSec = CronTab(crontabInfoDict[i+'_time']).next()
      if crontabInfoDict[i+'_nextRunSec'] < nextRunSec: crontabInfoDict[i+'_execFlag'] = 1
      crontabInfoDict[i+'_nextRunSec'] = nextRunSec
        
  def __checkTaskAndExec(self):
    '''Kiểm tra xem các task có thể chạy không'''
    if self.debugPrintTime == True: print(datetime.now())
    self.__refreshInfoDict()
    for i in crontabTaskList:
      if crontabInfoDict[i+'_execFlag'] == 1:
        crontabInfoDict[i+'_execFlag'] = 0
        if crontabInfoDict[i+'_execMode'] == 'thread_callback':
          threading.Thread(target=crontabInfoDict[i+'_callback']).start()
        elif crontabInfoDict[i+'_execMode'] == 'thread_winrun':
          subprocess.Popen(crontabInfoDict[i+'_callback'],shell=True)
        else:
          logger.error(">>>> Unknown execMode")
          return False
    
########################################