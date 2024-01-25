import __init
from task_args import *
from time import sleep,time
from Conf.loggingSetup import *
from Library.A5_MySQL.mySql_Wrap import genWhereCond, mySql_Wrapper as MYSQL
from pprint import pprint

#MySQL Configurations ##########################################
#🚨 CHÚ Ý: Đặt con trỏ vào MYSQL() và nhấn F12 để xem thêm thông tin về các tham số truyền vào.
gxMysql = MYSQL(hostAddress    = '192.168.68.143',            #Địa chỉ IP của MySQL server nội bộ tại nhà
                hostVpnAddress = '10.2.0.0',                  #Địa chỉ IP của MySQL server nội bộ được thiết đặt trong mạng VPN
                hostDdnsUrl    = 'lotus1104.synology.me',     #Địa chỉ URL của MySQL server thiết đặt trong mạng WAN (DDNS)
                database       = 'tik_vn_nancy_1',
                username       = 'root',
                password       = 'admin')
################################################################

readData = gxMysql.customSelect("SELECT * FROM vn_20_scanned_list LIMIT 1")
pprint(readData)

################################################################
# OUTPUT:
# ==============================================================
# === WORKSPACE PATH: D:\Database\GIT\LOTUS_Python_Framework ===
# ==============================================================
# Pinging 192.168.68.143 with 32 bytes of data:
# Request timed out.

# Ping statistics for 192.168.68.143:
#     Packets: Sent = 1, Received = 0, Lost = 1 (100% loss),

# Pinging 10.2.0.0 with 32 bytes of data:
# Reply from 10.2.0.0: bytes=32 time=15ms TTL=64

# Ping statistics for 10.2.0.0:
#     Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),
# Approximate round trip times in milli-seconds:
#     Minimum = 15ms, Maximum = 15ms, Average = 15ms
# [2023-03-04 17:26:37,535][INFO    ] => Connected to MySQL server (VPN) successfully! - Host IP (VPN): 10.2.0.0
# [{'id': 16466,
#   'key_type': 'bind',
#   'key_word': 'tinhgia727',
#   'status': '-999',
#   'timestamp': datetime.datetime(2023, 3, 3, 2, 54, 27),
#   'video_id': '7205989372875803930',
#   'video_link': 'https://www.tiktok.com/@tinhgia727/video/7205989372875803930',
#   'video_user': 'tinhgia727'}]
# PS D:\Database\GIT\LOTUS_Python_Framework> 