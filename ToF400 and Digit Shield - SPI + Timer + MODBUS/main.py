from machine import Pin, Timer, UART
from Digit_Shield import digit_shield
from ToF400 import ToF400
from time import sleep_ms



uart = UART(0, tx = Pin('D1'), rx = Pin('D0'), baudrate = 115200)

tof = ToF400(uart)
display = digit_shield()


while(True):
    r = tof.get_range()
    display.write(r)
    sleep_ms(1000)






