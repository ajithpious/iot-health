#sree
from umqtt.simple import MQTTClient
import ssd1306
import json
import time
from machine import Pin,SoftI2C


ubidotsToken = "BBFF-Bfw8lO95m9pzKw8zE0Zupzw5OrKDQ0"

clientID = "esp32"
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

client = MQTTClient("clientID", server="industrial.api.ubidots.com",port= 8883, user = ubidotsToken, password = ubidotsToken,keepalive=60,ssl=True)

ref=Pin(15,Pin.OUT)
ref.value(True)
print("value=",ref.value())

def call_back_function(topic, msg):
    m=msg.decode().strip("'\n")
    m=json.loads(m)
    print(m['value'])
    oled.fill(0)
    oled.text("temp:"+str(m['value']), 0, 0)
    oled.show()
def restart():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()
def on_disconnect(client, userdata, rc):
    print("client disconnected ok")
    restart()
    

def publish():
    
    try:
        oled.fill(0)
        oled.text("Connecting to Database......", 0, 0)
        while True:
            client.connect()
            client.subscribe(topic=b"/v1.6/devices/esp32/temp",qos=0)
            client.check_msg()
            time.sleep(5)
            client.disconnect()
    except OSError as e:
            restart()

client.set_callback(call_back_function)
publish()

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
