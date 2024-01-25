import mysql.connector

## Kết nối mySQL ##
myDb = mysql.connector.connect(
  host= "192.168.68.200",
  user= "tiktop",
  password= "",
  database= "tiktop_vn", #Tên cơ sở dữ liệu
  autocommit=True #Tự động cập nhật bảng và dữ liệu đang chạy.
)
myCursor = myDb.cursor(dictionary=True) #=> Xuất dữ liệu dạng dictionary (Giống object)

sql = "SELECT * from tiktop_vol23 WHERE task2_check_time = '-999' LIMIT 10000"
# sql = "SELECT * from tiktop_vol23 WHERE id = '269'"
myCursor.execute(sql)
abc = myCursor.fetchall()
print(abc[1539])
print(myCursor.rowcount)
