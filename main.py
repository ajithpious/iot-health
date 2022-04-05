#ajith
from umqtt.robust import MQTTClient
from machine import Pin,I2C

sda=Pin(21)
scl=Pin(22)             
i2c = I2C(scl=scl,sda=sda)
print('Scanning I2C devices...')
print(i2c.scan())

sensor = max30100.MAX30100(i2c=i2c)

print('Reading MAX30100 registers...')
print(sensor.get_registers())

sensor.enable_spo2()

print('Reading sensor...')

for count in range(500):  
  sensor.read_sensor()
  print(sensor.ir, sensor.red)  
  time.sleep(0.5)
