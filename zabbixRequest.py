import requests
import json

# url = 'http://157.65.24.169/chart.php?from=2023-06-25%2000%3A51%3A28&to=2023-06-25%2003%3A34%3A26&itemids%5B0%5D=44379&type=0&profileIdx=web.item.graph.filter&profileIdx2=44379&width=1082&height=200&_=w4hgj4m1'
url = 'http://157.65.24.169/api_jsonrpc.php'

headers = {
    'Content-Type': 'application/json-rpc'
}

# payload = {
#     "jsonrpc": "2.0",
#     "method": "host.get",
#     "params": {
#         "output": [
#             "hostid",
#             "host"
#         ],
#         "selectInterfaces": [
#             "interfaceid",
#             "ip"
#         ]
#     },
#     "id": 2,
#     "auth": "db8306b8d05b4534d4f074d6ca4a0f333a0a1ba43f13e09a0bd1b5ee23aa2e64"
# }

payload = {
    "jsonrpc": "2.0",
    "method": "graph.get",
    "params": {
        "output": "extend",
        "hostids": 10603,
        "sortfield": "name"
    },
    "id": 1,
    "auth": "db8306b8d05b4534d4f074d6ca4a0f333a0a1ba43f13e09a0bd1b5ee23aa2e64"
}



response = requests.post(url, headers=headers, data=json.dumps(payload))

data = response.content.decode('utf-8')

print(data)