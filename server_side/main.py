# #ajith reading heart rate sensor
# #https://things.ubidots.com/api/v1.6/devices/esp32/temp/values?token=BBFF-Bfw8lO95m9pzKw8zE0Zupzw5OrKDQ0&page_size=4
# #from umqtt.robust import MQTTClient
# from machine import Pin,I2C
# import max30100
# import time
# from convert import HRSpo2
# sda=Pin(21)
# scl=Pin(22)             
# i2c = I2C(scl=scl,sda=sda)
# print('Scanning I2C devices...')
# print(i2c.scan())
# #mode=max30100.MODE_SPO2
# sensor = max30100.MAX30100(i2c=i2c,sample_rate=100,
#                  pulse_width=1600)
# 
# print('Reading MAX30100 registers...')
# print(sensor.get_registers())
# 
# sensor.enable_spo2()
# 
# 
# print('Reading sensor...')
# prev=0
# hrSpo2=HRSpo2(debug=True)
# while(True):
#     sensor.read_sensor()
#     #print(sensor.ir)
#     hrSpo2.update(sensor.ir,sensor.red)
#     
#     time.sleep_ms(50)
#     
#     
#     
# #     if(hrSpo2.result.pulseDetected==True):
# #         print(hrSpo2.result.heartBPM)
#     
#     
#     
# #     dcFilterIR,prev=convert.dcRemove(val,prev)   
# #     meanDiffResIR=convert.meanDiff(dcFilterIR,meanDiffIR)
# #     convert.lowPassButterworthFilter(meanDiffResIR,lpbFilterIR)
# #     irACValueSqSum +=  dcFilterIR* dcFilterIR
# #     samplesRecorded+=1


#ubidots
from umqtt.simple import MQTTClient
import json
from machine import Pin,ADC,I2C
import time
import machine
import max30100
from convert import HRSpo2

ubidotsToken = "BBFF-Bfw8lO95m9pzKw8zE0Zupzw5OrKDQ0"

clientID = "esp32"

sda=Pin(21)
scl=Pin(22)             
i2c = I2C(scl=scl,sda=sda)
print('Scanning I2C devices...')
print(i2c.scan())
#mode=max30100.MODE_SPO2
sensor = max30100.MAX30100(i2c=i2c,sample_rate=100,
                 pulse_width=1600)

print('Reading MAX30100 registers...')
print(sensor.get_registers())

sensor.enable_spo2()

#client = MQTTClient("clientID", server="industrial.api.ubidots.com",port=8883,keepalive=60, user = ubidotsToken, password = ubidotsToken,ssl=True)
temp=ADC(Pin(36))
temp.atten(ADC.ATTN_11DB)
hrSpo2=HRSpo2(debug=True)


def restart():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()
def on_disconnect(client, userdata, rc):
    print("client disconnected ok")
    restart()
    
def publish():
    try:
        #client.connect()

        while True:
            
#             var = ((temp.read()*3.3)/4095)*100
#             msg = b'{"value":%s}' % (var)
            sensor.read_sensor()
            heartrate=hrSpo2.update(sensor.ir,sensor.red)
            print(heartrate)
#             client.publish(b"/v1.6/devices/esp32/temp", msg,qos=0,retain=True)
            time.sleep_ms(50)
    except OSError as e:
            restart()

#client.on_disconnect=on_disconnect
publish()

# #ajith
# #https://things.ubidots.com/api/v1.6/devices/esp32/temp/values?token=BBFF-Bfw8lO95m9pzKw8zE0Zupzw5OrKDQ0&page_size=4
# #from umqtt.robust import MQTTClient
# from machine import Pin,I2C
# import max30100
# import time
# from convert import HRSpo2
# sda=Pin(21)
# scl=Pin(22)             
# i2c = I2C(scl=scl,sda=sda)
# print('Scanning I2C devices...')
# print(i2c.scan())
# #mode=max30100.MODE_SPO2
# sensor = max30100.MAX30100(i2c=i2c,sample_rate=100,
#                  pulse_width=1600)
# 
# print('Reading MAX30100 registers...')
# print(sensor.get_registers())
# 
# sensor.enable_spo2()
# 
# 
# print('Reading sensor...')
# prev=0
# hrSpo2=HRSpo2(debug=True)
# while(True):
#     sensor.read_sensor()
#     #print(sensor.ir)
#     hrSpo2.update(sensor.ir,sensor.red)
#     
#     time.sleep_ms(50)
#     
    
    
#     if(hrSpo2.result.pulseDetected==True):
#         print(hrSpo2.result.heartBPM)
    
    
    
