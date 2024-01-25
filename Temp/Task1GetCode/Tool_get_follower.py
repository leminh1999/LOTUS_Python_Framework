
from bs4 import BeautifulSoup
import mysql.connector

file = open("README.html", "r",encoding="utf8", errors="surrogateescape")
htmlCode = file.readline()
soup = BeautifulSoup(htmlCode, 'html.parser')

mydb = mysql.connector.connect(
  host="192.168.68.200",
  user="tiktop_vn",
  password="ao!6ejM*7h8HtrgR",
  database="tiktop_vn"
)

# mycursor = mydb.cursor()
mycursor = mydb.cursor(dictionary=True)

# print(soup.prettify())
# for eachPost in soup.select(".job__list-item"):
#   print("===================================")
#   # title = eachPost.select(".job__list-item-title")[0].find('a',attrs={'href': 'https://123job.vn/viec-lam/tuyen-nhan-vien-ky-thuat-Xv90baMmqk'})
#   title = eachPost.select(".job__list-item-title")[0].find('a',attrs={'href': 'https://123job.vn/viec-lam/tuyen-nhan-vien-ky-thuat-Xv90baMmqk'})
#   print(title)

#Xóa hết tất cả các dòng trong bảng
sql = "DELETE FROM tiktop_follow_list"
mycursor.execute(sql)
mydb.commit()

i = 0
num = 0
for eachPost in soup.select(".user-title h4"):
  i += 1
  if i > 28:
    num += 1
    follower = eachPost.text
    print(str(i)+". "+follower)
    # INSERT vao MySQL
    sql = "INSERT INTO tiktop_follow_list (id, org_user, add_type) VALUES (%s,%s, %s)"
    val = (str(num),follower, "manual")
    mycursor.execute(sql, val)
    mydb.commit()
  
