import __init
from time import sleep
from SystemManager.Components.systemThreadWDT import *
from SystemManager.Components.systemThreadTimer import *
from SystemManager.Components.systemThreadCrontab import *
from SystemManager.Components.pcInfo import *


class SYS ():
  ################################
  # 1. Watchdog timer            #
  ################################
  class thread_WDT (threadWDT):
    '''Thread of Watchdog timer'''
    pass
  ################################
  # 2. Timer                     #
  ################################
  class thread_Timer (threadTimer):
    '''Thread of Timer'''
    pass
  ################################
  # 3. Crontab                   #
  ################################
  class thread_Crontab (threadCrontab):
    '''Thread of Crontab'''
    pass
  ################################
  # 4. PC Information            #
  ################################
  class pcInfo(pcInfoClass):
    pass