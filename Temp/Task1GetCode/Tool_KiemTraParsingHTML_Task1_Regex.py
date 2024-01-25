# Code này có chức năng Parsing HTML code từ file README.html sang các thông tin cần lấy
from A4_GetLink_Function import *
from Global.loggingSetup import *

task1GetLink = Task1GetLink
tikTopTaskMon.task2_running_flag  = "1"
try:
  file = open("README.html", "r",encoding="utf8", errors="surrogateescape")
  htmlCode = file.readline()

  logger.info(">>>>> STEP 5.1 Parsing dữ liệu từ web <<<<<")
  task1GetLink.parsingHTML_task2(str(htmlCode),minPost=1,debug=1)
  logger.info("\n=========> END PARSING HTML CODE")

  file.close()

except Exception as errMessage:
  logger.debug("!!!! ERROR !!!!")
  logger.error(errMessage)
finally:
  exit()

