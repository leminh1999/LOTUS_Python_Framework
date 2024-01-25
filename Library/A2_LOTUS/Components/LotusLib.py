# -*- coding`: utf-8 -*-
from __future__ import unicode_literals

import datetime
import shutil
import time

import keyboard  # using module keyboard
import pyautogui
import pyperclip
from PIL import Image, ImageDraw,ImageFont

import __init
from Conf.loggingSetup import *

GUI = pyautogui
taskKillerEndFlag = False
click = GUI.click
doubleClick = GUI.doubleClick
mousePos = GUI.moveTo
keys = GUI.typewrite  #Ex: pyautogui.typewrite(['a', 'b', 'left', 'left', 'X', 'Y'])
press = GUI.press

def rgb(red, green, blue): return (red,green,blue)

def delay(time_ms): return time.sleep(time_ms/1000)

####################################################################
import threading
import random


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
    if printLog == True: logger.info("\n===== USER CAN PRESS SHIFT+F5 OR SHIFT+F12 TO STOP =====\n")
    LotusLib.programTerminateConf(self.logPathAndPrefixName,self.pythonKillHotkey,self.vscodeKillHotkey)
####################################################################

class capture():
  def captureToImageVar():
    '''
    - `Name`: captureToImageVar
    - `Function`: Chụp màn hình và gán vào một biến nào đó
    - `Parameter`: None
    - `Return`: Trả về dữ liệu của màn hình hiện hành.
    - `Ex`:
      1. screenImage = captureToImageVar()\\
      2. checkColorWithoutCapture(screenImage,(100,100),(255,255,255),20,100)\\
        #Tìm trong màn hình screenImage tại vị trí (100,100) có màu RGB (255,255,255) hay không? Chờ 100ms sau khi lệnh chạy xong.
    '''
    GUI.screenshot()


