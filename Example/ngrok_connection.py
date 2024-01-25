import __init
from time import sleep
from Library.A1_PyAutoGUI.pyAutoGui_Wrap import pyAutoGui_Remap as GUI
from Library.A2_LOTUS.lotus_Wrap import lotus_Remap as LOTUS
from Library.A3_Selenium.selenium_Wrap import WEB, seleniumIDE_Remap as IDE
from pyngrok import ngrok, conf

#Pic: NgrokToken.png
ngrok.set_auth_token("3YxTA92tC95j8Ya3Mfgji_2W1fXJaUwJiouhrVUEak4") #Token ứng với tài khoản Ngrok. Token có được sau khi sign in ở web và vào phần xem token.

# https://ngrok.com/docs/ngrok-agent/config#config-region
# us -> United States
# eu -> Europe
# ap -> Asia/Pacific
# au -> Australia
# sa -> South America
# jp -> Japan
# in -> India
conf.get_default().region = "ap" #ap -> Asia/Pacific

# Open a HTTP tunnel on the default port 80
# <NgrokTunnel: "http://<public_sub>.ngrok.io" -> "http://localhost:80">
n = 1
while (1):
  try:
    print("=== TIME: ",n)   
    http_tunnel = ngrok.connect(80)
    print("A. DEFAULT TUNNEL: ",http_tunnel,"\n")
    public_url = ngrok.get_tunnels()
    print("B. LIST ORG TUNNEL: ",public_url,"\n")
    print("C. LIST URL TUNNEL: ")
    for i in range (0, len(public_url)):
      print("  "+str(i+1)+". ",public_url[i].public_url)
    print("\n")
    break
  except:
    n += 1
    print("\n")
    GUI.system.countdown(10)
    continue

# Open a SSH tunnel
# <NgrokTunnel: "tcp://0.tcp.ngrok.io:12345" -> "localhost:22">
# ssh_tunnel = ngrok.connect(22, "tcp")

print ("=== END ===")
ngrok.kill()
while(1):
  sleep(10)

