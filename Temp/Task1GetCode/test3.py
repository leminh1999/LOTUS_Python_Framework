import os
import datetime
import html
import shutil
import urllib.request
from A2_GetLink_ImportList import *
# os.rename('tempComment.png','ACB.png')
# # os.rename('ACB.png',a+".png")
# x = datetime.datetime.now()
# # t = x.hour*60 + x.minute
# print (str(datetime.datetime.now()).split(".")[0])


# import urllib.request
# videoSource2 = 'https://v9-vn.tiktokcdn.com/c22233af211f6ccff796f9e9c04e671c/604e0088/video/tos/useast2a/tos-useast2a-pve-0068/40140660650a490d8650f8f376b43e26/?a=1233&br=1650&bt=825&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=0&ds=3&er=&l=202103140624090102340820724106E2BF&lr=tiktok_m&mime_type=video_mp4&pl=0&qs=0&rc=M2hvNWhxdTtrNDMzZjczM0ApaWZpaWYzZTs0N2Q2ODg0PGduZmY0ZDZlbTNgLS1eMTZzczAtMTYxYmI0MzQzNDRhNS06Yw%3D%3D&vl=&vr='
# file_name = '../PostData/Vol7/trial_video.mp4' 
# urllib.request.urlretrieve(dwn_link, file_name)

# videoSource  = "https://v16-web.tiktok.com/video/tos/alisg/tos-alisg-pve-0037/8e01b43160e346d6a484bbc68bd2d403/?a=1988&br=2328&bt=1164&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=3&ds=3&er=&expire=1615732657&l=20210314083637010234106137230241EB&lr=tiktok&mime_type=video_mp4&pl=0&policy=2&qs=0&rc=M3M1aWpqNjd0NDMzZzgzM0ApZDUzZzNnNTw4Nzc5aWUzZWdmNW4wbWxsYzJgLS0yLzRzczBhLjZhMDJeL2EyNjZgNV86Yw%3D%3D&signature=284f1f8ac4edea0402f3880a7736a499&tk=tt_webid_v2&vl=&vr="
# file_name = "../PostData/Vol7/6720_6938824217437719810.mp4"
videoSource2 = "https://v16-web.tiktok.com/video/tos/alisg/tos-alisg-pve-0037/8e01b43160e346d6a484bbc68bd2d403/?a=1988&br=2328&bt=1164&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=3&ds=3&er=&expire=1615732657&l=20210314083637010234106137230241EB&lr=tiktok&mime_type=video_mp4&pl=0&policy=2&qs=0&rc=M3M1aWpqNjd0NDMzZzgzM0ApZDUzZzNnNTw4Nzc5aWUzZWdmNW4wbWxsYzJgLS0yLzRzczBhLjZhMDJeL2EyNjZgNV86Yw%3D%3D&signature=284f1f8ac4edea0402f3880a7736a499&tk=tt_webid_v2&vl=&vr="
videoSource3 = "https://v16.tiktokcdn.com/22c60d4156590f243511f2f32197daff/604e38f9/video/tos/alisg/tos-alisg-pve-0037/1d897aac4af74d1e9112dbc344a3908c/?a=1180&br=3334&bt=1667&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=3&ds=3&er=&l=202103141025190101150790700D048CB9&lr=tiktok&mime_type=video_mp4&pl=0&qs=0&rc=MzpkNDs7Z282MzMzMzgzM0ApZTY5Zzc7NTs5NzhpNjo7O2dlYHJxbHNpMXFgLS1fLzRzczAvYjIuXmFfMzEuYTMyYmE6Yw%3D%3D&vl=&vr="
# file_name2 = "abc.mp4"
# urllib.request.urlretrieve(videoSource2, file_name2)

# pyperclip.copy(videoSource3) #Copy nội dung tin nhắn vào clipboard
# GUI.click(100,1060)
# LotusLib.delay(1500)

# def saveVideoClip (videoURL,videoName):
#   #Đổi đường dẫn Linux "../../" sang Window "..\..\"
#   print(videoName)
#   videoNameWin = str(videoName).replace("/","\\")
#   print(videoName)
#   #Mở một tab mới và chờ tab mới hiện ra Images/16s.png
#   GUI.hotkey('ctrl','t')
#   LotusLib.waitColor((400,20),(255,255,255),10,15)
#   pyperclip.copy(str(videoURL)) #Copy nội dung tin nhắn vào clipboard
#   GUI.hotkey('ctrl','v')
#   LotusLib.delay(200)
#   GUI.press('enter')
#   LotusLib.delay(1000)
#   #Chờ cho màn hình load được video (Màn hình sẽ không còn màu trắng của trang Blank page)
#   LotusLib.waitNotColor((100,900),(255,255,255),10,15) #Chờ cho màu nền trắng của trang Blank page biến mất
#   LotusLib.delay(300)
#   LotusLib.waitNotColor((950,570),(0,0,0),10,15) #Chờ cho màu đen ở giữa màn hình biến mất -> Video đang chạy Images/17b.png
#   LotusLib.delay(1000)
#   GUI.hotkey('ctrl','s') #Gọi cửa sổ save
#   LotusLib.delay(300)
#   LotusLib.waitColor((1860,900),(255,255,255),10,15) #Chờ cho màu nền trắng của cửa sổ Save xuất hiện. Yêu cầu cửa sổ Save Maximize. Images/18b.png
#   pyperclip.copy(str(videoNameWin)) #Copy nội dung tin nhắn vào clipboard
#   GUI.hotkey('ctrl','v')
#   LotusLib.delay(200)
#   GUI.press('enter')
#   LotusLib.delay(1000)
#   LotusLib.waitNotColor((1901,1021),(0,0,0),10,15) #Chờ dòng trạng thái của nút tải video xuất hiện Images/19b.png
#   LotusLib.delay(100)
#   GUI.click(1901,1021) # Đóng dòng trạng thái tải video của Chrome Images/19b.png
#   LotusLib.delay(100)
#   GUI.click(1901,1021) # Đóng dòng trạng thái tải video của Chrome Images/19b.png
#   LotusLib.delay(100)
#   GUI.click(470,16) # Đóng Tab thứ 2
#   LotusLib.delay(500)
#   GUI.click(470,16) # Đóng Tab thứ 2


a = LotusLib.wait3NotColor((55,33),(60,60,60),10,(1861,17),(60,60,60),10,(50,940),(51,51,51),10,10)
print(a)