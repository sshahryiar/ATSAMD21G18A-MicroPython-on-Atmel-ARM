from machine import UART, Pin
from time import sleep_ms
from US100 import US100
from lcd import LCD

r = 0

disp = LCD('NEOPIXEL', 'D9', 'D2', 'D5', 'D6', 'D7')

uart = UART(0, tx = Pin('D1'), rx = Pin('D0'), baudrate = 9600)

sonar = US100(uart)

disp.goto_xy(0, 0)
disp.put_str("PY SAMD21 SONAR")
disp.goto_xy(0, 1)
disp.put_str("Range/mm:")


while(True):
    r = sonar.get_avg_range()
    disp.goto_xy(12, 1)
    disp.put_str(str("%4u" %r))    
    sleep_ms(400)