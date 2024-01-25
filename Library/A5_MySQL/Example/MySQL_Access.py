import __init
from time import sleep
from Conf.loggingSetup import *
from Library.A1_PyAutoGUI.pyAutoGui_Wrap import pyAutoGui_Remap as GUI
from Library.A2_LOTUS.lotus_Wrap import lotus_Remap as LOTUS
from Library.A3_Selenium.selenium_Wrap import Keys, WEB, seleniumIDE_Remap as IDE
from Library.A4_SendInBlue.sendInBlue_Wrap import class_contentMode, mailConfig, sendInBlue_Wrapper as SIB
from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
# from pyngrok import ngrok, conf
from pprint import *



################################################################
## B. Khai báo trong Application ##
import platform
MYSQL_HOST     = "178.128.216.233"
MYSQL_DATABASE = "tiktop_gx"
MYSQL_USER     = "tiktop_" + platform.uname()[1]
MYSQL_PASS     =  "Shinghen123!"
sql = MYSQL(MYSQL_HOST,MYSQL_USER,MYSQL_PASS,MYSQL_DATABASE)

################################################################
#1. Select Querry data from MySQL
readData = sql.customSelect("SELECT * FROM vn_20_scanned_list LIMIT 1")
pprint(readData)

#2. Insert Querry data from MySQL
columnString = "id, video_id, video_link, key_word, key_type, status, timestamp"
valueString  = "1, 'test', 'test', '', '', '-999', CURRENT_TIMESTAMP"
sql.insertRow("vn_20_scanned_list", columnString, valueString)

#3. Update row data in MySQL
updateString = "video_id = 'test2', key_word = 'test2', key_type = 'test2',\
                status = 'test2', timestamp = CURRENT_TIMESTAMP"
sql.updateRow("vn_20_scanned_list", updateString, whereCondition="id = 2")

#4. Delete Querry data from MySQL
sql.deleteRow("vn_20_scanned_list", whereCondition="id = 1")

#5. SELECT COUNT: Truy vấn cơ sở dũ liệu
readData = sql.countAllRows("vn_20_scanned_list")
print("Count Row (id): "+str(readData))

#6. COUNT WITH CONDITION
readData = sql.countRowWithCondition("vn_20_scanned_list", "id > 3700")
print("Count Row (id): "+str(readData))

#7. Finding the AVG of Values in a Column
readData = sql.findAvgValue("vn_20_scanned_list", "id", "id > 3700")
print("AVG Value (id): "+str(readData))

#7. Finding the Sum of Values in a Column
readData = sql.findSumValue("vn_20_scanned_list", "id", "id > 3700")
print("Sum Value (id): "+str(readData))

#8. Finding the Max Value in a Column
readData = sql.findMaxValue("vn_20_scanned_list","id", "id > 3700")
print("Max Value (id): "+str(readData))

#9. Finding the Min Value in a Column
readData = sql.findMinValue("vn_20_scanned_list","id", "id > 3700")
print("Min Value (id): "+str(readData))

#6. Finding the Average Value in a Column
readData = sql.findAvgValue("vn_20_scanned_list","id")
print("Average Value (Sum/count row): "+str(readData))


# sprintf(query,"SELECT time,data FROM %s.%s WHERE sm_id = %d AND SensKind = 52 AND (time BETWEEN (NOW() - INTERVAL %s HOUR) AND (NOW() - INTERVAL %s HOUR)) ORDER BY time DESC",db_name,db_table,sm_id,String(12+deltaTimezone),String(deltaTimezone));
  

#1. Select Querry data from MySQL
readData = sql.customSelect("SELECT * FROM vn_20_scanned_list WHERE "+genWhereCond.last_n_Hour(1))
pprint(readData)

# 1. Select Querry data from MySQL
# print(genWhereCond.between_2_timestamp("2020-01-01 00:00:00", "2022-01-01 00:00:00"))
readData = sql.customSelect("SELECT * FROM vn_20_scanned_list WHERE "\
           +genWhereCond.between_2_timestamp("2020-01-01 00:00:00", "2022-01-01 00:00:00"))
pprint(readData)

readData = sql.selectCondition("vn_20_scanned_list","*","id = 3508")
pprint(readData)

