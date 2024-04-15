from machine import Pin, ADC
from time import sleep_ms


seg_pos_list = [
    0xF1, # 1st
    0xF2, # 2nd
    0xF4, # 3rd
    0xF8, # 4th
]

seg_value = [
    0xC0,   #  0
    0xF9,   #  1
    0xA4,  #  2
    0xB0,  #  3
    0x99,  #  4
    0x92,  #  5
    0x82,  #  6
    0xF8,  #  7
    0x80,  #  8
    0x90,  #  9
]


class MF_Shield():
    def __init__(self, A4_function = False ):
        self.RCK_Pin = Pin("D2", Pin.OUT)
        self.SCK_Pin = Pin("D7", Pin.OUT)
        self.SER_Pin = Pin("NEOPIXEL", Pin.OUT)
        
        self.LED_1_Pin = Pin("D10", Pin.OUT)
        self.LED_2_Pin = Pin("D11", Pin.OUT)
        self.LED_3_Pin = Pin("D12", Pin.OUT)
        self.LED_4_Pin = Pin("D13", Pin.OUT)
        self.write_LEDs(0, 0, 0, 0)
        
        self.Buzzer_Pin = Pin("D3", Pin.OUT)
        self.buzzer_state(False)
        
        self.Key_1_Pin = Pin("A1", Pin.IN)
        self.Key_2_Pin = Pin("A2", Pin.IN)
        self.Key_3_Pin = Pin("A3", Pin.IN)
        
        if(A4_function):
            self.temp = ADC(Pin('A4'), average = 16)
        else:
            self.Digital_Pin = Pin("A4", Pin.IN)
        
                
        
    def write_7_segments(self, value, pos, dot):
        clks = 0x10
        
        temp = seg_value[value] 
        temp <<= 8
        temp |= seg_pos_list[pos]
        
        if(dot == True):
            temp &= 0x7FFF     
  
        self.RCK_Pin.off()

        while(clks > 0):
            if((temp & 0x8000) != 0x00):
                self.SER_Pin.on()
            else:
                self.SER_Pin.off()

            self.SCK_Pin.on()
            temp <<= 1
            clks -= 1
            self.SCK_Pin.off()

        self.RCK_Pin.on()
        
        
    def write_LEDs(self, l1, l2, l3, l4):
        self.LED_1_Pin.value(~l1)
        self.LED_2_Pin.value(~l2)
        self.LED_3_Pin.value(~l3)
        self.LED_4_Pin.value(~l4)
        
        
    def buzzer_state(self, state):
        self.Buzzer_Pin.value(~state)
        sleep_ms(2)
                
        
    def read_keys(self):
        key_value = 0
        
        if(self.Key_1_Pin.value() == False):
            key_value |= 0x01
            
        if(self.Key_2_Pin.value() == False):
            key_value |= 0x02
            
        if(self.Key_3_Pin.value() == False):
            key_value |= 0x04

        return key_value
    
    
    def read_AN(self):
        return (self.temp.read_u16())
    
            
    def read_digital_pin(self):
        return self.Digital_Pin.value()
        
