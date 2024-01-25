import __init
from Conf.loggingSetup import *
import mysql.connector


class genWhereCond():
  def last_n_Hour(n):
    '''
    - `name`: last_n_Hour
    - `description`: Trả về kiểu khai báo của câu lệnh WHERE -> để lấy dữ liệu từ n giờ vừa qua.
    - `parameters`:
      - `n`: số giờ muốn lấy dữ liệu
    - `return`: kiểu khai báo của câu lệnh WHERE
    - `Example`:
      - last_n_Hour(1) -> " timestamp >= DATE_SUB(NOW(), INTERVAL 1 HOUR) "
    - `PIC`: ✨ PIC/012.png
    '''
    return " timestamp >= DATE_SUB(NOW(), INTERVAL "+str(n)+" HOUR) "
  
  def last_n_Minute(n):
    '''
    - `name`: last_n_Minute
    - `description`: Trả về kiểu khai báo của câu lệnh WHERE -> để lấy dữ liệu từ n phút vừa qua.
    - `parameters`:
      - `n`: số phút muốn lấy dữ liệu
    - `return`: kiểu khai báo của câu lệnh WHERE
    - `Example`:
      - last_n_Minute(1) -> " timestamp >= DATE_SUB(NOW(), INTERVAL 1 MINUTE) "
    - `PIC`: ✨ PIC/012.png
    '''
    return " timestamp >= DATE_SUB(NOW(), INTERVAL "+str(n)+" MINUTE) "
  
  #Return the last n day
  def last_n_Day(n):
    '''
    - `name`: last_n_Day
    - `description`: Trả về kiểu khai báo của câu lệnh WHERE -> để lấy dữ liệu từ n ngày vừa qua.
    - `parameters`:
      - `n`: số ngày muốn lấy dữ liệu
    - `return`: kiểu khai báo của câu lệnh WHERE
    - `Example`:
      - last_n_Day(1) -> " timestamp >= DATE_SUB(NOW(), INTERVAL 1 DAY) "
    - `PIC`: ✨ PIC/012.png
    '''
    return " timestamp >= DATE_SUB(NOW(), INTERVAL "+str(n)+" DAY) "
  
  #Return the last n month
  def last_n_Month(n):
    '''
    - `name`: last_n_Month
    - `description`: Trả về kiểu khai báo của câu lệnh WHERE -> để lấy dữ liệu từ n tháng vừa qua.
    - `parameters`:
      - `n`: số tháng muốn lấy dữ liệu
    - `return`: kiểu khai báo của câu lệnh WHERE
    - `Example`:
      - last_n_Month(1) -> " timestamp >= DATE_SUB(NOW(), INTERVAL 1 MONTH) "
    - `PIC`: ✨ PIC/012.png
    '''
    return " timestamp >= DATE_SUB(NOW(), INTERVAL "+str(n)+" MONTH) "
  
  #Return the last n year
  def last_n_Year(n):
    '''
    - `name`: last_n_Year
    - `description`: Trả về kiểu khai báo của câu lệnh WHERE -> để lấy dữ liệu từ n năm vừa qua.
    - `parameters`:
      - `n`: số năm muốn lấy dữ liệu
    - `return`: kiểu khai báo của câu lệnh WHERE
    - `Example`:
      - last_n_Year(1) -> " timestamp >= DATE_SUB(NOW(), INTERVAL 1 YEAR) "
    - `PIC`: ✨ PIC/012.png
    '''
    return " timestamp >= DATE_SUB(NOW(), INTERVAL "+str(n)+" YEAR) "
  
  #Return between 2 timestamp
  def between_2_timestamp(timestamp1, timestamp2):
    '''
    - `name`: between_2_timestamp
    - `description`: Trả về kiểu khai báo của câu lệnh WHERE -> để lấy dữ liệu từ 2 timestamp.
    - `parameters`:
      - `timestamp1`: timestamp 1. Format dạng datetime.datetime. Ex: "2020, 1, 1, 0, 0, 0"
      - `timestamp2`: timestamp 2. Format dạng datetime.datetime. Ex: "2020, 1, 1, 0, 0, 0"
    - `return`: kiểu khai báo của câu lệnh WHERE
    - `Example`:
      -between_2_timestamp("2020-01-01 00:00:00", "2022-01-01 00:00:00") ->  " timestamp BETWEEN '2020-01-01 00:00:00' AND '2022-01-01 00:00:00' "
    - `PIC`: ✨ PIC/013.png
    '''
    return " timestamp BETWEEN '"+timestamp1+"' AND '"+timestamp2+"' "
    
