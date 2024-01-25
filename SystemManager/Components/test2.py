import __init
import schedule
import time
from Conf.loggingSetup import *

# def job1():
#   logger.info("I'm working 1...")
#   time.sleep(20)

# def job2():
#   logger.info("I'm working 2...")
#   time.sleep(5)
  
# schedule.every(10).seconds.do(job1)
# schedule.every(11).seconds.do(job2)



# counter = 0
# while (1):
#   time.sleep(1)
#   counter+=1
#   print(counter)
#   schedule.run_pending()


class Test(object):
    def __del__(self):
        print("Object deleted")

    def func(self):
        print("Random function")


obj = Test()
obj.func()
del obj

# obj.func()
