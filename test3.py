import __init
# from aiohttp import web
import socketio
# from aiohttp_cors import CorsConfig, ResourceOptions, setup as setup_cors
# from Library.B1_jsonFileControl.jsonFileControl import jsonFileRecord
# from Library.A9_MQTT.mqtt import mqttClass #pip install paho-mqtt
import threading
import random
import json
import asyncio
import time

# TOPIC_LICENSE_MANAGER_FILE = "/HShare/socketio_app/WS_ImportExportRegister.json"
# TOPIC_LICENSE_MANAGER = jsonFileRecord()
# topicLicenseManager   = dict(TOPIC_LICENSE_MANAGER.loadFromJsonFile(TOPIC_LICENSE_MANAGER_FILE))

# # broker = 'lotus1104.synology.me' #Broker IP
# broker = '100.100.100.3' #Broker IP
# port = 1885
# client_id = f'SK_MQTT_ID_'+str(random.randint(0, 10000))
# username = 'mqtt_broker'
# password = '!Da#ImU%VuF3V'

# MQTT = mqttClass(broker, port, client_id, username, password)

# def listenForever2():
#   # Khởi tạo client Socket.IO phụ để gửi tin nhắn đến trung tâm điều phối tin nhắn
#   sio_client = socketio.Client()
#   # sio_client.connect('http://localhost:5000')  # Địa chỉ của Socket.IO server
#   sio_client.connect('http://lotus1104.synology.me:83')   # Địa chỉ server SocketIO
#   sio_client.wait()                                       # Lắng nghe dữ liệu từ server
# webSocket2 = threading.Thread(target=listenForever2)
# webSocket2.start()
sio_client = socketio.Client()
# sio_client.connect('http://localhost:5000')  # Địa chỉ của Socket.IO server
sio_client.connect('http://lotus1104.synology.me:83')   # Địa chỉ server SocketIO
sio_client.wait()   

# # Khởi tạo server Socket.IO
# #Bước 1: Khởi tạo ứng dụng web và kết nối với Socket.IO
# sio_server = socketio.Server(cors_allowed_origins='*') #Creates a new Async Socket IO Server
#                                                 #with cors_allowed_origins='*'
# app = socketio.WSGIApp(sio_server)                     #Creates a new Web Application


# ##############################################################
# # Node MQTT M0 Trong Mô Hình                                 #
# ##############################################################
# #CHECK WS_IMPORT OR WS_IMPORT_EXPORT LICENSE TO SUBCRIBE MQTT TOPIC
# for topic in topicLicenseManager:
#   if "IMPORT" in topicLicenseManager[topic]["license"]:
#     MQTT.subscribe(topic)
#     print(f"Subcribed to topic: {topic}")

# def subcribeFilter(msg):
#   try:
#     #Convert msg.payload from string to dict
#     jsonData = json.loads(msg.payload.decode())
    
#     #Check sender uid
#     if jsonData["uid"] == client_id: return #Ignore message sent by itself
    
#     #Check license
#     for topic in topicLicenseManager:
#       if topic == msg.topic and ("WS_IMPORT" in topicLicenseManager[topic]["license"] or "WS_IMPORT_EXPORT" in topicLicenseManager[topic]["license"]):
#         # emit to socketio with topic name and msg
#         print(f"Received from MQTT Broker: {msg.topic} - {msg.payload.decode()}")
#         print(f"Send to SocketIO: {msg.topic} - {jsonData['message']}")
#         # sio_client.emit(msg.topic,jsonData["message"]) #Send message as asynchronous function
#         break
      
#     #Register License for Topic
#     if topic == "SK_LICENSE_REGISTER": #SOCKETIO REGISTER LICENSE FOR TOPIC
#       # Có 4 loại: WS_IMPORT, WS_EXPORT, WS_IMPORT_EXPORT, "" (không có license)
#       registerTopic = jsonData["message"]["topic"]
#       registerLicense = jsonData["message"]["license"]
#       topicLicenseManager[registerTopic] = dict()
#       topicLicenseManager[registerTopic]["license"] = registerLicense
#       TOPIC_LICENSE_MANAGER.syncToJsonFile(fileName=TOPIC_LICENSE_MANAGER_FILE, profileManager=topicLicenseManager)
#       print(f"Registered license for topic: {registerTopic} - {registerLicense}")
#   except Exception as e:
#     print(f"ERROR: {e}")
  
# MQTT.subscribe("SK_LICENSE_REGISTER")
# MQTT.msgRcvFilter = subcribeFilter
# threading.Thread(target=MQTT.listen).start()
# ##############################################################



# # print(topicLicenseManager)

# # topicLicenseManager["topic1"] = dict()
# # topicLicenseManager["topic1"]["license"] = "WS_IMPORT"
# # topicLicenseManager["topic2"] = dict()
# # topicLicenseManager["topic2"]["license"] = "WS_EXPORT"
# # topicLicenseManager["topic3"] = dict()
# # topicLicenseManager["topic3"]["license"] = "WS_IMPORT_EXPORT"
# # TOPIC_LICENSE_MANAGER.syncToJsonFile(fileName=TOPIC_LICENSE_MANAGER_FILE, profileManager=topicLicenseManager)


# ##################################################################################################


# ##################################################################################################
# #Bước 2: Định nghĩa lại các sự kiện của Socket.IO ở đây                                                 
# @sio_server.on('connect')
# def connect(sid, environ):
#     print(f'Client connected: {sid}')

# @sio_server.on('disconnect')
# def disconnect(sid, environ):
#     print(f'Client connected: {sid}')

# # Khi nhận được tin nhắn từ client đến trung tâm điều phối tin nhắn: SKRX
# @sio_server.on('SKRX')
# def SKRX(sid, data):
#     print(f'[SKRX] Received message from {sid}: {data}')
#     #1.Convert data to JSON
#     if type(data) == str:
#       jsonData = json.loads(data)
#     elif type(data) == dict:
#       jsonData = data
#     else:
#       print("[SKRX] Received message is not string or dict => Skip message")
#       return
#     #2.Lan truyền gói tin cho các client khác
#     topic   = str(jsonData['topic'])
#     message = str(jsonData['message'])
#     print(f'[SKRX] Received message from {topic}: {message}')
#     sio_server.emit(topic,message,skip_sid=sid) #Send message to all clients except sender
#     #CHECK LICENSE
#     if topic not in topicLicenseManager:
#       pass
#     else:
#       if "WS_EXPORT" in topicLicenseManager[topic]["license"] or "WS_IMPORT_EXPORT" in topicLicenseManager[topic]["license"]: #WS_EXPORT or WS_IMPORT_EXPORT License
#         #SEND TO MQTT BROKER
#         sendData = '{"uid": "'+str(client_id)+'","message":"'+message+'"}'
#         MQTT.publish(topic=topic, msg=sendData) #Send message to MQTT Broker
          
# ##################################################################################################
# #Bước 3: Cấu hình cho ứng dụng web
# print("\n\nSOCKETIO SERVER STARTING UP...")


# def listenForever():
#     eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
# webSocket = threading.Thread(target=listenForever)
# webSocket.start()

# while True:
#   print("DEBUG: 1")
#   time.sleep(1)
