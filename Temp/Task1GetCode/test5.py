import urllib.request
import os

link =  "https://v16.tiktokcdn.com/bda6cb2e7b004f54e6b2d1db650950a3/60c29e50/video/tos/alisg/tos-alisg-pve-0037/9d6fa7d76cd6449aba5a0e5a40d0a4ee/?a=1180&br=3266&bt=1633&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=3&ds=3&er=&l=202106101720360101152290630D249F61&lr=tiktok&mime_type=video_mp4&net=0&pl=0&qs=0&rc=M3N3eDhseXluNTMzODgzM0ApaWRnO2RoZzw0Nzo6M2hoaGdkcTI2XjY1Yy1gLS1kLzRzczFiYV9gLl5fYjFgMy5gYDU6Yw%3D%3D&vl=&vr="
link2 = "https://v16-web.tiktok.com/video/tos/useast2a/tos-useast2a-ve-0068c001/21b776432a83453f9c67af4c54ee4bf4/?a=1988&br=4244&bt=2122&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=0&ds=3&er=&expire=1623370764&l=2021061018185301011501700703282AC0&lr=tiktok_m&mime_type=video_mp4&net=0&pl=0&policy=2&qs=0&rc=M2R3eTxndXNrNjMzNzczM0ApOjQ1NTg5NWQ0N2RoZmZkNmctZjFrNHMzXy1gLS1kMTZzc182NDYxNDIyLjQ1YDBgXy46Yw%3D%3D&signature=99e66a5f43583419a19d9b271264605e&tk=tt_webid_v2&vl=&vr="
file_name = '../trial_video.mp4'
file_name2 = "Z:/Tiktop_Development_Version/Task1GetCode/../PostData/Vol31/5600_6971877842955078917.mp4"


try:
  print("Lưu Video: %s",file_name2.split('/')[-1])
  urllib.request.urlretrieve(link, file_name2+"_script.mp4")
except Exception as errMessage:
  print(errMessage)
  print("ERROR: Không tải được video")
  
  
# import requests 
# from bs4 import BeautifulSoup 
  
# ''' 
# URL of the archive web-page which provides link to 
# all video lectures. It would have been tiring to 
# download each video manually. 
# In this example, we first crawl the webpage to extract 
# all the links and then download videos. 
# '''
  
# # specify the URL of the archive here 
# archive_url = "http://www-personal.umich.edu/~csev/books/py4inf/media/"
  
# def get_video_links(): 
      
#     # create response object 
#     r = requests.get(archive_url) 
      
#     # create beautiful-soup object 
#     soup = BeautifulSoup(r.content,'html5lib') 
      
#     # find all links on web-page 
#     links = soup.findAll('a') 
  
#     # filter the link sending with .mp4 
#     video_links = [archive_url + link['href'] for link in links if link['href'].endswith('mp4')] 
  
#     return video_links 
  
  
# def download_video_series(link): 
#   # obtain filename by splitting url and getting 
#   # last string 
#   file_name = "test.mp4" 

#   print( "Downloading file:%s"%file_name) 
    
#   # create response object 
#   r = requests.get(link, stream = False) 
    
#   # download started 
#   with open(file_name, 'wb') as f: 
#       for chunk in r.iter_content(chunk_size = 1024*1024): 
#           if chunk: 
#               f.write(chunk) 
    
#   print( "%s downloaded!\n"%file_name )
#   return

# download_video_series(link2)
# print(os.stat('test.mp4').st_size)