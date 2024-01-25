import socketio
import threading
sio = socketio.Client() # Khởi tạo client Socket.io
sid = ""
class toObj():
    toServer       = "toServer"           #EX: toValue = common_message
    toUserId       = "toUserId"           #EX: toValue = hvcb1fHKARdpQ9C6AAAh (20 ký tự).
    toUserNickName = "toUserNickName"     #EX: toValue = Node_SaiGon_1104
    toRoomName     = "toRoomName"         #EX: toValue = LOTUS_ROOM
    toAll          = "toAll"              #EX: toValue = toAll

def sendMessage(toValue:str="", toContent="",sendType:str=toObj.toRoomName):
    msgData = dict()
    msgData['type']    = sendType
    msgData['from']    = sid
    msgData['to']      = toValue
    msgData['content'] = toContent

    if toValue != "":
        sio.emit("SKRX", msgData)
    else:
        print("toValue is empty. Please check again!")
            

################################################################################
# PART 1: Đăng ký sự kiện connect, disconnect, common_message                  #
################################################################################
# Đăng ký sự kiện connect
@sio.event
def connect():
    global sid
    print('connection established')
    sid = sio.get_sid()

# Đăng ký sự kiện disconnect
@sio.event
def disconnect():
    print('disconnected from server')

# Đăng ký sự kiện common_message: Các tin nhắn qua lại chung giữa server và máy đang chạy.
# Chủ yếu để gửi thông báo, cảnh báo, lỗi, ... cho máy đang chạy.
@sio.event
def common_message(data):
    print("[Common Message] " + str(data))
    
################################################################################
# PART 2: Đăng ký sự kiện riêng cho máy đang chạy                              #
# Các sự kiện như tên nhóm chat (room) và tên sự kiện (event name) là duy nhất #
# VD: Tên nhóm chat là LOTUS_ROOM, SeasideConsultingRoom, TokyoRoom, ...       #
################################################################################
# Đăng ký sự kiện message từ các server/client khác
@sio.on('WSN_GW_01C821')
def WSN_GW_01C821(data):
    print('[RCV Message]: ' + str(data))

################################################################################
# PART 3: Tạo Thread kết nối và lắng nghe dữ liệu từ server                    #
################################################################################
sio.connect('http://lotus1104.synology.me:83')   # Địa chỉ server SocketIO
def listenForever():
    sio.wait()                                       # Lắng nghe dữ liệu từ server
webSocket = threading.Thread(target=listenForever)
webSocket.start()
print("WebSocket server started!")
################################################################################
# PART 4: Code bên ngoài Thread webSocket                                      #
################################################################################
sendMessage(toObj.toRoomName,"WSN_GW_01C821","Hello Lotus Room 1")
sendMessage(toObj.toRoomName,"WSN_GW_01C821","Hello Lotus Room 2")
sendMessage(toObj.toRoomName,"WSN_GW_01C821","Hello Lotus Room 3")
sendMessage(toObj.toRoomName,"WSN_GW_01C821","Hello Lotus Room 4")

