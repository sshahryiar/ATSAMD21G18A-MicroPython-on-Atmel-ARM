from micropython import const
from time import sleep_ms


disp_width = const(128)
disp_height = const(64)
x_size = const(128)
x_max = const(x_size)
x_min = const(0)
y_size = const(64)
y_max = const(y_size >> 3)
y_min = const(0)

buffer_size = const(x_max * y_max)


buffer = bytearray(buffer_size)

# Constants
SSD1306_I2C_address = const(0x3C)

SSD1306_SET_CONTRAST = const(0x81)
SSD1306_DISPLAY_ALL_ON_RESUME = const(0xA4)
SSD1306_DISPLAY_ALL_ON = const(0xA5)
SSD1306_NORMAL_DISPLAY = const(0xA6)
SSD1306_INVERT_DISPLAY = const(0xA7)
SSD1306_DISPLAY_OFF = const(0xAE)
SSD1306_DISPLAY_ON = const(0xAF)
SSD1306_SET_DISPLAY_OFFSET = const(0xD3)
SSD1306_SET_COM_PINS = const(0xDA)
SSD1306_SET_VCOM_DETECT = const(0xDB)
SSD1306_SET_DISPLAY_CLOCK_DIV = const(0xD5)
SSD1306_SET_PRECHARGE = const(0xD9)
SSD1306_SET_MULTIPLEX = const(0xA8)
SSD1306_SET_LOW_COLUMN = const(0x00)
SSD1306_SET_HIGH_COLUMN = const(0x10)
SSD1306_SET_START_LINE = const(0x40)
SSD1306_MEMORY_MODE = const(0x20)
SSD1306_COLUMN_ADDR = const(0x21)
SSD1306_PAGE_ADDR = const(0x22)
SSD1306_COM_SCAN_INC = const(0xC0)
SSD1306_COM_SCAN_DEC = const(0xC8)
SSD1306_SEG_REMAP = const(0xA0)
SSD1306_CHARGE_PUMP = const(0x8D)
SSD1306_EXTERNAL_VCC = const(0x01)
SSD1306_SWITCH_CAP_VCC = const(0x02)
SSD1306_SET_PAGE_START_ADDR = const(0xB0)

SSD1306_ACTIVATE_SCROLL = const(0x2F)
SSD1306_DEACTIVATE_SCROLL = const(0x2E)
SSD1306_SET_VERTICAL_SCROLL_AREA = const(0xA3)
SSD1306_RIGHT_HORIZONTAL_SCROLL = const(0x26)
SSD1306_LEFT_HORIZONTAL_SCROLL = const(0x27)
SSD1306_VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL = const(0x29)
SSD1306_VERTICAL_AND_LEFT_HORIZONTAL_SCROLL  = const(0x2A)

CMD = const(0x00)
DAT = const(0x60)


