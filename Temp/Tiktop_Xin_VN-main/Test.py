import mysql.connector
import platform
from seleniumFirefox import *


MYSQL_IP = "192.168.68.200"
MYSQL_DB = "tiktop_gx"
pc_name_current = platform.uname()[1]


## Kết nối mySQL ##
myDb = mysql.connector.connect(
  host= MYSQL_IP,
  user= "tiktop_"+pc_name_current,
  password= "",
  database= MYSQL_DB, #Tên cơ sở dữ liệu
  autocommit=True #Tự động cập nhật bảng và dữ liệu đang chạy.
)
myCursor = myDb.cursor(dictionary=True) #=> Xuất dữ liệu dạng dictionary (Giống object)

myDbZalo = mysql.connector.connect(
  host= MYSQL_IP,
  user= 'tiktop_'+pc_name_current,
  password= '',
  database= 'zalo_bot', #Tên cơ sở dữ liệu
  autocommit=True #Tự động cập nhật bảng và dữ liệu đang chạy.
)
myCursorZalo = myDbZalo.cursor(dictionary=True) #=> Xuất dữ liệu dạng dictionary (Giống object)


app = Test()
app.setup_method(headless = False)

app.downloadVideo()

app.driver.close()
app.driver.quit()