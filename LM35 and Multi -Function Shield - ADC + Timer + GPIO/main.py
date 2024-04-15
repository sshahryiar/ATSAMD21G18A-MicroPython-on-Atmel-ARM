from machine import Timer
from time import sleep_ms
from MF_Shield import MF_Shield


pt = False
seg = 0
val = 0
value = 0


mf = MF_Shield(True)
tim0 = Timer()


def timer_callback(t):
    global val, seg, pt, value
    
    pt = False
            
    if(seg == 0):
        val = ((value // 1000) % 1000)
    elif(seg == 1):
        val = ((value % 1000) // 100)
        pt = True
    elif(seg == 2):
        val = ((value % 100) // 10)
    else:
        val = (value % 10)
    
    mf.write_7_segments(val, seg, pt)
    seg += 1
   
    if(seg > 3):
        seg = 0


tim0.init(mode = Timer.PERIODIC, period = 1,  callback = timer_callback)


while(True ):
    value = (mf.read_AN() >> 4)
    sleep_ms(900)
    