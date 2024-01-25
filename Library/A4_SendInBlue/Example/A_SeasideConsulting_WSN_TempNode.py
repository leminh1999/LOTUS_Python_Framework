import __init
print("==== START ====")
from time import sleep
from Conf.loggingSetup import *
from Library.A4_SendInBlue.sendInBlue_Wrap import class_contentMode, mailConfig, sendInBlue_Wrapper as SIB
print("==== FINISH IMPORT ====")

import base64
################################
#1. Prepare data               #
################################
#1.1. Encode picture local data to string of base64
picFile = open('Library/A4_SendInBlue/Components/PIC/LocalPicAttachment.png', 'rb')
picEncodeBase64 = str(base64.b64encode(picFile.read()),'utf-8')
picFile.close()
#1.2. Encode zip local data to string of base64
zipFile = open('Library/A4_SendInBlue/Components/PIC/LocalZipAttachment.zip', 'rb')
zipEncodeBase64 = str(base64.b64encode(zipFile.read()),'utf-8')
zipFile.close()
#1.3. Define URL file attachment
urlLink = "https://picsum.photos/200/300.jpg"
#1.4. Embeded image in mail content (Load from zalo)
# PIC: Library/A4_SendInBlue/Components/PIC/zaloQrcodeBase64_html_sourcecode.png
file = open("Library/A4_SendInBlue/Components/PIC/zaloQrcodeBase64.txt", "r")
zaloQrcodeBase64 = file.read()
file.close()
#1.5. Embeded image in mail content (Load from local image)
localEmbeded = "data:embededImage2/png;base64,"+picEncodeBase64

################################
#2. Create a mailConfig object #
################################
mailConfig.sender = {"email":"no-reply@cmengineering.wsn.com","name":"CME WSN Service"}
# mailConfig.to  = MAIL_TO_ALL  = [{"email":'m_hase_mgc_4x@icloud.com',"name":"Hasegawa"},{"email":'m.hase.mgc.4x@gmail.com',"name":"Hasegawa"},{"email":'info@seaside.green',"name":"SeasideConsulting"},{"email":'tran.dung@cmengineering.com.vn',"name":"Tran Dung"},{"email":'nguyen.phuc@cmengineering.com.vn',"name":"Nguyen Phuc"},{"email":'phan.tien@cmengineering.com.vn',"name":"Phan Tien"}]
mailConfig.to  = MAIL_TO_ALL  = [{"email":'tran.dung@cmengineering.com.vn',"name":"Tran Dung"}]
mailConfig.subject = "WSN WARNING: Low Battery - TEMP NODE 2"
mailConfig.content_mode = class_contentMode.HTML_CONTENT
# mailConfig.html_content ="<html><body><h1>Zalo Embeded QRCode</h1><img src='"+zaloQrcodeBase64+"' alt='QR Code'><h1>USER Embeded Picture Frome Local Image</h1><img src='"+localEmbeded+"' alt='QR Code'></body></html>"
#Load mail content from file
file = open("D:/Database/GIT/LOTUS_Python_Framework//A_SeasideConsulting_tempNodeAlert.html", "r")
mailConfig.html_content = file.read()
mailConfig.attachment = []

################################
#3. Send mail                  #
################################
SIB.sendMail(mailConfig)

################################
#4. Result                     #
################################
# PIC: Library/A4_SendInBlue/Components/PIC/mailAttachmentResult.png
