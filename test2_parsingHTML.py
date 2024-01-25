import __init
from lxml import html
from time import sleep
from Library.A1_PyAutoGUI.pyAutoGui_Wrap import pyAutoGui_Remap as GUI
from Library.A2_LOTUS.lotus_Wrap import rgb,lotus_Remap as LOTUS
import pyperclip

#########################################################
# Name: getCode
# Function: Kiểm tra mở của sổ xem code và load hết code
#           rồi trả về code HTML
# Parameter: None
# Return: Trả về htmlCode dạng string
#########################################################
def getCode():
  GUI.mouse.click(1451,116) #Click vào tab Element. Images/7s.png
  sleep(0.5)
  GUI.mouse.moveTo(1830,200) #Di chuyển chuột vào vùng code có thể cuộn chuột được.
  sleep(0.2)
  GUI.mouse.scroll(2000) #Scroll lên trên cùng
  sleep(0.5)
  GUI.mouse.click(1400,140) #Click vào vị trí thẻ <!DOCUMENT html>.
  LOTUS.color.waitColor((1700,140),rgb(207,232,252),20,15,0) # đợi dòng được chọn
  sleep(0.3)
  GUI.key.press('down') #Xuống thẻ <html>
  sleep(0.5)
  #Collapse children
  GUI.key.hotkey('shift','f10') # Images/58s.png Mở bẳng dropbox
  sleep(1)
  GUI.key.press('c')
  sleep(0.5)
  GUI.key.press('c') 
  sleep(0.5)
  GUI.key.press('c')
  sleep(0.5)
  GUI.key.press('enter') #Chọn dòng Collapse children
  sleep(1)
  GUI.key.press('esc') # Images/58s.png .Thoát bảng dropbox nếu nó không tự tắt
  sleep(0.5)
  #Copy nội dung html body
  GUI.key.press('down')
  sleep(0.5)
  GUI.key.press('down')
  sleep(0.5)
  GUI.key.hotkey('shift','f10') # Images/58s.png Mở bẳng dropbox
  sleep(1)
  GUI.key.press('c')
  sleep(0.5)
  GUI.key.press('c')
  sleep(0.5)
  GUI.key.press('enter')
  sleep(0.5)
  GUI.key.press('enter') #Chọn "copy element"
  sleep(0.5)
  GUI.key.press('up') #Tránh màn hình bị xanh do đang chọn code
  sleep(1)
  htmlCode = pyperclip.paste() #Gán html code từ clipboard vào biến
  htmlCode = htmlCode.replace('\n',' ')
  
  return htmlCode
  
#Tham khảo: https://stackoverflow.com/questions/11465555/can-we-use-xpath-with-beautifulsoup

# #1. Load HTML file to variable
# #open text file in read mode
# text_file = open("MyAPP\TiktopApp\GX\HTM_PROFILE.html", "r", encoding="utf8")
# #read whole file to a string
# htmlCode = text_file.read()
# #close file
# text_file.close()
# htmlCode = htmlCode.replace('\n',' ')

GUI.mouse.click(x=120,y=1070) #Vị trí Chrome
sleep(3)
GUI.mouse.rightClick(x=0,y=120) #Vị trí Chrome
sleep(1)
GUI.key.press('up');sleep(0.5)
GUI.key.press('enter');sleep(4)
htmlCode = getCode()

#2. Parse HTML code to get data
# re.sub(r'.*?author-uniqueId.*?\>(.*?)<.*',r'\1',htmlParsing0).strip()

tree = html.fromstring(htmlCode)
#This will create a list of buyers:
newClipLink = tree.xpath("//div[contains(@class,'DivItemContainerV2')]//a[contains(@href,'video')]/@href")[0]
newClipId = newClipLink.split("/")[-1]
newClipUser = newClipLink.split("/")[-3].split("@")[-1]

print("newClipId: ",newClipId)
print("newClipUser: ",newClipUser)
print("newClipLink: ",newClipLink)

print("==== Finish ====")