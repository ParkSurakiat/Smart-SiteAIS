import smbus2
import time

# กำหนดหมายเลขของ I2C bus
bus_number = 6 #cause i2c-6 is opened

# กำหนด I2C address ของอุปกรณ์
device_address = 0x68

# สร้างตัวแปรสำหรับเชื่อมต่อกับ I2C bus
bus = smbus2.SMBus(bus_number)

# กำหนด register address ที่คุณต้องการอ่านข้อมูล
register_address = 0x00  # ตัวอย่างเท่านั้น

try:
    while True:
        # อ่านข้อมูลจากอุปกรณ์ที่ตัวอยู่ device_address และ register_address
        data = bus.read_byte_data(device_address, register_address)
        
        print("Read data:", data)
        
        # หน่วงเวลาสั้นๆ ก่อนอ่านข้อมูลอีกครั้ง
        time.sleep(1)
        
except KeyboardInterrupt:
    # ปิดการเชื่อมต่อกับ I2C bus เมื่อกด Ctrl+C
    bus.close()
