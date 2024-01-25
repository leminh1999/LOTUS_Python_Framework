import __init
from paho.mqtt import client as mqtt_client #pip install paho-mqtt
import random
import time

class mqttClass ():
    def __init__(self, broker="", port=1883, client_id=f"ClientId_{random.randint(0, 1000)}", username="not_required", password="not_required"):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.username = username
        self.password = password
        self.client = mqtt_client.Client(client_id)
        self.client.username_pw_set(username, password)
        self.client.connect(broker, port, keepalive=15)
        self.client.reconnect_delay_set(min_delay=1, max_delay=120)

    def msgRcvFilter(self,msg):
        pass

    def on_message(self, client, userdata, msg):
        # print(f"MQTT received `{msg.payload.decode()}` from `{msg.topic}` topic.")
        self.msgRcvFilter(msg)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
            
    def on_disconnect(self, client, userdata, rc):    
        print("Disconnected from MQTT Broker.")
        while True:
            try:
                print("Reconnect every 5 seconds...")
                self.client.reconnect()
                break
            except:
                pass
            time.sleep(5)
            
    def on_connect_fail(self,client, userdata):
        print("Connection failed.")
        while True:
            try:
                print("Reconnect every 5 seconds...")
                self.client.reconnect()
                break
            except:
                pass
            time.sleep(5)
        
    def publish(self, topic, msg):
        self.client.publish(topic, msg)

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def disconnect(self):
        print("Client wants to disconnect with MQTT Broker...")
        self.client.loop_stop()
        self.client.disconnect()
    
    def listen(self):
        self.client.on_message      = self.on_message
        self.client.on_connect      = self.on_connect
        self.client.on_disconnect   = self.on_disconnect
        self.client.on_connect_fail = self.on_connect_fail
        self.client.loop_forever()