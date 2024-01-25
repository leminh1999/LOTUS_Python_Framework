# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pyautogui
import platform

####### PARAMETER DEFINE #######
GUI = pyautogui
CHROME_POS = 55,1065   #Position of Chrome on Taskbar
DEFAULT_URL = "https://www.tiktok.com/@meomay22/video/6938120430037339393"
# DEFAULT_URL = "www.tiktok.com/@nam.11.01/video/6984706632072613121"
RESOLUTION = 1920,1080
TIKTOK_USERNAME = ''
TIKTOK_PASSWORD = ''
ADDR_BAR = 755,45 # Vị trí thanh địa chỉ Chrome
VPN_NATION = 'vietnam'

#MySQL Database
MYSQL_IP = "192.168.68.200"
# MYSQL_USER = "tiktop_vn"
# MYSQL_PASS = "ao!6ejM*7h8HtrgR"

if "DevelopmentABCD" in platform.uname()[1]:
  print('##################################################')
  print("########### RUNNING WITH DEVELOPMENT PC ##########")
  print('##################################################')
  MYSQL_DB = "tiktop_vn_devmode"
else:
  print("----------------------------------------")
  print("---------- RUNNING WITH NV PC ----------")
  print("----------------------------------------")
  MYSQL_DB = "tiktop_vn"

# FUN_ICON = "🤣,😅,😂,😁,😝,😄,😆,😏,😸,😹"


## LOTUS DELAY
DELAY100MS = 100
DELAY200MS = 200
DELAY300MS = 300
DELAY400MS = 400
DELAY500MS = 500
DELAY600MS = 600
DELAY800MS = 800
DELAY1000MS = 1000

#### PARSING HTML CODE ####
HTMLSPLIT_USERUNIQ_START     = "<h3 class=\"author-uniqueId jsx-405177348\" style=\"text-decoration: none;\">" #Duy nhất trong code của phần video
HTMLSPLIT_USERUNIQ_END       = "<"                 #Thông thường là </h3>. Chỉ xuất hiện <svg nếu tài khoản có stick xanh Images/26s.png
HTMLSPLIT_USERCUSTOM_START   = "<h4 class=\"author-nickname jsx-405177348\">"                                  #Duy nhất trong code của phần video
HTMLSPLIT_USERCUSTOM_END     = "HAVE NO"
HTMLSPLIT_POSTDAY_START      = "<span class=\"jsx-442964640\"> · </span>"                                       #Duy nhất trong code của phần video
HTMLSPLIT_POSTDAY_END        = "</h4>"
HTMLSPLIT_VIDEOLINK_START    = "https://www.tiktok.com" #Duy nhất trong code của phần video
HTMLSPLIT_VIDEOLINK_END      = "\""
HTMLSPLIT_VIDEOSOURCE_START  = "<video authorid" #Chỉ check tại task2 (khi video được gọi đến)
HTMLSPLIT_VIDEOSOURCE_END    = "/video>"
HTMLSPLIT_LIKENUM_START      = "title=\"like\">"        #Duy nhất trong code của phần video
HTMLSPLIT_LIKENUM_END        = "</strong>"
HTMLSPLIT_COMMENTNUM_START   = "title=\"comment\">"     #Duy nhất trong code của phần video
HTMLSPLIT_COMMENTNUM_END     = "</strong>"
HTMLSPLIT_SHARENUM_START     = "title=\"share\">"       #Duy nhất trong code của phần video
HTMLSPLIT_SHARENUM_END       = "</strong>"

# STEP 5 #
HTMLCODE_NAVICON_POS   = 263,12    # Images/2b.png
HTMLCODE_NAVICON_COLOR = 40,18,22  # Images/2s.png