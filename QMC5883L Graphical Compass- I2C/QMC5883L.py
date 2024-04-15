from micropython import const
from time import sleep_ms
import math


QMC5883L_I2C_address = const(0x0D)

QMC5883L_output_X_LSB_reg = const(0x00)
QMC5883L_output_X_MSB_reg = const(0x01)
QMC5883L_output_Y_LSB_reg = const(0x02)
QMC5883L_output_Y_MSB_reg = const(0x03)
QMC5883L_output_Z_LSB_reg = const(0x04)
QMC5883L_output_Z_MSB_reg = const(0x05)
QMC5883L_status_reg = const(0x06)
QMC5883L_T_output_LSB_reg = const(0x07)
QMC5883L_T_output_MSB_reg = const(0x08)
QMC5883L_control_reg_1 = const(0x09)
QMC5883L_control_reg_2 = const(0x0A)
QMC5883L_period_set_reset_reg = const(0x0B)

QMC5883L_DRDY_flag = const(0x01)
QMC5883L_OVL_flag = const(0x02)
QMC5883L_DOR_flag = const(0x04)

QMC5883L_standby_mode = const(0x00)
QMC5883L_continuous_mode = const(0x01)

QMC5883L_output_data_rate_10Hz = const(0x00)
QMC5883L_output_data_rate_50Hz = const(0x04)
QMC5883L_output_data_rate_100Hz = const(0x08)
QMC5883L_output_data_rate_200Hz = const(0x0C)

QMC5883L_full_scale_range_2G = const(0x00)
QMC5883L_full_scale_range_8G = const(0x10)

QMC5883L_over_sample_ratio_512 = const(0x00)
QMC5883L_over_sample_ratio_256 = const(0x40)
QMC5883L_over_sample_ratio_128 = const(0x80)
QMC5883L_over_sample_ratio_64 = const(0xC0)

QMC5883L_interrupt_pin_disable = const(0x00)
QMC5883L_interrupt_pin_enable = const(0x01)

QMC5883L_I2C_pointer_roll_over_off = const(0x00)
QMC5883L_I2C_pointer_roll_over_on = const(0x40)

QMC5883L_soft_reset = const(0x80)


class QMC5883L():
    
    def __init__(self, _i2c):
        self.i2c = _i2c        
        self.init()
        
        
    def write(self, reg, value):
        if not type(value) is bytearray:
            value = bytearray([value])
        
        self.i2c.writeto_mem(QMC5883L_I2C_address, reg, value)
        
        
    def read_byte(self, reg):
        retval = self.i2c.readfrom_mem(QMC5883L_I2C_address, reg, 0x01)    
        return retval[0x00]
    
    
    def read_word(self, reg):        
        value = self.i2c.readfrom_mem(QMC5883L_I2C_address, reg, 0x02)
        retval = value[0x01]
        retval <<= 0x08
        retval |= value[0x00]
        
        return retval
    
    
    def read_signed_word(self, address):
        retval = self.read_word(address)

        if(retval > 32767):
            retval -= 65536

        return retval
        
        
    def init(self):
        self.write(QMC5883L_control_reg_2, QMC5883L_soft_reset)
        sleep_ms(10)
        self.write(QMC5883L_period_set_reset_reg, 0x01)
        self.write(QMC5883L_control_reg_1, (QMC5883L_continuous_mode | QMC5883L_output_data_rate_10Hz | QMC5883L_full_scale_range_2G | QMC5883L_over_sample_ratio_512))
        
        
    def get_T(self):
        value = self.read_signed_word(QMC5883L_T_output_LSB_reg)
        tmp = (value / -100.0)
        
        return tmp
    
    
    def get_axes(self):
        x_axis = self.read_signed_word(QMC5883L_output_X_LSB_reg)        
        y_axis = self.read_signed_word(QMC5883L_output_Y_LSB_reg) 
        z_axis = self.read_signed_word(QMC5883L_output_Z_LSB_reg) 
        
        return (x_axis, y_axis, z_axis) 
    
    
    def heading(self, a, b):
        pi = 3.142
  
        value = math.atan2(a, b)
        
        if(value < 0):
            value += (2 * pi)
            
        if(value > (2 * pi)):
            value -= (2 * pi)
            
        deg = (value * (180 / pi))        
        return value, deg
        