from machine import  Pin, I2C
from time import sleep_ms
from MPR121 import MPR121

SCL_pin = Pin("SCL")
SDA_pin = Pin("SDA")

L0 = Pin("D0", Pin.OUT)
L1 = Pin("D1", Pin.OUT)
L2 = Pin("D4", Pin.OUT)
L3 = Pin("D3", Pin.OUT)
L4 = Pin("D2", Pin.OUT)
L5 = Pin("D5", Pin.OUT)
L6 = Pin("D6", Pin.OUT)
L7 = Pin("D7", Pin.OUT)


i2c = I2C(3, scl = SCL_pin, sda = SDA_pin, freq = 400000)

cap = MPR121(i2c)
  

while(True):
    i = cap.get_sensors()
    L6.toggle()
    L4.toggle()
    L2.toggle()
    L0.toggle()
    sleep_ms(10 + i)
    L7.toggle()
    L5.toggle()
    L3.toggle()
    L1.toggle()
    sleep_ms(10 + i)