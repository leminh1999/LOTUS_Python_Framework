import __init
from Conf.loggingSetup import *
from Library.C2_NAS.nas import NAS_Wrapper
import time

    
######## TEST ######################################################
NAS  = NAS_Wrapper()
print("#### 1. TEST CONNECTION ####")
NAS.testConnection()

print("#### 2. Execute command on NAS - WITH WAIT ####")
NAS.cmdExecWait("echo START;sleep 5; echo a > abc.txt;echo DONE1")

print("#### 3. Execute command on NAS - NO WAIT ####")
NAS.cmdExecNoWait("echo START;sleep 5; echo a > abc.txt;echo DONE1")

for i in range(10):
  #print out number of wait seconds
  print("System's free in " + str(i)+ " seconds")
  time.sleep(1)
  
print("#### FINISHED ####")