from machine import Pin, I2C
from TWI_LCD import PCF8574_LCD
from AHT21B import AHT21B
from time import sleep_ms


SCL_pin = Pin("SCL")
SDA_pin = Pin("SDA")

i2c = I2C(3, scl = SCL_pin, sda = SDA_pin, freq = 400000)

lcd = PCF8574_LCD(i2c)
rht = AHT21B(i2c)

lcd.clear_home()

lcd.goto_xy(0, 0)
lcd.put_str("RH/%:")
lcd.goto_xy(0, 1)
lcd.put_str("T/'C:")


while(True ):
    rh, t, status, crc = rht.read_sensor()
    lcd.goto_xy(11, 0)
    lcd.put_str(str("%2.2f " %rh))
    lcd.goto_xy(11, 1)
    lcd.put_str(str("%2.2f " %t))
    sleep_ms(600)