#     dcFilterIR,prev=convert.dcRemove(val,prev)   
#     meanDiffResIR=convert.meanDiff(dcFilterIR,meanDiffIR)
#     convert.lowPassButterworthFilter(meanDiffResIR,lpbFilterIR)
#     irACValueSqSum +=  dcFilterIR* dcFilterIR
#     samplesRecorded+=1

# Thingspeak
#sree
# from umqtt.robust import MQTTClient
# import json
# from machine import Pin,ADC
# import time
# import machine
# 
# ubidotsToken = "BBFF-Bfw8lO95m9pzKw8zE0Zupzw5OrKDQ0"
# 
# topic= "channels/" +"1686267" + "/publish/" + "03M1AR86K87VQ2AN"
# clientID = "esp32"
# #user = "CREGMQITDQgZMBYYBDYdNhs", password ="RpMWJqFLBNG4eXQSd6MRGEs9"
# client = MQTTClient("esp1234",server="mqtt.thingspeak.com",port=8883,ssl=True)
# temp=ADC(Pin(36))
# temp.atten(ADC.ATTN_11DB)
# 
# def restart():
#     print('Failed to connect to MQTT broker. Reconnecting...')
#     time.sleep(10)
#     machine.reset()
# def on_disconnect(client, userdata, rc):
#     print("client disconnected ok")
#     restart()
#     
# def publish():
#     try:
#         client.connect()
# 
#         while True: 
#             var = ((temp.read()*3.3)/4095)*100
#             msg="field1="+str(var)
#             print(msg)
#             client.publish(topic, msg)
#             time.sleep(1)
#     except OSError as e:
#             restart()
# 
# client.on_disconnect=on_disconnect
# publish()

## The file name needs to be renamed to main.py for it work on the ESP 32 board

# import utime
# from util import create_mqtt_client, get_telemetry_topic, get_c2d_topic, parse_connection
# from machine import ADC,Pin
# 
# #HostName=health-iot.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=zT5A7Bw3lE9rt+cbPRIpcpLGWjf6omTHMSoqf12vFMY=
# HOST_NAME = "HostName"
# SHARED_ACCESS_KEY_NAME = "SharedAccessKeyName"
# SHARED_ACCESS_KEY = "SharedAccessKey"
# SHARED_ACCESS_SIGNATURE = "SharedAccessSignature"
# DEVICE_ID = "DeviceId"
# MODULE_ID = "ModuleId"
# GATEWAY_HOST_NAME = "GatewayHostName"
# 
# temp=ADC(Pin(36))
# temp.atten(ADC.ATTN_11DB)
# ## Parse the connection string into constituent parts
# dict_keys = parse_connection("HostName=health-iot.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=zT5A7Bw3lE9rt+cbPRIpcpLGWjf6omTHMSoqf12vFMY=")
# print(dict_keys)
# shared_access_key = dict_keys.get(SHARED_ACCESS_KEY)
# shared_access_key_name =  dict_keys.get(SHARED_ACCESS_KEY_NAME)
# gateway_hostname = dict_keys.get(GATEWAY_HOST_NAME)
# hostname = dict_keys.get(HOST_NAME)
# device_id = "esp32"
# module_id = dict_keys.get(MODULE_ID)
# 
# ## Create you own shared access signature from the connection string that you have
# ## Azure IoT Explorer can be used for this purpose.
# sas_token_str = "SharedAccessSignature sr=health-iot.azure-devices.net%2Fdevices%2Fesp32&sig=y6jB46iLOK93d6w3zzqd4kqHfx7pNqn8rtxgajOb0Rc%3D&se=60000001649789840"
# 
# ## Create username following the below format '<HOSTNAME>/<DEVICE_ID>'
# username = hostname + '/' + "esp32"
# 
# 
# ## Create UMQTT ROBUST or UMQTT SIMPLE CLIENT
# print(hostname)
# print(username)
# print(sas_token_str)
# mqtt_client = create_mqtt_client(client_id="esp32", hostname=hostname, username=username, password=sas_token_str, port=8883, keepalive=120, ssl=True)
# 
# print("connecting")
# mqtt_client.connect()
# 
# def callback_handler(topic, message_receive):
#     print("Received message")
#     print(message_receive)
# 
# # subscribe_topic = get_c2d_topic(device_id)
# # mqtt_client.set_callback(callback_handler)
# # mqtt_client.subscribe(topic=subscribe_topic)
# 
# print("Publishing")
# topic = get_telemetry_topic(device_id)
# 
# ## Send telemetry
# messages = [1,2,3,4,5,6,7,8,9,10]
# while(True):
#     
#     var = ((temp.read()*3.3)/4095)*100
#     msg="field1="+str(var)
#     print("Sending message " +msg)
#     mqtt_client.publish(topic=topic, msg=msg)
#     utime.sleep(2)

## Send a C2D message and wait for it to arrive at the device
# print("waiting for message")
# mqtt_client.wait_msg()