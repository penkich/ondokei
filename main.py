# ondokei test script for MicroPython on ESP8266. 2016-06-04 by penkich
# 温度センサー：http://akizukidenshi.com/download/ds/akizuki/AE-ADT7410_aw.pdf
# 
# 
#
import webrepl
webrepl.start()
from machine import Pin,I2C,Timer
i2c = I2C(scl=Pin(5),sda=Pin(4),freq=1000000)
import ustruct
import time

i2c.writeto(0x48,b'\x03\x80')

i2c.writeto(0x70,b'\x21')
i2c.writeto(0x70,b'\xe8')
i2c.writeto(0x70,b'\x81')


def seg7(i2c_addr,four_letter,dotpos):
    v0 = int(four_letter[0])
    v1 = int(four_letter[1])
    v2 = int(four_letter[2])
    v3 = int(four_letter[3])
    data = [0xfc, 0x60, 0xda, 0xf2, 0x66, 0xb6, 0xbe, 0xe4, 0xfe, 0xe6]
    dot  = [0,0,0,0]
    dot[dotpos]=1
    i2c.writeto(i2c_addr, ustruct.pack('bb',00,data[v0]+dot[0]))
    i2c.writeto(i2c_addr, ustruct.pack('bb',02,data[v1]+dot[1]))
    i2c.writeto(i2c_addr, ustruct.pack('bb',04,data[v2]+dot[2]))
    i2c.writeto(i2c_addr, ustruct.pack('bb',06,data[v3]+dot[3]))

##while(1):
##    temp=ustruct.unpack('>H',i2c.readfrom(0x48,2))[0]/128.0
##    seg7(0x70,str(temp*100),1)
##    time.sleep(1)

tim = Timer(-1)
tim.init(period=1000,mode=Timer.PERIODIC,callback=lambda t:seg7(0x70,str(ustruct.unpack('>H',i2c.readfrom(0x48,2))[0]/128.0*100),1))
