from machine import  Pin, I2C, SoftSPI
from time import sleep_ms, sleep_us
from I2C_LCD import MCP23017_LCD
from MAX31865 import MAX31865

T = 0

SCL_pin = Pin("SCL")
SDA_pin = Pin("SDA")

i2c = I2C(3, scl = SCL_pin, sda = SDA_pin, freq = 400000)
lcd = MCP23017_LCD(i2c)

spi = SoftSPI(baudrate=1000000, polarity=0, phase=0, sck = Pin('D10'), mosi = Pin('D11'), miso = Pin('D12'))
rtd = MAX31865(spi, 'D13')

lcd.clear_home()

lcd.goto_xy(0, 0)
lcd.put_str("MAX31865  SAMD21")
lcd.goto_xy(0, 1)
lcd.put_str("T/K:")


while(True):
    T = (rtd.get_T() + 273)
    lcd.goto_xy(10, 1)
    lcd.put_str(str("%3.1f" %T))
    sleep_ms(600)
