from random import randint
import mysql.connector
import datetime
from A5_GetLink_PrimaryFunction import *

myDb = mysql.connector.connect(
  host="192.168.68.200",
  user="tiktop_vn",
  password="ao!6ejM*7h8HtrgR",
  database="tiktop_vn"
)
myCursor = myDb.cursor(dictionary=True)

sql = "SELECT * FROM tiktop_config_vpn WHERE country = 'vietnam' LIMIT 1"
myCursor.execute(sql)
readData = myCursor.fetchall()
if len(readData) != 0: #Có dữ liệu
  locationList = readData[0]['surfshark_location_list'].split(',')
  workingLocation = readData[0]['surfshark_working']
  # print(len(locationList))
  if len(locationList) != 1:
    nextLocationWorking = workingLocation
    while nextLocationWorking == workingLocation:
      nextLocationWorking = locationList[randint(0,len(locationList)-1)]
      print(nextLocationWorking)
    # Cập nhật location mới
    sql = "UPDATE tiktop_config_vpn SET country = %s, surfshark_working = %s WHERE country = 'vietnam'"
    val = ('vietnam',nextLocationWorking)
    myCursor.execute(sql, val)
    myDb.commit()
else:
  logger.error('CONFIG VPN FOR COUNTRY %s NOT FOUND!!!','vietnam')
exit()
          
          
          
# #Diền -999 vào bảng
# for i in range (0,251):
#   sql = "UPDATE tiktop_vol32 SET task2_check_time = %s, Task2_PIC = %s, checking_retry = %s WHERE id = "+str(i)
#   val = ("-999","-","0")
#   myCursor.execute(sql, val)
#   myDb.commit()
# exit()

#Lấy tin -999 hoặc CHECKING (Nếu hết -999)
sql = "SELECT * FROM tiktop_vol14 WHERE task2_check_time = "+str(-999)+" LIMIT 1"
myCursor.execute(sql)
readData = myCursor.fetchall()
print(readData)
print(len(readData))
# if len(readData) != 0: #Có tin -999
#   rowStatus = "-999"
exit()

sql = "SELECT * FROM tiktop_vol1 WHERE task2_check_time = 'DONE' LIMIT 3"

myCursor.execute(sql)
readData = myCursor.fetchall() #Fetch là lấy dòng đầu tiên
if len(readData) == 0:
  print ("Rong")
else:
  print (myCursor.rowcount)
  print (len(readData))
  print (readData[0]['org_user'])
exit()

# x=datetime.datetime.now()
# b = x.strftime("%Y-%m-%d %H:%M:%S")

sql = "UPDATE tiktop_vol7 SET updated_time = '"+LotusLib.getCurTime()+"' WHERE id = '1'"
myCursor.execute(sql)
myDb.commit()

#Kiểm tra lại
sql = "SELECT * from tiktop_vol7  WHERE id = '1'"
myCursor.execute(sql)
blacklist = myCursor.fetchall()
print(blacklist)

# sql = "UPDATE tiktop_vol7 SET updated_time = %s, video_source = %s WHERE id = 1"
# val = (LotusLib.getCurTime(),"ABC")
# myCursor.execute(sql, val)
# myDb.commit()
        
# config.time.strftime("%Y-%m-%d %H:%M:%S",/
# config.time.localtime(config.time.time()))

# create a new table geeksforgeekscopy and copy all  
# records from geeksfoegeeks into the newly created table 
#myCursor.execute("create table tiktop_vol1 (id INT AUTO_INCREMENT PRIMARY KEY) select * from tiktop_vol0_master") 

# #Thêm dòng
# sql = "INSERT INTO tiktop_day (like_num, user) VALUES (%s, %s)"
# val = ("35", "JUBEI2")
# myCursor.execute(sql, val)
# myDb.commit()

# #Xóa dòng
# sql = "DELETE FROM tiktop_day WHERE id = '1'"
# myCursor.execute(sql)
# myDb.commit()

# #Update dòng
# sql = "UPDATE tiktop_day SET like_num = '300',user = 'ABC' WHERE id = '5'"
# myCursor.execute(sql)
# myDb.commit()


# # Cập nhật dữ liệu. Nếu chưa tồn tại thì tạo thêm mới
# sql = "SELECT * from tiktop_blacklist"
# myCursor.execute(sql)
# blacklist = myCursor.fetchall()
# blacklistUser = []
# for i in range (0,len(blacklist)):
#   blacklistUser.append(blacklist[i][1])
# print(blacklistUser)

# a = "DungTran"
# if a in blacklistUser:
#   print("YES")
# else:
#   print("NO")


# if myCursor.rowcount == 0:
#   sql = "INSERT INTO tiktop_day (like_num, user) VALUES (%s, %s)"
#   val = ("300", "ABC")
#   myCursor.execute(sql, val)
#   myDb.commit()
# else:
#   sql = "UPDATE tiktop_day SET like_num = '300',user = 'ABC' WHERE id = '5'"
#   myCursor.execute(sql)
#   myDb.commit()

# print(myCursor.rowcount, "record inserted.")

    # stringData = str(postInfo.date)
    # stringData = stringData.replace('giờ trước','*1',2) #Đổi "Giờ Trước"
    # stringData = stringData.replace('ngày trước','*24',2) #Đổi "ngày trước"
    # stringData = stringData.replace('tuần trước','*24',2) #Đổi "tuần trước"
    # stringData = stringData.replace('-','*1000*',2) #Đổi "11-17"

# def aa():
#   retNum = "Chia sẻ"
#   retNum = retNum.replace('K','*1000',2) #Đổi "Giờ Trước"
#   retNum = retNum.replace('M','*1000000',2) #Đổi "ngày Trước"
#   try:
#     return eval(retNum)
#   except:
#     print("====> LỖI không giải mã được ngày post: ")
#     return 0

# print(aa())
# print("123")