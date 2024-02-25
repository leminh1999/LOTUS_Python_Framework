##################################################################
# Vai trò:
#  - Quản lý và cập nhật danh sách khởi tạo các container theo thời gian như crontab.
#  - Kết nối vào gửi thông tin quản lý lên Zabbix Server. Bao gồm:
#    + Tên từng channel, số lượng following, like, video.
#    + Trạng thái hoạt động, lỗi, hình lỗi.
#  - Force chạy một task tức thì và xuất VNC nếu bật.
# Hoạt động:
#  - Kiểm tra Timestamp của bảng manager có bị cập nhật và enable có đang bật không? (Nếu enable là 0 thì thêm # và đầu contab)
#  - Force số lần chạy của mỗi task.
#
import __init
import MyAPP.TiktopApp.GX.DynamicParamPC as PARAM
from Conf.loggingSetup import *
try:
  from MyAPP.TiktopApp.GX.TaskManClass import *
except Exception as e:
  if "Can't connect to MySQL server" in str(e):
    from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
    #Kiểm tra kết nối với MySQL server
    for i in range(1,24):
      try:
        #Phục hồi lại dữ liệu MySQL server bị mất trước đó x giờ.
        logger.info("Try to restore MySQL server...last "+str(i)+"h")
        command = "mysql -u root -padmin < /mySqlBackupDir/backup_last_"+str(i)+"h.sql"
        dockerExec="docker exec -it lotus_mysql bash -c '"+command+"'"
        os.system(dockerExec)
        #Access to MySQL server
        sql = MYSQL(hostAddress = PARAM.MYSQL_HOST,database= "tik_0_man",username= PARAM.MYSQL_USER,password = PARAM.MYSQL_PASS)
        #Access OK
        from MyAPP.TiktopApp.GX.TaskManClass import *
        break
      except Exception as e:
        logger.error(str(e))
        if i == 24:
          logger.critical("Can't connect to MySQL server: "+str(e))
          exit(0)
    
    
  



from SystemManager.system_Wrap import *
MAN = TaskManager


########### MAIN ############
if os.path.isfile(PARAM.PATH_LAST_MAN_UPDATE): os.remove(PARAM.PATH_LAST_MAN_UPDATE) #Lần chạy đầu tiên.
#print confirm("Do you want to update Lotus Framework Lite & NAS Scripts?") then get input from user
if SYS.pcInfo.pcName() == "CMEV-PC157":
  print("Cập nhật Master Code cho các container? (Y/N): ",end="")
  if input() == "Y" or input() == "y":
      logger.info("### Update Lotus Framework Lite & NAS Scripts ###")
      MAN.genLotusFrameworkLite() #Generate Lotus Framework Lite Only Execute by CMEV-PC157
      print("")
      print("\033[1;31;40m##########################################################################################\033[0m")
      print("\033[1;31;40m### CẬP NHẬT XONG MASTER CODE - Máy docker cần chạy lại screen cho Tik_Man.sh để Apply ###\033[0m")
      print("\033[1;31;40m##########################################################################################\033[0m")
      exit(0)
  else:
    logger.warning("### Not Update Lotus Framework Lite & NAS Scripts ###")

if SYS.pcInfo.pcName() == "CMEV-PC157":
  MAN.forceTaskRun(channelId=1, taskNum=1, vncNum=1, debugNum=1)

while True:
  MAN.checkChanelConfigTableChangedByHandToUpdateScheduleList() #Kiểm tra MySQL table (channel_config) có channel nào thay đổi bằng tay không. Nếu có thì cập nhật Schedule List cho toàn bộ task con của channel đó.
  MAN.checkTimeToRunInScheduleList() #Kiểm tra xem có task nào đến giờ chạy không. Nếu có thì chạy task đó. Và cập nhật giờ chạy tiếp theo treen MySQL table.
  MAN.checkReqManKillFile(PARAM.REQ_MAN_KILL) #Kiểm tra xem có file yêu cầu kill task không. Nếu có thì kill task đó.
  MAN.killLongTask(timeLimitSec=30*60, taskNameContain="_con_") #Kill Container chạy quá 30 phút.
  #print data time in HH:MM:SS
  print("=> Cur Time: "+datetime.datetime.now().strftime("%H:%M:%S"),end="\r")
  time.sleep(1)

