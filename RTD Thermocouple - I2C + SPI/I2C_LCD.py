from time import sleep_ms
from micropython import const


"""
Pinout of MCP23017 to LCD

GPIOA
      7      6     5    4    3    2    1    0
    EN  RW   RS   X    L-   L+  X   X   

GPIOB 
    7       6     5      4      3      2       1       0
    D7  D6   D5   D4    D3   D2    D1     D0
"""


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

DAT = const(1)
CMD = const(0)


class I2C_LCD():
    def __init__(self):
        self.init()
        
    
    def send(self, value, mode):
        if(mode):
            self.lcd_ctrl |= 0x20 
        else:
            self.lcd_ctrl &= 0xDF
        
        self.write(MCP23017_GPIOA, self.lcd_ctrl)
        self.send_data(value)
        
    
    def send_data(self, value):
        if(self.bits):
            self.write(MCP23017_GPIOB, value)
            self.toggle_EN()
        else:
            self.write(MCP23017_GPIOB, (value & 0xF0))
            self.toggle_EN()
            self.write(MCP23017_GPIOB, ((value & 0x0F) << 4))
            self.toggle_EN()
        
        
    def toggle_EN(self):
        self.lcd_ctrl |= 0x80
        self.write(MCP23017_GPIOA, self.lcd_ctrl)
        sleep_ms(1)
        self.lcd_ctrl &= 0x7F
        self.write(MCP23017_GPIOA, self.lcd_ctrl)
        sleep_ms(1)
        

    def init(self):
        if(self.bits):
            self.send((_8_pin_interface | _2_row_display | _5x7_dots), CMD)
        else:
            self.send((_4_pin_interface | _2_row_display | _5x7_dots), CMD)
            
        self.send((display_on | cursor_off | blink_off), CMD) 
        self.send((clear_display), CMD)       
        self.send((cursor_direction_inc | display_no_shift), CMD)

        
        
    def clear_home(self):
        self.send(clear_display, CMD)
        self.send(goto_home, CMD)
        
        
    def goto_xy(self, x_pos, y_pos):
        if(y_pos == 1):
            self.send((0x80 | (line_2_y_pos + x_pos)), CMD)
            
        elif(y_pos == 2):
            self.send((0x80 | (line_3_y_pos + x_pos)), CMD)
            
        elif(y_pos == 3):
            self.send((0x80 | (line_4_y_pos + x_pos)), CMD)
            
        else:
            self.send((0x80 | (line_1_y_pos + x_pos)), CMD)
    
    
    def put_chr(self, ch):
        self.send(ord(ch), DAT)
        
        
    def put_str(self, ch_string):
        for chr in ch_string:
            self.put_chr(chr)



            
MCP23017_I2C_address = const(0x20)

MCP23017_IODIRA = const(0x00)        
MCP23017_IODIRB = const(0x01)      
MCP23017_IPOLA = const(0x02)       
MCP23017_IPOLB = const(0x03)      
MCP23017_GPINTENA = const(0x04) 
MCP23017_GPINTENB = const(0x05)      
MCP23017_DEFVALA = const(0x06)        
MCP23017_DEFVALB = const(0x07)
MCP23017_INTCONA = const(0x08)        
MCP23017_INTCONB = const(0x09)           
MCP23017_IOCON = const(0x0A)                      
MCP23017_GPPUA = const(0x0C)   
MCP23017_GPPUB = const(0x0D)      
MCP23017_INTFA = const(0x0E)       
MCP23017_INTFB = const(0x0F)   
MCP23017_INTCAPA = const(0x10)  
MCP23017_INTCAPB = const(0x11) 
MCP23017_GPIOA = const(0x12)      
MCP23017_GPIOB = const(0x13)     
MCP23017_OLATA = const(0x14)      
MCP23017_OLATB = const(0x15)                 
            
            
class MCP23017_LCD(I2C_LCD):
    def __init__(self, _i2c, lcd_bit_mode = True, default_i2c_address = MCP23017_I2C_address):
        self.i2c = _i2c
        self.addr = default_i2c_address
        self.bits = lcd_bit_mode 
        self.lcd_ctrl = 0x00
        self.init_GPIO()
        self.init()
        
        
    def init_GPIO(self):
        self.write(MCP23017_IOCON, 0x18)
        self.write(MCP23017_IODIRA, 0x00)
        self.write(MCP23017_IODIRB, 0x00)
        self.write(MCP23017_GPIOA, 0x00)
        self.write(MCP23017_GPIOB, 0x00)
        
        
    def read(self, address):
        retval = self.i2c.readfrom_mem(self.addr, address, 1)    
        return retval[0]
        
        
    def write(self, reg, value):
        if not type(value) is bytearray:
            value = bytearray([value])        
        self.i2c.writeto_mem(self.addr, reg, value)

