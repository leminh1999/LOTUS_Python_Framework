from PIL import Image
from LotusLib_v1r1 import *


newCyberImage = Image.open('cyberNationIp_2.png')
checkColor = newCyberImage.getpixel((160,15))
if 245 < checkColor[0] and 194<checkColor[1]<214 and checkColor[2]<10:
  print("OK")
else:
  print("NO")
