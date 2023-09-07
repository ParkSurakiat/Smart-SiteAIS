import serial
import time
import datetime

serial_port = serial.Serial('/dev/ttyS0', 115200) 
current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

try:
    while True:
        data_to_send = current_datetime.strftime("OTPi"+"123456"+"D"+"%d"+"M"+"%m"+"Y"+"%Y"+"H"+"%H"+"Mi"+"%M"+"S"+"%S"+"END\n") 
        serial_port.write(data_to_send.encode()) 
        print(data_to_send)
        

except KeyboardInterrupt:
    pass

finally:
    serial_port.close()
