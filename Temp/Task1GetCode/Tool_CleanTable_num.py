import mysql.connector
import datetime
from A5_GetLink_PrimaryFunction import *

mydb = mysql.connector.connect(
  host="192.168.68.200",
  user="tiktop_vn",
  password="",
  database="tiktop_vn"
)

mycursor = mydb.cursor(dictionary=True)

#Diền -999 vào bảng
for i in range (1,2000):
  sql = "UPDATE tiktop_vol23 SET task2_check_time = %s, Task2_PIC = %s, checking_retry = %s, video_source = %s WHERE id = "+str(i)
  val = ("-999","-","0","")
  mycursor.execute(sql, val)
  mydb.commit()
  
