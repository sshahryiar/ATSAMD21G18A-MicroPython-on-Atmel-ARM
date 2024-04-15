from machine import  Pin
from time import sleep_us
from micropython import const


TM1636_Write_Display_Data_Cmd = const(0x40)
TM1636_Read_Key_Data_Cmd = const(0x42)
TM1636_Auto_Address_Increment = const(0x40)
TM1636_Fixed_Addressing = const(0x44)
TM1636_Normal_Mode = const(0x40)
TM1636_Test_Mode = const(0x48)

TM1636_Display_Address = const(0xC0)

TM1636_point = const(0x80)


seg_code_list = [
  0x3F, 0x06, 0x5B, 
  0x4F, 0x66, 0x6D, 
  0x7D, 0x07, 0x7F, 
  0x6F, 0x77, 0x7C, 
  0x39, 0x5E, 0x79, 
  0x71, 0x40, 0x00, 
  0x77, 0x58, 0x5E, 
  0x79, 0x71, 0x74, 
  0x10, 0x37, 0x54, 
  0x5C, 0x73, 0x50, 
  0x6D, 0x78, 0x3E
]


class TM1636():
    def __init__(self, _clk_pin, _data_pin):
        self.Off = const(0x80)
        self.On = const(0x88)
        self.dat_pin = _data_pin
        self.clk_pin = Pin(_clk_pin, Pin.OUT)
        self.data_pin = Pin(self.dat_pin, Pin.OUT)
        self.clear()
        
    
    def start(self):
        self.clk_pin.on()
        self.data_pin.on()
        self.data_pin.off()
        
    
    def stop(self):
        self.clk_pin.off()
        self.data_pin.off()
        self.clk_pin.on()
        self.data_pin.on()
        
        
    def ack(self):
        self.clk_pin.off()
        self.data_pin = Pin(self.dat_pin, Pin.IN, Pin.PULL_UP)
        while(self.data_pin.value()):
            pass
        self.clk_pin.on()
        self.clk_pin.off()
        self.data_pin = Pin(self.dat_pin, Pin.OUT)
         
         
    def write(self, value):
        for i in range(0, 8):
            self.clk_pin.off()
            
            if(value & 0x01):
                self.data_pin.on()
            else:
                self.data_pin.off()
            
            value >>= 1
            self.clk_pin.on()
            
    
    def read(self):
        value = 0
        
        self.start()
        self.write(TM1636_Read_Key_Data_Cmd)
        self.ack()
        self.data_pin.on()
        
        for i in range(0, 8):
            self.clk_pin.off()
            value >>= 1
            sleep_us(30)
            self.data_pin = Pin(self.dat_pin, Pin.IN, Pin.PULL_UP)
            
            if(self.data_pin.value()):
                value |= 0x80
                
            sleep_us(30)
            
        self.ack()
        self.stop()
        
        return value
        
        
    def show(self, value, pos, pt = False):
        self.start()
        self.write(TM1636_Fixed_Addressing)
        self.ack()
        self.stop()
        
        self.start()
        self.write((TM1636_Display_Address) | (pos & 0x03))
        self.ack()
        
        if(pt):
            self.write(seg_code_list[value] | TM1636_point)
        else:
            self.write(seg_code_list[value])
            
        self.ack()
        self.stop()
        
        
    def status(self, brightness, state):
        self.start()
        self.write((state | (brightness & 0x07)))
        self.ack()
        self.stop()
        
        
    def clear(self):
        for i in range (0, 4):
            self.show(0x11, i)