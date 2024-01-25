import asyncio
import websockets
import paho.mqtt.client as mqtt

# Dictionnary để lưu trữ các nhóm client WebSocket
websocket_groups = {}

# Callback khi client MQTT kết nối thành công
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("mqtt_to_ws")

# Callback khi nhận tin nhắn MQTT mới
def on_message(client, userdata, msg):
    print("Received MQTT message: " + msg.payload.decode())
    try:
        event, message = msg.payload.decode().split(':', 1)
        if event in websocket_groups:
            asyncio.get_event_loop().run_until_complete(send_to_websockets(websocket_groups[event], message))
    except ValueError:
        print("Invalid format for message:", msg.payload.decode())

# Callback khi có kết nối WebSocket mới
async def websocket_handler(websocket, path):
    try:
        event = await websocket.recv()
        if event not in websocket_groups:
            websocket_groups[event] = set()
        websocket_groups[event].add(websocket)
        try:
            async for message in websocket:
                print(f"Received WebSocket message in event {event}: {message}")
        finally:
            websocket_groups[event].remove(websocket)
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed")

# Gửi tin nhắn đến một nhóm client WebSocket
async def send_to_websockets(client_group, message):
    if client_group:
        await asyncio.wait([client.send(message) for client in client_group])

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

# Khởi động server WebSocket
start_server = websockets.serve(websocket_handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
