import sys
import paho.mqtt.client as mqtt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit

class MQTTClient(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MQTT Client")
        self.setGeometry(100, 100, 400, 300)

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(20, 20, 360, 200)

        self.connect_button = QPushButton("Connect", self)
        self.connect_button.setGeometry(120, 230, 160, 30)
        self.connect_button.clicked.connect(self.connect_to_mqtt)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.text_edit.append("Connected to MQTT server")
            self.mqtt_client.subscribe("topic/to/subscribe")  # Đặt topic muốn subscribe vào đây
        else:
            self.text_edit.append(f"Failed to connect, error code: {rc}")

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        self.text_edit.append(f"Received message: {message}")

    def connect_to_mqtt(self):
        self.mqtt_client.connect("broker_ip", 1883)  # Thay "broker_ip" bằng địa chỉ IP của MQTT broker
        self.mqtt_client.loop_start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MQTTClient()
    window.show()
    sys.exit(app.exec_())