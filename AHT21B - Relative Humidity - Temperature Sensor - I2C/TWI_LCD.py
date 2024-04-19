from time import sleep_ms
from micropython import const


clear_display = const(0x01)
goto_home = const(0x02)
         
cursor_direction_inc = const(0x06)
cursor_direction_dec = const(0x04)
display_shift = const(0x05)
display_no_shift = const(0x04)

display_on = const(0x0C)
display_off = const(0x0A)
cursor_on = const(0x0A)
cursor_off = const(0x08)
blink_on = const(0x09)
blink_off = const(0x08)
                                    
_8_pin_interface = const(0x30)
_4_pin_interface = const(0x20)
_2_row_display = const(0x28)
_1_row_display = const(0x20)
_5x10_dots = const(0x60)
_5x7_dots = const(0x20)

line_1_y_pos = const(0x00)
line_2_y_pos = const(0x40)
line_3_y_pos = const(0x14)
line_4_y_pos = const(0x54)

BL_ON = const(1)
BL_OFF = const(0)

DAT = const(1)
CMD = const(0)


class TWI_LCD():
    def ___init__(self):
        self.init()
        
        
    def init(self):
        self.bl_state = BL_ON
        self.data_value |= 0x04        
        self.write(self.data_value)
        sleep_ms(10)
        self.send_data(0x33, CMD)
        self.send_data(0x32, CMD)
        self.send_data((_4_pin_interface | _2_row_display | _5x7_dots), CMD)
        self.send_data((display_on | cursor_off | blink_off), CMD)
        self.send_data(clear_display, CMD)
        self.send_data((cursor_direction_inc | display_no_shift), CMD)
        
        
    def send_data(self, value, mode):              
        if(mode == CMD):
            self.data_value &= 0xF4
        else:
            self.data_value |= 0x01
            
        if(self.bl_state == BL_ON):
            self.data_value |= 0x08
        else:
            self.data_value &= 0xF7
            
        self.write(self.data_value)
        self.quad_bit_send(value)
        sleep_ms(1)
        
                
    def toggle_EN(self):
        self.data_value |= 0x04
        self.write(self.data_value)
        sleep_ms(1)
        self.data_value &= 0xF9
        self.write(self.data_value)
        sleep_ms(1)


    def quad_bit_send(self, lcd_data):        
        temp = (lcd_data & 0xF0)
        self.data_value &= 0x0F
        self.data_value |= temp
        self.write(self.data_value)
        self.toggle_EN()        
        temp = (lcd_data & 0x0F)
        temp <<= 0x04
        self.data_value &= 0x0F
        self.data_value |= temp
        self.write(self.data_value)
        self.toggle_EN()
        
        
    def clear_home(self):        
        self.send_data(clear_display, CMD)
        self.send_data(goto_home, CMD)
        
        
    def goto_xy(self, x_pos, y_pos):
        if(y_pos == 1):
            self.send_data((0x80 | (x_pos + line_2_y_pos)), CMD)
            
        elif(y_pos == 2):
            self.send_data((0x80 | (x_pos + line_3_y_pos)), CMD)
            
        elif(y_pos == 3):
            self.send_data((0x80 | (x_pos + line_4_y_pos)), CMD)
            
        else:
            self.send_data((0x80 | (x_pos + line_1_y_pos)), CMD)
         
             
    def put_chr(self, ch):        
        self.send_data(ord(ch), DAT)
            
            
    def put_str(self, ch_string):        
        for chr in ch_string:
            self.put_chr(chr)
        
        
        
        
PCF8574_DEFAULT_I2C_ADDRESS = const(0x27)
        

class PCF8574_LCD(TWI_LCD):    
    def __init__(self, i2c, i2c_addr = PCF8574_DEFAULT_I2C_ADDRESS):        
        self.i2c = i2c
        self.addr = i2c_addr
        self.bl_state = 0
        self.data_value = 0
        self.init()        
        
        
    def read(self, mask):
        self.write(mask)
        retval = self.i2c.readfrom(self.addr, 1)    
        return retval[0]
        
        
    def write(self, value):
        self.i2c.writeto(self.addr, bytes([value]))
        