from machine import  Pin,  DAC
from time import sleep_ms, ticks_ms


t1 = 0
t2 = 0
value = 500


S1 = Pin("D0", Pin.IN)
S2 = Pin("D1", Pin.IN)

dac = DAC(0)


def S1_EXTI(pin):
    global t1
    t1 = ticks_ms()
    

def S2_EXTI(pin):
    global t2
    t2= ticks_ms()
    
    
S1.irq(trigger = Pin.IRQ_FALLING, handler = S1_EXTI) 
S2.irq(trigger = Pin.IRQ_FALLING, handler = S2_EXTI)



while(True ):
    print("T1: " + str("%u" %t1) + "  T2: " + str("%u" %t2) + "  DAC: " + str("%4u" %value))
    
    if(t1 > t2):
        print("Left to Right")
        value -= 50
        t1 = 0
        t2 = 0
        
    if(t2 > t1):
        print("Right to Left")
        value += 50
        t1 = 0
        t2 = 0
        
    if(value > 1000):
        value = 1000
        
    if(value <= 0):
        value = 0
        
    dac.write(value)
        
    sleep_ms(400)