class OLED1306():
    def __init__(self, _i2c, _i2c_addr = SSD1306_I2C_address):      
        self.WHITE = 1
        self.BLACK = 0
        
        self.i2c = _i2c
        self.i2c_addr = _i2c_addr

        self.temp = bytearray(2) 

        self.init_display()


    def write(self, value, dat_cmd):
        self.temp[0] = dat_cmd  
        self.temp[1] = value
        self.i2c.writeto(self.i2c_addr, self.temp)


    def init_display(self):
        self.clr_all()
        self.write(SSD1306_DISPLAY_OFF, CMD)
        self.write(SSD1306_SET_DISPLAY_CLOCK_DIV, CMD)
        self.write(0x80, CMD)

        self.write(SSD1306_SET_MULTIPLEX, CMD)
        self.write(0x3F, CMD)

        self.write(SSD1306_SET_DISPLAY_OFFSET, CMD)
        self.write(0x00, CMD)

        self.write((SSD1306_SET_START_LINE | 0x00), CMD)
   
        self.write(SSD1306_CHARGE_PUMP, CMD)
        self.write(0x14, CMD)  # 0x10  # 0x14

        self.write(SSD1306_MEMORY_MODE, CMD)
        self.write(0x00, CMD)

        self.write((SSD1306_SEG_REMAP | 0x01), CMD)
        self.write(SSD1306_COM_SCAN_DEC, CMD)
        self.write(SSD1306_SET_COM_PINS, CMD)
        self.write(0x12, CMD)

        self.write(SSD1306_SET_CONTRAST, CMD)
        self.write(0x9F, CMD) # 0x9F # 0xCF

        self.write(SSD1306_SET_PRECHARGE, CMD)
        self.write(0xF1, CMD) # 0x22 # 0xF1

        self.write(SSD1306_SET_VCOM_DETECT, CMD)
        self.write(0x40, CMD)

        self.write(SSD1306_DISPLAY_ALL_ON_RESUME, CMD)
        self.write(SSD1306_NORMAL_DISPLAY, CMD)
        self.write(SSD1306_DISPLAY_ON, CMD)
        
        
    def gotoxy(self, x_pos, y_pos):
        self.write((SSD1306_SET_PAGE_START_ADDR + y_pos), CMD)
        self.write((SSD1306_SET_LOW_COLUMN | (x_pos & 0x0F)), CMD)
        self.write((SSD1306_SET_HIGH_COLUMN | ((x_pos & 0xF0) >> 0x04)), CMD)
        
    
    def fill(self, bmp):
        for p in range(0, y_max):
            self.gotoxy(x_min, p)
            for i in range(x_min, x_max):
                self.write(bmp, DAT)
                
                
    def clr_buffer(self):
        for i in range (0, buffer_size):
            buffer[i] = 0x00
        
    
    def clr_screen(self):
        self.fill(0x00)
        
        
    def clr_all(self):
        self.clr_buffer()
        self.clr_screen()
        
        
    def pixel(self, x_pos, y_pos, colour):
        page = (y_pos // y_max)
        bit_pos = (y_pos - (page * y_max))
        value = buffer[(page * x_max) + x_pos]
        
        if(colour):
            value |= (1 << bit_pos)
        
        else:
            value &= (~(1 << bit_pos))
            
        buffer[((page * x_max) + x_pos)] = value
        self.gotoxy(x_pos, page)
        self.write(value, DAT)


    def line(self, x1, y1, x2, y2, colour):
        dx = (x2 - x1)
        dy = (y2 - y1)
        
        if (dy < 0):
            dy = -dy
            stepy = -1
        else:
            stepy = 1
            
        if (dx < 0):
            dx = -dx
            stepx = -1
        else:
            stepx = 1

        dx <<= 1
        dy <<= 1
        
        self.pixel(x1, y1, colour)
        
        if(dx > dy):
            fraction = (dy - (dx >> 1))
            while(x1 != x2):
                if(fraction >= 0):
                    y1 += stepy
                    fraction -= dx
                
                x1 += stepx
                fraction += dy
                
                self.pixel(x1, y1, colour)
                
        else:
            fraction = (dx - (dy >> 1))
            while(y1 != y2):
                if(fraction >= 0):
                    x1 += stepx
                    fraction -= dy
                
                y1 += stepy
                fraction += dx
                
                self.pixel(x1, y1, colour)
        
        
    def rect(self,  x1, y1, x2, y2, fill, colour):
        if(fill):
            if(x1 < x2):
                xmin = x1
                xmax = x2;
            else:
                xmin = x2
                xmax = x1
                
            if(y1 < y2):
                ymin = y1
                ymax = y2;
            else:
                ymin = y2
                ymax = y1
            
            while(xmin <= xmax):
                xmin += 1
                for i in range(ymin, ymax):
                    i += 1
                    self.pixel(xmin, i, colour)
                    
        else:
            self.line(x1, y1, x2, y1, colour)
            self.line(x1, y2, x2, y2, colour)
            self.line(x1, y1, x1, y2, colour)
            self.line(x2, y1, x2, y2, colour)
            
            
    def circle(self, xc, yc, r, fill, colour):
        a = 0
        b = r
        P = (1 - b)
        
        while(a < (b  + 1)):
            if(fill):
                self.line((xc - a), (yc + b), (xc + a), (yc + b), colour)
                self.line((xc - a), (yc - b), (xc + a), (yc - b), colour)
                self.line((xc - b), (yc + a), (xc + b), (yc + a), colour)
                self.line((xc - b), (yc - a), (xc + b), (yc - a), colour)
                
            else:
                self.pixel((xc + a), (yc + b), colour)
                self.pixel((xc + b), (yc + a), colour)
                self.pixel((xc - a), (yc + b), colour)
                self.pixel((xc - b), (yc + a), colour)
                self.pixel((xc + b), (yc - a), colour)
                self.pixel((xc + a), (yc - b), colour)
                self.pixel((xc - a), (yc - b), colour)
                self.pixel((xc - b), (yc - a), colour)
                
            if(P < 0):
                a += 1
                P += (3 + (2 * a))
            
            else:
                a += 1
                b -= 1
                P += (5 + (2 * (a - b)))
            