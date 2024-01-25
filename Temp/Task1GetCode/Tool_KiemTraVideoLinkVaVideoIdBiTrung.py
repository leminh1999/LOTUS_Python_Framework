import mysql.connector

volNum = 40

 
mydb = mysql.connector.connect(
  host="192.168.68.200",
  user="tiktop_vn",
  password="ao!6ejM*7h8HtrgR",
  database="tiktop_vn"
)
#20: 6992108267493215514
mycursor = mydb.cursor(dictionary=True)

sql = "SELECT * FROM tiktop_vol"+str(volNum)
mycursor.execute(sql)
readData = mycursor.fetchall()

print ("Tổng số dòng: ",len(readData))
print("### KIỂM TRA VIDEO_LINK VÀ VIDEO_ID BỊ TRÙNG ###")
for i in range(0,len(readData)):
  if i+1 < len(readData):
    for j in range(i+1,len(readData)):
      if readData[i]['video_link'] == readData[j]['video_link']: print("Video_link trùng tại ID: "+str(readData[i]['id'])+" và "+str(readData[j]['id']))
      if readData[i]['video_id'] == readData[j]['video_id']: print("Video_id trùng tại ID: "+str(readData[i]['id'])+" và "+str(readData[j]['id']))
      
print("################### DONE #######################")