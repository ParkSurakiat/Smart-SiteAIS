import smbus2 as smbus
import time

# กำหนดหมายเลขของ I2C Bus
bus_number_GY = 6
device_address = 0x68  # ที่อยู่เริ่มต้นของ GY-521
i2c_address = 0x40  # ที่อยู่ I2C ของ SHT20

# สร้างออบเจกต์สำหรับ I2C Bus
busGY = smbus.SMBus(bus_number_GY)

# ส่งคำสั่งให้ GY-521 เปิดใช้งานการวัด
busGY.write_byte_data(device_address, 0x6B, 0)

try:
    while True:

        accel_xout_H = busGY.read_byte_data(device_address, 0x3B)
        accel_xout_L = busGY.read_byte_data(device_address, 0x3C)
        accel_xout = (accel_xout_H << 8) | accel_xout_L

        # อ่านค่าความเร็วแกน Y
        accel_yout_H = busGY.read_byte_data(device_address, 0x3D)
        accel_yout_L = busGY.read_byte_data(device_address, 0x3E)
        accel_yout = (accel_yout_H << 8) | accel_yout_L

        # อ่านค่าความเร็วแกน Z
        accel_zout_H = busGY.read_byte_data(device_address, 0x3F)
        accel_zout_L = busGY.read_byte_data(device_address, 0x40)
        accel_zout = (accel_zout_H << 8) | accel_zout_L

        # อ่านค่าอัตราความเร็วแกน X
        gyro_xout_H = busGY.read_byte_data(device_address, 0x43)
        gyro_xout_L = busGY.read_byte_data(device_address, 0x44)
        gyro_xout = (gyro_xout_H << 8) | gyro_xout_L

        # อ่านค่าอัตราความเร็วแกน Y
        gyro_yout_H = busGY.read_byte_data(device_address, 0x45)
        gyro_yout_L = busGY.read_byte_data(device_address, 0x46)
        gyro_yout = (gyro_yout_H << 8) | gyro_yout_L

        # อ่านค่าอัตราความเร็วแกน Z
        gyro_zout_H = busGY.read_byte_data(device_address, 0x47)
        gyro_zout_L = busGY.read_byte_data(device_address, 0x48)
        gyro_zout = (gyro_zout_H << 8) | gyro_zout_L

        # แปลงค่าให้อยู่ในรูปแบบที่ถูกต้อง (เช่น 2's complement)
        def twos_complement(val, bits):
            if (val & (1 << (bits - 1))) != 0:
                val = val - (1 << bits)
            return val

        # แปลงค่าให้อยู่ในหน่วยที่ถูกต้อง (เช่น g และ deg/s)
        accel_scale = 16384.0  # สำหรับ MPU6000
        gyro_scale = 131.0  # สำหรับ MPU6000

        # ค่าที่ใช้ในการกำหนดข้อความแจ้งเตือน
        threshold_accel = 1.2  # ค่าความเร็วสูงสุดที่ยอมรับในแกน X, Y, และ Z (g)
        threshold_gyro = 120.0  # ค่าอัตราความเร็วสูงสุดที่ยอมรับในแกน X, Y, และ Z (deg/s)

        accel_x = twos_complement(accel_xout, 16) / accel_scale
        accel_y = twos_complement(accel_yout, 16) / accel_scale
        accel_z = twos_complement(accel_zout, 16) / accel_scale

        gyro_x = twos_complement(gyro_xout, 16) / gyro_scale
        gyro_y = twos_complement(gyro_yout, 16) / gyro_scale
        gyro_z = twos_complement(gyro_zout, 16) / gyro_scale

        if abs(accel_x) > threshold_accel or abs(accel_y) > threshold_accel or abs(accel_z) > threshold_accel:
            print("มีการขยับเซ็นเซอร์ในแกนความเร็ว")
            # สร้างเหตุการณ์แจ้งเตือนที่นี่ (เช่น ส่งอีเมล์ หรือแจ้งเตือนผ่านแอพพลิเคชัน)

        if abs(gyro_x) > threshold_gyro or abs(gyro_y) > threshold_gyro or abs(gyro_z) > threshold_gyro:
            print("มีการหมุนเซ็นเซอร์ในแกนอัตราความเร็ว")
            # สร้างเหตุการณ์แจ้งเตือนที่นี่ (เช่น ส่งอีเมล์ หรือแจ้งเตือนผ่านแอพพลิเคชัน)

        # แสดงผลค่า
        print("ความเร็วในแกน X (g): {:.2f}".format(accel_x))
        print("ความเร็วในแกน Y (g): {:.2f}".format(accel_y))
        print("ความเร็วในแกน Z (g): {:.2f}".format(accel_z))

        print("อัตราความเร็วในแกน X (deg/s): {:.2f}".format(gyro_x))
        print("อัตราความเร็วในแกน Y (deg/s): {:.2f}".format(gyro_y))
        print("อัตราความเร็วในแกน Z (deg/s): {:.2f}".format(gyro_z))

        print("-" * 20)
        time.sleep(3)
        

except KeyboardInterrupt:
    pass

# ปิดการใช้งาน I2C Bus
busGY.close()



