from machine import  Pin, I2C
from SSD1306_I2C import OLED1306
from QMC5883L import QMC5883L
from time import sleep_ms
import math


heading = 0

SCL_pin = Pin("SCL")
SDA_pin = Pin("SDA")

i2c = I2C(3, scl = SCL_pin, sda = SDA_pin, freq = 400000)

disp = OLED1306(i2c)
compass = QMC5883L(i2c)


def plot_heading(heading, on_off):
    v = (25 * math.sin(heading))
    h = (25 * math.cos(heading))    
    disp.line(63, 31, int(63 + h), int(31 + v), on_off)

disp.fill(0x00)
disp.circle(63, 31, 30, 0, 1)


while(True ):
    
    x, y, z = compass.get_axes()
    plot_heading(heading, 0)
    heading, deg = compass.heading(z, x)
    print(deg)
    plot_heading(heading, 1)
    sleep_ms(1000)