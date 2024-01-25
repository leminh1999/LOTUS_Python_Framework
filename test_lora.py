import time
from time import sleep
import serial
import threading
import os
 
class loraClass():
  def __init__(self,serPort='/dev/ttyS0',baudrate=9600):
    # os.system("sudo chmod 777 "+serPort)
    self.loraSer = serial.Serial(serPort,baudrate);sleep(0.1)
    self.loraSer.flush()
    self.rxQueue = []            #RX Data Queue
    self.rxRawBuffer = []        #RX Raw Buffer
    self.realtimeRxData = ""     #Realtime RX Data
    self.MAX_BUFFER_SIZE = 10    #Max size of rxRawBuffer
    self.curTxGroupId = 0        #Current TX Group ID
    self.rfRxCountDownSec = 1800 #Count down time for RF RX
    print("Start LORA RX thread...")
    threading.Thread(target=self.RX_Center).start()

  def defaultConf(self,RX_GID:str="0",TX_GID:str="1"):
    '''Default configuration for LoRa module'''
    self.selfConf("AT",waitRxModule="OK",retryNum=3,printLog=False)
    self.selfConf("AT+DEBUG=0",waitRxModule="OK",retryNum=3,printLog=False)
    self.selfConf("AT+FCU=0",waitRxModule="OK",retryNum=3,printLog=False)
    self.selfConf("AT+FCD=0",waitRxModule="OK",retryNum=3,printLog=False)
    self.selfConf("AT+FRE=921.400,921.400",retryNum=3,waitRxModule="OK",printLog=False)
    self.selfConf("AT+GROUPMOD="+TX_GID+","+RX_GID,waitRxModule="OK",retryNum=3,printLog=False)   # TX_GROUP:1 , RX_GROUP:0
    self.curTxGroupId = 1
    self.selfConf("AT+BW=2,2",waitRxModule="OK",retryNum=3,printLog=False)
    self.selfConf("AT+SF=7,7",waitRxModule="OK",retryNum=3,printLog=False)
    self.selfConf("AT+POWER=22",waitRxModule="OK",retryNum=3,printLog=False)
    self.selfConf("AT+CRC=1,1",waitRxModule="OK",retryNum=3,printLog=False)
    self.selfConf("AT+HEADER=0,0",waitRxModule="OK",retryNum=3,printLog=False)
    self.selfConf("AT+CR=1,1",waitRxModule="OK",retryNum=3,printLog=False)
    self.selfConf("AT+IQ=0,0",waitRxModule="OK",retryNum=3,printLog=False)
    self.selfConf("AT+PREAMBLE=8,8",waitRxModule="OK",retryNum=3,printLog=False)
    self.selfConf("AT+SYNCWORD=1",waitRxModule="OK",retryNum=3,printLog=False)
    self.selfConf("AT+RXMOD=65535,0",waitRxModule="OK",retryNum=3,printLog=False)
    self.selfConf("AT+RXDAFORM=0",waitRxModule="OK",retryNum=3,printLog=False)
    self.selfConf("AT+WAITTIME=1000",waitRxModule="OK",retryNum=3,printLog=False)
    self.selfConf("ATZ",waitRxModule="********",retryNum=3,printLog=False)

  #9. CleanUp
  def cleanUp (self):
    '''Clean up TX/RX buffer'''
    self.loraSer.flush()
    self.loraSer.read_all()
    self.rxQueue = []
    
  #################################################################
  # RECEIVE DATA                                                  #
  #################################################################
  def RX_Center(self):
    '''Receive data from LoRa module.
    + RX DATA will be added to rxQueue.
    + RX RAW DATA will be added to rxRawBuffer.'''
    #--- PRIVATE FUNCTION ---------
    def __addDataToRxRawBuffer(data:str=""):
      '''Add Raw RX data to rxRawBuffer'''
      self.rxRawBuffer.append(data)  # Thêm giá trị mới vào danh sách
      if len(self.rxRawBuffer) > self.MAX_BUFFER_SIZE:
          self.rxRawBuffer.pop(0)  # Loại bỏ giá trị đầu tiên nếu danh sách đã đủ 10 phần tử
    #------------------------------
    while (1):
      time.sleep(0.01)
      try:
        rx_data = str(self.loraSer.readline())
        self.realtimeRxData = rx_data
        # print(rx_data)
      except Exception as e:
        print(e)
        rx_data = ""
        continue
      #Convert binary to string
      rx_data = rx_data.split('b\'')[1].split('\'')[0]
      #remove \r\n
      rx_data = rx_data.replace('\\r','').replace('\\n','')
      
      #print if rx_data is not empty
      if rx_data != "":
        __addDataToRxRawBuffer(rx_data)
      if "Data: (HEX:)" in rx_data:
        #Convert HEX array to ASCII.
        rx_data = rx_data.split('HEX:)')[1].replace(' ','')
        if rx_data == "": return
        rx_channel = int(rx_data[0:2],16)
        if rx_data[-2:] == '0a':
          rx_data = rx_data[2:-2] #remove 0a and channel number
        else: 
          rx_data = rx_data[2:] #remove channel number (first 2 bytes)
        try:
          rx_data = bytes.fromhex(rx_data).decode('utf-8')
          rx_data = rx_data.rstrip()
          rx_dataJson = {"CH": rx_channel,"DATA": rx_data}
          self.rxQueue.append(rx_dataJson)
          self.rfRxCountDownSec = 1800 #reset count down from 30 minutes
        except Exception as e:
          continue
        pass

  #################################################################
  # TRANSMIT DATA                                                 #
  #################################################################
  def selfConf(self,command:str,waitRxModule="",retryNum=0,waitTimeMs=5000,printLog=True):
    '''Send configuration to LoRa module'''
    retryCnt = 0
    startTimeMs = time.time()*1000
    remainTimeMs = waitTimeMs*retryNum
    while retryCnt <= retryNum and remainTimeMs >= 0:
      self.loraSer.write((command+'\n\r').encode())
      if waitRxModule != "":
        sendStatus = self.waitForModule(waitRxModule,waitTimeMs)
        if sendStatus[0] == True: #Wait successfully
          return True #Return True if send successfully and wait successfully
        else:
          retryCnt += 1
      else:
        return True #If Not define Wait => return True
      remainTimeMs = waitTimeMs*retryNum - (time.time()*1000 - startTimeMs)
    return False
  
  def sendData(self,txGroupId:int=1,data:str="",retryNum=0,waitTimeMs=5000,needConvertDataToHex=True,printLog=True):
    '''Send data to WSN nodes'''
    retryCnt = 0
    while retryCnt <= retryNum:
      if needConvertDataToHex == True:
        converStringToHex = ''.join('{:02x}'.format(ord(c)) for c in data)
      else:
        converStringToHex = data
      sendData = "AT+SEND=0,"+str(converStringToHex)+",0,0"
      if self.selfConf(command=sendData,waitRxModule="txDone",retryNum=0,waitTimeMs=waitTimeMs,printLog=False) == True:
        return True
      else:
        retryCnt += 1

      
  #################################################################
  # WAIT DATA                                                     #
  #################################################################
  #4. Wait for a string from rxQueue in a certain time
  def waitForRxData(self,string,timeoutMs=1000):
    startTimeMs = time.time()*1000
    while (time.time()*1000 - startTimeMs < timeoutMs):
      if len(self.rxQueue) > 0:
        recData = str(self.rxQueue.pop(0)["DATA"])
        if string in recData:
          #return True and pop the string from rxQueue
          return True, recData
    return False, "Timeout"

  def waitForModule(self,string,timeoutMs=1000):
    startTimeMs = time.time()*1000
    self.realtimeRxData = ""
    while (time.time()*1000 - startTimeMs < timeoutMs):
      if string in self.realtimeRxData:
        #return True and pop the string from rxQueue
        return True,self.realtimeRxData
    return False, "Timeout"
  
  #################################################################
  # Other commands                                                #
  #################################################################
  #3. fetch a string from the rxQueue
  def fetch(self):
    if len(self.rxQueue) > 0:
      return self.rxQueue.pop(0)
    else:
      return ""
  
  #5. close the serial port
  def close(self):
    self.loraSer.close()
  
  #6. open the serial port
  def open(self):
    self.loraSer.open()
  
  #7. flush the serial port
  def flush(self):
    self.loraSer.flush()
  
  #8. flush the rxQueue
  def flushRxQueue(self):
    self.rxQueue = []
    

    

