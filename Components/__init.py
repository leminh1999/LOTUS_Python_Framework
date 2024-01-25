import sys,os
curPath = os.path.dirname(os.path.abspath(__file__))

#check exist file
if os.path.isfile(curPath+"/main.py"):
  # print("==== SYSTEM TEST ====")
  workspacePath = curPath #Về thư mục gốc
  # print(workspacePath)
  sys.path.insert(0,workspacePath)
else:
  # print("==== UNIT TEST ====")
  workspacePath = curPath+"/../../../" #Về thư mục gốc
  # print(workspacePath)
  sys.path.insert(0,workspacePath)