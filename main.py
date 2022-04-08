#ajith
#https://things.ubidots.com/api/v1.6/devices/esp32/temp/values?token=BBFF-Bfw8lO95m9pzKw8zE0Zupzw5OrKDQ0&page_size=4
from umqtt.robust import MQTTClient
from machine import Pin,I2C
import max30100
import time
from convert import HRSpo2
sda=Pin(21)
scl=Pin(22)             
i2c = I2C(scl=scl,sda=sda)
print('Scanning I2C devices...')
print(i2c.scan())

sensor = max30100.MAX30100(i2c=i2c,sample_rate=100,
                 led_current_ir=50.0,
                 pulse_width=1600)

print('Reading MAX30100 registers...')
print(sensor.get_registers())

sensor.disable_spo2()


print('Reading sensor...')
prev=0
hrSpo2=HRSpo2(debug=True)
while(True):
    sensor.read_sensor()
    val=sensor.ir
    hrSpo2.update(val)
    if(hrSpo2.result.pulseDetected==True):
        print(hrSpo2.result.heartBPM)
    
    
    
#     dcFilterIR,prev=convert.dcRemove(val,prev)   
#     meanDiffResIR=convert.meanDiff(dcFilterIR,meanDiffIR)
#     convert.lowPassButterworthFilter(meanDiffResIR,lpbFilterIR)
#     irACValueSqSum +=  dcFilterIR* dcFilterIR
#     samplesRecorded+=1
    
    
  
