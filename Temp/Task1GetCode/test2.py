import mysql.connector
import datetime
from A5_GetLink_PrimaryFunction import *


mydb = mysql.connector.connect(
  host="192.168.68.200",
  user="tiktop_vn",
  password="ao!6ejM*7h8HtrgR",
  database="zalo_bot"
)

# mycursor = mydb.cursor()
mycursor = mydb.cursor(dictionary=True)

# #Diền -999 vào bảng
# for i in range (0,251):
#   sql = "UPDATE tiktop_vol32 SET task2_check_time = %s, Task2_PIC = %s, checking_retry = %s WHERE id = "+str(i)
#   val = ("-999","-","0")
#   mycursor.execute(sql, val)
#   mydb.commit()
# exit()

#Lấy tin -999 hoặc CHECKING (Nếu hết -999)
sql = "SELECT * FROM tx_buffer WHERE note = '"+str('tiktop_vn_script')+"' ORDER BY send_timestamp_sec DESC LIMIT 1"
mycursor.execute(sql)
readData = mycursor.fetchall()
print(readData)
print(len(readData))
print(int(readData[0]['send_timestamp_sec']))
print(int(datetime.datetime.now().timestamp()))
exit()

sql = "SELECT * FROM tiktop_vol1 WHERE task2_check_time = 'DONE' LIMIT 3"

mycursor.execute(sql)
readData = mycursor.fetchall() #Fetch là lấy dòng đầu tiên
if len(readData) == 0:
  print ("Rong")
else:
  print (mycursor.rowcount)
  print (len(readData))
  print (readData[0]['org_user'])
exit()

# x=datetime.datetime.now()
# b = x.strftime("%Y-%m-%d %H:%M:%S")

sql = "UPDATE tiktop_vol7 SET updated_time = '"+LotusLib.getCurTime()+"' WHERE id = '1'"
mycursor.execute(sql)
mydb.commit()

#Kiểm tra lại
sql = "SELECT * from tiktop_vol7  WHERE id = '1'"
mycursor.execute(sql)
blacklist = mycursor.fetchall()
print(blacklist)

# sql = "UPDATE tiktop_vol7 SET updated_time = %s, video_source = %s WHERE id = 1"
# val = (LotusLib.getCurTime(),"ABC")
# mycursor.execute(sql, val)
# mydb.commit()
        
# config.time.strftime("%Y-%m-%d %H:%M:%S",/
# config.time.localtime(config.time.time()))

# create a new table geeksforgeekscopy and copy all  
# records from geeksfoegeeks into the newly created table 
#mycursor.execute("create table tiktop_vol1 (id INT AUTO_INCREMENT PRIMARY KEY) select * from tiktop_vol0_master") 

# #Thêm dòng
# sql = "INSERT INTO tiktop_day (like_num, user) VALUES (%s, %s)"
# val = ("35", "JUBEI2")
# mycursor.execute(sql, val)

# #Xóa dòng
# sql = "DELETE FROM tiktop_day WHERE id = '1'"
# mycursor.execute(sql)

# #Update dòng
# sql = "UPDATE tiktop_day SET like_num = '300',user = 'ABC' WHERE id = '5'"
# mycursor.execute(sql)
# mydb.commit()


# # Cập nhật dữ liệu. Nếu chưa tồn tại thì tạo thêm mới
# sql = "SELECT * from tiktop_blacklist"
# mycursor.execute(sql)
# blacklist = mycursor.fetchall()
# blacklistUser = []
# for i in range (0,len(blacklist)):
#   blacklistUser.append(blacklist[i][1])
# print(blacklistUser)

# a = "DungTran"
# if a in blacklistUser:
#   print("YES")
# else:
#   print("NO")


# if mycursor.rowcount == 0:
#   sql = "INSERT INTO tiktop_day (like_num, user) VALUES (%s, %s)"
#   val = ("300", "ABC")
#   mycursor.execute(sql, val)
#   mydb.commit()
# else:
#   sql = "UPDATE tiktop_day SET like_num = '300',user = 'ABC' WHERE id = '5'"
#   mycursor.execute(sql)
#   mydb.commit()

# print(mycursor.rowcount, "record inserted.")

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