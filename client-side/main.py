# #sree
# from umqtt.simple import MQTTClient
# import ssd1306
# import json
# import time
# from machine import Pin,SoftI2C
# 
# 
# ubidotsToken = "BBFF-Bfw8lO95m9pzKw8zE0Zupzw5OrKDQ0"
# 
# clientID = "esp32"
# i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
# oled_width = 128
# oled_height = 64
# oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
# 
# client = MQTTClient("clientID", server="industrial.api.ubidots.com",port= 8883, user = ubidotsToken, password = ubidotsToken,keepalive=60,ssl=True)
# 
# ref=Pin(15,Pin.OUT)
# ref.value(True)
# print("value=",ref.value())
# 
# def call_back_function(topic, msg):
#     m=msg.decode().strip("'\n")
#     m=json.loads(m)
#     print(m['value'])
#     oled.fill(0)
#     oled.text("temp:"+str(m['value']), 0, 0)
#     oled.show()
# def restart():
#     print('Failed to connect to MQTT broker. Reconnecting...')
#     time.sleep(10)
#     machine.reset()
# def on_disconnect(client, userdata, rc):
#     print("client disconnected ok")
#     restart()
#     
# 
# def publish():
#     
#     try:
#         oled.fill(0)
#         oled.text("Connecting to Database......", 0, 0)
#         while True:
#             client.connect()
#             client.subscribe(topic=b"/v1.6/devices/esp32/temp",qos=0)
#             client.check_msg()
#             time.sleep(5)
#             client.disconnect()
#     except OSError as e:
#             restart()
# 
# client.set_callback(call_back_function)
# publish()

# thingspeak configuration

# #sree
# from umqtt.simple import MQTTClient
# import ssd1306
# import json
# import time
# from machine import Pin,SoftI2C
# 
# 
# ubidotsToken = "BBFF-Bfw8lO95m9pzKw8zE0Zupzw5OrKDQ0"
# 
# clientID = "esp32"
# i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
# oled_width = 128
# oled_height = 64
# oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
# t= bytes("channels/{:s}/subscribe/fields/field1/{:s}".format("1686267","P8PTSB5DRTSRWAZ0"),'utf-8')
# #,user = "mwa0000024793831", password ="P8PTSB5DRTSRWAZ0"
# #,user = "CREGMQITDQgZMBYYBDYdNhs", password ="RpMWJqFLBNG4eXQSd6MRGEs9"
# client = MQTTClient("esp1234",server="mqtt.thingspeak.com",port=8883,user = "CREGMQITDQgZMBYYBDYdNhs", password ="RpMWJqFLBNG4eXQSd6MRGEs9",ssl=True)
# 
# ref=Pin(15,Pin.OUT)
# ref.value(True)
# print("value=",ref.value())
# 
# def call_back_function(topic, msg):
#     print(msg)
#     m=msg.decode().strip("'\n")
#     m=json.loads(m)
#     print(m['value'])
#     oled.fill(0)
#     oled.text("temp:"+str(m['value']), 0, 0)
#     oled.show()
# def restart():
#     print('Failed to connect to MQTT broker. Reconnecting...')
#     time.sleep(10)
#     machine.reset()
# def on_disconnect(client, userdata, rc):
#     print("client disconnected ok")
#     restart()
#     
# 
# def publish():
#     
# #     try:json/P8PTSB5DRTSRWAZ0
#     print(client.connect())
#     print(t)
#     client.subscribe(topic="channels/1686267/subscribe/fileds/field1/P8PTSB5DRTSRWAZ0",qos=0)
#     oled.fill(0)
#     oled.text("Connecting to Database......", 0, 0)
#     oled.show()
#     while True:
#         client.check_msg()
#         time.sleep_ms(10)
# #     except OSError as e:
# #             print(e)
#             #restart()
# 
# client.set_callback(call_back_function)
# client.on_disconnect=on_disconnect
# publish()


# Azure Configuration

## The file name needs to be renamed to main.py for it work on the ESP 32 board

import utime
from util import create_mqtt_client, get_telemetry_topic, get_c2d_topic, parse_connection
from machine import ADC,Pin
import ssd1306
import json
import time
from machine import Pin,SoftI2C


#HostName=health-iot.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=zT5A7Bw3lE9rt+cbPRIpcpLGWjf6omTHMSoqf12vFMY=
HOST_NAME = "HostName"
SHARED_ACCESS_KEY_NAME = "SharedAccessKeyName"
SHARED_ACCESS_KEY = "SharedAccessKey"
SHARED_ACCESS_SIGNATURE = "SharedAccessSignature"
DEVICE_ID = "DeviceId"
MODULE_ID = "ModuleId"
GATEWAY_HOST_NAME = "GatewayHostName"

temp=ADC(Pin(36))
temp.atten(ADC.ATTN_11DB)
## Parse the connection string into constituent parts
dict_keys = parse_connection("HostName=health-iot.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=zT5A7Bw3lE9rt+cbPRIpcpLGWjf6omTHMSoqf12vFMY=")
print(dict_keys)
shared_access_key = dict_keys.get(SHARED_ACCESS_KEY)
shared_access_key_name =  dict_keys.get(SHARED_ACCESS_KEY_NAME)
gateway_hostname = dict_keys.get(GATEWAY_HOST_NAME)
hostname = dict_keys.get(HOST_NAME)
device_id = "esp32"
module_id = dict_keys.get(MODULE_ID)

## Create you own shared access signature from the connection string that you have
## Azure IoT Explorer can be used for this purpose.
sas_token_str = "SharedAccessSignature sr=health-iot.azure-devices.net%2Fdevices%2Fesp32&sig=y6jB46iLOK93d6w3zzqd4kqHfx7pNqn8rtxgajOb0Rc%3D&se=60000001649789840"

## Create username following the below format '<HOSTNAME>/<DEVICE_ID>'
username = hostname + '/' + "esp32"


## Create UMQTT ROBUST or UMQTT SIMPLE CLIENT
print(hostname)
print(username)
print(sas_token_str)
mqtt_client = create_mqtt_client(client_id="esp32", hostname=hostname, username=username, password=sas_token_str, port=8883, keepalive=120, ssl=True)

print("connecting")
# mqtt_client.connect()

def callback_handler(topic, message_receive):
    print("Received message")
    print(message_receive)

subscribe_topic = get_c2d_topic(device_id)
mqtt_client.set_callback(callback_handler)
# mqtt_client.subscribe(topic=subscribe_topic)

print("Publishing")
topic = get_telemetry_topic(device_id)

## Send telemetry
messages = [1,2,3,4,5,6,7,8,9,10]
while(True):
    mqtt_client.connect()
    mqtt_client.subscribe(topic=subscribe_topic)
    mqtt_client.check_msg()
    mqtt_client.disconnect()
    utime.sleep(1)
    
