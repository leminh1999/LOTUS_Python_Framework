# -*- coding: utf-8 -*-
# source: https://www.smartfile.com/blog/what-is-good-logging-in-python/
import logging
import datetime
import platform
import os
osName = platform.uname()[0]
nodeName = platform.uname()[1]

# Tạo thư mục Logs
if os.path.exists("Logs") == False:
  os.mkdir("Logs")
  
curDay  = datetime.datetime.now()
logName = 'Logs\Logfile_'+str(nodeName)+'_'+str(curDay.day)+str(curDay.strftime("%b"))+'_'+str(curDay.strftime("%H.%M.%S"))+".txt"




#Hướng dẫn sử dụng in biến#
# EX: logger.info('----- MAIN TASK: đăng nhập Tài Khoản: %s,%s -----',name,password)




################################################################################################
################################ USER DEFINE CODE ##############################################
################################################################################################
#1. Set level of logfile and console print out
#   a. DEBUG   : Thông tin chi tiết, thường là thông tin để tìm lỗi.
#   b. INFO    : Là các thông báo thông thường, các thông tin in ra khi chương trình chạy theo đúng kịch bản.
#   c. WARNING : Thông báo khi nghi vấn bất thường hoặc lỗi có thể xảy ra, tuy nhiên chương trình vẫn có thể hoạt động.
#   d. ERROR   : Lỗi. Chương trình có thể không hoạt động được một số chức năng. Thường thì nên dùng khi bắt được exception.
#   e. CRITICAL: Lỗi nghiêm trọng. Chương trình khi gặp lỗi nghiêm trọng không thể giải quyết được và bắt buộc phải dừng lại.
LEVEL_PRINT_LOGFILE = 'DEBUG'
LEVEL_PRINT_CONSOLE = 'DEBUG'

#2. Set file name for output file
# LOG_FILE_NAME = 'RunLogFile.txt'
LOG_FILE_NAME = logName
#3. Define output format display
NEW_FORMAT = '[%(asctime)s][%(levelname)s] %(filename)s:%(funcName)s()[Line %(lineno)d] - %(message)s'

#4. Tạo file log mới và ghi đề lên ở mỗi lần chạy ghi 1, ghi nối tiếp file cũ ghi 0
OVER_WRITE_LOG_FILE = 1


################################################################################################
################################ DON'T TOUCH CODE ##############################################
################################################################################################
# create the logging instance for logging to file only
logger = logging.getLogger('SmartfileTest')
# create the handler for the main logger
if OVER_WRITE_LOG_FILE == 1:
  file_logger = logging.FileHandler(LOG_FILE_NAME,'w','utf-8')
else:
  file_logger = logging.FileHandler(LOG_FILE_NAME,'utf-8')

file_logger_format = logging.Formatter(NEW_FORMAT)

# tell the handler to use the above format
file_logger.setFormatter(file_logger_format)

# finally, add the handler to the base logger
logger.addHandler(file_logger)

# remember that by default, logging will start at \'warning\' unless
# we set it manually
if LEVEL_PRINT_LOGFILE == "DEBUG"   : logger.setLevel(logging.DEBUG) #Thiết lập mức độ in ra console
if LEVEL_PRINT_LOGFILE == "INFO"    : logger.setLevel(logging.INFO) #Thiết lập mức độ in ra console
if LEVEL_PRINT_LOGFILE == "WARNING" : logger.setLevel(logging.WARNING) #Thiết lập mức độ in ra console
if LEVEL_PRINT_LOGFILE == "ERROR"   : logger.setLevel(logging.ERROR) #Thiết lập mức độ in ra console
if LEVEL_PRINT_LOGFILE == "CRITICAL": logger.setLevel(logging.CRITICAL) #Thiết lập mức độ in ra console

# source: https://www.smartfile.com/blog/what-is-good-logging-in-python/
# now we can add the console logging
console = logging.StreamHandler()
console.setFormatter(file_logger_format)
if LEVEL_PRINT_CONSOLE == "DEBUG"   : console.setLevel(logging.DEBUG) #Thiết lập mức độ in ra console
if LEVEL_PRINT_CONSOLE == "INFO"    : console.setLevel(logging.INFO) #Thiết lập mức độ in ra console
if LEVEL_PRINT_CONSOLE == "WARNING" : console.setLevel(logging.WARNING) #Thiết lập mức độ in ra console
if LEVEL_PRINT_CONSOLE == "ERROR"   : console.setLevel(logging.ERROR) #Thiết lập mức độ in ra console
if LEVEL_PRINT_CONSOLE == "CRITICAL": console.setLevel(logging.CRITICAL) #Thiết lập mức độ in ra console


logging.getLogger('SmartfileTest').addHandler(console)

# log some stuff!
#logger.debug("This is a debug message!")
#logger.info("This is an info message!")
#logger.warning("This is a warning message!")