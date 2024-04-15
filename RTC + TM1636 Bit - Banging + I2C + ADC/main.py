from machine import  Pin, SoftI2C, ADC
from micropython import const
from time import sleep_ms
from TM1636 import TM1636
from DS1307 import DS1307


Menu_BTN = const(0x01)
Inc_BTN = const(0x02)
Dec_BTN = const(0x03)


i = 0
hour = 10
minute = 10
second = 30
date = 1
day = 1
month = 1
year = 0
disp_mode = 0
run = True


G_LED = Pin('D2', Pin.OUT)
Y_LED = Pin('D3', Pin.OUT)
R_LED = Pin('D4', Pin.OUT)
B_LED = Pin('D5', Pin.OUT)

BUZZER = Pin('D6', Pin.OUT)

menu_key = Pin('D11', Pin.IN, Pin.PULL_UP)
inc_key = Pin('D10', Pin.IN, Pin.PULL_UP)
dec_key = Pin('D9', Pin.IN, Pin.PULL_UP)

disp = TM1636("D7", "NEOPIXEL")
disp.status(2, disp.On)

i2c = SoftI2C(scl = Pin('A5'), sda = Pin('A4'), freq = 100000)
rtc = DS1307(i2c)

adc_pin = Pin('A1')
adc_pin.init()
light_lvl = ADC(adc_pin)


def check_RTC():
    if(rtc.read_RAM(0x09) == 0x00):
        pass
    
    else:
        rtc.set(hour, minute, second, day, date, month, year)
        rtc.write_RAM(0x09, 0x00)
        


def LED_states(r, g, y, b):
    R_LED.value(r)
    G_LED.value(g)
    Y_LED.value(y)
    B_LED.value(b)


def key_click():
    BUZZER.on()
    sleep_ms(4)
    BUZZER.off()


def get_key():
    if(menu_key.value() == False):
        key_click()
        return Menu_BTN
    
    elif(inc_key.value() == False):
        key_click()
        return Inc_BTN
    
    elif(dec_key.value() == False):
        key_click()
        return Dec_BTN
    
    else:
        return 0

 
def change_value(value, value_min, value_max):
    if(get_key() == Inc_BTN):
        value += 1
    
    if(value > value_max):
        value = value_min
         
    if(get_key() == Dec_BTN):
         value -= 1
         
    if(value < value_min):
        value = value_max
        
    return value


def show_num(value, dot_1 = False , dot_2 = False):
    disp.show((value // 1000), 0, False)
    disp.show(((value % 1000) // 100), 1, False)
    disp.show(((value % 100) // 10), 2, dot_1)
    disp.show((value  % 10), 3, dot_2)
    
    
def show_time(tgl):
    global hour, minute
    show_num(((hour * 100) + minute), tgl, tgl)
    LED_states(1, 0, 0, 0)
    
    
def show_date():
    global date, month
    show_num(((date * 100) + month), False, True)
    LED_states(0, 1, 0, 0)
 
 
def show_day():
    global day
    tmp = bytearray(4)
    
    LED_states(0, 0, 1, 0)
                
    if(day == 1):
        tmp[0] = 30
        tmp[1] = 32
        tmp[2] = 26
        tmp[3] = 17
        
    elif(day == 2):
        tmp[0] = 25
        tmp[1] = 25
        tmp[2] = 27
        tmp[3] = 26
        
    elif(day == 3):
        tmp[0] = 31
        tmp[1] = 32
        tmp[2] = 21
        tmp[3] = 17
        
    elif(day == 4):
        tmp[0] = 32
        tmp[1] = 32
        tmp[2] = 21
        tmp[3] = 20
        
    elif(day == 5):
        tmp[0] = 31
        tmp[1] = 23
        tmp[2] = 29
        tmp[3] = 17
        
    elif(day == 6):
        tmp[0] = 22
        tmp[1] = 29
        tmp[2] = 24
        tmp[3] = 17
                
    else:
        tmp[0] = 30
        tmp[1] = 18
        tmp[2] = 31
        tmp[3] = 17
        
    for i in range(0, 4):
        disp.show(tmp[i], i)
        
        
def show_year():
    global year
    show_num((2000 + year), False, False)
    LED_states(0, 0, 0, 1)
        
        
def set_date_time():
    global disp_mode, hour, minute, second, day, date, month, year, toggle, run
    
    if((get_key() == Menu_BTN) and (run == True)):
        while(get_key() == Menu_BTN):
            pass
        run = False
        toggle = 1
        disp_mode = 1
       
    if(get_key() == Menu_BTN):
        while(get_key() == Menu_BTN):
            pass
        disp_mode += 1
        
    if(disp_mode == 1):
        hour = change_value(hour, 0, 23)
        
    if(disp_mode == 2):
        minute = change_value(minute, 0, 59)
        
    if(disp_mode == 3):
        date = change_value(date, 1, 31)
        
    if(disp_mode == 4):
        month = change_value(month, 1, 12)
        
    if(disp_mode == 5):
        day = change_value(day, 0, 6)
        
    if(disp_mode == 6):
        year = change_value(year, 0, 99)
       
    if((disp_mode == 7) and (run == False)):
        disp.clear()        
        LED_states(1, 1, 1, 1)        
        rtc.set(hour, minute, second, date, day, month, year)
        sleep_ms(400)
        rtc.write_RAM(0x09, 0x00)
        sleep_ms(200)
        LED_states(0, 0, 0, 0)
        disp_mode = 1
        run = True
        

def run_rtc():
    global disp_mode, hour, minute, second, day, date, month, year, toggle, run
    
    if(run == True):
        hour, minute, second, date, day, month, year = rtc.get()
        disp_mode += 1
        
        if(disp_mode >= 7):
            disp_mode = 1

        sleep_ms(900)
    
    else:
        disp.clear()
        sleep_ms(20)

            
def show_items():
    global disp_mode, hour, minute, second, day, date, month, year
    j = 0
     
    if(disp_mode  < 3):
        if(run == True):
            for i in range(0, 6):
                sleep_ms(450)
                show_time(j)
                j ^= 1
                
        else:
            show_time(1)
                        
    if((disp_mode == 3) or (disp_mode  == 4)):
                        show_date()
                        
    if(disp_mode == 5):
        show_day()
         
    if(disp_mode == 6):
        show_year()
        
        
def adjust_brightness():
    lvl = ((light_lvl.read_u16() - 20000) // 7000)    
    disp.status((7 - lvl), disp.On)
    
    
check_RTC()


while(True ):
    show_items()
    set_date_time()
    run_rtc()
    adjust_brightness()
    


