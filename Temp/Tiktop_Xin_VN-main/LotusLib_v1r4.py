# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import time
from Global.loggingSetup import *
import pyautogui
import pyperclip
import keyboard  # using module keyboard

GUI = pyautogui
taskKillerEndFlag = False
click = GUI.click
doubleClick = GUI.doubleClick
mousePos = GUI.moveTo
keys = GUI.typewrite  #Ex: pyautogui.typewrite(['a', 'b', 'left', 'left', 'X', 'Y'])
press = GUI.press

def rgb(red, green, blue): return (red,green,blue)

def delay(time_ms): return time.sleep(time_ms/1000)

def copyToClipboard(data): pyperclip.copy(data)
def pasteFromClipboard(): GUI.hotkey('ctrl','v')
def pasteFromClipboardToVar(): return pyperclip.paste() 

####################################################################
import threading
#Configure for Task Killer
class TaskKiller (threading.Thread):
  def __init__(self, threadID, name,logPathAndPrefixName='./',pythonKillHotkey = 'shift+f12',vscodeKillHotkey = 'shift+f5'):
     threading.Thread.__init__(self)
     self.threadID = threadID
     self.name = name
     self.logPathAndPrefixName = logPathAndPrefixName
     self.pythonKillHotkey = pythonKillHotkey
     self.vscodeKillHotkey = vscodeKillHotkey
  def run(self):
    logger.info("\n===== USER CAN PRESS SHIFT+F5 OR SHIFT+F12 TO STOP =====\n")
    LotusLib.programTerminateConf(self.logPathAndPrefixName,self.pythonKillHotkey,self.vscodeKillHotkey)
####################################################################

