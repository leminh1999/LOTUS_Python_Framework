import __init
from time import sleep
from SystemManager.system_Wrap import *

def hamGoiKhiWDT_Timeout():
   print("Hàm này được gọi khi Watchdog timeout")
   
#############################
# Example 2                 #
#############################
# Create new threads
watchDog = SYS.thread_WDT(threadID = 1, name = "watchDog", timeThresSec = 30)
# Start new Threads
watchDog.start()
print("=====================")
sleep(5)
watchDog.pause()
print(watchDog.timeCounter) # Mong đợi counter là 25 (Tức 30 - 5)
sleep(5)
print(watchDog.timeCounter) # Mong đợi counter là 25 vì counter đã bị pause
watchDog.resume()
sleep(5)
watchDog.forceTimeout() # Force timeout => Hàm callbackFunc không được khai báo => Reboot lại (default)
print(watchDog.timeCounter) # Mong đợi counter là 20 vì chương trình bị force nhảy đến callback.