##################################################################################################
# CHÚ Ý 1: Cần mở UART5 trên board Pi4 trước khi chạy
# 1. Chạy lệnh sau: "sudo nano /boot/config.txt"
# 2. Xuống cuối file nhập dòng sau: "dtoverlay=uart5,txd5_pin=32,rxd5_pin=33"
# 3. Reboot lại thiết bị.
# 4. Sau khi khởi động lại. Chạy lệnh: "ls -l /dev/" sẽ thấy xuất hiện thêm 1 UART nữa là "ttyAMA1"
# CHÚ Ý 2: Cần tắt Console trên GUI trước. Vì nó sẽ dùng UART0.
##################################################################################################



LORA = loraClass(serPort='COM5',baudrate=9600)    ## LORA.defaultConf() 
LORA.cleanUp()

########### CONFIGURE1 LORA MODULE ############
# LORA.selfConf("AT",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+BW=0,0",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+SF=12,12",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+POWER=14",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+CRC=1,1",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+HEADER=0,0",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+CR=1,1",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+IQ=0,0",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+PREAMBLE=8,8",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+SYNCWORD=1",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+RXMOD=65535,0",waitRxModule="OK",retryNum=3,printLog=False)
# # LORA.selfConf("AT+RXDAFORM=0",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+WAITTIME=1000",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("ATZ",waitRxModule="********",retryNum=3,printLog=False)

########### CONFIGURE1 LORA MODULE ############
# LORA.selfConf("AT",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+BW=0,0",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+SF=12,12",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+POWER=22",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+CRC=1,1",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+HEADER=0,0",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+CR=1,1",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+IQ=0,0",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+PREAMBLE=8,8",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+SYNCWORD=1",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+RXMOD=65535,0",waitRxModule="OK",retryNum=3,printLog=False)
# # LORA.selfConf("AT+RXDAFORM=0",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("AT+WAITTIME=1000",waitRxModule="OK",retryNum=3,printLog=False)
# LORA.selfConf("ATZ",waitRxModule="********",retryNum=3,printLog=False)

while True:
  #Print time to format HH:MM:SS
  print(time.strftime("%H:%M:%S", time.localtime()))
  sendTime = time.strftime("%H%M%S", time.localtime())
  LORA.sendData(txGroupId=1,data=sendTime,needConvertDataToHex=False,printLog=True)
  # LORA.selfConf("AT+RECV=0",waitRxModule="OK",retryNum=3,printLog=False)
  # sleep(1)