class LotusLib (capture):
  def addImageToHtmlLog(image):
    #Check if image exist
    imageName = image.split("/")[-1]
    if os.path.isfile(HTML_LOG_DIR+"/data/"+imageName) == True:
      pass
    else:
      #Copy image to html log dir
      shutil.copyfile(image, HTML_LOG_DIR+"/data/"+imageName)
    logger.html("<img src='data/"+imageName+"'>")

  def addMediaToHtmlLog(text="",mediaPath="None",rowIndex:int=0,mediaWidth=300,mediaHeight=300):
    #Detect media type
    mediaType = mediaPath.split(".")[-1]
    if mediaType in ["png","jpg","jpeg","gif","bmp"]:
      mediaType = "image"
    if mediaType in ["mp4","avi","mov","wmv","flv","mkv","webm"]:
      mediaType = "video"
    if mediaType in ["mp3","wav","wma","ogg","flac","aac","alac","aiff","dsd","pcm"]:
      mediaType = "audio"
    if mediaType in ["pdf","doc","docx","xls","xlsx","ppt","pptx","txt","csv","xml","json","html","htm","js","css","php","py","java","c","cpp","cs","go","swift","sql","sh","bat","exe","apk","ipa","dmg","iso","zip","rar","7z","tar","gz","bz2","xz","z"]:
      mediaType = "file"
    if mediaType == "None":
      mediaType = "None"
      
    #Copy media to html log dir
    mediaName = mediaPath.split("/")[-1]
    if os.path.isfile(HTML_LOG_DIR+"/data/"+mediaName) == True:
      pass
    else:
      #Copy image to html log dir
      shutil.copyfile(mediaPath, HTML_LOG_DIR+"/data/"+mediaName)
    mediaLocalPath = "data/"+mediaName
      
    #############################
    ### Add media to html log ###
    #############################
    #check odd or even row
    if rowIndex%2 == 0:
      rowClass = "evenRow"
    else:
      rowClass = "oddRow"
    mediaUID = mediaName.split(".")[0] +"_"+ str(random.randint(0,999999))
    timeMark = str(datetime.datetime.now())
    #Media type: image
    if mediaType == "image":
      addData = f'''
      <div class="{rowClass} toggle-btn" onclick="toggleImage('{mediaUID}')" onmouseover="showThumbnail('{mediaLocalPath}', this)" onmouseout="hideThumbnail()">
        <div style="height: 40px">
          <span class="mediaIconBox"><img width="40px" src="{mediaLocalPath}" alt="{mediaName}"></span>
          {text}
          <span class="timeMark">[{timeMark}]</span>
        </div>
        <div id="{mediaUID}" class="image-container" style="display: none;">
          <img src="{mediaLocalPath}" alt="{mediaName}">
        </div>
      </div>
      '''
      logger.html(addData)
    #Media type: video
    if mediaType == "video":
      logger.html("<video width='"+str(mediaWidth)+"' height='"+str(mediaHeight)+"' controls><source src='data/"+mediaName+"' type='video/mp4'></video>")
    #Media type: audio
    if mediaType == "audio":
      logger.html("<audio controls><source src='data/"+mediaName+"' type='audio/mpeg'></audio>")
    #Media type: file
    if mediaType == "file":
      logger.html("<a href='data/"+mediaName+"' download>"+text+"</a>")
    #Media type: None
    if mediaType == "None":
      addData = f'''
      <div class="{rowClass} toggle-btn">
        <div style="height: 40px">
          <span class="mediaIconBox"><img width="40px" src="" style="visibility: hidden;"></span>
          {text}
          <span class="timeMark">[{timeMark}]</span>
        </div>
      </div>
      '''
      logger.html(addData)
    
    logger.rowCnt += 1


    
  def addScreenCaptureToHtmlLog():
    # Capture screen and save to html log dir
    # Make a random name for image
    randomName = str(datetime.datetime.now()).replace(" ","_").replace(":","_").replace(".","_")
    imageName = "FSCapture_"+randomName+".png"
    GUI.screenshot(HTML_LOG_DIR+"/data/"+imageName)
    logger.html("<img src='data/"+imageName+"'>")

  def addRectScreenCaptureToHtmlLog(imagePath="",region_xyxy=(0,0,100,100),textPos=(0,0),fontPath='Conf/Fonts/ARLRDBD.ttf', fontSize=20, caption="",radius=30, borderColor=(0,0,0),textColor=(255,0,0), borderWidth=10 , printPosInside=True,savePath=""):
    '''
    - `Name`: rectBorder
    - `Function`: xuất ra màn hình ảnh với vị trí click cùng màu RGB tại điểm đó.
    - `Parameter`:
      - `imagePath`: Đường dẫn đến ảnh. Nếu không có thì sẽ lấy màn hình hiện hành.
      - `region_xyxy`: Vùng màn hình cần lấy ảnh. (x1,y1,x2,y2)
      - `textPos`: Vị trí chèn text. (x,y)
      - `fontPath`: Đường dẫn đến font chữ. Ex: 'Conf/Fonts/arial.ttf'
      - `caption`: Nội dung chèn vào ảnh.
      - `fontSize`: Kích thước chữ.
      - `radius`: Bán kính bo tròn.
      - `borderColor`: Màu của viền (R,G,B[,A]).
      - `textColor`: Màu của chữ (R,G,B[,A]).
      - `borderWidth`: Độ dày của viền.
      - `printPosInside`:Chèn vị trí click và màu trong ảnh.
      - `savePath`: Đường dẫn lưu ảnh.
    - `Return`: None
    - `Ex`: LOTUS.log.addRectScreenCaptureToHtmlLog(radius=30,caption="ABC",fontPath='Conf/Fonts/arial.ttf',region_xyxy=(0,100,300,300),printPosInside=True,savePath="PIC/rectBorder.png")
            => PIC/rectBorder.png
    '''
    # Capture screen and save to html log dir
    # Make a random name for image
    randomName = str(datetime.datetime.now()).replace(" ","_").replace(":","_").replace(".","_")
    imageName = "RectCapture_"+randomName+".png"
    if savePath == "":
      savePath = HTML_LOG_DIR+"/data/"+imageName
    else:
      savePath = savePath
    LotusLib.roundRectBorderImage(imagePath=imagePath,region_xyxy=region_xyxy,textPos=textPos, caption=caption,fontPath=fontPath,fontSize=fontSize,radius=radius, borderColor=borderColor,textColor=textColor, borderWidth=borderWidth , printPosInside=printPosInside,savePath=savePath)
    logger.html("<img src='data/"+imageName+"'>")
    
  def addClickPosToHtmlLog(xPos=0, yPos=0,imagePath=None, radius=100, borderColor=(255,0,0), borderWidth=10 , printPosInside=True):
    '''
    - `Name`: addClickPosToHtmlLog
    - `Function`: Chụp màn hình và gán vào một biến nào đó
    - `Parameter`:
      - `xPos`: Vị trí x của điểm click.
      - `yPos`: Vị trí y của điểm click.
      - `imagePath`: Đường dẫn đến ảnh. Nếu không có thì sẽ lấy màn hình hiện hành.
      - `radius`: Bán kính của hình tròn.
      - `borderColor`: Màu của viền.
      - `borderWidth`: Độ dày của viền.
      - `printPosInside`:Chèn vị trí click và màu trong ảnh. PIC/circularImage.png
      - `savePath`: Đường dẫn lưu ảnh.
    - `Return`:
      - Trả về chuỗi JSON với các thông tin sau: inputImg, outputImg, clickColor
    - `Ex`:
      - `EX1`: addClickPosToHtmlLog(450,900,'PIC/1920_1080_sample.jpg'). # PIC/circularImage.png
      - `EX2`: addClickPosToHtmlLog(450,900). # PIC/circularImage.png
    '''
    # Make a random name for image
    randomName = str(datetime.datetime.now()).replace(" ","_").replace(":","_").replace(".","_")
    imageName = "ClickCapture_"+randomName+".png"
    LotusLib.saveClickImage(xPos, yPos,imagePath, radius, borderColor, borderWidth , printPosInside,HTML_LOG_DIR+"/data/"+imageName)
    logger.html("<img src='data/"+imageName+"'>")

  ####################################################################
  def saveClickImage(xPos=0, yPos=0,imagePath=None, radius=100, borderColor=(255,0,0), borderWidth=10 , printPosInside=True,savePath="circularImage.png"):
    '''
    - `Name`: showClickImage
    - `Function`: xuất ra màn hình ảnh với vị trí click cùng màu RGB tại điểm đó.
    - `Parameter`:
      - `xPos`: Vị trí x của điểm click.
      - `yPos`: Vị trí y của điểm click.
      - `imagePath`: Đường dẫn đến ảnh. Nếu không có thì sẽ lấy màn hình hiện hành.
      - `radius`: Bán kính của hình tròn.
      - `borderColor`: Màu của viền.
      - `borderWidth`: Độ dày của viền.
      - `printPosInside`:Chèn vị trí click và màu trong ảnh. PIC/circularImage.png
      - `savePath`: Đường dẫn lưu ảnh.
    - `Return`:
      - Trả về chuỗi JSON với các thông tin sau: inputImg, outputImg, clickColor
    - `Ex`:
      - `EX1`: showClickImage(450,900,'PIC/1920_1080_sample.jpg'). # PIC/circularImage.png
               => {'inputImg': '1920_1080_sample.jpg', 'outputImg': 'circularImage.png', 'clickColor': (182, 180, 159)}
      - `EX2`: showClickImage(450,900).                            #PIC/circularImage_2.png
               => {'inputImg': 'fullScreenCapture.png', 'outputImg': 'circularImage.png', 'clickColor': (182, 180, 159)}
      - `EX3`: showClickImage(50,50) #Lấy màn hình hiện hành. Tại vị trí (50,50) # PIC/circularImage_3.png
               => {'inputImg': 'fullScreenCapture.png', 'outputImg': 'circularImage.png', 'clickColor': (255, 255, 255)}
    '''
    if type(imagePath) == str:
        im = Image.open(imagePath)
        pixColor = im.getpixel((xPos,yPos))
        pixColorInvert = (255-pixColor[0],255-pixColor[1],255-pixColor[2])
    else:
        import os
        os.system("rm -f fullScreenCapture.png")
        im = GUI.screenshot('fullScreenCapture.png')
        pixColor = im.getpixel((xPos,yPos))
        pixColorInvert = (255-pixColor[0],255-pixColor[1],255-pixColor[2])
    im = im.crop((xPos-radius,yPos-radius, xPos+radius, yPos+radius))
    # Make a circular image
    # Define the circle's center coordinates and radius
    center_x, center_y = im.size[0]/2, im.size[1]/2
    radius = min(im.size) / 2
    # Create a mask image the same size as the original image
    mask = Image.new("L", im.size, 0)
    # Draw the circle on the mask image
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse([center_x-radius, center_y-radius, center_x+radius, center_y+radius], fill=255, outline=128,width=borderWidth)
    draw_mask.ellipse([center_x-borderWidth, center_y-borderWidth, center_x+borderWidth, center_y+borderWidth], fill=128)
    # Create a result image the same size as the original image
    rgbaColor = borderColor + (0,) # Convert rgb (Ex: 255,0,0) to rgba (Ex: 255,0,0,0)
    result = Image.new("RGBA", im.size, rgbaColor)
    # Paste the original image over the result image using the mask
    result.paste(im, mask=mask)
    # Add position
    if printPosInside == True:
      draw_mask = ImageDraw.Draw(result)
      textBox = [center_x-radius/2, center_y-radius/6+radius/1.65, center_x+radius/2, center_y+radius/6+radius/1.65]
      textPos = textBox[0]+(textBox[2]-textBox[0])/2 - radius/4.5, textBox[1]+(textBox[3]-textBox[1])/2   - 12
      textColor = textBox[0]+(textBox[2]-textBox[0])/2 - radius/2.8, textBox[1]+(textBox[3]-textBox[1])/2 + 1
      draw_mask.rounded_rectangle(textBox, fill=pixColor,radius=radius/10, outline=borderColor, width=3)
      draw_mask.text(textPos, str(xPos)+","+str(yPos), fill=pixColorInvert, font=None, anchor=None, spacing=0, align="center")
      draw_mask.text(textColor, str(pixColor).replace(" ",""), fill=pixColorInvert, font=None, anchor=None, spacing=0, align="center")
    # Save the modified image
    result.save(savePath)
    # Return the modified image
    if type(imagePath) == str:
        return {'inputImg': imagePath, 'outputImg': savePath,'clickColor': pixColor}
    else:
        return {'inputImg': "fullScreenCapture.png", 'outputImg': savePath,'clickColor': pixColor}

  def roundRectBorderImage(imagePath="", region_xyxy=(0,0,200,200),textPos=(0,0), caption="",fontPath='Conf/Fonts/ARLRDBD.ttf',fontSize=20,radius=100, borderColor=(255,0,0),textColor=(255,0,0), borderWidth=10 , printPosInside=True,savePath="circularImage.png"):
    '''
    - `Name`: rectBorder
    - `Function`: xuất ra màn hình ảnh với vị trí click cùng màu RGB tại điểm đó.
    - `Parameter`:
      - `imagePath`: Đường dẫn đến ảnh. Nếu không có thì sẽ lấy màn hình hiện hành.
      - `region_xyxy`: Vùng màn hình cần lấy ảnh. (x1,y1,x2,y2)
      - `textPos`: Vị trí chèn text. (x,y)
      - `caption`: Nội dung chèn vào ảnh.
      - `fontSize`: Kích thước chữ.
      - `radius`: Bán kính bo tròn.
      - `borderColor`: Màu của viền (R,G,B[,A]).
      - `textColor`: Màu của chữ (R,G,B[,A]).
      - `borderWidth`: Độ dày của viền.
      - `printPosInside`:Chèn vị trí click và màu trong ảnh.
      - `savePath`: Đường dẫn lưu ảnh.
    - `Return`:
      - Trả về chuỗi JSON với các thông tin sau: inputImg, outputImg
    '''
    if imagePath != "":
        im = Image.open(imagePath).crop(region_xyxy)
    else:
        im = GUI.screenshot().crop(region_xyxy)
    # Create a mask image the same size as the original image
    mask = Image.new("L", im.size, 0)
    # Draw the circle on the mask image
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle(xy=(0,0,region_xyxy[2]-region_xyxy[0],region_xyxy[3]-region_xyxy[1]),radius=radius, fill=255, outline=128,width=borderWidth)
    rgbaColor = borderColor + (0,) # Convert rgb (Ex: 255,0,0) to rgba (Ex: 255,0,0,0)
    result = Image.new("RGBA", im.size, rgbaColor)
    # Paste the original image over the result image using the mask
    result.paste(im, mask=mask)
    # Add position
    if printPosInside == True:
      draw_mask = ImageDraw.Draw(result)
      if textPos == (0,0):
        textPosX = im.size[0]/3
        textPosY = im.size[1]*4/5
        if im.size[1] - textPosY < 30:
          textPosY = im.size[1] - 30
      else:
        textPosX = 0
        textPosY = 0
      font = ImageFont.truetype(font=fontPath,size=fontSize, encoding="unic")
      # Draw the text with a border
      for i in range(-2, 3):
        for j in range(-2, 3):
          draw_mask.text((textPosX+i,textPosY+j), caption, fill=(255,255,255), font=font, anchor=None, spacing=0, align="right")
      # Draw multiple text layers with different colors and offsets
      draw_mask.text((textPosX,textPosY), caption, fill=textColor, font=font, anchor=None, spacing=0, align="right")
    # Save the modified image
    result.save(savePath)
    # Return the modified image
    if imagePath != "":
        return {'inputImg': imagePath, 'outputImg': savePath}
    else:
        return {'inputImg': "fullScreenCapture.png", 'outputImg': savePath}
      
  ####################################################################
  def waitImage(image,confidence=0.8,timeout_sec=30,delayFinish_ms=100,printLog=True):
    '''
    - `Name`: waitImage
    - `Function`: Đợi hình ảnh xuất hiện
    - `Parameter`:
      - `image``: đường dẫn đến file ảnh
      - `confidence`: độ chính xác [0-1]. Mặc định 0.8
      - `timeout_sec`: thời gian time out. Mặc định 15 giây
      - `delayFinish_ms`: thời gian delay sau khi hoàn thành
    - `Return`: Trả về thông số vị trí giữa tấm ảnh.
            Có thể kết hợp như sau:
            GUI.click(waitImage(....))
    - `Ex`: waitImage('iconFirefox.png',90)
    '''
    if printLog == True:
      logger.debug('Subtask`: waitImage(image=%s,timeout_sec=%s)',str(image),str(timeout_sec))
      LotusLib.addImageToHtmlLog(image)
    pos =0
    pos1=0
    pos2=0
    pos3=0
    pos4=0
    timeCnt = time.time();
    while (time.time() - timeCnt) < timeout_sec : #Chưa hết thời gian time out
      pos = GUI.locateOnScreen(image,confidence=confidence)
      if pos != None:
        pos1,pos2,pos3,pos4 = pos
        if printLog == True: logger.html('  Image Found')
        LotusLib.delay(delayFinish_ms)
        return round(pos1+pos3/2),round(pos2+pos4/2)
    if printLog == True:
      logger.error('  Image NOT Found!!!')
      LotusLib.addScreenCaptureToHtmlLog()
    LotusLib.delay(delayFinish_ms)
    return False
  
  ####################################################################
  def waitNotImage(image="",confidence=0.8,timeout_sec=30,delayFinish_ms=100,printLog=True):
    '''
    - `Name`: waitNotImage
    - `Function`: Đợi hình ảnh biến mất
    - `Parameter`:
      - `image``: đường dẫn đến file ảnh
      - `confidence`: độ chính xác [0-1]. Mặc định 0.8
      - `timeout_sec`: thời gian time out. Mặc định 15 giây
      - `delayFinish_ms`: thời gian delay sau khi hoàn thành
    - `Return`:
      - `True`: Nếu hình ảnh biến mất
      - `False`: Nếu hình ảnh vẫn còn
    - `Ex`: waitImage('iconFirefox.png',90)
    '''
    if printLog == True:
      logger.debug('Subtask`: waitNotImage(image=%s,timeout_sec=%s)',str(image),str(timeout_sec))
      LotusLib.addImageToHtmlLog(image)
    timeCnt = time.time();
    while (time.time() - timeCnt) < timeout_sec : #Chưa hết thời gian time out
      pos = GUI.locateOnScreen(image,confidence=confidence)
      if pos == None:
        LotusLib.delay(delayFinish_ms)
        return True
    if printLog == True: logger.error('  Image STILL APPEAR!!!')
    LotusLib.delay(delayFinish_ms)
    return False
  
  ####################################################################
  def clickImage(image="",confidence=0.8,timeout_sec=30,delayFinish_ms=100,printLog=True):
    '''
    - `Name`: clickImage
    - `Function`: Đợi hình ảnh xuất hiện và click vào nó
    - `Parameter`:
       - `image`: đường dẫn đến file ảnh.
       - `confidence`: độ chính xác [0-1]. Mặc định 0.8
       - `timeout`: thời gian time out. Mặc định 15 giây
       - `delayFinish_ms`: thời gian delay sau khi hoàn thành
    - `Return`:
       - Trả về True nếu có hình và click.
       - Trả về False nếu không có hình.
    - `EX`: clickImage('iconChat.png',20)
    '''
    pos = LotusLib.waitImage(image,confidence,timeout_sec,printLog=False)
    if printLog == True:
      logger.debug('Subtask`: clickImage(image=%s,timeout_sec=%s)',str(image),str(timeout_sec))
      LotusLib.addImageToHtmlLog(image)
    if pos != None and pos != False:
      if printLog == True: logger.html('  Click vào image tại vị trí`: %s',str(pos))
      GUI.click(pos,tween=pyautogui.easeInOutBounce , duration=0.5)
      LotusLib.delay(delayFinish_ms)
      return True
    if printLog == True: logger.error('  Image NOT Found!!!')
    LotusLib.addScreenCaptureToHtmlLog()
    LotusLib.delay(delayFinish_ms)
    return False
  
  ####################################################################
  def getColor(posX,posY):
    '''
    - `Name`: getColor
    - `Function`: kiểm tra màu tại 1 vị trí nào đó
    - `Parameter`:
       - `pos`: Vị trí quan sát màu. pos là một list gồm 2 gía trị X,Y
    - `Return`: Trả về màu của điểm ảnh.
    '''
  # if printLog == True: logger.debug('Subtask`: getColor(posX=%d,posY=%d)',posX,posY)
    color = GUI.screenshot().getpixel((posX,posY))
  # if printLog == True: logger.debug('  Màu đọc được`: %s',str(color))
    return color
  
  def checkColorWithCapture(pos=(0,0),colorRGB=(0,0,0),delta=20,delayFinish_ms=100,printLog=True):
    '''
    - `Name`: checkColorWithCapture
    - `Function`: kiểm tra màu tại 1 điểm sau khi chụp ảnh màn hình
    - `Parameter`:
      - `pos`: Vị trí quan sát màu. pos là một list gồm 2 gía trị X,Y
      - `color`: Giá trị màu mong đợi. color là một list gồm 3 gía trị R,G,B
      - `delta`: khoảng sai số chấp nhận được so với giá trị gốc.
      - `delayFinish_ms`: thời gian delay sau khi hoàn thành
    - `Return`: 
      - Trả về True nếu điều kiện đúng.
      - Trả về False nếu điều kiện sai.
    '''
    # if printLog == True: logger.debug('Subtask`: checkColorWithCapture(pos=%s,colorRGB=%s,delta=%s)',str(pos),str(colorRGB),str(delta))
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
      if printLog == True: logger.debug('Màu kiểm tra nằm trong kỳ vọng. Giá trị màu đọc đưọc RGB`: %d,%d,%d',red,green,blue)
      LotusLib.delay(delayFinish_ms)
      return True
    # if printLog == True: logger.warning('Màu kiểm tra KHÔNG nằm trong kỳ vọng!!! Giá trị màu đọc đưọc RGB`: %d,%d,%d',red,green,blue)
    LotusLib.delay(delayFinish_ms)
    return False
  
  ####################################################################
  def checkColorWithoutCapture(image="",pos=(0,0),colorRGB=(0,0,0),delta=20,delayFinish_ms=100,printLog=True):
    '''
    - `Name`: checkColorWithoutCapture
    - `Function`: kiểm tra màu tại 1 điểm dựa vào tấm ảnh đã có
    - `Parameter`:
      - `image`: tấm hình được chụp với lệnh GUI.screenshot()
      - `pos`: Vị trí quan sát màu. pos là một list gồm 2 gía trị X,Y
      - `color`: Giá trị màu mong đợi. color là một list gồm 3 gía trị R,G,B
      - `delta`: khoảng sai số chấp nhận được so với giá trị gốc.
      - `delayFinish_ms`: thời gian delay sau khi hoàn thành
    - `Return`:
      - Trả về True nếu điều kiện đúng.
      - Trả về False nếu điều kiện sai.
    - `Ex`:
      1. screenImage = captureToImageVar()\\
      2. checkColorWithoutCapture(screenImage,(100,100),(255,255,255),20,100)\\
        #Tìm trong màn hình screenImage tại vị trí (100,100) có màu RGB (255,255,255) hay không? Chờ 100ms sau khi lệnh chạy xong.
    '''
    # if printLog == True: logger.debug('Subtask`: checkColorWithCapture(image=%s,pos=%s,colorRGB=%s,delta=%s)',str(image),str(pos),str(colorRGB),str(delta))
  
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
      # if printLog == True: logger.debug('Màu kiểm tra nằm trong kỳ vọng. Giá trị màu đọc đưọc RGB`: %d,%d,%d',red,green,blue)
      LotusLib.delay(delayFinish_ms)
      return True
    # if printLog == True: logger.warning('Màu kiểm tra KHÔNG nằm trong kỳ vọng!!! Giá trị màu đọc đưọc RGB`: %d,%d,%d',red,green,blue)
    LotusLib.delay(delayFinish_ms)
    return False
  
  ####################################################################
  def waitColor(pos=(0,0),colorRGB=(0,0,0),delta=20,timeout_sec=15,delayFinish_ms=100,printLog=True):
    '''
    - `Name`: waitColor
    - `Function`: Đợi màu tại 1 vị trí nào đó
    - `Parameter`:
      - `pos`: Vị trí quan sát màu. pos là một list gồm 2 gía trị X,Y
      - `color`: Giá trị màu mong đợi. color là một list gồm 3 gía trị R,G,B
      - `delta`: khoảng sai số chấp nhận được so với giá trị màu gốc.
      - `timeout`: thời gian time out. Mặc định 15 giây
      - `delayFinish_ms`: thời gian delay sau khi hoàn thành
    - `Return`: Trả về màu của điểm ảnh. Khi nó nằm trong delta.
    '''
    # if printLog == True: logger.debug('Subtask`: waitColor(pos=%s,colorRGB=%s,delta=%s,timeout_sec=%s)',str(pos),str(colorRGB),str(delta),str(timeout))
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
    while (time.time() - timeCnt) < timeout_sec: #Chưa hết thời gian time out
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
        # if printLog == True: logger.debug('  Đã đợi được màu mong muốn. Giá trị màu đọc đưọc RGB`: %d,%d,%d',red,green,blue)
        LotusLib.delay(delayFinish_ms)
        return red,green,blue
    if printLog == True: logger.error('  TIMEOUT!!! KHÔNG đợi được màu mong muốn '+str(colorRGB)+' tại Pos = '+str(pos)+'.')
    LotusLib.delay(delayFinish_ms)
    return False
  
  ####################################################################
  def waitNotColor(pos=(0,0),colorRGB=(0,0,0),delta=20,timeout_sec=15,delayFinish_ms=100,printLog=True):
    '''
    - `Name`: waitNotColor
    - `Function`: Đợi màu tại 1 vị trí nào đó khác với màu cung cấp
    - `Parameter`:
       - `pos`: Vị trí quan sát màu. pos là một list gồm 2 gía trị X,Y
       - `color`: Giá trị màu KHONG mong đợi. color là một list gồm 3 gía trị R,G,B
       - `delta`: khoảng sai số chấp nhận được so với giá trị gốc.
       - `timeout`: thời gian time out. Mặc định 15 giây
       - `delayFinish_ms`: thời gian delay sau khi hoàn thành
    - `Return`: Trả về màu của điểm ảnh. Khi nó nằm ngoai delta.
    '''
    # if printLog == True: logger.debug('Subtask`: waitNotColor(pos=%s,colorRGB=%s,delta=%s,timeout_sec=%s)',str(pos),str(colorRGB),str(delta),str(timeout))
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
    while (time.time() - timeCnt) < timeout_sec : #Chưa hết thời gian time out
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
        if printLog == True: logger.debug('  waitNOTcolor thành công. Giá trị màu đọc đưọc RGB`: %d,%d,%d',red,green,blue)
        LotusLib.delay(delayFinish_ms)
        return red,green,blue
    if printLog == True: logger.error('  TIMEOUT!!! Màu sắc '+str(colorRGB)+'tại Pos = '+str(pos)+' không thay đổi!!!')
    LotusLib.delay(delayFinish_ms)
    return False
  
  ####################################################################
  def wait3Color(pos1,color1,delta1,\
                 pos2,color2,delta2,\
                 pos3,color3,delta3,\
                 timeout_sec=15,delayFinish_ms=100,printLog=True):
    '''
    - `Name`: wait3Color
    - `Function`: Đợi màu tại 3 vị trí nào đó
    - `Parameter`:
      - `pos[1..3]`: Vị trí quan sát màu. pos là một list gồm 2 gía trị X,Y
      - `color[1..3]`: Giá trị màu mong đợi. color là một list gồm 3 gía trị R,G,B
      - `delta[1..3]`: khoảng sai số chấp nhận được so với giá trị màu gốc.
      - `timeout`: thời gian time out. Mặc định 15 giây
      - `delayFinish_ms`: thời gian delay sau khi hoàn thành
    - `Return`:
      - Trả về True nếu cả 3 màu tồn tại trong khoảng timeout.
      - Trả về False nếu đã hết thời
    - `EX`:
      - wait3Color(\\
       [ 27, 48],[238, 79, 48],20,\\
       [727,126],[238, 77, 45],20,\\
       [396,217],[ 73,203,221],20,20)
    '''
    if printLog == True: logger.debug('Subtask`: wait3Color(pos1=%s,color1=%s,delta1=%s,pos2=%s,color2=%s,delta2=%s,pos3=%s,color3=%s,delta3=%s,timeout_sec=%s)',str(pos1),str(color1),str(delta1),str(pos2),str(color2),str(delta2),str(pos3),str(color3),str(delta3),str(timeout_sec))
    timeCnt = time.time()
    spendTime = 0
    if LotusLib.waitColor(pos1,color1,delta1,timeout_sec,delayFinish_ms=0) == 0:
      if printLog == True: logger.error('TIMEOUT!!! và màu tại vị trí 1 không khớp')
      LotusLib.delay(delayFinish_ms)
      return False
    spendTime = time.time() - timeCnt
    remainTime = 0 if spendTime >= timeout_sec else timeout_sec - spendTime
    timeCnt = time.time();
    if LotusLib.waitColor(pos2,color2,delta2,remainTime,delayFinish_ms=0) == 0:
      if printLog == True: logger.error('TIMEOUT!!! và màu tại vị trí 2 không khớp')
      LotusLib.delay(delayFinish_ms)
      return False
    spendTime = time.time() - timeCnt
    remainTime = 0 if spendTime >= remainTime else remainTime - spendTime
    if LotusLib.waitColor(pos3,color3,delta3,remainTime,delayFinish_ms=0) == 0:
      if printLog == True: logger.error('TIMEOUT!!! và màu tại vị trí 3 không khớp')
      LotusLib.delay(delayFinish_ms)
      return False
    if printLog == True: logger.debug('Đã tìm thấy màu trùng khớp tại 3 vị trí mong ước')
    LotusLib.delay(delayFinish_ms)
    return True

  ####################################################################
  def wait3NotColor(pos1,colorRGB1,delta1,\
                    pos2,colorRGB2,delta2,\
                    pos3,colorRGB3,delta3,\
                    timeout_sec=15,delayFinish_ms=100,printLog=True):
    '''
    - `Name`: wait3NotColor
    - `Function`: Đợi màu tại 3 vị trí nào đó. Nếu có bất kỳ sự thay đổi tại 1 trong 3 điểm sẽ thoát
    - `Parameter`:
       - `pos[1..3]`: Vị trí quan sát màu. pos là một list gồm 2 gía trị X,Y
       - `colorRGB[1..3]`: Giá trị màu mong đợi. color là một list gồm 3 gía trị R,G,B
       - `delta[1..3]`: khoảng sai số chấp nhận được so với giá trị gốc.
       - `timeout`: thời gian time out. Mặc định 15 giây
       - `delayFinish_ms`: thời gian delay sau khi hoàn thành
    - `Return`:
       - Trả về 1 nếu vị trí 1 có sự thay đổi màu trong khoảng timeout
       - Trả về 2 nếu vị trí 2 có sự thay đổi màu trong khoảng timeout
       - Trả về 3 nếu vị trí 3 có sự thay đổi màu trong khoảng timeout
       - Trả về 0 nếu đã hết thời gian timeout và không có sự thay đổi màu
    - `EX`:
       - wait3NotColor(\\
         [ 27, 48],[238, 79, 48],20,\\
         [727,126],[238, 77, 45],20,\\
         [396,217],[ 73,203,221],20,20)
    '''
    if printLog == True: logger.debug('Subtask`: wait3NotColor(pos1=%s,colorRGB1=%s,delta1=%s,pos2=%s,colorRGB2=%s,delta2=%s,pos3=%s,colorRGB3=%s,delta3=%s,timeout_sec=%s)',str(pos1),str(colorRGB1),str(delta1),str(pos2),str(colorRGB2),str(delta2),str(pos3),str(colorRGB3),str(delta3),str(timeout_sec))
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
    while (time.time() - timeCnt) < timeout_sec : #Chưa hết thời gian time out
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
        if printLog == True: logger.debug('  Đã đợi được màu KHÔNG mong muốn tại vị trí 1. Giá trị màu đọc đưọc RGB1`: %d,%d,%d',red1,green1,blue1)
        LotusLib.delay(delayFinish_ms)
        return 1
      if   (lowerThresRed2   <= colorRGB2[0] <= upperThresRed2  )\
        and(lowerThresGreen2 <= colorRGB2[1] <= upperThresGreen2)\
        and(lowerThresBlue2  <= colorRGB2[2] <= upperThresBlue2 ):
        pass
      else:
        if printLog == True: logger.debug('  Đã đợi được màu KHÔNG mong muốn tại vị trí 2. Giá trị màu đọc đưọc RGB2`: %d,%d,%d',red2,green2,blue2)
        LotusLib.delay(delayFinish_ms)
        return 2
      if   (lowerThresRed3   <= colorRGB3[0] <= upperThresRed3  )\
        and(lowerThresGreen3 <= colorRGB3[1] <= upperThresGreen3)\
        and(lowerThresBlue3  <= colorRGB3[2] <= upperThresBlue3 ):
        pass
      else:
        if printLog == True: logger.debug('  Đã đợi được màu KHÔNG mong muốn tại vị trí 3. Giá trị màu đọc đưọc RGB3`: %d,%d,%d',red3,green3,blue3)
        LotusLib.delay(delayFinish_ms)
        return 3
    if printLog == True: logger.error('  TIMEOUT!!! KHÔNG đợi được màu KHÔNG mong muốn')
    LotusLib.delay(delayFinish_ms)
    return False

  ####################################################################
  def keyDownPeriod(key,time):
    '''
    - `Name`: keyDownPeriod
    - `Function`: Nhấn 1 phím và giữ nó trong 1 khoảng thời gian
    - `Parameter`:
       - `key`: Phím cần nhấn
       - `time(s)`: Thời gian gĩư
    - `Return`: None
    '''
    GUI.keyDown(key)
    time.sleep(time)
    GUI.keyUp(key)
    
  ####################################################################
  def delay (time_ms=100):
    '''
    - `Name`: delay
    - `Function`: delay 1 khoảng thời gian
    - `Parameter`:
       - `time_ms`: Thời gian đơn vị mili giây
    - `Return`: None
    '''
    time_sec = time_ms/1000
    time.sleep(time_sec)
  
  ####################################################################
  def midRec (pos):
    '''
    - `Name`: midRec
    - `Function`: Xác định vị trí trung tâm hình chữ nhật
    - `Parameter`:
       - `pos`: Pos bao gồm pos1, pos2, pos3, pos4
    - `Return`: Trả về tọa độ trung tâm
    '''
    return pos[0]+pos[2]/2,pos[1]+pos[3]/2

  ####################################################################
  def midRecInt (pos):
    '''
    - `Name`: midRecInt
    - `Function`: Xác định vị trí trung tâm hình chữ nhật.
    - `Parameter`:
       - pos`: Pos bao gồm pos1, pos2, pos3, pos4
    - `Return`: Trả về tọa độ trung tâm theo dạng integer
    '''
    return int(pos[0]+pos[2]/2),int(pos[1]+pos[3]/2)
  
  ####################################################################
  def sendMsg (Message):
    '''
    - `Name`: sendMsg
    - `Function`: chạy hàm print()
    - `Parameter`: None
    - `Return`: None
    '''
    print(Message)
  
  ####################################################################
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

  ####################################################################
  def convertToHour(postTime,printLog=True):
    '''
    - `Name`: convertToHour
    - `Function`: Đổi thông tin thời gian đăng thành giờ
    - `Parameter`:
       - `postTime`: Thời gian đăng dạng string.\\
         \+ postTime = "51phút trước"\\
         \+ postTime = "4giờ trước"\\
         \+ postTime = "3ngày trước"\\
         \+ postTime = "1tuần trước"\\
         \+ postTime = "12-19"\\
         \+ postTime = "2015-12-19"
    - `Return`: Trả về số giờ (hour) so với hiện tại.
    '''
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
      if printLog == True: logger.fatal("====> LỖI không giải mã được ngày post`: "+str(postTime))
      exit()

  ####################################################################
  def convertHumanNumToInt(humanNum,printLog=True):
    '''
    - `Name`: convertHumanNumToInt
    - `Function`: Đổi con số dạng cho người xem sang số thực
    - `Parameter`:
       - `humanNum`: Con số dạng người xem
    - `Return`: Giả về số thực
    - `Ex`: 1.1K -> 1100, 2.3M -> 2300000, 570 -> 570
    '''
    retNum = str(humanNum)
    retNum = retNum.replace('K','*1000',2) #Đổi "Giờ Trước"
    retNum = retNum.replace('M','*1000000',2) #Đổi "ngày Trước"
    try:
      return eval(retNum.lstrip('0'))
    except:
      if printLog == True: logger.fatal("====> LỖI không giải mã được ra Human Number`: "+str(humanNum))
      return False # Dành cho các trường hợp lỗi TikTok. VD`: humanNum = "Chia Sẻ"
    
  ####################################################################
  def getCurTime ():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  
  ####################################################################
  def horFindColor(findColor=(255,255,255),deltaFindColor=5,xFrom=0,xEnd=1000,xStep=1,yPos=0,printLog=True):
    '''
    - `Name`: horFindColor
    - `Function`: Tìm màu mong muốn theo chiều ngang
    - `Parameter`:
       - `findColor`: màu cần tìm.
       - `deltaFindColor`: sau số biến cho phép của màu.
       - `xFrom`: tọa độ X bắt đầu. Chú ý`: xFrom có thể lớn hơn xEnd.
       - `xEnd`: tọa độ X kết thúc. Chú ý`: xEnd có thể nhỏ hơn xFrom.
       - `xStep`: bước nhảy
       - `yPos`: vị trí tọa độ Y
    - `Return`: Trả về tọa độ của vị trí dầu tên tìm được.
    - `Ex`: horFindColor (rgb(92,201,145),5,0,1919,1,65)
    '''
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

  ####################################################################
  def horFindColorFromPilImage(pilImage=None,findColor=(255,255,255),deltaFindColor=5,xFrom=0,xEnd=1000,xStep=1,yPos=0,printLog=True):
    '''
    - `Name`: horFindColorFromPilImage
    - `Function`: Tìm màu mong muốn theo chiều ngang
    - `Parameter`:
       - `pilImage`: Đường dẫn đến hình ảnh dạng PIL.
       - `findColor`: màu cần tìm.
       - `deltaFindColor`: sau số biến cho phép của màu.
       - `xFrom`: tọa độ X bắt đầu. Chú ý`: xFrom có thể lớn hơn xEnd.
       - `xEnd`: tọa độ X kết thúc. Chú ý`: xEnd có thể nhỏ hơn xFrom.
       - `xStep`: bước nhảy
       - `yPos`: vị trí tọa độ Y
    - `Return`: Trả về tọa độ của vị trí dầu tên tìm được.
    - `Ex`: horFindColorFromImage (rgb(92,201,145),5,0,1919,1,65)
    '''
    screen = pilImage
      
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
  
  ####################################################################
  def verFindColor(findColor=(255,255,255),deltaFindColor=5,yFrom=0,yEnd=1000,yStep=1,xPos=0,printLog=True):
    '''
    - `Name`: verFindColor
    - `Function`: Tìm màu mong muốn theo chiều dọc
    - `Parameter`:
       - `findColor`: màu cần tìm.
       - `deltaFindColor`: sau số biến cho phép của màu.
       - `yFrom`: tọa độ Y bắt đầu. Chú ý`: yFrom có thể lớn hơn yEnd.
       - `yEnd`: tọa độ Y kết thúc. Chú ý`: yEnd có thể nhỏ hơn yFrom.
       - `yStep`: bước nhảy
       - `xPos`: vị trí tọa độ X
    - `Return`: Trả về tọa độ của vị trí dầu tên tìm được.
    - `Ex`: verFindColor (rgb(92,201,145),5,0,1079,1,65)
    '''
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

  ####################################################################
  def programTerminateConf (logPathAndPrefixName = './',pythonKillHotkey = 'shift+f12',vscodeKillHotkey = 'shift+f5',printLog=True):
    '''
    - `Name`: programTerminateConf
    - `Function`:
       - Dùng kết hợp với Threading để giám sát và tắt chương trình thông qua hotkey.
       - Trước khi tắt sẽ chụp màn hình và lưu lại.
    - `Parameter`:
       - `logPathAndPrefixName`: Đường dẫn và tiền tố cho ảnh chụp màn hình.
       - `pythonKillHotkey`: phím hoặc tổ hợp phím khi kill tất cả python đang chạy.
       - `vscodeKillHotkey`: phím hoặc tổ hợp phím khi kill tất cả VSCode đang chạy.
    - `Ex`: programTerminateConf ('./','shift+f12','shift+f5')
    '''
    global taskKillerEndFlag
    while True: #making a loop
      # print(taskKillerEndFlag,logPathAndPrefixName,pythonKillHotkey,vscodeKillHotkey)
      #Kill ALL python (include VSCode)
      if keyboard.is_pressed(pythonKillHotkey): # Terminate the program
        if printLog == True: logger.error('Terminal key has been pressed')
        if printLog == True: logger.error('KILL ALL PYTHON')
        #Capture Screen
        GUI.screenshot().save(logPathAndPrefixName+"_HandTerminate_"+str(datetime.datetime.now().strftime("%H.%M.%S"))+".png")
        os.system("taskkill /im python.exe /F") #Kill VSCode
      
      #Kill VSCode only
      if keyboard.is_pressed(vscodeKillHotkey): #Terminate the program
        if printLog == True: logger.error('Terminal key has been pressed')
        if printLog == True: logger.error('KILL VSCODE')
        #Capture Screen
        GUI.screenshot().save(logPathAndPrefixName+"_HandTerminate_"+str(datetime.datetime.now().strftime("%H.%M.%S"))+".png")
        os.system("taskkill /im Code.exe") #Kill VSCode
        
      if taskKillerEndFlag == True:
        exit()
  
  ####################################################################
  def taskKillerStart(threadID = 1, threadName = 'TaskKiller',logPathAndPrefixName = './',pythonKillHotkey = 'shift+f12',vscodeKillHotkey = 'shift+f5',printLog=True):
    '''
    - `Name`: taskKillerSetup
    - `Function`:
       - Dùng kết hợp với Threading để giám sát và tắt chương trình thông qua hotkey.
       - Trước khi tắt sẽ chụp màn hình và lưu lại.
    - `Parameter`:
       - `threadID`: số ID của thread
       - `threadName`: Tên Alias của thread
       - `logPathAndPrefixName`: Đường dẫn và tiền tố cho ảnh chụp màn hình.
       - `pythonKillHotkey`: phím hoặc tổ hợp phím khi kill tất cả python đang chạy.
       - `vscodeKillHotkey`: phím hoặc tổ hợp phím khi kill tất cả VSCode đang chạy.
    - `Ex`: taskKillerSetup (1,TaskKiller,'./','shift+f12','shift+f5')
    '''
    taskKiller = TaskKiller(threadID,threadName,logPathAndPrefixName,pythonKillHotkey,vscodeKillHotkey)
    taskKiller.start()
  
  ####################################################################
  def taskKillerEnd():
    global taskKillerEndFlag
    taskKillerEndFlag = True

  ####################################################################
  def findAllImageOnScreen(image,confidence=0.8,printLog=True):
    '''
    - `Name`: findAllImageOnScreen
    - `Function`: Tìm kiếm trên màn hình có chỗ nào giống ảnh cung cấp thì trả về vị trí trung tâm của hình đó.
    - `Parameter`:
       - `image`: Đường dẫn đến hình cần tìm
       - `confidence`: Độ chính xác của hình ảnh [1-0]. Mặc định là 0.5
    - `Return`:
       - Một mảng các phần tử là vị trí PosXY của ảnh tìm được.
       - Nếu không tìm thấy thì trả về mảng rỗng []
    - `Ex`: findAllImageOnScreen('Images/23s.png')\\
       => [(231, 613), (231, 685), (231, 757), (231, 829)] #Tìm được 4 vị trí.
    '''
    if printLog == True:
      logger.debug('Subtask: findAllImageOnScreen(image="{}",confidence={})'.format(image,confidence))
      LotusLib.addImageToHtmlLog(image)
    listPosImage = list()
    listBox = list(pyautogui.locateAllOnScreen(image,confidence=confidence))
    if len(listBox) > 0:
      for eachBox in listBox:
        boxPos = LotusLib.midRecInt(eachBox)
        listPosImage.append(boxPos)
    return listPosImage
  
  ####################################################################
  def findAllImageRegionScreen(image="",confidence=0.8,beginPosXY=(0,0),endPosXY=(1919,1079),printLog = True):
    '''
    - `Name`: findAllImageRegionScreen
    - `Function`: Tìm kiếm MỘT VÙNG trên màn hình có chỗ nào giống ảnh cung cấp thì trả về vị trí trung tâm của hình đó.
    - `Parameter`:
       - `image`: Đường dẫn đến hình cần tìm
       - `confidence`: Độ chính xác của hình ảnh [1-0]. Mặc định là 0.5
       - `beginPosXY`: vị trí (x,y) điểm đầu.
       - `endPosXY`: vị trí (x,y) điểm cuối.
    - `Return`:
       - Một mảng các phần tử là vị trí PosXY của ảnh tìm được.
       - Nếu không tìm thấy thì trả về mảng rỗng []
    - `Ex`: findAllImageRegionScreen('Images/23s.png',(100,100),(500,500))
    '''
    if printLog == True:
      logger.debug('Subtask: findAllImageRegionScreen(image="{}",confidence={},beginPosXY={},endPosXY={})'.format(image,confidence,beginPosXY,endPosXY))
      LotusLib.addImageToHtmlLog(image)
    listPosImage = list()
    listBox = list(pyautogui.locateAllOnScreen(image,confidence=confidence))
    if len(listBox) > 0:
      for eachBox in listBox:
        #boxPos = LotusLib.midRecInt(eachBox)
        #Kiểm tra eachBox có nằm trong phạm vi tìm kiến cho phép không.
        if beginPosXY[0] <= eachBox[0] and eachBox[0]+eachBox[2] <= endPosXY[0] and \
          beginPosXY[1] <= eachBox[1] and eachBox[1]+eachBox[3] <= endPosXY[1]:
          boxPos = LotusLib.midRecInt(eachBox)
          listPosImage.append(boxPos)
    return listPosImage
  
  ####################################################################
  def listDir(path="",returnFullPath = 1):
    '''
    - `Name`: listDir
    - `Function`: Trả về một danh sách các file/thư mục được list ra bên trong đường dẫn
    - `Parameter`:
       - `path`: Đường dẫn đến thư mục cần list
       - `returnFullPath`: Kết quả liệt kê sẽ chứa cả đường dẫn input
    - `Return`: Danh sách các dữ liệu nằm ngay trong đường dẫn tìm kiếm.
    - `Ex`: listDir("G:\PostData_VN\",returnFullPath = 1)
    '''
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
  
  ####################################################################
  def taskKiller (taskExeName = ""):
    '''
    - `Name`: taskKiller
    - `Function`: Ép một chương trình nào đó phải tắt đi.
    - `Parameter`:
       - `taskExeName`: Tên file .exe của chương trình sẽ bị tắt đi.\\
          CHÚ Ý`: ĐỂ XEM ĐƯỢC TÊN TASK.EXE CẦN MỞ TASK MANAGER RỒI VÀO\\
                  TAB DETAIL SẼ XUÂT HIỆN TÊN EXE VÀ TASK ID.
    - `Return`: None.
    - `Ex1`: taskKiller("chrome.exe")
    - `Ex2`: taskKiller('"Wondershare Filmora9.exe"') <--- CHÚ Ý: Nếu có space 
       thì để trong dấu nháy đơn \' và đến nháy kép \". KHÔNG ĐẺ NGƯỢC LẠI.
    '''
    import os
    os.system("taskkill /f /im "+str(taskExeName))

  ####################################################################
  def programOpenJoinIn (command = ""):
    '''
    - `Name`: programOpenJoinIn
    - `Function`: Chạy lệnh như đăng nhập vào của sổ Run của Window.\\
              Chú ý là chương trình mở ra như là 1 dòng lệnh trong code.\\
              Điều này có nghĩa là dòng code bên dưới chỉ chạy tiếp Khi
              chương trình này bị tắt.
    - `Parameter`:
       - `command`: Lệnh/đường dẫn chương trình
    - `Return`: None.
    - `Ex1`: programOpenJoinIn("calc") #Mở máy tính tay calculator
    - `Ex2`: programOpenJoinIn("notepad D:\\abc.txt")
    - `Ex3`: programOpenJoinIn("D:\\Video_Make.wfp") <----- Dùng chương trình mặc định để mở file (Filmora)
    - `Ex4`: programOpenJoinIn("D:\\hello.pptx")     <----- Dùng chương trình mặc định để mở file (Power Point)
    
    - `CHÚ Ý`: Không phải lệnh nào chạy được ở RUN thì đều chạy được với winRun.\\
      Một số lệnh như mở "chrome.exe", "wordpad D:\\abc.txt" Không chạy được.\\
      Muốn chạy thì phải cung cấp đường dẫn tuyệt đối đến chương trình.
    '''
    from subprocess import check_output as winRun
    winRun(command, shell=True).decode()
  
  ####################################################################
  def programOpenParallel (programPath = "", filePath = ""):
    '''
    - `Name`: programOpenParallel (Popen)
    - `Function`: Mở một chương trình cho phép có khoảng trắng trong đường dẫn.
    - `Parameter`:
       - `programPath`: Đường đẫn đến chương trình.
       - `filePath`: Đường dẫn đến file cần mở.
    - `Return`: số program ID (pid)
    - `Ex`:
       1. app  = "C:\Program Files\Wondershare\Filmora9\Wondershare Filmora9.exe"
       2. file = "G:\Video_Make.wfp"
       3. pid  = programOpenParallel (programPath = app, filePath = file)
    - `Ex2`: programOpenParallel("C:\Program Files\Google\Chrome\Application\chrome.exe"," -incognito") #Mở Chrome với tùy chọn incognito
    '''
    from subprocess import Popen
    pid = Popen([programPath, filePath]).pid
    return pid
  
  ####################################################################
  def copyToClipboard(data):
    '''
    - `Name`: copyToClipboard
    - `Function`: Copy dữ liệu vào clipboard
    - `Parameter`:
       - `data`: Dữ liệu cần copy vào clipboard
    - `Return`: None
    - `Ex`: copyToClipboard("Hello Lotus!!!")
    '''
    pyperclip.copy(data)
  
  ####################################################################
  def pasteFromClipboard():
    '''
    - `Name`: pasteFromClipboard
    - `Function`: Dán Ctrl+V
    - `Parameter`: None
    - `Return`: None
    - `Ex`: pasteFromClipboard()
    '''
    GUI.hotkey('ctrl','v')
  
  ####################################################################
  def pasteFromClipboardToVar():
    '''
    - `Name`: pasteFromClipboardToVar
    - `Function`: Trả dữ liệu ra biến ngoài
    - `Parameter`: None
    - `Return`: Trả về data từ clipboard
    - `Ex`: copiedData = pasteFromClipboardToVar()
    '''
    return pyperclip.paste() 
  
  ####################################################################
  def pasteFromClipboardToVarBigData():
    '''
    - `Name`: pasteFromClipboardToVar
    - `Function`: Trả dữ liệu ra biến ngoài
    - `Parameter`: None
    - `Return`: Trả về data từ clipboard
    - `Ex`: copiedData = pasteFromClipboardToVar()
    '''
    import subprocess
    return subprocess.check_output(['xclip', '-selection', 'clipboard', '-o']).decode('utf-8')
