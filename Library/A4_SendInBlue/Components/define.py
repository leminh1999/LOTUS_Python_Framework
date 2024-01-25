import __init
from Library.C5_RsaEncrypt.rsa_Wrap import RSA_Class
import datetime
import os
#https://app.brevo.com/settings/keys/api
SIB_BIN_API_KEY  = b'n\xb8U\xf7\xad\x07{\xce\xa9\x08\x9eC?QJ\xd5\xc0\xfc\xcf\x0f\x83\xe5\x01\xe7\xf5OL\xfbN\x95\xf8\xa5d\x8d\xd6\x8e\x06\xf8\xb2r%@\xb5\xc5\x9c\x13:y\xcc3q\xa4\xaf\xe7\xf5\x82S\x80\xf2(+\x9d\xc0\ra\xa0\xe6f\xeenx\x9b\xac\x94\x1fH4h9\xa58Wb\xae\xbf%Qk\x96\xc8;\x01\x8b\xd8\xf5Y\xdc\xb3\x96\xfe\xde\x06\xe1\xb0\xfc\x05\xa7\xbbv\xab\xf9{u\xee%\xd0&\xda\xe9\xd8m\x9b\xc7Fh\xe2\x02\x1a\xc5S\x86\xe4\rNl\'\xb1l\xc4\x0f\xaf\xaeRh\x04-<<\x95\xac\xd5\x1f\nq\xb4\xdf~\x08I\xb3fA\x89\x9f\xcaf\xbb\x9d-A\x8e\x9e\x05=\x86\xa2g\x01\x0b\xb1f(\xe5-v\xd8\xda\x14"\x84\xc1\x97h\x15\xfa\x92\xc5\x96r\x13B\xc5\xc9\xdd\x98\xe4\xf7\xe1%^i\nP\xea\xfc\x0c\x7f\x07\x91\xd5\xb9\x8d\xbc\xf8u>\xd5\x0b}\xe3\x0f\xde/\xec\xa4\xda7@)\xf7\x8a\xb5\xf7\xc8\xfe$5\x02\x0e8D\xd1\xc0\x8b\x93\x8f'
if os.path.exists("Library/A4_SendInBlue/Components/SIB_private.pem"):
  RSA_SIB = RSA_Class(privateKeyPath="Library/A4_SendInBlue/Components/SIB_private.pem")
else:
  exit("ERROR: SIB_private.pem not found!")
DEFAULT_API_KEY = RSA_SIB.decrypt(SIB_BIN_API_KEY) #decrypt data
print("SIB_API_KEY:",DEFAULT_API_KEY)

DEFAULT_SENDER   = {"email":"wsn_system@cmengineering.com","name":"WSN System"}
DEFAULT_TO       = [{"email":'tran.dung@cmengineering.com.vn',"name":"Tran Dung"}]
DEFAULT_CC       = None # [{"email":"example2@example2.com","name":"Janice Doe"}]
DEFAULT_BCC      = None # [{"name":"John Doe","email":"example@example.com"}]
DEFAULT_REPLY_TO = None #{"email":"replyto@domain.com","name":"John Doe"}

DEFAULT_SUBJECT   = "Hello I'm test mail"

DEFAULT_TEXT_CONT = "Mail scheduled at: " + str(datetime.datetime.now())
DEFAULT_HTML_CONT = "<html><body><h1>This is testing mail. Please is ignore!</h1></body></html>"

# Pass the absolute URL (no local file) or the base64 content of the attachment along with the attachment name (Mandatory if attachment content is passed).
# For example, `[{\"url\":\"https://attachment.domain.com/myAttachmentFromUrl.jpg\", \"name\":\"myAttachmentFromUrl.jpg\"}, 
#                {\"content\":\"base64 example content\", \"name\":\"myAttachmentFromBase64.jpg\"}]`.
# Allowed extensions for attachment file: xlsx, xls, ods, docx, docm, doc, csv, pdf, txt, gif, jpg, jpeg, png, tif, tiff, rtf, bmp, cgm, css, shtml, html, htm, zip,
# xml, ppt, pptx, tar, ez, ics, mobi, msg, pub, eps, odt, mp3, m4a, m4v, wma, ogg, flac, wav, aif, aifc, aiff, mp4, mov, avi, mkv, mpeg, mpg, wmv, pkpass and xlsm
# ( If 'templateId' is passed and is in New Template Language format then both attachment url and content are accepted. If template is in Old template Language format, then 'attachment' is ignored )  # noqa: E501
# DEFAULT_ATTACHMENT = "https://www.dropbox.com/s/vfc36yzbqi7mogp/haha.PNG"
DEFAULT_ATTACHMENT = []