import asyncio
import websockets
import paho.mqtt.client as mqtt

# Callback khi client MQTT kết nối thành công
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("mqtt_to_ws")

# Callback khi nhận tin nhắn MQTT mới
def on_message(client, userdata, msg):
    print("Received MQTT message: " + msg.payload.decode())
    # Gửi tin nhắn đến tất cả các client WebSocket đã kết nối
    asyncio.get_event_loop().run_until_complete(send_to_websockets(msg.payload.decode()))

# Callback khi có kết nối WebSocket mới
async def websocket_handler(websocket, path):
    clients.add(websocket)
    print(clients)
    try:
        async for message in websocket:
            print("Received WebSocket message: " + message)
            await send_to_websockets("HELLO")
    finally:
        clients.remove(websocket)
        print("Client disconnected: " + str(websocket))

# Gửi tin nhắn đến tất cả các client WebSocket đã kết nối
async def send_to_websockets(message):
    if clients:
        await asyncio.wait([client.send(message) for client in clients])

# Thiết lập thông tin kết nối MQTT
broker_address = "test.mosquitto.org"
port = 1883

# Tạo một client MQTT
mqtt_client = mqtt.Client()

# Đăng ký các callback cho client MQTT
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Kết nối đến broker MQTT
mqtt_client.connect(broker_address, port)
mqtt_client.loop_start()

# Khởi tạo set lưu trữ các client WebSocket
clients = set()

# Khởi động server WebSocket
start_server = websockets.serve(websocket_handler, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
print("WebSocket server started!")