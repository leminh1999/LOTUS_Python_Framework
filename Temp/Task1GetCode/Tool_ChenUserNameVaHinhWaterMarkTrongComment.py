from pymediainfo import MediaInfo
import os
import mysql.connector
from PIL import Image

volNum = 48

myDb = mysql.connector.connect(
  host="192.168.68.200",
  user="tiktop_vn",
  password="ao!6ejM*7h8HtrgR",
  database="tiktop_vn"
)
myCursor = myDb.cursor(dictionary=True)

logoPath = 'G:\Biz\YoTu\TikTop\TikTop_Filmora\Images\Logo_White_Border.png'
workingPath = 'G:/Biz/YoTu/TikTop/TikTopData/PostData_VN/Vol'+str(volNum)+'/'

#########################################################
# Name: getFileList
# Function: Lấy danh sách các files ứng với loại filetype
#           nhập vào.
# Parameter:
#   + path: đường dẫn đến thư mục tìm kiếm.
#   + filetype: đuôi file tìm kiếm. Có thể nhập dạng list.
# Return: List chứa danh danh các file được liệt kê.
# Ex: listFileImage = getFileList(path='D:/Images/',filetype='jpg,bmp')
#########################################################
def getFileList(path="",fileType=""):
  accTime = 0
  clipNum = 0
  clipTimeMin = 0
  clipTimeSec = 0
  if path == "" or fileType == "":
    return ""
  else:
    print("Hello2")
    outputList = list()
    fileTypeList = fileType.replace(' ','').split(',')
    for ftype in fileTypeList:
      print ("List for filetype: ",ftype)
      listFile = os.listdir(path)
      listFile.sort(reverse=True)
      for i in listFile:
        if i.endswith(ftype):
          # print("- File: ",path+i)
          outputList.append(path+i)
          # Extract duration
          media_info = MediaInfo.parse(path+i)
          for track in media_info.tracks:
            if track.track_type == 'Video':
              clipNum += 1
              durationMs = track.duration
              clipTime = int(durationMs/1000)
              clipTimeMin = int(clipTime/60)
              clipTimeSec = clipTime%60
              accTime += durationMs
              print("{}.Clip [{}:{}] {}".format(clipNum,clipTimeMin,clipTimeSec,path+i))

  accTimeHour = int(accTime/3600000)
  accTimeRemain = accTime%3600000
  accTimeMin = int(accTimeRemain/60000)
  accTimeRemain = accTimeRemain%60000
  accTimeSec = int(accTimeRemain/1000)
  accTimeRemain = accTimeRemain%1000
  accTimeMs = accTimeRemain
  print("Total Time: {}h{}m{}.{}s".format(accTimeHour,accTimeMin,accTimeSec,accTimeMs))
          
  return outputList
  
  
#1. Gán user vào cuối file
listFile = getFileList(workingPath,'mp4')

for i in range(0,len(listFile)):
  videoId = listFile[i].split('_')[2].split('.mp4')[0]
  print (videoId)
  sql = "SELECT * FROM tiktop_vol"+str(volNum)+" WHERE video_id ='"+videoId+"' LIMIT 1"
  myCursor.execute(sql)
  readData = myCursor.fetchall()[0]
  if len(readData) != 0: #Có dữ liệu
    username = readData['org_user']
    print(username)
  else:
    exit()
  
  # Gán username vào cuối file
  if len(listFile[i].split('_')) <= 3:
    print("=> Rename")
    newNameMp4 = listFile[i].replace('.mp4','_'+username+'.mp4')
    newNamePng = listFile[i].replace('.mp4','_'+username+'.png')
    os.rename(listFile[i],newNameMp4)
    os.rename(listFile[i].replace('.mp4','.png'),newNamePng)
  else: 
    newNameMp4 = listFile[i]
    newNamePng = listFile[i].replace('.mp4','.png')
    print(newNamePng)
    
  #2. Gán hình watermark vào comment
  logoPic = Image.open(logoPath)
  commentPic = Image.open(newNamePng)
  logoResize = logoPic.resize((500,500))

  background = Image.new('RGB',(500,500),(248,248,248))
  background.paste(logoResize,(0,0),logoResize)
  # background.save('background.png')
  background.putalpha(6)
  # background.save('backgroundAlpha.png')

  commentPic.paste(background,(10,200),background)
  commentPic.save(newNamePng)