################################################################
## A. Khai báo class MySQL ##
class mySqlClass ():
  #0. Init MySQL
  def __init__(self,hostAddress:str="200.200.200.1",port=3306,username="root",password="",database="tiktop_gx",hostVpnAddress:str="",hostDdnsUrl:str=""):
    ### Private Functions ###
    def __connectMysql(host:str="",database:str=database,username:str=username,password:str=password):
      try:
        myDb = mysql.connector.connect(
          host       = host,
          port       = port,
          user       = username,
          password   = password,
          database   = database, #Tên cơ sở dữ liệu
          autocommit = True      #Tự động cập nhật bảng và dữ liệu đang chạy.
        )
        return True, myDb
      except:
        return False, None
    def __ping(host:str):
      import subprocess
      param = '-n' if platform.system().lower()=='windows' else '-c'
      command = ['ping', param, '1', '-w', '1', host]
      return subprocess.call(command) == 0
    ##### MAIN #####
    if hostVpnAddress != "" or hostDdnsUrl != "":
      if hostAddress != "" and __ping(hostAddress) == True:
        # print("=> Host IP (LAN):", hostAddress)
        connResult = __connectMysql(host=hostAddress)
        if connResult[0] == True:
          logger.info("=> Connected to MySQL server (LAN) successfully! - Host IP (LAN): "+hostAddress)
          self.myDb = connResult[1]
      else:
        if hostVpnAddress != "" and __ping(hostVpnAddress) == True:
          # print("=> Host IP (VPN):", hostVpnAddress)
          connResult = __connectMysql(host=hostVpnAddress)
          if connResult[0] == True:
            logger.info("=> Connected to MySQL server (VPN) successfully! - Host IP (VPN): "+hostVpnAddress)
            self.myDb = connResult[1]
        else:
          if hostDdnsUrl != "":
            # print("=> Host IP (DDNS):", hostDdnsUrl)
            connResult = __connectMysql(host=hostDdnsUrl)
            if connResult[0] == True:
              logger.info("=> Connected to MySQL server (DDNS) successfully! - Host URL (DDNS): "+hostDdnsUrl)
              self.myDb = connResult[1]
            else:
              errorMsg = "=> Can't connect to MySQL server! with:\n+ hostAddress: "+hostAddress+"\n+ hostVpnAddress: "+hostVpnAddress+"\n+ hostDdnsUrl: "+hostDdnsUrl
              logger.error(errorMsg)
              raise Exception(errorMsg)
    else:
      connResult = __connectMysql(host=hostAddress)
      if connResult[0] == True:
        if hostVpnAddress != "" or hostDdnsUrl != "":
          logger.info("=> Connected to MySQL server (LAN) successfully! - Host IP (LAN): "+hostAddress)
        else:
          logger.info("=> Connected to Target Host IP of MySQL server successfully! - Target Host IP: "+hostAddress)
        self.myDb = connResult[1]
      else:
        errorMsg ="=> Can't connect to MySQL server! with:\n+ hostAddress: "+hostAddress+"\n+ hostVpnAddress: "+hostVpnAddress+"\n+ hostDdnsUrl: "+hostDdnsUrl
        logger.error(errorMsg)
        raise Exception(errorMsg)
        
    self.myCursor = self.myDb.cursor(dictionary=True) # Xuất dữ liệu dạng dictionary (Giống object)

  #0. Set global timezone
  def setGlobalTimezone(self, timezone='+7:00'): #Asia/Ho_Chi_Minh
    '''
    - `name`: setGlobalTimezone
    - `description`: Đặt lai thời gian timezone của MySQL
    - `parameters`: timezone: Thời gian timezone. Ví dụ: +7:00, Asia/Ho_Chi_Minh,...
    - `return`: None
    - `Example`: mySqlClass.setGlobalTimezone('+7:00')
    '''
    self.timezone = timezone
    self.myCursor.execute("SET GLOBAL time_zone = '"+str(timezone)+"';")
    self.myDb.commit()
    
  #1. SELECT: Truy vấn cơ sở dũ liệu
  def customSelect(self, queryString):
    '''
    - `name`: customSelect
    - `description`: Truy vấn SELECT theo câu lệnh SQL được truyền vào.
    - `parameters`: queryString: Câu lệnh SQL
    - `return`: Trả về dữ liệu dạng list.
    - `Example`:
      1. readData = sql.customSelect("SELECT * FROM vn_20_scanned_list LIMIT 1")
      2. pprint(readData)
    - `PIC`:
      - ✨`Conmand`:  PIC/002.png
      - ✨`Result`:  PIC/001.png
    '''
    self.myCursor.execute(queryString)
    return self.myCursor.fetchall()
  
  def selectCondition(self, table="" , selectColumn="*" , whereCondition=""):
    '''
    - `name`: selectCondition
    - `description`: Truy vấn SELECT theo điều kiện WHERE
    - `parameters`:
      - `tableName`: Tên bảng
      - `selectColumn`: Cột cần lấy
      - `whereCondition`: Điều kiện WHERE
    - `return`: Trả về dữ liệu dạng list.
    - `Example`: readData = sql.selectCondition("vn_20_scanned_list","*","id = 3508")
    '''
    queryString = "SELECT "+str(selectColumn)+" FROM "+str(table)+" WHERE "+str(whereCondition)+";"
    self.myCursor.execute(queryString)
    return self.myCursor.fetchall()
  
  #2. UPDATE:Cập nhật giá trị trong cơ sở dữ liệu
  def updateRow(self, table, updateString, whereCondition):
    '''
    - `name`: updateRow
    - `description`: Cập nhật giá trị trong cơ sở dữ liệu
    - `parameters`:
      - `tableName`: Tên bảng
      - `updateString`: Dữ liệu cột và value cần cập nhật.\\
         Ví dụ: "name = 'Tran Van A' , age = 20"
      - `whereCondition`: Điều kiện WHERE
    - `return`: None
    - `Example`:
      - B1: updateString = "video_id = 'test2', key_word = 'test2', key_type = 'test2', status = 'test2', timestamp = CURRENT_TIMESTAMP"
      - B2: sql.updateRow("vn_20_scanned_list", updateString, whereCondition="id = 2")
    - `PIC`:
      - ✨ PIC/003.png
    '''
    queryString = "UPDATE "+str(table)+" SET "+str(updateString)+" WHERE "+str(whereCondition)+";"
    self.myCursor.execute(queryString)
    self.myDb.commit()

  #3. INSERT: Thêm dữ liệu vào cơ sở dữ liệu
  def insertRow(self, table, columnString, valueString):
    '''
    - `name`: insertRow
    - `description`: Thêm dữ liệu vào cơ sở dữ liệu
    - `parameters`:
      - `tableName`: Tên bảng
      - `columnString`: Danh sách cột
      - `valueString`: Danh sách giá trị
    - `return`: None
    - `Example`:
      - B1: columnString = "id, video_id, video_link, key_word, key_type, status, timestamp"
      - B2: valueString  = "1, 'test', 'test', '', '', '-999', CURRENT_TIMESTAMP"
      - B3: sql.insertRow("vn_20_scanned_list", columnString, valueString)
    - `PIC`:
      - ✨ PIC/004.png
    '''
    try:
      queryString = "INSERT INTO "+str(table)+" ("+str(columnString)+") VALUES ("+str(valueString)+");"
      self.myCursor.execute(queryString)
      self.myDb.commit()
    except Exception as e:
      if ("Duplicate entry" in str(e)):
        logger.warning(">>> Querry String: "+str(queryString))
        logger.warning("Duplicate entry: "+str(e))
      else:
        logger.error(">>> Querry String: "+str(queryString))
        logger.error(">>> Error: "+str(e))

        
  #4. DELETE: Xóa dữ liệu khỏi cơ sở dữ liệu
  def deleteRow(self, table, whereCondition):
    '''
    - `name`: deleteRow
    - `description`: Xóa dữ liệu khỏi cơ sở dữ liệu
    - `parameters`:
      - `tableName`: Tên bảng
      - `whereCondition`: Điều kiện WHERE
    - `return`: None
    - `Example`:
      - sql.deleteRow("vn_20_scanned_list", "id = 2")
    - `PIC`:
      - ✨ PIC/005.png
    '''
    queryString = "DELETE FROM "+str(table)+" WHERE "+str(whereCondition)+";"
    self.myCursor.execute(queryString)
    self.myDb.commit()

  #5. DELETE All Rows: Xóa tất cả dòng dữ liệu khỏi bảng
  def deleteAllRows(self, table):
    '''
    - `name`: deleteAllRows
    - `description`: Xóa tất cả dòng dữ liệu khỏi bảng
    - `parameters`:
      - `tableName`: Tên bảng
    - `return`: None
    - `Example`:
      - sql.deleteAllRows("vn_20_scanned_list")
    '''
    queryString = "DELETE FROM "+str(table)+";"
    self.myCursor.execute(queryString)
    self.myDb.commit()
    
  #6. SELECT COUNT: Đếm số dòng dữ liệu trong bảng
  def countAllRows(self, tableName):
    '''
    - `name`: countAllRows
    - `description`: Đếm số dòng dữ liệu trong bảng
    - `parameters`:
      - `tableName`: Tên bảng
    - `return`: Số dòng dữ liệu trong bảng
    - `Example`:
      - sql.countAllRows("vn_20_scanned_list")
    - `PIC`:
      - ✨ PIC/006.png
    '''
    queryString = "SELECT COUNT(*) FROM "+str(tableName)+";"
    self.myCursor.execute(queryString)
    return self.myCursor.fetchall()[0]['COUNT(*)']
  
  def countRowWithCondition(self, table, whereCondition):
    '''
    - `name`: countRowWithCondition
    - `description`: Đếm số dòng dữ liệu trong bảng với điều kiện WHERE
    - `parameters`:
      - `tableName`: Tên bảng
      - `whereCondition`: Điều kiện WHERE
    - `return`: Số dòng dữ liệu trong bảng
    - `Example`:
      - sql.countRowWithCondition("vn_20_scanned_list", "id > 3700")
    - `PIC`:
      - ✨ PIC/007.png
    '''
    queryString = "SELECT COUNT(*) FROM "+str(table)+" WHERE "+str(whereCondition)+";"
    self.myCursor.execute(queryString)
    return self.myCursor.fetchall()[0]['COUNT(*)']
   
  #7. Finding the Average Value in a Column
  def findAvgValue(self, tableName, columnName, whereCondition=""):
    '''
    - `name`: findAvgValue
    - `description`: Tính giá trị trung bình của cột (Bằng tổng giá trị cột / số dòng dữ liệu)
    - `parameters`:
      - `tableName`: Tên bảng
      - `columnName`: Tên cột
      - `whereCondition`: Điều kiện WHERE
    - `return`: Giá trị trung bình của cột
    - `Example`:
      - EX1: sql.findAvgValue("vn_20_scanned_list", "id", "id > 3700")
      - EX2: sql.findAvgValue("vn_20_scanned_list", "id"")
    - `PIC`:
      - ✨ PIC/008.png
    '''
    if whereCondition == "":
      queryString = "SELECT AVG("+str(columnName)+") FROM "+str(tableName)+";"
    else:
      queryString = "SELECT AVG("+str(columnName)+") FROM "+str(tableName)+" WHERE "+str(whereCondition)+";"
    self.myCursor.execute(queryString)
    return self.myCursor.fetchall()[0]['AVG('+str(columnName)+')']
  
  #8. Finding the Sum of Values in a Column
  def findSumValue(self, tableName, columnName, whereCondition=""):
    '''
    - `name`: findSumValue
    - `description`: Tính tổng giá trị của cột
    - `parameters`:
      - `tableName`: Tên bảng
      - `columnName`: Tên cột
      - `whereCondition`: Điều kiện WHERE
    - `return`: Tổng giá trị của cột
    - `Example`:
      - EX1: sql.findSumValue("vn_20_scanned_list", "id", "id > 3700")
      - EX2: sql.findSumValue("vn_20_scanned_list", "id"")
    - `PIC`:
      - ✨ PIC/009.png
    '''
    if whereCondition == "":
      queryString = "SELECT SUM("+str(columnName)+") FROM "+str(tableName)+";"
    else:
      queryString = "SELECT SUM("+str(columnName)+") FROM "+str(tableName)+" WHERE "+str(whereCondition)+";"
    self.myCursor.execute(queryString)
    return self.myCursor.fetchall()[0]['SUM('+str(columnName)+')']
  
  #9. Finding the Max Value in a Column
  def findMaxValue(self, tableName, columnName, whereCondition=""):
    '''
    - `name`: findMaxValue
    - `description`:  Tìm giá trị lớn nhất của cột
    - `parameters`:
      - `tableName`: Tên bảng
      - `columnName`: Tên cột
      - `whereCondition`: Điều kiện WHERE
    - `return`: Giá trị lớn nhất của cột
    - `Example`:
      - EX1: sql.findMaxValue("vn_20_scanned_list", "id", "id > 3700")
      - EX2: sql.findMaxValue("vn_20_scanned_list", "id"")
    - `PIC`:
      - ✨ PIC/010.png
    '''
    if whereCondition == "":
      queryString = "SELECT MAX("+str(columnName)+") FROM "+str(tableName)+";"
    else:
      queryString = "SELECT MAX("+str(columnName)+") FROM "+str(tableName)+" WHERE "+str(whereCondition)+";"
    self.myCursor.execute(queryString)
    return self.myCursor.fetchall()[0]['MAX('+str(columnName)+')']
  
  #10. Finding the Min Value in a Column
  def findMinValue(self, tableName, columnName, whereCondition=""):
    '''
    - `name`: findMinValue
    - `description`: Tìm giá trị nhỏ nhất của cột
    - `parameters`:
      - `tableName`: Tên bảng
      - `columnName`: Tên cột
      - `whereCondition`: Điều kiện WHERE
    - `return`: Giá trị nhỏ nhất của cột
    - `Example`:
      - EX1: sql.findMinValue("vn_20_scanned_list", "id", "id > 3700")
      - EX2: sql.findMinValue("vn_20_scanned_list", "id"")
    - `PIC`:
      - ✨ PIC/011.png
    '''
    if whereCondition == "":
      queryString = "SELECT MIN("+str(columnName)+") FROM "+str(tableName)+";"
    else:
      queryString = "SELECT MIN("+str(columnName)+") FROM "+str(tableName)+" WHERE "+str(whereCondition)+";"
    self.myCursor.execute(queryString)
    return self.myCursor.fetchall()[0]['MIN('+str(columnName)+')']
  
  def checkConnectionToReconnect(self):
    '''Kiểm tra kết nối và tự động kết nối lại nếu mất kết nối.\n
    Tránh lỗi mất kết nối: "2013 (HY000): Lost connection to MySQL server during query"'''
    if self.myDb.is_connected() == False:
      logger.warning("MySQL connection was lost => Reconected")
      self.myDb.reconnect() #Tránh lỗi mất kết nối: "2013 (HY000): Lost connection to MySQL server during query"


  
  
  

  

  

  