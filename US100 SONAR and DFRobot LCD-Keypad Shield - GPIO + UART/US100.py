from micropython import const
from time import sleep_ms


US100_RX_data_packet_size = const(2)


class US100():
    def __init__(self, _uart):
        self.uart = _uart
        
        
    def get_range(self):
        rx_data_frame = bytearray(US100_RX_data_packet_size)

        d = 0
        
        self.uart.write('U')
        
        if(self.uart.any()):
            rx_data_frame = self.uart.read(US100_RX_data_packet_size)
            d = ((rx_data_frame[0] << 8) | rx_data_frame[1])
        
        return d
    
    
    def get_avg_range(self):
        i = 0
        avg = 0
        
        for i in range(0, 4, 1):
            avg += self.get_range()
            sleep_ms(100)
            
        avg >>= 2
            
        return avg
            