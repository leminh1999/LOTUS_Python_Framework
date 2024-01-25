import __init
from time import sleep
from SystemManager.system_Wrap import *

def hamGoiKhiTimer_Timeout():
   print("Hàm này được gọi khi Timer timeout. Delay 3s trong hàm này")
   sleep(3)
   
#############################
# Example 1                 #
#############################
# Create new threads
Timer = SYS.thread_Timer(threadID = 1, name = "Timer", timeThresSec = 30, callbackFunc = hamGoiKhiTimer_Timeout, class_timerRepeateMode = timerRepeateMode.REPEAT_SEVERAL_TIMES, repeatTime= 1, class_timerCallbackMode = timerCallbackMode.CALLBACK_THEN_REPEAT)
# Start new Threads
Timer.start()
print("=====================")
sleep(5)
Timer.pause()
print(Timer.remainCounterSec) # Mong đợi counter là 25 (Tức 30 - 5)
sleep(5)
print(Timer.remainCounterSec) # Mong đợi counter là 25 vì counter đã bị pause
Timer.resume()
sleep(5)
Timer.forceTimeout() # Force timeout => Gọi hàm callbackFunc
print(Timer.remainCounterSec) # Mong đợi counter là 20 vì chương trình bị force nhảy đến callback.

### Kết quả: PIC/Timer_EX1.png ###