import jwt
import datetime

# Thông tin payload (dữ liệu chứa trong JWT)
payload = {
    "user_id": "mqtt_broker",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=100)  # Thời gian hết hạn
}

# Khóa bí mật để ký JWT (chỉ cần phía máy chủ biết)
secret_key = "!Da#ImU%VuF3V"

# Tạo JWT
jwt_token = jwt.encode(payload, secret_key, algorithm="HS256")
print(jwt_token)
