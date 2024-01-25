import requests
import json
import base64
from PIL import Image
import time,datetime


class omoCaptcha ():
  def __init__ (self, TOKEN="7763GCksrK3YNP7QSZjf1wq2FP5zf2Gtg6VmW6AhEbtM8y4iwuKfFpx9wkMm7A8ipZ68vANGMuHZkxIO"):
    self.TOKEN = TOKEN
    self.urlCreateJob = "https://omocaptcha.com/api/createJob"
    self.urlGetJobResult = "https://omocaptcha.com/api/getJobResult"
    self.urlGetBalance = "https://omocaptcha.com/api/getBalance"
    
  def waitResult(self,job_id):
    '''Chờ cho đến khi Server xử lý xong và trả về kết quả'''
    getResult ={
      "api_token": self.TOKEN,
      "job_id": job_id
    }
    timeMark = time.time()
    timeOut = 60
    while time.time() - timeMark < timeOut:
        response = requests.post(self.urlGetJobResult, json=getResult)
        getResultResult = json.loads(response.text) #Convert string to JSON
        if getResultResult['status'] == 'success':
          return getResultResult
        time.sleep(1)
    return False
  
  def getBalance(self):
    '''`Desciption`: Kiểm tra số dư tài khoản. Đơn vị USD\n
    `Returns`:
     + (True, balance): if success
     + (False, message): if error\n
    `Example`:
      OMO = omoCaptcha()\n
      print(OMO.getBalance())
        + (True, 1000): if balance is 1000
        + (False, "Invalid token"): if token is invalid'''
    response = requests.post(self.urlGetBalance, json={'api_token': self.TOKEN})
    #Convert string of JSON to dict
    responseDict = json.loads(response.text)
    if responseDict['error'] == False:
      return True,responseDict['balance']
    else:
      return False,responseDict['message']
  
  def solveTiktokChoose2Same(self,imagePath=""):
    '''`Desciption`: Giải captcha chọn 2 hình giống nhau'''
    try:
      # Load the image using PIL
      image = Image.open(imagePath)
      # Convert the image to a base64-encoded string
      with open(imagePath, "rb") as image_file:
          encoded_string = str(base64.b64encode(image_file.read())).split('\'')[1]
      # The URL of the API endpoint that you want to send the POST request to
      captReq ={
        "api_token": self.TOKEN,
        "data": {
          "type_job_id": "22",
          "image_base64": str(encoded_string),
          "width_view": image.size[0],
          "height_view": image.size[1]
        }
      }
      response = requests.post(self.urlCreateJob, json=captReq)
      captReqResult = json.loads(response.text) #Convert string to JSON
      
      # Nhận về kết quả:
      getResultResult = self.waitResult(captReqResult['job_id'])
      
      if getResultResult == False:
        return False,"Time out"
      else:
        return True,getResultResult['result']
    except Exception as e:
      return False,str(e)

  def solveTiktokRotateImage(self,imageOutsidePath="",imageInsidePath=""):
    '''`Desciption`: Giải captcha xoay 2 hình cho khớp với nhau'''
    try:
      # Convert the image to a base64-encoded string
      # with open(imageOutsidePath, "rb") as image_file:
          # imageOutsideB64 = str(base64.b64encode(image_file.read())).split('\'')[1]
          
      # with open(imageInsidePath, "rb") as image_file:
          # imageInsideB64 = str(base64.b64encode(image_file.read())).split('\'')[1]
          
          
      #convert image inside to base64 from url
      # with open(imageOutsidePath, "rb") as image_file from imageOutsidePath URL
      response = requests.get(imageInsidePath)
      imageInsideB64 = str(base64.b64encode(response.content)).split('\'')[1]
      response = requests.get(imageOutsidePath)
      imageOutsideB64 = str(base64.b64encode(response.content)).split('\'')[1]

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
      print(captReqResult['job_id'])
      
      # Nhận về kết quả:
      getResultResult = self.waitResult(captReqResult['job_id'])
      print(getResultResult)
      
      if getResultResult == False:
        return False,"Time out"
      else:
        return True,getResultResult['result']
    except Exception as e:
      print(str(e))
      return False,str(e)
    
OMO = omoCaptcha()
print(OMO.getBalance())
# print(OMO.solveTiktokChoose2Same("captcha.png"))
outsideImg = "https://p16-captcha-va.ibyteimg.com/tos-maliva-i-71rtze2081-us/3edac5dd33654402b1d249f9c3caed11~tplv-71rtze2081-1.png"
insideImg  = "https://p16-captcha-va.ibyteimg.com/tos-maliva-i-71rtze2081-us/03b27b7271dd468395b63fce04305c94~tplv-71rtze2081-1.png"
OMO.solveTiktokRotateImage(imageOutsidePath=outsideImg,imageInsidePath=insideImg)
print(OMO.getBalance())


