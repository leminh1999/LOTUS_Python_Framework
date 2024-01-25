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
mailConfig.subject = "Zalo QRCode"
mailConfig.content_mode = class_contentMode.HTML_CONTENT
mailConfig.html_content ="<html><body><h1>Zalo Embeded QRCode</h1><img src='"+zaloQrcodeBase64+"' alt='QR Code'><h1>USER Embeded Picture Frome Local Image</h1><img src='"+localEmbeded+"' alt='QR Code'></body></html>"
#Load mail content from file
# file = open("D:/Database/GIT/LOTUS_Python_Framework//tempNodeAlert.html", "r")
# mailConfig.html_content = file.read()
mailConfig.attachment = [{'content':picEncodeBase64, 'name':'LocalPicAttachment.png'},
                         {'content':zipEncodeBase64, 'name':'LocalZipAttachment.zip'},
                         {'url': urlLink, 'name':'https_link_Image.jpg'}
                        ]

################################
#3. Send mail                  #
################################
SIB.sendMail(mailConfig)

################################
#4. Result                     #
################################
# PIC: Library/A4_SendInBlue/Components/PIC/mailAttachmentResult.png
