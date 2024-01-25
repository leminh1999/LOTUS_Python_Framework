# importing the requests library
import requests
from pprint import pprint
  
# api-endpoint
URL = "http://rest.esms.vn/MainService.svc/json/GetBalance/BFC842F60541885DB7EB57AB37DE5C/A29AA58CADDD6813537BCB81A9F5A8"
URL1 = "https://rest.esms.vn/MainService.svc/json/SendMultipleMessage_V4_get?Phone=84769807636&Content=DemoText&ApiKey=BFC842F60541885DB7EB57AB37DE5C&SecretKey=A29AA58CADDD6813537BCB81A9F5A8&SmsType=8&Sandbox=1"
URL2 = "https://rest.esms.vn/MainService.svc/json/SendMultipleMessage_V4_get?Phone=0908549354&Content=DemoText&ApiKey=BFC842F60541885DB7EB57AB37DE5C&SecretKey=A29AA58CADDD6813537BCB81A9F5A8&SmsType=2&Brandname=Baotrixemay&Sandbox=0"
URL3 = "https://rest.esms.vn/MainService.svc/json/SendMultipleMessage_V4_get?Phone=0934193965&Content=NhanDuocTinNhanKhongVo&ApiKey=BFC842F60541885DB7EB57AB37DE5C&SecretKey=A29AA58CADDD6813537BCB81A9F5A8&SmsType=8&Sandbox=0"
URL4 = "https://rest.esms.vn/MainService.svc/json/SendMultipleMessage_V4_get?Phone=0379631953&Content=NhanDuocTinNhanKhongVo&ApiKey=BFC842F60541885DB7EB57AB37DE5C&SecretKey=A29AA58CADDD6813537BCB81A9F5A8&SmsType=8&Sandbox=0"
# URL5 = "http://rest.esms.vn/MainService.svc/{ResponseType}/GetListBrandname/{ApiKey}/{SecretKey}"
  
# sending get request and saving the response as response object
r = requests.get(url = URL2)

# extracting data in json format
data = r.json()
pprint(data)