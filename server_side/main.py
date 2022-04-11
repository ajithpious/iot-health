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


#sree
from umqtt.robust import MQTTClient
import json
from machine import Pin,ADC
import time
import machine

ubidotsToken = "BBFF-Bfw8lO95m9pzKw8zE0Zupzw5OrKDQ0"

clientID = "esp32"

client = MQTTClient("clientID", server="industrial.api.ubidots.com",port=8883, user = ubidotsToken, password = ubidotsToken,ssl=True)
temp=ADC(Pin(36))
temp.atten(ADC.ATTN_11DB)

def restart():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()
def on_disconnect(client, userdata, rc):
    print("client disconnected ok")
    restart()
    
def publish():
    try:
        client.connect()

        while True: 
            var = ((temp.read()*3.3)/4095)*100
            msg = b'{"temp": {"value":%s, "context":{"stat":%s}}}' % (var, 10)
            print(msg)
            client.publish(b"/v1.6/devices/esp32", msg)
            time.sleep(1)
    except OSError as e:
            restart()

client.on_disconnect=on_disconnect
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
