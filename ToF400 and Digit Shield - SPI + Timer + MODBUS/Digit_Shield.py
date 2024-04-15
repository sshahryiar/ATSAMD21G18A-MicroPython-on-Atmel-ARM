from machine import Pin, SoftSPI, Timer


seg_pos_list = [
    0xE0, # 1st
    0xD0, # 2nd
    0xB0, # 3rd
    0x70, # 4th
]


seg_value = [
    0x00,   #  0
    0x08,   #  1
    0x04,   #  2
    0x0C,   #  3
    0x02,   #  4
    0x0A,   #  5
    0x06,   #  6
    0x0E,   #  7
    0x01,   #  8
    0x09,   #  9
]


class digit_shield():
    def __init__(self):
        self.pt = 0
        self.seg = 0
        self.val = 0
        self.dot_state = 0
        self.pt_pos = 0
        self.value = 0
        self.RCK_Pin = Pin("D3", Pin.OUT)
        self.DOT_Pin = Pin("D5", Pin.OUT)
        self.soft_spi = SoftSPI(baudrate = 400000, polarity = 0, phase = 0, sck = Pin('D4'), mosi = Pin('D2'), miso =  Pin('D13'))
        self.timer = Timer()
        self.timer.init(mode = Timer.PERIODIC, period = 1,  callback = self.timer_isr)
       
                        
    def send(self, value, pos):
        temp = seg_value[value]
        temp |= seg_pos_list[pos]

        self.RCK_Pin.off()
        self.soft_spi.write(bytearray([temp]))
        self.RCK_Pin.on()
        
    
    def timer_isr(self, t):
        self.DOT_Pin.on()  
        if(self.seg == 0):
            self.val = ((self.value // 1000) % 1000)
        elif(self.seg == 1):
            self.val = ((self.value % 1000) // 100)
        elif(self.seg == 2):
            self.val = ((self.value % 100) // 10)
        else:
            self.val = (self.value % 10)
        
        self.send(self.val, self.seg)
        
        if((self.pt_pos == self.seg) and (self.dot_state)):
           self.DOT_Pin.off()     
        else:
           self.DOT_Pin.on()    
        
        self.seg += 1
        
        if(self.seg > 3):
            self.seg = 0
            
    
    def write(self, num, pos = 4, dot = False):
        if(num >= 9999):
            num = 9999
            
        if(num <= 0):
            num = 0
        
        self.value = num
        self.pt_pos = pos
        self.dot_state = dot
        
            