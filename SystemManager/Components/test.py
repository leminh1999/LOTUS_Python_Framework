import datetime
import time



time_1 = datetime.datetime.now()
time.sleep(2)
time_2 = datetime.datetime.now()
delta_time = time_2 - time_1

print(delta_time)
print(delta_time.seconds)


class aaa ():
  a = 1
  b = 2
  c = 3
  
  
bbb = aaa.a

print(bbb)
