import __init
import requests
import json
import base64
from PIL import Image
import time,datetime

#Tài khoản tại (tranhuudung1986@gmail.com/S*3): https://achicaptcha.com/?page=account
class omoCaptcha ():
  def __init__ (self, TOKEN="ac496690dc21d582e912818f7c5c9295"):
    self.TOKEN = TOKEN
    self.urlCreateJob    = "http://api.achitech.site/createTask"
    self.urlGetJobResult = "http://api.achitech.site/getTaskResult"
    self.urlGetBalance   = "https://omocaptcha.com/api/getBalance"
  
  def getBalance(self):
    '''`Desciption`: Kiểm tra số dư tài khoản. Đơn vị USD\n
    `Returns`:
     + (True, balance): if success
     + (False, message): if error\n
    `Example`:
      OMO = omoCaptcha()\n
      print(OMO.getBalance())
        + (True, 1000): if balance is 1000$
        + (False, "Invalid token"): if token is invalid'''
    response = requests.post(self.urlGetBalance, json={'api_token': self.TOKEN})
    #Convert string of JSON to dict
    responseDict = json.loads(response.text)
    if responseDict['error'] == False:
      return True,responseDict['balance']
    else:
      return False,responseDict['message']
  
  def solveTiktokChoose2Same(self,imagePathOrUrl=""):
    '''`Desciption`: Giải captcha chọn 2 hình giống nhau. Library\C3_OmoCaptcha\Components\PIC\choose2Samecaptcha.png
       `Params`: imagePath: đường dẫn đến file ảnh.
       `Return`: 
    \n'''
    try:
      # Load the image using PIL
      if imagePathOrUrl.startswith("http"):
        #convert image inside to base64 from url
        response = requests.get(imagePathOrUrl)
        encoded_string = str(base64.b64encode(response.content)).split('\'')[1]
      else:
        # Convert the image to a base64-encoded string
        with open(imagePathOrUrl, "rb") as image_file:
            encoded_string = str(base64.b64encode(image_file.read())).split('\'')[1]
            
      # The URL of the API endpoint that you want to send the POST request to
      captReq ={
        "clientKey": self.TOKEN,
        "task": {
          "type": "TiktokCaptchaTask",
          "image": str(encoded_string),
          "subType": 2
        }
      }
      response = requests.post(self.urlCreateJob, json=captReq)
      captReqResult = json.loads(response.text) #Convert string to JSON
      
      # Nhận về kết quả:
      getResultResult = self.__waitResult(captReqResult['taskId'])
      
      if getResultResult == False:
        return False,"Time out"
      else:
        return True,getResultResult['result']
    except Exception as e:
      return False,str(e)

  def solveTiktokRotateImage(self,imageInsidePathOrUrl="",imageOutsidePathOrUrl=""):
    '''`Desciption`: Giải captcha xoay 2 hình cho khớp với nhau'''
    try:
      # Load the image using PIL
      if imageInsidePathOrUrl.startswith("http"):
        #convert image inside to base64 from url
        response = requests.get(imageInsidePathOrUrl)
        imageInsideB64 = str(base64.b64encode(response.content)).split('\'')[1]
      else:
        # Convert the image to a base64-encoded string
        with open(imageInsidePathOrUrl, "rb") as image_file:
            imageInsideB64 = str(base64.b64encode(image_file.read())).split('\'')[1]

      # Load the image using PIL
      if imageOutsidePathOrUrl.startswith("http"):
        #convert image inside to base64 from url
        response = requests.get(imageOutsidePathOrUrl)
        imageOutsideB64 = str(base64.b64encode(response.content)).split('\'')[1]
      else:
        # Convert the image to a base64-encoded string
        with open(imageOutsidePathOrUrl, "rb") as image_file:
            imageOutsideB64 = str(base64.b64encode(image_file.read())).split('\'')[1]

      # The URL of the API endpoint that you want to send the POST request to
      captReq ={
        "api_token": self.TOKEN,
        "data": {
          "type_job_id": "23",
          "image_base64": str(imageInsideB64)+"|"+str(imageOutsideB64),
        }
      }
      response = requests.post(self.urlCreateJob, json=captReq)
      captReqResult = json.loads(response.text) #Convert string to JSON
      # print(captReqResult['job_id'])
      
      # Nhận về kết quả:
      getResultResult = self.__waitResult(captReqResult['job_id'])
      # print(getResultResult)
      
      if getResultResult == False:
        return False,"Time out"
      else:
        return True,getResultResult['solution']
    except Exception as e:
      print(str(e))
      return False,str(e)
    
  def __waitResult(self,job_id):
    '''Chờ cho đến khi Server xử lý xong và trả về kết quả'''
    getResult ={
      "clientKey": self.TOKEN,
      "taskId": job_id
    }
    timeMark = time.time()
    timeOut = 60
    while time.time() - timeMark < timeOut:
        response = requests.post(self.urlGetJobResult, json=getResult)
        getResultResult = json.loads(response.text) #Convert string to JSON
        if getResultResult['status'] == 'ready':
          return getResultResult
        time.sleep(1)
    return False
  
  
  
OMO = omoCaptcha()
# print(OMO.getBalance())
print(OMO.solveTiktokChoose2Same("Library/C4_AchiCaptcha/Components/PIC/choose2Samecaptcha.png"))
# insideImg  = "https://p16-captcha-va.ibyteimg.com/tos-maliva-i-71rtze2081-us/03b27b7271dd468395b63fce04305c94~tplv-71rtze2081-1.png"
# outsideImg = "https://p16-captcha-va.ibyteimg.com/tos-maliva-i-71rtze2081-us/3edac5dd33654402b1d249f9c3caed11~tplv-71rtze2081-1.png"
# OMO.solveTiktokRotateImage(imageInsidePathOrUrl=insideImg,imageOutsidePathOrUrl=outsideImg)
# print(OMO.getBalance())



