from micropython import const
from machine import  Pin


MAX31865_CONFIG_REG = const(0x00)
MAX31865_RTD_MSB_REG = const(0x01)
MAX31865_RTD_LSB_REG = const(0x02)
MAX31865_HFAULT_MSB_REG = const(0x03)
MAX31865_HFAULT_LSB_REG = const(0x04)
MAX31865_LFAULT_MSB_REG = const(0x05)
MAX31865_LFAULT_LSB_REG = const(0x06)
MAX31865_FAULT_STATUS_REG = const(0x07)

#    Configuration Definitions
MAX31865_CONFIG_BIAS = const(0x80)
MAX31865_CONFIG_MODE_AUTO = const(0x40)
MAX31865_CONFIG_MODE_OFF = const(0x00)
MAX31865_CONFIG_1SHOT = const(0x20)
MAX31865_CONFIG_3_WIRE = const(0x10)
MAX31865_CONFIG_2_or_4_WIRE = const(0x00)
MAX31865_CONFIG_FAULT_STATUS = const(0x02)
MAX31865_CONFIG_FILTER_50Hz = const(0x01)
MAX31865_CONFIG_FILTER_60Hz = const(0x00)

#    Fault Definitions 
MAX31865_FAULT_HIGH_THRESHOLD = const(0x80)
MAX31865_FAULT_LOW_THRESHOLD = const(0x40)
MAX31865_FAULT_REF_IN_LOW = const(0x20)
MAX31865_FAULT_REF_IN_HIGH = const(0x10)
MAX31865_FAULT_RTD_IN_LOW = const(0x08)
MAX31865_FAULT_OV_UV = const(0x04)

MAX31865_RTD_A = 0.00390803
MAX31865_RTD_B = -0.000000577
MAX31865_Reference_Resistance = 430
MAX31865_RTD_Nominal_Value = 100.0 # 100 for PT100  and  1000 for PT1000
                             
                             
class MAX31865():
    def __init__(self, _spi, _csn):
        self.spi = _spi
        self.csn = Pin(_csn, Pin.OUT)
        self.init()
        
        
    def init(self):
        self.csn.on()
        self.write_byte(MAX31865_CONFIG_REG, MAX31865_CONFIG_BIAS
                        | MAX31865_CONFIG_MODE_AUTO
                        | MAX31865_CONFIG_2_or_4_WIRE
                        | MAX31865_CONFIG_FAULT_STATUS
                        | MAX31865_CONFIG_FILTER_60Hz)
        
    def write_byte(self, address, value):
        self.csn.off()
        self.spi.write(bytearray([address | 0x80]))
        self.spi.write(bytearray([value]))
        self.csn.on()
        
        
    def read_byte(self, address):
        retval = 0
        self.csn.off()
        self.spi.write(bytearray([address]))
        retval = self.spi.read(0x01, 0x00)
        self.csn.on()
        return retval[0]
    
    
    def read_word(self, address):
        hb = 0
        lb = 0
        retval = 0
        
        hb = self.read_byte(address)
        lb = self.read_byte(address + 1)
        
        retval = ((hb << 0x08) | lb)
        return retval
    
    
    def get_RTD(self):
        value = 0
        value = self.read_word(MAX31865_RTD_MSB_REG)
        value >>= 1
        return value
    
    
    def get_T(self):
        rt = 0
        T = 0
        
        T = self.get_RTD()
        rt = (T * MAX31865_Reference_Resistance)
        rt /= 32768
        rt /= MAX31865_RTD_Nominal_Value
        rt = (rt -1)
        T = (rt / MAX31865_RTD_A)
        
        return T
        
        
        
        