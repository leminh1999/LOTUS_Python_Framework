import requests

# Thiết lập thời gian chờ tối đa (trong giây)
timeout = 10

# Tạo một session và đặt thời gian chờ cho session này
session = requests.Session()
session.timeout = timeout

# Gửi yêu cầu "do_request" bằng session đã tạo
response = session.do_request(...)