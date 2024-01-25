import __init
import random
import datetime
from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
from Library.A7_Zalo.Zalo_Wrap import msgType, zaloMysql,zalo_Wrapper as ZALO

# ZALO.dummyTxTest()
send_timestamp_sec = int(datetime.datetime.now().timestamp())
send_schedule = datetime.datetime.fromtimestamp(send_timestamp_sec)
sendTo = '0908549354'

#Send Text
ZALO.sendMessage(sendTo="0908549354",messType="text",messData="Xin chào bạn")
#Send Text with delay in seconds
ZALO.sendMessage(sendTo="0908549354",messType="text",messData="Xin chào bạn (Delayed message in 10s)!",sendDelayInSec=10)
#Send file
filePath = 'D:\\Database\\Local_GIT_WorkingDir\\LOTUS_Python_Framework\\Library\\A7_Zalo\\Components\\PIC\\001.png'
ZALO.sendMessage(sendTo="0908549354",messType="file",messData=filePath)
#Send Sticker
ZALO.sendMessage(sendTo="0908549354",messType="sticker",messData="Hey")
#Send GIF
ZALO.sendMessage(sendTo="0908549354",messType="gif",messData="Hello")
#Send Location
locationPos = "10.8132583,106.712124" #Lat,Lon: https://www.google.com/maps?q=10.8132583,106.712124&z=14&t=m
ZALO.sendMessage(sendTo="0908549354",messType="location",messData=locationPos)
#Send Image
imagePath = 'D:\\Database\\Local_GIT_WorkingDir\\LOTUS_Python_Framework\\Library\\A7_Zalo\\Components\\PIC\\003.png'
ZALO.sendMessage(sendTo="0908549354",messType="image",messData=imagePath)