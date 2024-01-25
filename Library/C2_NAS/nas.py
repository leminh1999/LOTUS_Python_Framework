import __init
from Conf.loggingSetup import *

class NAS_Wrapper:
  def __init__(self, nasLocalAddr:str = '192.168.68.143', nasLocalPort:int = 222 ,
                     nasDdnsAddr:str = "lotus1104.synology.me", nasDdnsPort:int = 14322 ,
                     nasAccount:str = 'meomay22', nasSshKeyPath:str = 'C:/Users/tran.dung.CMEV/.ssh/id_rsa'):
    def __ping(host:str):
      import subprocess
      param = '-n' if platform.system().lower()=='windows' else '-c'
      command = ['ping', param, '1', '-w', '1', host]
      return subprocess.call(command) == 0
    ##### MAIN #####
    self.nasLocalAddr  = nasLocalAddr
    self.nasLocalPort  = nasLocalPort
    self.nasDdnsAddr   = nasDdnsAddr
    self.nasDdnsPort   = nasDdnsPort
    self.nasAccount    = nasAccount
    self.nasSshKeyPath = nasSshKeyPath
    self.nasAddr = ""
    self.nasPort = ""
    #Kiểm tra xem NAS Local có hoạt động không?
    if self.nasLocalAddr != "" and self.nasAddr == "":
      if __ping(nasLocalAddr) == True:
        self.nasAddr = self.nasLocalAddr
        self.nasPort = self.nasLocalPort
    if self.nasDdnsAddr != "" and self.nasAddr == "":
      self.nasAddr = self.nasDdnsAddr
      self.nasPort = self.nasDdnsPort
    
  def cmdExecNoWait(self,scriptCommand:str):
    '''Chạy script trên NAS, không đợi kết quả. Lệnh bên dưới có thể chạy ngay (Có thể chạy python3 script.py, shell script, ...)
    Ex1: NAS.cmdExecNoWait("echo START;sleep 5; echo a > abc.txt;echo DONE1")
    Ex2: NAS.cmdExecNoWait("python3 Script/Biz/script.py")
    Ex3: NAS.cmdExecNoWait("sh Script/Biz/script.sh")
    '''
    import subprocess
    command = ['ssh', '-p', str(self.nasPort), '-i',self.nasSshKeyPath, self.nasAccount + '@' + self.nasAddr, scriptCommand]
    subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

  def cmdExecWait(self,scriptCommand:str):
    '''Chạy script trên NAS có đợi kết quả mới thực thi lệnh tiếp theo bên dưới (Có thể chạy python3 script.py, shell script, ...)
    Ex1: NAS.cmdExecWait("echo START;sleep 5; echo a > abc.txt;echo DONE1")
    Ex2: NAS.cmdExecWait("python3 Script/Biz/script.py")
    Ex3: NAS.cmdExecWait("sh Script/Biz/script.sh")
    '''
    import subprocess
    command = ['ssh', '-p', str(self.nasPort), '-i',self.nasSshKeyPath, self.nasAccount + '@' + self.nasAddr, scriptCommand]
    subprocess.call(command)
    
  def testConnection(self):
    '''
    Kiểm tra kết nối SSH đến NAS'''
    import subprocess
    command = ['ssh', '-p', str(self.nasPort), '-i',self.nasSshKeyPath, self.nasAccount + '@' + self.nasAddr, 'echo "Test Connection"']
    # subprocess.call(command)
    if subprocess.call(command)==0:
      logger.info("SSH Connection OK")
    else:
      logger.error("SSH Connection Failed")
    
######## TEST ######################################################
# NAS = NAS_Wrapper()
# NAS.cmdExecNoWait("echo START;sleep 5; echo a > abc.txt;echo DONE1")
# print("DONE1")
# NAS.testConnection()
# print("DONE2")

