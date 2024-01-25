import __init
from time import sleep
from Conf.loggingSetup import *
import threading
import time
import os

ALLOW_WDT_REBOOT_SYSTEM = False

# 1. Configure for Watchdog
class threadWDT (threading.Thread):
   '''Chức năng: Tạo ra một Thread chạy WDT. Khi timeout sẽ chạy callbackFunc hoặc reset thiết bị'''
   def __init__(self, threadID, name, timeThresSec, callbackFunc = None):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.timeThresSec = timeThresSec
      self.timeCounter = timeThresSec
      self.callbackWDT = callbackFunc
      self.pauseFlag = False
      self.stopFlag = False
      self.forceTimeoutFlag = False
      
   def run(self): #Bắt buộc phải có tên là run()
      # Re-initialize the timer counter and other flags
      self.timeCounter = self.timeThresSec
      self.pauseFlag = False
      self.stopFlag = False
      self.forceTimeoutFlag = False
      # Start watchdog
      logger.info (">>>> Starting " + self.name +" <<<<")
      while self.timeCounter > 0:
        time.sleep(1)
        if self.pauseFlag == True: continue # Skip the rest of the loop if paused
        if self.stopFlag == True: return    # Stop the loop if stopped
        if self.forceTimeoutFlag == True: break # Force timeout
        self.timeCounter -= 1 # Decrement the counter 1 second
      
      #######################
      ### WATCHDOG ACTION ###
      #######################
      if self.callbackWDT != None:
         logger.info(">>>> WATCHDOG(" + self.name +") TIMEOUT => CALLBACK FUNCTION <<<<")
         self.callbackWDT()
      else:
         if ALLOW_WDT_REBOOT_SYSTEM == True:
            logger.info(">>>> WATCHDOG(" + self.name +") TIMEOUT => SYSTEM REBOOTING <<<<")
            time.sleep(1)
            os.system("shutdown -t 0 -r -f")
         else:
            logger.info(">>>> WATCHDOG(" + self.name +") TIMEOUT => DO NOTHING <<<<")
      
   def pause(self):
      '''Tạm dừng WDT'''
      self.pauseFlag = True
      logger.info(">>>> WATCHDOG(" + self.name +") PAUSED <<<<")
      
   def resume(self):
      '''Tiếp tục chạy WDT'''
      self.pauseFlag = False
      logger.info(">>>> WATCHDOG(" + self.name +") RESUMED <<<<")
      
   def stop(self):
      '''Dừng WDT'''
      self.stopFlag = True
      logger.info(">>>> WATCHDOG(" + self.name +") STOPPED <<<<")
      
   def forceTimeout(self):
      '''Ép WDT timeout và chạy callback'''
      self.forceTimeoutFlag = True
      logger.info(">>>> WATCHDOG(" + self.name +") FORCE TO TIMEOUT <<<<")
      
   def refreshWDT(self):
      '''Refresh WDT'''
      self.timeCounter = self.timeThresSec
         
   def getTimeCounter(self):
      '''Lấy thời gian counter còn lại của WDT'''
      return self.timeCounter
