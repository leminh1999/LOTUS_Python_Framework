import requests
import json
import time,datetime

##############################################################
#Convert Image to Base64
import base64
from PIL import Image

# Load the image using PIL
image = Image.open("captcha.png")
print(image.size)

# Convert the image to a base64-encoded string
with open("captcha.png", "rb") as image_file:
    encoded_string = str(base64.b64encode(image_file.read())).split('\'')[1]


# The URL of the API endpoint that you want to send the POST request to
url = "https://omocaptcha.com/api/createJob"
captReq ={
  "api_token": "7763GCksrK3YNP7QSZjf1wq2FP5zf2Gtg6VmW6AhEbtM8y4iwuKfFpx9wkMm7A8ipZ68vANGMuHZkxIO",
	"data": {
		"type_job_id": "22",
		"image_base64": str(encoded_string),
		"width_view": image.size[0],
		"height_view": image.size[1]
	}
}
response = requests.post(url, json=captReq)
captReqResult = json.loads(response.text) #Convert string to JSON
print(type(captReqResult))
print(captReqResult['job_id'])

print("Current time: ", datetime.datetime.now())
# time.sleep(3)
##############################################################
# Nhận về kết quả:
url = "https://omocaptcha.com/api/getJobResult"
getResult ={
  "api_token": "7763GCksrK3YNP7QSZjf1wq2FP5zf2Gtg6VmW6AhEbtM8y4iwuKfFpx9wkMm7A8ipZ68vANGMuHZkxIO",
	"job_id": captReqResult['job_id']
}
while True:
    response = requests.post(url, json=getResult)
    getResultResult = json.loads(response.text) #Convert string to JSON
    print(type(getResultResult))
    print(getResultResult['status'])
    if getResultResult['status'] == 'success':
        break
    time.sleep(1)
    print("Current time: ", datetime.datetime.now())
    
print("Current time: ", datetime.datetime.now())
print(getResultResult)