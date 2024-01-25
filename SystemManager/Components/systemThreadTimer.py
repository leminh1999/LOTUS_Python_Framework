import __init
from time import sleep
import time
from Conf.loggingSetup import *
import threading
import datetime
from enum import Enum

class timerCallbackMode (Enum):
   CALLBACK_THEN_REPEAT = 1
   CALLBACK_WHILE_REPEAT = 2
   
class timerRepeateMode (Enum):
   NO_REPEAT = 1
   REPEAT_SEVERAL_TIMES = 2
   REPEAT_FOREVER = 3

class threadTimer (threading.Thread):
   '''
   - `Name`: threadTimer
   - `Function`: Tạo ra một Thread timer đếm ngược thời gian. Khi Timeout thì chạy callbackFunc
   - `Parameter`:
      - `threadID`: Số ID của thread.
      - `name`: Tên gợi nhớ chức năng của thread. Đặt tùy ý.
      - `timeThresSec`: Cài đặt thời gian đếm ngược.
      - `callbackFunc`: Hàm callback khi Timeout.
      - `class_timerRepeateMode`:\\
         . `NO_REPEAT`: Không lặp lại.\\
         . `REPEAT_SEVERAL_TIMES`: Lặp lại với số lần lặp lại.\\
         . `REPEAT_FOREVER`: Lặp lại vô tận.
      - `class_timerCallbackMode`: Cài đặt chế độ chạy callbackFunc.\\
         . `CALLBACK_THEN_REPEAT`: Chạy hàm callback xong rồi mới repeat.\\
         . `CALLBACK_WHILE_REPEAT`: Chạy hàm callback và repeat timer đồng thời.\\
   - `Return`: None
   - `EX`:
      1. Timer = threadTimer(threadID = 1, name = "Timer", timeThresSec = 20, callbackFunc = hamGoiKhiTimer_Timeout, class_timerRepeateMode = timerRepeateMode.REPEAT_SEVERAL_TIMES, repeatTime= 1, class_timerCallbackMode = timerCallbackMode.CALLBACK_THEN_REPEAT)\\
      2. Timer.start()
   '''
   def __init__(self, threadID, name, timeThresSec, callbackFunc, class_timerRepeateMode = timerRepeateMode.NO_REPEAT, repeatTime = 0, class_timerCallbackMode = timerCallbackMode.CALLBACK_THEN_REPEAT):
      threading.Thread.__init__(self)
      self.threadID = threadID
      '''Số ID của thread'''
      
      self.name = name
      '''Tên gợi nhớ chức năng của thread. Đặt tùy ý.'''
      
      self.timeThresSec = timeThresSec
      '''Cài đặt thời gian đếm ngược.'''
      
      self.remainCounterSec = timeThresSec
      
      self.callbackTimer = callbackFunc
      '''Hàm callback khi Timeout.'''
      
      self.repeatMode = class_timerRepeateMode
      '''Cài đặt chế độ lặp lại:
         - `NO_REPEAT`: Không lặp lại.
         - `REPEAT_SEVERAL_TIMES`: Lặp lại với số lần lặp lại.
         - `REPEAT_FOREVER`: Lặp lại vô tận.'''
      
      self.repeatTime = repeatTime
      '''Cấu hình số lần repeat'''
      
      self.repeatCounter = 0
      '''Biến đếm số lần lặp lại'''
      
      self.pauseFlag = False
      '''Cờ báo tạm dừng Timer'''
      
      self.stopFlag = False
      '''Cờ báo dừng timer'''
      
      self.forceTimeoutFlag = False
      '''Cờ ép tràn timer'''
      
      self.startTimerMark = 0
      '''Đánh dấu mốc thời điểm bắt đầu timer'''
      
      self.pauseTimerMark = 0
      '''Đánh dấu mốc thời điểm bị dừng'''
      
      self.pauseDuration = 0
      '''Tổng thời gian dừng của Timer.'''
      
      self.callbackMode = class_timerCallbackMode
      '''Cài đặt chế chạy của callbackFunc timer có repeat:
         - `CALLBACK_THEN_REPEAT`: Chạy hàm callback xong rồi mới repeat.
         - `CALLBACK_WHILE_REPEAT`: Chạy hàm callback và repeat timer đồng thời.'''
      
   def run(self): #Bắt buộc phải có tên là run()
      # Re-initialize the timer counter and other flags
      self.startTimerMark = datetime.datetime.now()
      self.pauseTimerMark = 0
      self.remainCounterSec = self.timeThresSec
      self.pauseFlag = False
      self.stopFlag = False
      self.forceTimeoutFlag = False
      self.pauseDuration = 0
      # Start timer
      logger.info (">>>> Starting " + self.name +" <<<<")
      
      runLoop = True
      while runLoop == True:
         while (datetime.datetime.now() - self.startTimerMark).seconds < self.timeThresSec + self.pauseDuration:
            self.remainCounterSec = self.timeThresSec - (datetime.datetime.now() - self.startTimerMark).seconds + self.pauseDuration
            while self.pauseFlag == True: 
               if self.stopFlag == True or self.forceTimeoutFlag == True:
                  break
            if self.stopFlag == True: return    # Stop the loop if stopped
            if self.forceTimeoutFlag == True: break # Force timeout
            
         ########################
         ###   TIMER ACTION   ###
         ########################
         if self.callbackMode == timerCallbackMode.CALLBACK_THEN_REPEAT:
            logger.info(">>>> TIMER(" + self.name +") TIMEOUT => CALLBACK FUNCTION <<<<")
            self.callbackTimer()
         
         self.startTimerMark = datetime.datetime.now()
         self.remainCounterSec = self.timeThresSec
         self.forceTimeoutFlag = False
         
         if self.callbackMode == timerCallbackMode.CALLBACK_WHILE_REPEAT:
            logger.info(">>>> TIMER(" + self.name +") TIMEOUT => CALLBACK FUNCTION <<<<")
            self.callbackTimer()
         
         ###########################
         ###   REPEAT CHECKING   ###
         ###########################
         if self.repeatMode == timerRepeateMode.NO_REPEAT:
            runLoop = False
            break
         if self.repeatMode == timerRepeateMode.REPEAT_SEVERAL_TIMES:
            if self.repeatCounter < self.repeatTime:
               self.repeatCounter += 1
               self.pauseDuration = 0
               runLoop = True
            else:
               runLoop = False
               break
         if self.repeatMode == timerRepeateMode.REPEAT_FOREVER:
            self.pauseDuration = 0
            continue

   def pause(self):
      '''Tạm dừng Timer'''
      self.pauseFlag = True
      self.pauseTimerMark = datetime.datetime.now()
      logger.info(">>>> TIMER(" + self.name +") PAUSED <<<<")
      
   def resume(self):
      '''Tiếp tục chạy Timer'''
      self.pauseFlag = False
      self.pauseDuration += (datetime.datetime.now() - self.pauseTimerMark).seconds
      logger.info(">>>> TIMER(" + self.name +") RESUMED <<<<")
      
   def stop(self):
      '''Dừng Timer'''
      self.stopFlag = True
      logger.info(">>>> TIMER(" + self.name +") STOPPED <<<<")
      
   def forceTimeout(self):
      '''Ép Timer timeout và chạy callback'''
      self.forceTimeoutFlag = True
      logger.info(">>>> TIMER(" + self.name +") FORCE TO TIMEOUT <<<<")
         
   def getTimeCounter(self):
      '''Lấy thời gian counter còn lại của Timer'''
      return self.remainCounterSec
