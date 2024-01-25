import requests

url = "https://omocaptcha.com/api/getBalance"

# data ="{'api_token': '7763GCksrK3YNP7QSZjf1wq2FP5zf2Gtg6VmW6AhEbtM8y4iwuKfFpx9wkMm7A8ipZ68vANGMuHZkxIO'}"
data ={
  'api_token': '7763GCksrK3YNP7QSZjf1wq2FP5zf2Gtg6VmW6AhEbtM8y4iwuKfFpx9wkMm7A8ipZ68vANGMuHZkxIO'
}

#Convert dict to JSON
# import json
# data = json.dumps(data)

print(type(data))

response = requests.post(url, json=data)
print(response.text)