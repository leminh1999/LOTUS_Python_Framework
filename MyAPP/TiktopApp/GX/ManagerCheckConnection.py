import platform
import os

INTERNET = 'google.com'
NAS_LOCAL = '192.168.68.143'

def ping(host:str):
  import subprocess
  param = '-n' if platform.system().lower()=='windows' else '-c'
  command = ['ping', param, '1', '-w', '1', host]
  return subprocess.call(command) == 0

if ping(NAS_LOCAL) == False or ping(INTERNET) == False:
  os.system("echo 'Thiết bị không có kết nối mạng' >> /root/checkConnectionLog.txt")
  #Restart lại máy tính
  os.system("reboot")