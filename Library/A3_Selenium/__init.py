import sys,os

workspacePath = os.path.dirname(os.path.abspath(__file__))
for i in range (0,10):
  if os.path.isfile(workspacePath+"/main.py"):
    workspacePath = os.path.abspath(workspacePath)
    sys.path.insert(0,workspacePath)
    string = "=== WORKSPACE PATH: "+workspacePath+ " ==="
    print("="*string.__len__())
    print(string)
    print("="*string.__len__()+"\n")
    sys.path.insert(0,workspacePath)
    os.chdir(workspacePath)
    break
  else:
    workspacePath += "/.."
    