class LotusLib ():
  #####################################################
  # Name: waitImage
  # Function: Đợi hình ảnh xuất hiện
  # Parameter:
  #   + image: đường dẫn đến file ảnh
  #   + timeout_sec: thời gian time out. Mặc định 15 giây
  #   + delayFinish_ms: thời gian delay sau khi hoàn thành
  # Return: Trả về thông số vị trí giữa tấm ảnh.
  #         Có thể kết hợp như sau:
  #         GUI.click(waitImage(....))
  # Ex: waitImage('iconFirefox.png',90)
  #####################################################
  def waitImage(image,timeout_sec=15,delayFinish_ms=100):
    logger.debug('Subtask: waitImage(image=%s,timeout_sec=%s)',str(image),str(timeout_sec))
    pos =0
    pos1=0
    pos2=0
    pos3=0
    pos4=0
    timeCnt = time.time();
    while (time.time() - timeCnt) < timeout_sec : #Chưa hết thời gian time out
      pos = GUI.locateOnScreen(image)
      if pos != None:
        pos1,pos2,pos3,pos4 = pos
        logger.debug('  Image Found')
        LotusLib.delay(delayFinish_ms)
        return round(pos1+pos3/2),round(pos2+pos4/2)
    logger.error('  Image NOT Found!!!')
    LotusLib.delay(delayFinish_ms)
    return False
  
  #####################################################
  # Name: clickImage
  # Function: Đợi hình ảnh xuất hiện và click vào nó
  # Parameter:
  #   + image: đường dẫn đến file ảnh
  #   + timeout: thời gian time out. Mặc định 15 giây
  #   + delayFinish_ms: thời gian delay sau khi hoàn thành
  # Return: Trả về True nếu có hình và click.
  #         Trả về False nếu không có hình.
  # EX: clickImage('iconChat.png',20)
  #####################################################
  def clickImage(image,timeout=15,delayFinish_ms=100):
    logger.debug('Subtask: clickImage(image=%s,timeout=%s)',str(image),str(timeout))
    pos = LotusLib.waitImage(image,timeout)
    if pos != None:
      logger.debug('  Click vào image tại vị trí: %s',str(pos))
      GUI.click(pos)
      LotusLib.delay(delayFinish_ms)
      return True
    logger.error('  Image NOT Found!!!')
    LotusLib.delay(delayFinish_ms)
    return False
  
  #####################################################
  # Name: getColor
  # Function: kiểm tra màu tại 1 vị trí nào đó
  # Parameter:
  #   + pos: Vị trí quan sát màu. pos là một list gồm 2 gía trị X,Y
  # Return: Trả về màu của điểm ảnh.
  #####################################################
  def getColor(posX,posY):
    # logger.debug('Subtask: getColor(posX=%d,posY=%d)',posX,posY)
    color = GUI.screenshot().getpixel((posX,posY))
    # logger.debug('  Màu đọc được: %s',str(color))
    return color
  
  #####################################################
  # Name: checkColorWithCapture
  # Function: kiểm tra màu tại 1 điểm sau khi chụp ảnh màn hình
  # Parameter:
  #   + pos: Vị trí quan sát màu. pos là một list gồm 2 gía trị X,Y
  #   + color: Giá trị màu mong đợi. color là một list gồm 3 gía trị R,G,B
  #   + delta: khoảng sai số chấp nhận được so với giá trị gốc.
  #   + delayFinish_ms: thời gian delay sau khi hoàn thành
  # Return: - Trả về True nếu điều kiện đúng.
  #         - Trả về False nếu điều kiện sai.
  #####################################################
  def checkColorWithCapture(pos,colorRGB,delta=20,delayFinish_ms=100):
    # logger.debug('Subtask: checkColorWithCapture(pos=%s,colorRGB=%s,delta=%s)',str(pos),str(colorRGB),str(delta))
    red=None
    green=None
    blue=None
    lowerThresRed   = None
    upperThresRed   = None
    lowerThresGreen = None
    upperThresGreen = None
    lowerThresBlue  = None
    upperThresBlue  = None
  
    red,green,blue = GUI.screenshot().getpixel((pos[0],pos[1]))
    lowerThresRed = 0 if(red <= delta) else red - delta
    lowerThresGreen = 0 if(green <= delta) else green - delta
    lowerThresBlue = 0 if(blue <= delta) else blue - delta
    upperThresRed = 255 if((red + delta)>=255) else red + delta
    upperThresGreen = 255 if((green + delta)>=255) else green + delta
    upperThresBlue = 255 if((blue + delta)>=255) else blue + delta
    if (lowerThresRed<= colorRGB[0] <= upperThresRed)\
      and(lowerThresGreen<= colorRGB[1] <= upperThresGreen)\
      and(lowerThresBlue<= colorRGB[2] <= upperThresBlue):
      logger.debug('Màu kiểm tra nằm trong kỳ vọng. Giá trị màu đọc đưọc RGB: %d,%d,%d',red,green,blue)
      LotusLib.delay(delayFinish_ms)
      return True
    # logger.warning('Màu kiểm tra KHÔNG nằm trong kỳ vọng!!! Giá trị màu đọc đưọc RGB: %d,%d,%d',red,green,blue)
    LotusLib.delay(delayFinish_ms)
    return False
  
  #####################################################
  # Name: checkColorWithoutCapture
  # Function: kiểm tra màu tại 1 điểm dựa vào tấm ảnh đã có
  # Parameter:
  #   + image: tấm hình được chụp với lệnh GUI.screenshot()
  #   + pos: Vị trí quan sát màu. pos là một list gồm 2 gía trị X,Y
  #   + color: Giá trị màu mong đợi. color là một list gồm 3 gía trị R,G,B
  #   + delta: khoảng sai số chấp nhận được so với giá trị gốc.
  #   + delayFinish_ms: thời gian delay sau khi hoàn thành
  # Return: - Trả về True nếu điều kiện đúng.
  #         - Trả về False nếu điều kiện sai.
  #####################################################
  def checkColorWithoutCapture(image,pos,colorRGB,delta=20,delayFinish_ms=100):
    # logger.debug('Subtask: checkColorWithCapture(image=%s,pos=%s,colorRGB=%s,delta=%s)',str(image),str(pos),str(colorRGB),str(delta))
  
    red=None
    green=None
    blue=None
    lowerThresRed   = None
    upperThresRed   = None
    lowerThresGreen = None
    upperThresGreen = None
    lowerThresBlue  = None
    upperThresBlue  = None
  
    red,green,blue = image.getpixel((pos[0],pos[1]))
    lowerThresRed = 0 if(red <= delta) else red - delta
    lowerThresGreen = 0 if(green <= delta) else green - delta
    lowerThresBlue = 0 if(blue <= delta) else blue - delta
    upperThresRed = 255 if((red + delta)>=255) else red + delta
    upperThresGreen = 255 if((green + delta)>=255) else green + delta
    upperThresBlue = 255 if((blue + delta)>=255) else blue + delta
    if (lowerThresRed<= colorRGB[0] <= upperThresRed)\
      and(lowerThresGreen<= colorRGB[1] <= upperThresGreen)\
      and(lowerThresBlue<= colorRGB[2] <= upperThresBlue):
      logger.debug('Màu kiểm tra nằm trong kỳ vọng. Giá trị màu đọc đưọc RGB: %d,%d,%d',red,green,blue)
      LotusLib.delay(delayFinish_ms)
      return True
    # logger.warning('Màu kiểm tra KHÔNG nằm trong kỳ vọng!!! Giá trị màu đọc đưọc RGB: %d,%d,%d',red,green,blue)
    LotusLib.delay(delayFinish_ms)
    return False
  
  #####################################################
  # Name: waitColor
  # Function: Đợi màu tại 1 vị trí nào đó
  # Parameter:
  #   + pos: Vị trí quan sát màu. pos là một list gồm 2 gía trị X,Y
  #   + color: Giá trị màu mong đợi. color là một list gồm 3 gía trị R,G,B
  #   + delta: khoảng sai số chấp nhận được so với giá trị màu gốc.
  #   + timeout: thời gian time out. Mặc định 15 giây
  #   + delayFinish_ms: thời gian delay sau khi hoàn thành
  # Return: Trả về màu của điểm ảnh. Khi nó nằm trong delta.
  #####################################################
  def waitColor(pos,colorRGB,delta=20,timeout=15,delayFinish_ms=100):
    # logger.debug('Subtask: waitColor(pos=%s,colorRGB=%s,delta=%s,timeout=%s)',str(pos),str(colorRGB),str(delta),str(timeout))
    red=None
    green=None
    blue=None
    lowerThresRed   = None
    upperThresRed   = None
    lowerThresGreen = None
    upperThresGreen = None
    lowerThresBlue  = None
    upperThresBlue  = None  
    timeCnt = time.time();
    while (time.time() - timeCnt) < timeout : #Chưa hết thời gian time out
      red, green, blue = GUI.screenshot().getpixel((pos[0],pos[1]))
      lowerThresRed = 0 if(red <= delta) else red - delta
      lowerThresGreen = 0 if(green <= delta) else green - delta
      lowerThresBlue = 0 if(blue <= delta) else blue - delta
      upperThresRed = 255 if((red + delta)>=255) else red + delta
      upperThresGreen = 255 if((green + delta)>=255) else green + delta
      upperThresBlue = 255 if((blue + delta)>=255) else blue + delta
      if (lowerThresRed<= colorRGB[0] <= upperThresRed)\
        and(lowerThresGreen<= colorRGB[1] <= upperThresGreen)\
        and(lowerThresBlue<= colorRGB[2] <= upperThresBlue):
        # logger.debug('  Đã đợi được màu mong muốn. Giá trị màu đọc đưọc RGB: %d,%d,%d',red,green,blue)
        LotusLib.delay(delayFinish_ms)
        return red,green,blue
    logger.error('  TIMEOUT!!! KHÔNG đợi được màu mong muốn '+str(colorRGB)+' tại Pos = '+str(pos)+'.')
    LotusLib.delay(delayFinish_ms)
    return False
  
  #####################################################
  # Name: waitNotColor
  # Function: Đợi màu tại 1 vị trí nào đó khác với màu cung cấp
  # Parameter:
  #   + pos: Vị trí quan sát màu. pos là một list gồm 2 gía trị X,Y
  #   + color: Giá trị màu KHONG mong đợi. color là một list gồm 3 gía trị R,G,B
  #   + delta: khoảng sai số chấp nhận được so với giá trị gốc.
  #   + timeout: thời gian time out. Mặc định 15 giây
  #   + delayFinish_ms: thời gian delay sau khi hoàn thành
  # Return: Trả về màu của điểm ảnh. Khi nó nằm ngoai delta.
  #####################################################
  def waitNotColor(pos,colorRGB,delta=20,timeout=15,delayFinish_ms=100):
    # logger.debug('Subtask: waitNotColor(pos=%s,colorRGB=%s,delta=%s,timeout=%s)',str(pos),str(colorRGB),str(delta),str(timeout))
    red=None
    green=None
    blue=None
    lowerThresRed   = None
    upperThresRed   = None
    lowerThresGreen = None
    upperThresGreen = None
    lowerThresBlue  = None
    upperThresBlue  = None
    timeCnt = time.time();
    while (time.time() - timeCnt) < timeout : #Chưa hết thời gian time out
      red, green, blue = GUI.screenshot().getpixel((pos[0],pos[1]))
      lowerThresRed = 0 if(red <= delta) else red - delta
      lowerThresGreen = 0 if(green <= delta) else green - delta
      lowerThresBlue = 0 if(blue <= delta) else blue - delta
      upperThresRed = 255 if((red + delta)>=255) else red + delta
      upperThresGreen = 255 if((green + delta)>=255) else green + delta
      upperThresBlue = 255 if((blue + delta)>=255) else blue + delta
      if (lowerThresRed<= colorRGB[0] <= upperThresRed)\
        and(lowerThresGreen<= colorRGB[1] <= upperThresGreen)\
        and(lowerThresBlue<= colorRGB[2] <= upperThresBlue):
        pass
      else:
        logger.debug('  waitNOTcolor thành công. Giá trị màu đọc đưọc RGB: %d,%d,%d',red,green,blue)
        LotusLib.delay(delayFinish_ms)
        return red,green,blue
    logger.error('  TIMEOUT!!! Màu sắc '+str(colorRGB)+'tại Pos = '+str(pos)+' không thay đổi!!!')
    LotusLib.delay(delayFinish_ms)
    return False
  
  #####################################################
  # Name: wait3Color
  # Function: Đợi màu tại 3 vị trí nào đó
  # Parameter:
  #   + pos[1..3]: Vị trí quan sát màu. pos là một list gồm 2 gía trị X,Y
  #   + color[1..3]: Giá trị màu mong đợi. color là một list gồm 3 gía trị R,G,B
  #   + delta[1..3]: khoảng sai số chấp nhận được so với giá trị màu gốc.
  #   + timeout: thời gian time out. Mặc định 15 giây
  #   + delayFinish_ms: thời gian delay sau khi hoàn thành
  # Return: + Trả về 1 nếu cả 3 màu tồn tại trong khoảng timeout.
  #         + Trả về None nếu đã hết thời
  # EX:
  #       wait3Color([ 27, 48],[238, 79, 48],20,\
  #                  [727,126],[238, 77, 45],20,\
  #                  [396,217],[ 73,203,221],20,20)
  #####################################################
  def wait3Color(pos1,color1,delta1,\
                 pos2,color2,delta2,\
                 pos3,color3,delta3,\
                 timeout=15,delayFinish_ms=100):
    logger.debug('Subtask: wait3Color(pos1=%s,color1=%s,delta1=%s,pos2=%s,color2=%s,delta2=%s,pos3=%s,color3=%s,delta3=%s,timeout=%s)',str(pos1),str(color1),str(delta1),str(pos2),str(color2),str(delta2),str(pos3),str(color3),str(delta3),str(timeout))
    timeCnt = time.time()
    spendTime = 0
    if LotusLib.waitColor(pos1,color1,delta1,timeout,delayFinish_ms=0) == 0:
      logger.error('TIMEOUT!!! và màu tại vị trí 1 không khớp')
      LotusLib.delay(delayFinish_ms)
      return False
    spendTime = time.time() - timeCnt
    remainTime = 0 if spendTime >= timeout else timeout - spendTime
    timeCnt = time.time();
    if LotusLib.waitColor(pos2,color2,delta2,remainTime,delayFinish_ms=0) == 0:
      logger.error('TIMEOUT!!! và màu tại vị trí 2 không khớp')
      LotusLib.delay(delayFinish_ms)
      return False
    spendTime = time.time() - timeCnt
    remainTime = 0 if spendTime >= remainTime else remainTime - spendTime
    if LotusLib.waitColor(pos3,color3,delta3,remainTime,delayFinish_ms=0) == 0:
      logger.error('TIMEOUT!!! và màu tại vị trí 3 không khớp')
      LotusLib.delay(delayFinish_ms)
      return False
    logger.debug('Đã tìm thấy màu trùng khớp tại 3 vị trí mong ước')
    LotusLib.delay(delayFinish_ms)
    return True
  #####################################################
  # Name: wait3NotColor
  # Function: Đợi màu tại 3 vị trí nào đó. Nếu có bất kỳ sự thay đổi tại 1 trong 3 điểm sẽ thoát
  # Parameter:
  #   + pos[1..3]: Vị trí quan sát màu. pos là một list gồm 2 gía trị X,Y
  #   + colorRGB[1..3]: Giá trị màu mong đợi. color là một list gồm 3 gía trị R,G,B
  #   + delta[1..3]: khoảng sai số chấp nhận được so với giá trị gốc.
  #   + timeout: thời gian time out. Mặc định 15 giây
  #   + delayFinish_ms: thời gian delay sau khi hoàn thành
  # Return: + Trả về 1 nếu vị trí 1 có sự thay đổi màu trong khoảng timeout
  #         + Trả về 2 nếu vị trí 2 có sự thay đổi màu trong khoảng timeout
  #         + Trả về 3 nếu vị trí 3 có sự thay đổi màu trong khoảng timeout
  #         + Trả về 0 nếu đã hết thời gian timeout và không có sự thay đổi màu
  # EX:
  #       wait3NotColor([ 27, 48],[238, 79, 48],20,\
  #                     [727,126],[238, 77, 45],20,\
  #                     [396,217],[ 73,203,221],20,20)
  #####################################################
  def wait3NotColor(pos1,colorRGB1,delta1,\
                    pos2,colorRGB2,delta2,\
                    pos3,colorRGB3,delta3,\
                    timeout=15,delayFinish_ms=100):
    logger.debug('Subtask: wait3NotColor(pos1=%s,colorRGB1=%s,delta1=%s,pos2=%s,colorRGB2=%s,delta2=%s,pos3=%s,colorRGB3=%s,delta3=%s,timeout=%s)',str(pos1),str(colorRGB1),str(delta1),str(pos2),str(colorRGB2),str(delta2),str(pos3),str(colorRGB3),str(delta3),str(timeout))
    # Monitoring point 1
    red1=None
    green1=None
    blue1=None
    lowerThresRed1   = None
    upperThresRed1   = None
    lowerThresGreen1 = None
    upperThresGreen1 = None
    lowerThresBlue1  = None
    upperThresBlue1  = None
    # Monitoring point 2
    red2=None
    green2=None
    blue2=None
    lowerThresRed2   = None
    upperThresRed2   = None
    lowerThresGreen2 = None
    upperThresGreen2 = None
    lowerThresBlue2  = None
    upperThresBlue2  = None
    # Monitoring point 3
    red3=None
    green3=None
    blue3=None
    lowerThresRed3   = None
    upperThresRed3   = None
    lowerThresGreen3 = None
    upperThresGreen3 = None
    lowerThresBlue3  = None
    upperThresBlue3  = None
    
    timeCnt = time.time()
    while (time.time() - timeCnt) < timeout : #Chưa hết thời gian time out
      #Cập nhật thông số màu điểm quan sát 1
      red1, green1, blue1 = GUI.screenshot().getpixel((pos1[0],pos1[1]))
      lowerThresRed1 = 0 if(red1 <= delta1) else red1 - delta1
      lowerThresGreen1 = 0 if(green1 <= delta1) else green1 - delta1
      lowerThresBlue1 = 0 if(blue1 <= delta1) else blue1 - delta1
      upperThresRed1 = 255 if((red1 + delta1)>=255) else red1 + delta1
      upperThresGreen1 = 255 if((green1 + delta1)>=255) else green1 + delta1
      upperThresBlue1 = 255 if((blue1 + delta1)>=255) else blue1 + delta1
      #Cập nhật thông số màu điểm quan sát 2
      red2, green2, blue2 = GUI.screenshot().getpixel((pos2[0],pos2[1]))
      lowerThresRed2 = 0 if(red2 <= delta2) else red2 - delta2
      lowerThresGreen2 = 0 if(green2 <= delta2) else green2 - delta2
      lowerThresBlue2 = 0 if(blue2 <= delta2) else blue2 - delta2
      upperThresRed2 = 255 if((red2 + delta2)>=255) else red2 + delta2
      upperThresGreen2 = 255 if((green2 + delta2)>=255) else green2 + delta2
      upperThresBlue2 = 255 if((blue2 + delta2)>=255) else blue2 + delta2
      #Cập nhật thông số màu điểm quan sát 3
      red3, green3, blue3 = GUI.screenshot().getpixel((pos3[0],pos3[1]))
      lowerThresRed3 = 0 if(red3 <= delta3) else red3 - delta3
      lowerThresGreen3 = 0 if(green3 <= delta3) else green3 - delta3
      lowerThresBlue3 = 0 if(blue3 <= delta3) else blue3 - delta3
      upperThresRed3 = 255 if((red3 + delta3)>=255) else red3 + delta3
      upperThresGreen3 = 255 if((green3 + delta3)>=255) else green3 + delta3
      upperThresBlue3 = 255 if((blue3 + delta3)>=255) else blue3 + delta3
      
      #Kiểm tra sự biến đổi màu
      if   (lowerThresRed1   <= colorRGB1[0] <= upperThresRed1  )\
        and(lowerThresGreen1 <= colorRGB1[1] <= upperThresGreen1)\
        and(lowerThresBlue1  <= colorRGB1[2] <= upperThresBlue1 ):
        pass
      else:
        logger.debug('  Đã đợi được màu KHÔNG mong muốn tại vị trí 1. Giá trị màu đọc đưọc RGB1: %d,%d,%d',red1,green1,blue1)
        LotusLib.delay(delayFinish_ms)
        return 1
      if   (lowerThresRed2   <= colorRGB2[0] <= upperThresRed2  )\
        and(lowerThresGreen2 <= colorRGB2[1] <= upperThresGreen2)\
        and(lowerThresBlue2  <= colorRGB2[2] <= upperThresBlue2 ):
        pass
      else:
        logger.debug('  Đã đợi được màu KHÔNG mong muốn tại vị trí 2. Giá trị màu đọc đưọc RGB2: %d,%d,%d',red2,green2,blue2)
        LotusLib.delay(delayFinish_ms)
        return 2
      if   (lowerThresRed3   <= colorRGB3[0] <= upperThresRed3  )\
        and(lowerThresGreen3 <= colorRGB3[1] <= upperThresGreen3)\
        and(lowerThresBlue3  <= colorRGB3[2] <= upperThresBlue3 ):
        pass
      else:
        logger.debug('  Đã đợi được màu KHÔNG mong muốn tại vị trí 3. Giá trị màu đọc đưọc RGB3: %d,%d,%d',red3,green3,blue3)
        LotusLib.delay(delayFinish_ms)
        return 3
    logger.error('  TIMEOUT!!! KHÔNG đợi được màu KHÔNG mong muốn')
    LotusLib.delay(delayFinish_ms)
    return False
  #####################################################
  # Name: keyDownPeriod
  # Function: Nhấn 1 phím và giữ nó trong 1 khoảng thời gian
  # Parameter:
  #   + key: Phím cần nhấn
  #   + time(s): Thời gian gĩư
  # Return: None
  #####################################################
  def keyDownPeriod(key,time):
    GUI.keyDown(key)
    time.sleep(time)
    GUI.keyUp(key)
  
  #####################################################
  # Name: delay
  # Function: delay 1 khoảng thời gian
  # Parameter:
  #   + time_ms: Thời gian đơn vị mili giây
  # Return: None
  #####################################################
  def delay (time_ms=100):
    time_sec = time_ms/1000
    time.sleep(time_sec)
  
  #####################################################
  # Name: midRec
  # Function: Xác định vị trí trung tâm hình chữ nhật
  # Parameter:
  #   + pos: Pos bao gồm pos1, pos2, pos3, pos4
  # Return: Trả về tọa độ trung tâm
  #####################################################
  def midRec (pos):
    return pos[0]+pos[2]/2,pos[1]+pos[3]/2

  #####################################################
  # Name: midRecInt
  # Function: Xác định vị trí trung tâm hình chữ nhật.
  # Parameter:
  #   + pos: Pos bao gồm pos1, pos2, pos3, pos4
  # Return: Trả về tọa độ trung tâm theo dạng integer
  #####################################################
  def midRecInt (pos):
    return int(pos[0]+pos[2]/2),int(pos[1]+pos[3]/2)
  
  #####################################################
  # Name: sendMsg
  # Function: Gửi tin nhắn đến user
  # Parameter:
  #   + pos: Pos bao gồm pos1, pos2, pos3, pos4
  # Return: Trả về tọa độ trung tâm
  #####################################################
  def sendMsg (Message):
    print(Message)
  
  def restart (err_code = 0):
    print("Program will be restarted!!!")
    #Chụp màn hình gửi Facebook
  
    #Send FBChat kem err_code
  
    #restart command
    GUI.click(190,750) #Bấm vào cửa sổ đầu tiên ở thanh tác vụ
    LotusLib.delay(500)
    GUI.click(190,750) #Bấm vào cửa sổ đầu tiên ở thanh tác vụ
    LotusLib.delay(500)
    GUI.click(190,750) #Bấm vào cửa sổ đầu tiên ở thanh tác vụ
    LotusLib.delay(500)
    GUI.click(190,750) #Bấm vào cửa sổ đầu tiên ở thanh tác vụ
    LotusLib.delay(500)
    GUI.click(190,750) #Bấm vào cửa sổ đầu tiên ở thanh tác vụ
    exit()

  #####################################################
  # Name: convertToHour
  # Function: Đổi thông tin thời gian đăng thành giờ
  # Parameter:
  #   + postTime: Thời gian đăng dạng string
  # Return: Giả về số giờ so với hiện tại
  #####################################################
  def convertToHour(postTime):
    # VD: postTime = "51phút trước"
    # VD: postTime = "4giờ trước"
    # VD: postTime = "3ngày trước"
    # VD: postTime = "1tuần trước"
    # VD: postTime = "12-19"
    # VD: postTime = "2015-12-19"
    clipHour = str(postTime)
    clipHour = clipHour.replace("phút trước",'*0',2) #Đổi "phút trước"
    clipHour = clipHour.replace("giờ trước",'*1',2) #Đổi "giờ Trước"
    clipHour = clipHour.replace("ngày trước",'*24',2) #Đổi "ngày Trước"
    clipHour = clipHour.replace("tuần trước",'*7*24',2) #Đổi "tuần Trước"
    clipHour = clipHour.replace("m ago",'*0',2) #Đổi "phút trước"
    clipHour = clipHour.replace("h ago",'*1',2) #Đổi "giờ Trước"
    clipHour = clipHour.replace("d ago",'*24',2) #Đổi "ngày Trước"
    clipHour = clipHour.replace("w ago",'*7*24',2) #Đổi "tuần Trước"
    checkDate = clipHour.split('-')
    if len(checkDate) == 2:
      curDay  = datetime.datetime.now().strftime("%j")
      clipDay = datetime.datetime(int(datetime.datetime.now().year),int(checkDate[0]),int(checkDate[1])).strftime("%j")
      clipHour = str(eval(curDay.lstrip('0') + "-" + clipDay.lstrip('0'))*24)
    elif len(checkDate) == 3:
      curDay  = datetime.datetime.now().strftime("%j")
      clipDay = datetime.datetime(int(checkDate[0]),int(checkDate[1]),int(checkDate[2])).strftime("%j")
      clipHour = str(((int(datetime.datetime.now().year) - int(checkDate[0]))*365  +eval(curDay.lstrip('0') + "-" + clipDay.lstrip('0')))*24)
    try:
      return eval(clipHour.lstrip('0'))
    except:
      logger.fatal("====> LỖI không giải mã được ngày post: "+str(postTime))
      exit()
 
  #####################################################
  # Name: convertHumanNumToInt
  # Function: Đổi con số dạng cho người xem sang số thực
  # Parameter:
  #   + humanNum: Con số dạng người xem
  # Return: Giả về số thực
  # VD: 1.1K -> 1100, 2.3M -> 2300000, 570 -> 570
  #####################################################
  def convertHumanNumToInt(humanNum):
    retNum = str(humanNum)
    retNum = retNum.replace('K','*1000',2) #Đổi "Giờ Trước"
    retNum = retNum.replace('M','*1000000',2) #Đổi "ngày Trước"
    try:
      return eval(retNum.lstrip('0'))
    except:
      logger.fatal("====> LỖI không giải mã được ra Human Number: "+str(humanNum))
      return False # Dành cho các trường hợp lỗi TikTok. VD: humanNum = "Chia Sẻ"
    
  def getCurTime ():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  
  #########################################################
  # Name: horFindColor
  # Function: Tìm màu mong muốn theo chiều ngang
  # Parameter:
  #   + findColor: màu cần tìm.
  #   + deltaFindColor: sau số biến cho phép của màu.
  #   + xFrom: tọa độ X bắt đầu. Chú ý: xFrom có thể lớn hơn xEnd.
  #   + xEnd: tọa độ X kết thúc. Chú ý: xEnd có thể nhỏ hơn xFrom.
  #   + xStep: bước nhảy
  #   + yPos: vị trí tọa độ Y
  # Return: Trả về tọa độ của vị trí dầu tên tìm được.
  # Ex: horFindColor (rgb(92,201,145),5,0,1919,1,65)
  #########################################################
  def horFindColor(findColor=(255,255,255),deltaFindColor=5,xFrom=0,xEnd=1000,xStep=1,yPos=0):
    screen = GUI.screenshot()
    checkPos = [xFrom,yPos]
    fCont = 0
    findDir = 'leftToRight'
    if xFrom <= xEnd:
      findDir = 'leftToRight'
      if xEnd - xFrom > 0: fCont = 1
    else:
      findDir = 'rightToLeft'
      if xFrom - xEnd > 0: fCont = 1
    
    while fCont == 1:
      if LotusLib.checkColorWithoutCapture(screen,checkPos,findColor,deltaFindColor,0) == True:
        return checkPos
      else:
        if findDir == 'leftToRight':
          checkPos[0] += xStep
          if checkPos[0] <= xEnd:
            fCont = 1
          else:
            fCont = 0
        else:
          checkPos[0] -= xStep
          if checkPos[0] > xEnd:
            fCont = 1
          else:
            fCont = 0
    return False

  #########################################################
  # Name: verFindColor
  # Function: Tìm màu mong muốn theo chiều dọc
  # Parameter:
  #   + findColor: màu cần tìm.
  #   + deltaFindColor: sau số biến cho phép của màu.
  #   + yFrom: tọa độ Y bắt đầu. Chú ý: yFrom có thể lớn hơn yEnd.
  #   + yEnd: tọa độ Y kết thúc. Chú ý: yEnd có thể nhỏ hơn yFrom.
  #   + yStep: bước nhảy
  #   + xPos: vị trí tọa độ X
  # Return: Trả về tọa độ của vị trí dầu tên tìm được.
  # Ex: verFindColor (rgb(92,201,145),5,0,1079,1,65)
  #########################################################
  def verFindColor(findColor=(255,255,255),deltaFindColor=5,yFrom=0,yEnd=1000,yStep=1,xPos=0):
    screen = GUI.screenshot()
    checkPos = [xPos,yFrom]
    fCont = 0
    findDir = 'topToBot'
    if yFrom <= yEnd:
      findDir = 'topToBot'
      if yEnd - yFrom > 0: fCont = 1
    else:
      findDir = 'botToTop'
      if yFrom - yEnd > 0: fCont = 1
    
    while fCont == 1:
      if LotusLib.checkColorWithoutCapture(screen,checkPos,findColor,deltaFindColor,0) == True:
        return checkPos
      else:
        if findDir == 'topToBot':
          checkPos[1] += yStep
          if checkPos[1] <= yEnd:
            fCont = 1
          else:
            fCont = 0
        else:
          checkPos[1] -= yStep
          if checkPos[1] > yEnd:
            fCont = 1
          else:
            fCont = 0
    return False

  #########################################################
  # Name: programTerminateConf
  # Function: - Dùng kết hợp với Threading để giám sát và
  #             tắt chương trình thông qua hotkey.
  #           - Trước khi tắt sẽ chụp màn hình và lưu lại.
  # Parameter:
  #   + logPathAndPrefixName: Đường dẫn và tiền tố cho ảnh chụp màn hình.
  #   + pythonKillHotkey: phím hoặc tổ hợp phím khi kill tất cả python đang chạy.
  #   + vscodeKillHotkey: phím hoặc tổ hợp phím khi kill tất cả VSCode đang chạy.
  # Ex: programTerminateConf ('./','shift+f12','shift+f5')
  #########################################################
  def programTerminateConf (logPathAndPrefixName = './',pythonKillHotkey = 'shift+f12',vscodeKillHotkey = 'shift+f5'):
    global taskKillerEndFlag
    while True:  # making a loop
      # print(taskKillerEndFlag,logPathAndPrefixName,pythonKillHotkey,vscodeKillHotkey)
      #Kill ALL python (include VSCode)
      if keyboard.is_pressed(pythonKillHotkey):  # Terminate the program
        logger.error('Terminal key has been pressed')
        logger.error('KILL ALL PYTHON')
        #Capture Screen
        GUI.screenshot().save(logPathAndPrefixName+"_HandTerminate_"+str(datetime.datetime.now().strftime("%H.%M.%S"))+".png")
        os.system("taskkill /im python.exe /F") #Kill VSCode
      
      #Kill VSCode only
      if keyboard.is_pressed(vscodeKillHotkey):  # Terminate the program
        logger.error('Terminal key has been pressed')
        logger.error('KILL VSCODE')
        #Capture Screen
        GUI.screenshot().save(logPathAndPrefixName+"_HandTerminate_"+str(datetime.datetime.now().strftime("%H.%M.%S"))+".png")
        os.system("taskkill /im Code.exe") #Kill VSCode
        
      if taskKillerEndFlag == True:
        exit()
        
  #########################################################
  # Name: taskKillerSetup
  # Function: - Dùng kết hợp với Threading để giám sát và
  #             tắt chương trình thông qua hotkey.
  #           - Trước khi tắt sẽ chụp màn hình và lưu lại.
  # Parameter:
  #   + threadID: số ID của thread
  #   + threadName: Tên Alias của thread
  #   + logPathAndPrefixName: Đường dẫn và tiền tố cho ảnh chụp màn hình.
  #   + pythonKillHotkey: phím hoặc tổ hợp phím khi kill tất cả python đang chạy.
  #   + vscodeKillHotkey: phím hoặc tổ hợp phím khi kill tất cả VSCode đang chạy.
  # Ex: taskKillerSetup (1,TaskKiller,'./','shift+f12','shift+f5')
  #########################################################
  def taskKillerStart(threadID = 1, threadName = 'TaskKiller',logPathAndPrefixName = './',pythonKillHotkey = 'shift+f12',vscodeKillHotkey = 'shift+f5'):
    taskKiller = TaskKiller(threadID,threadName,logPathAndPrefixName,pythonKillHotkey,vscodeKillHotkey)
    taskKiller.start()
    
  def taskKillerEnd():
    global taskKillerEndFlag
    taskKillerEndFlag = True

  #########################################################
  # Name: findAllImageOnScreen
  # Function: Tìm kiếm trên màn hình có chỗ nào giống ảnh cung cấp thì trả về
  #           vị trí trung tâm của hình đó.
  # Parameter:
  #   + image: Đường dẫn đến hình cần tìm
  # Return: + Một mảng các phần tử là vị trí PosXY của ảnh tìm được.
  #         + Nếu không tìm thấy thì trả về mảng rỗng []
  #    
  # Ex: findAllImageOnScreen('Images/23s.png')
  # => [(231, 613), (231, 685), (231, 757), (231, 829)] #Tìm được 4 vị trí.
  #########################################################
  def findAllImageOnScreen(image):
    listPosImage = list()
    listBox = list(pyautogui.locateAllOnScreen(image))
    if len(listBox) > 0:
      for eachBox in listBox:
        boxPos = LotusLib.midRecInt(eachBox)
        listPosImage.append(boxPos)
    return listPosImage
  
  #########################################################
  # Name: findAllImageRectScreen
  # Function: Tìm kiếm trên phạm vi 1 phần màn hình có chỗ nào giống ảnh cung cấp
  #           thì trả về vị trí trung tâm của hình đó.
  # Parameter:
  #   + image: Đường dẫn đến hình cần tìm
  #   + beginPosXY: Điểm góc TopLeft của phạm vi hình chữ nhật tìm kiến.
  #   + endPosXY: Điểm góc BotRight của phạm vi hình chữ nhật tìm kiến.
  # Return: + Một mảng các phần tử là vị trí PosXY của ảnh tìm được.
  #         + Nếu không tìm thấy thì trả về mảng rỗng []
  #    
  # Ex: findAllImageRectScreen('Images/23s.png',beginPosXY=(0,0),endPosXY=(1919,1079))
  # => [(231, 613), (231, 685)] #Tìm được 2 vị trí.
  #########################################################
  def findAllImageRectScreen(image="",beginPosXY=(0,0),endPosXY=(1919,1079)):
    listPosImage = list()
    listBox = list(pyautogui.locateAllOnScreen(image))
    if len(listBox) > 0:
      for eachBox in listBox:
        # boxPos = LotusLib.midRecInt(eachBox)
        # Kiểm tra eachBox có nằm trong phạm vi tìm kiến cho phép không.
        if beginPosXY[0] <= eachBox[0] and eachBox[0]+eachBox[2] <= endPosXY[0] and \
          beginPosXY[1] <= eachBox[1] and eachBox[1]+eachBox[3] <= endPosXY[1]:
          boxPos = LotusLib.midRecInt(eachBox)
          listPosImage.append(boxPos)
    return listPosImage
  
  #########################################################
  # Name: listDir
  # Function: Trả về một danh sách các file/thư mục được list ra bên trong đường dẫn
  # Parameter:
  #   + path: Đường dẫn đến thư mục cần list
  #   + returnFullPath: Kết quả liệt kê sẽ chứa cả đường dẫn input
  # Return: Danh sách các dữ liệu nằm ngay trong đường dẫn tìm kiếm.
  #    
  # Ex: listDir("G:\PostData_VN\",returnFullPath = 1)
  #########################################################
  def listDir(path="",returnFullPath = 1):
    from os import listdir
    listData = listdir(path)
    
    returnList = list()
    if returnFullPath == 1:
      for i in listData:
        returnList.append(path+i)
      return returnList
    else:
      returnList = listData
      return returnList
    
  #########################################################
  # Name: taskKiller
  # Function: Ép một chương trình nào đó phải tắt đi.
  # Parameter:
  #   + taskExeName: Tên file .exe của chương trình sẽ bị tắt đi.
  #     CHÚ Ý: ĐỂ XEM ĐƯỢC TÊN TASK.EXE CẦN MỞ TASK MANAGER RỒI VÀO
  #            TAB DETAIL SẼ XUÂT HIỆN TÊN EXE VÀ TASK ID.
  # Return: None.
  # Ex: taskKiller("chrome.exe")
  # Ex: taskKiller('"Wondershare Filmora9.exe"') #<--- CHÚ Ý: Nếu có space
  #     thì để trong dấu nháy đơn và đến nháy kép. KHÔNG ĐẺ NGƯỢC LẠI.
  #########################################################
  def taskKiller (taskExeName = ""):
    import os
    os.system("taskkill /f /im "+str(taskExeName))

  #########################################################
  # Name: programOpenJoinIn
  # Function: Chạy lệnh như đăng nhập vào của sổ Run của Window.
  #           Chú ý là chương trình mở ra như là 1 dòng lệnh trong code.
  #           Điều này có nghĩa là dòng code bên dưới chỉ chạy tiếp Khi
  #           chương trình này bị tắt.
  # Parameter:
  #   + command: Lệnh/đường dẫn chương trình
  # Return: None.
  # Ex1: programOpenJoinIn("calc") #Mở máy tính tay calculator
  # Ex2: programOpenJoinIn("notepad D:\\abc.txt")
  # Ex3: programOpenJoinIn("D:\\Video_Make.wfp") <----- Dùng chương trình mặc định để mở file (Filmora)
  #      programOpenJoinIn("D:\\hello.pptx")     <----- Dùng chương trình mặc định để mở file (Power Point)
  #
  # CHÚ Ý: Không phải lệnh nào chạy được ở RUN thì đều chạy được với
  # winRun. Một số lệnh như mở "chrome.exe", "wordpad D:\\abc.txt" Không
  # chạy được. Muốn chạy thì phải cung cấp đường dẫn tuyệt đối đến chương trình.
  #########################################################
  def programOpenJoinIn (command = ""):
    from subprocess import check_output as winRun
    winRun(command, shell=True).decode()
    
  #########################################################
  # Name: programOpenParallel (Popen)
  # Function: Mở một chương trình cho phép có khoảng trắng trong đường dẫn.
  # Parameter:
  #   + programPath: Đường đẫn đến chương trình.
  #   + filePath: Đường dẫn đến file cần mở.
  # Return: số program ID (pid)
  # Ex:
  # app  = "C:\Program Files\Wondershare\Filmora9\Wondershare Filmora9.exe"
  # file = "G:\Video_Make.wfp"
  # pid  = programOpenParallel (programPath = app, filePath = file)
  #########################################################
  def programOpenParallel (programPath = "", filePath = ""):
    from subprocess import Popen
    pid = Popen([programPath, filePath]).pid
    return pid