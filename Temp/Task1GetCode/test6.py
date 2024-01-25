import re
import datetime
import time

pat1 = '^[0-9.,KMkm]+$'
string = '01.23586K10M0'
regex = re.compile(pat1)
mo2 = regex.search(string) != None
print(mo2)

curDay  = datetime.datetime.now().strftime("%X")
print(curDay)

a = "002"

print(eval("002".lstrip('0')+"*60"))

b = "00:01:22"

c = re.sub(r'0(\d)',r'\1',b)

print(c)