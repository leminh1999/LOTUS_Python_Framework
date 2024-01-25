import mysql.connector

myDb = mysql.connector.connect(
  host="192.168.68.200",
  user="tiktop_vn123",
  password="",
  database="tiktop_vn"
)
myCursor = myDb.cursor(dictionary=True)

sql = "SELECT SUM(heart_click) FROM tiktop_vol59"
myCursor.execute(sql)
checkLastSent = myCursor.fetchall()[0]['SUM(heart_click)']

myDb.close()

print(checkLastSent)