import __init
from Library.A5_MySQL.Components.mySql import *

class mySql_Wrapper(mySqlClass): 
  '''
  Initialize:
  `MYSQL(hostAddress,hostVpnAddress,hostDdnsUrl,database,username,password)`\n
  Nếu hostVpnAddress và hostDdnsUrl không được khai báo thì sẽ kết nối qua hostAddress chỉ định.
  Nếu một trong hai hoặc cả 2 thông số trên được khia báo thì chương trình sẽ dò xem máy hiện tại và máy MySQL server có nằm trong mạng LAN > VPN > WAN (DDNS) hay không.
  Giúp tối ưu tốc độ và hỗ trợ một khai báo duy nhất cho truy cập của máy host từ bất kỳ nơi nào.\n
  Thứ tự kết nối:
  1. Nếu host đang chạy script và máy target ở trong cùng mạng LAN thì trả về kết nối MySQL server qua hostAddress (Địa chỉ IP của máy target trong mạng LAN)
  2. Nếu host đang chạy script và máy target ở trong cùng mạng VPN thì trả về kết nối MySQL server qua hostVpnAddress (Địa chỉ IP của máy target trong mạng VPN)
  3. Nếu host đang chạy script và máy target ở trong cùng mạng WAN (Wide Area Network) thì trả về kết nối MySQL server qua hostDdnsUrl (Địa chỉ URL của máy target trong mạng WAN)
  4. Nếu không kết nối được MySQL server qua các địa chỉ IP và URL trên thì trả về kết nối MySQL server qua targetLanIp (Địa chỉ IP của máy target trong mạng LAN)
  \nVí dụ:
  gxMysql = MYSQL(hostAddress="192.168.68.143", hostVpnAddress = "10.2.0.0", hostDdnsUrl = "lotus1104.synology.me",...)
  => Ưu tiên kết nối với mạng LAN trước, nếu không thì kết nối với mạng VPN, nếu không thì kết nối với mạng WAN (DDNS)
  '''
  pass
