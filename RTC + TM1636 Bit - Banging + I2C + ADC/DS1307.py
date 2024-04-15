from micropython import const


DS1307_I2C_address = const(0x68)

DS1307_sec_reg = const(0x00)
DS1307_min_reg = const(0x01)
DS1307_hr_reg = const(0x02)
DS1307_day_reg = const(0x03)
DS1307_date_reg = const(0x04)
DS1307_month_reg = const(0x05)
DS1307_year_reg = const(0x06)
DS1307_control_reg = const(0x07)


class DS1307():
    def __init__(self, _I2C):
        self.i2c = _I2C
        self.set_control(False , False, 0x00)
        self.start()
        
    
    def write(self, reg, value):
        if not type(value) is bytearray:
            value = bytearray([value])        
        self.i2c.writeto_mem(DS1307_I2C_address, reg, value)
        
        
    def read(self, reg):
        value = self.i2c.readfrom_mem(DS1307_I2C_address, reg, 1)    
        return value[0]
    
    
    def bcd_to_decimal(self, value):
        return ((value & 0x0F) + (((value & 0xF0) >> 0x04) * 0x0A))


    def decimal_to_bcd(self, value):
        return (((value // 0x0A) << 0x04) & 0xF0) | ((value % 0x0A) & 0x0F)
    
    
    def start(self):
         self.write(DS1307_sec_reg, 0x00)
         
         
    def stop(self):
         self.write(DS1307_sec_reg, 0x80)
    
    
    def get(self):
        second = self.bcd_to_decimal((self.read(DS1307_sec_reg) & 0x7F))
        minute = self.bcd_to_decimal((self.read(DS1307_min_reg) & 0x7F))
        hour = self.bcd_to_decimal((self.read(DS1307_hr_reg) & 0x3F))
        day = self.bcd_to_decimal((self.read(DS1307_day_reg) & 0x07))
        date = self.bcd_to_decimal((self.read(DS1307_date_reg) & 0x3F))
        month = self.bcd_to_decimal((self.read(DS1307_month_reg) & 0x1F))
        year = self.bcd_to_decimal(self.read(DS1307_year_reg))
        
        return hour, minute, second, date, day, month, year
    
    
    def set(self, hour, minute, second, date, day, month, year):
        self.stop()
        self.write(DS1307_sec_reg, self.decimal_to_bcd(second))
        self.write(DS1307_min_reg, self.decimal_to_bcd(minute))
        self.write(DS1307_hr_reg, self.decimal_to_bcd(hour))
        self.write(DS1307_day_reg, self.decimal_to_bcd(day))
        self.write(DS1307_date_reg, self.decimal_to_bcd(date))
        self.write(DS1307_month_reg, self.decimal_to_bcd(month))
        self.write(DS1307_year_reg, self.decimal_to_bcd(year))
        self.start()
        
        
    def set_control(self, output = False, SQWE = False, osc = 0x00):
        value = (output << 0x07)
        value |= (SQWE << 0x04)
        value |= (osc & 0x03)
        self.write(DS1307_control_reg, value)
    
    
    def write_RAM(self, addr, value):
        if((addr >= 0x08) and (addr <= 0x3F)):
            self.write(addr, value)
        
        else:
            print("Wrong RAM address!")
            
            
    def read_RAM(self, addr):
        if((addr >= 0x08) and (addr <= 0x3F)):
            value = self.read(addr)
            return value
        
        else:
            print("Wrong RAM address!")
            return -1