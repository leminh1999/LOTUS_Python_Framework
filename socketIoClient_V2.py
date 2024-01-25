import socketio

# Tạo một client socketio
sio = socketio.Client()

# Khi kết nối thành công
@sio.event
def connect():
    print('Kết nối thành công')

# Khi nhận được sự kiện 'my_event' từ server
@sio.event
def my_event(data):
    print('Nhận được sự kiện:', data)

# Kết nối tới server socketio
sio.connect('http://lotus1104.synology.me:83')

# Kích hoạt sự kiện 'my_event' và truyền dữ liệu
while True:
    message = input('Nhập tin nhắn để gửi tới server (hoặc "exit" để thoát): ')
    if message.lower() == 'exit':
        break
    sio.emit('WSN_GW_01C823', '{"topic":"WSN_GW_01C823","message":"'+message+'"}')  # Gửi tin nhắn lên server
    #
sio.emit('WSN_GW_01C823', "HELLO WORLD")

# Ngắt kết nối
# sio.disconnect()