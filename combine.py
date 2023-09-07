import cv2
import time
import datetime
import serial
import subprocess
import smbus2 as smbus


# cvlc v4l2:///dev/video5 --sout '#transcode{vcodec=h264,acodec=none}:rtp{sdp=rtsp://:8554/}'

# กำหนด URL ของกล้องผ่าน RTSP
rtsp_url = "rtsp://192.168.194.243:8554/"

# เปิดการเชื่อมต่อกับกล้อง
cap = cv2.VideoCapture(rtsp_url)

# กำหนดขนาดของวิดีโอ
frame_width = 640
frame_height = 480
frame_rate = 15

#ที่อยู่ของ mp4 และ video ที่ถูกบันทึก
output_mp4AndJpg_path = '/home/linaro/AIS_Smart_Site/Photo_and_Video/'

# กำหนดระยะเวลาหน่วงระหว่างการบันทึก snapshot (วินาที)
snapshot_interval_P1 = 1 #ทุกๆ 1 วิ
snapshot_interval_P2 = 180 #ทุกๆ 3 นาที
last_snapshot_time = 0
#หัวใจ
last_time_H = 0
Time_interval_H = 8
#GY
last_time_GY = 0
Time_interval_GY = 5
#Time2Print
last_time_print = 0
Time_interval_print = 2
last_time_print2 = 0
Time_interval_print2 = 2


### GPIO ###
# Define the GPIO pin number (e.g., GPIO 123)
led_gpio_pin_D = 121
led_gpio_pin_H = 125
led_gpio_pin_GY = 126
subprocess.run(['gpio', '-g', 'mode', str(led_gpio_pin_D), 'out'])
subprocess.run(['gpio', '-g', 'mode', str(led_gpio_pin_H), 'out'])
subprocess.run(['gpio', '-g', 'mode', str(led_gpio_pin_GY), 'out'])
# subprocess.run(['gpio', '-g', 'mode', str(button_gpio_pin), 'in'])

led_state = 0  # กำหนดสถานะเริ่มต้นของ LED เป็นปิด
subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin_D), str(led_state)])

### I2C ###
# กำหนดหมายเลขของ I2C Bus
bus_number = 6
# กำหนดที่อยู่ของ GY-521
device_address = 0x68  # ที่อยู่เริ่มต้นของ GY-521
i2c_address = 0x40  # ที่อยู่ I2C ของ SHT20

# สร้างออบเจกต์สำหรับ I2C Bus
busGY = smbus.SMBus(bus_number)
busSHT = smbus.SMBus(bus_number)

# ส่งคำสั่งให้ GY-521 เปิดใช้งานการวัด
busGY.write_byte_data(device_address, 0x6B, 0)
# อ่านข้อมูลจากเซ็นเซอร์ SHT20
data = busSHT.read_i2c_block_data(i2c_address, 0xE3, 4) 
#OTP
serial_port = serial.Serial('/dev/ttyS0', 115200) 

# ตรวจสอบว่าเชื่อมต่อกล้องสำเร็จหรือไม่
if not cap.isOpened():
    print("ไม่สามารถเชื่อมต่อกล้องได้")
    exit()

recording = False
out = None


while True:
    #จังหวะหัวใจเด้อ
    current_time_H = time.time()
    if current_time_H - last_time_H >= Time_interval_H:
        last_time_H = current_time_H  # อัปเดตเวลาของ snapshot ล่าสุด
        subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin_H), str(1)])
        print("Heartbeat : 1")
    else:
        current_time_print = time.time()
        if current_time_print - last_time_print >= Time_interval_print and current_time_H - last_time_H < Time_interval_H:
            last_time_print = current_time_print
            subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin_H), str(0)])
            print("Heartbeat : 0")

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
    threshold_accel = 1.5  # ค่าความเร็วสูงสุดที่ยอมรับในแกน X, Y, และ Z (g)
    threshold_gyro = 150.0  # ค่าอัตราความเร็วสูงสุดที่ยอมรับในแกน X, Y, และ Z (deg/s)

    accel_x = twos_complement(accel_xout, 16) / accel_scale
    accel_y = twos_complement(accel_yout, 16) / accel_scale
    accel_z = twos_complement(accel_zout, 16) / accel_scale

    gyro_x = twos_complement(gyro_xout, 16) / gyro_scale
    gyro_y = twos_complement(gyro_yout, 16) / gyro_scale
    gyro_z = twos_complement(gyro_zout, 16) / gyro_scale

    if abs(accel_x) > threshold_accel or abs(accel_y) > threshold_accel or abs(accel_z) > threshold_accel:
        print("มีการขยับเซ็นเซอร์ในแกนความเร็ว")
        subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin_GY), str(0)])
        # สร้างเหตุการณ์แจ้งเตือนที่นี่ (เช่น ส่งอีเมล์ หรือแจ้งเตือนผ่านแอพพลิเคชัน)
    else:
        current_time_GY = time.time()
        if current_time_GY - last_time_GY >= Time_interval_GY:
            last_time_GY = current_time_GY  # อัปเดตเวลาของ snapshot ล่าสุด
            subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin_GY), str(1)])

    if abs(gyro_x) > threshold_gyro or abs(gyro_y) > threshold_gyro or abs(gyro_z) > threshold_gyro:
        print("มีการหมุนเซ็นเซอร์ในแกนอัตราความเร็ว")
        subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin_GY), str(0)])
        # สร้างเหตุการณ์แจ้งเตือนที่นี่ (เช่น ส่งอีเมล์ หรือแจ้งเตือนผ่านแอพพลิเคชัน)
    else:
        current_time_GY = time.time()
        if current_time_GY - last_time_GY >= Time_interval_GY:
            last_time_GY = current_time_GY  # อัปเดตเวลาของ snapshot ล่าสุด
            subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin_GY), str(1)])

    # แสดงผลค่า
    current_time_print2 = time.time()
    if current_time_print2 - last_time_print2 >= Time_interval_print2:
        last_time_print2 = current_time_print2
        print("ความเร็วในแกน X (g): {:.2f}".format(accel_x))
        print("ความเร็วในแกน Y (g): {:.2f}".format(accel_y))
        print("ความเร็วในแกน Z (g): {:.2f}".format(accel_z))

        print("อัตราความเร็วในแกน X (deg/s): {:.2f}".format(gyro_x))
        print("อัตราความเร็วในแกน Y (deg/s): {:.2f}".format(gyro_y))
        print("อัตราความเร็วในแกน Z (deg/s): {:.2f}".format(gyro_z))

        print("-" * 20)


    # แปลงข้อมูลเป็นค่าอุณหภูมิ
    raw_temp = (data[0] << 8) + data[1]
    temperature = -46.85 + (175.72 * raw_temp / 65536.0)

    # อ่านข้อมูลความชื้นจากเซ็นเซอร์ SHT20
    data_humidity = busSHT.read_i2c_block_data(i2c_address, 0xE5, 2)

    # แปลงข้อมูลเป็นค่าความชื้น
    raw_humidity = (data_humidity[0] << 8) + data_humidity[1]
    humidity = -6.0 + (125.0 * raw_humidity / 65536.0)

    # แสดงผลค่า
    current_time_print = time.time()
    if current_time_print - last_time_print >= Time_interval_print:
        last_time_print = current_time_print
        print("Temperature:", temperature, "°C")
        print("Humidity:", humidity, "%")

        
    # อ่านเฟรมภาพจากกล้อง
    ret, frame = cap.read()

    # รับวันที่และเวลาปัจจุบัน
    current_datetime = datetime.datetime.now()
    # แปลงวันที่และเวลาเป็นสตริงแบบกำหนดรูปแบบ
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    
    #OTP
    data_to_send = current_datetime.strftime("OTPi"+"123456"+"D"+"%d"+"M"+"%m"+"Y"+"%Y"+"H"+"%H"+"Mi"+"%M"+"S"+"%S"+"END\n") 
    serial_port.write(data_to_send.encode()) 
    
    if not ret:
        print("เกิดข้อผิดพลาดในการอ่านเฟรมภาพ")
        break
    # แสดงภาพที่ได้จากกล้อง
    cv2.imshow("Camera Steaming", frame)

    #รอรับคำสั่งจากผู้ใช้
    if cv2.waitKey(1) & 0xFF == ord('o') and not recording:
        # เริ่มบันทึกวิดีโอ
        snapshot_counter = 0
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter(output_mp4AndJpg_path + f'Video_{formatted_datetime}.mp4', fourcc, frame_rate, (frame_width, frame_height))
        recording = True
        print("Start recording")
        led_state = 1 #door open state
        subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin_D), str(led_state)])
        
    elif cv2.waitKey(1) & 0xFF == ord('k') and recording:
        # หยุดบันทึกวิดีโอ
        if out is not None:
            out.release()
            recording = False
            snapshot_interval_P1 = 1 #ทุกๆ 1 วิ
            snapshot_interval_P2 = 180 #ทุกๆ 3 นาที
            last_snapshot_time = 0
            print("Stop recording")
            print("SnapShot Success")
            led_state = 0 #door close state
            subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin_D), str(led_state)])

    if recording == True :
        out.write(frame)
        if snapshot_counter < 20:
            current_time = time.time()  # เวลาปัจจุบัน
            if current_time - last_snapshot_time >= snapshot_interval_P1:
                snapshot_path = f"snapshot_{formatted_datetime}_{snapshot_counter+1}.jpg"
                cv2.imwrite(output_mp4AndJpg_path + snapshot_path, frame)
                snapshot_counter += 1
                last_snapshot_time = current_time  # อัปเดตเวลาของ snapshot ล่าสุด
                print(f"Saved snapshot: {snapshot_path}")
        
        elif snapshot_counter >= 20:
            current_time = time.time()  # เวลาปัจจุบัน
            if current_time - last_snapshot_time >= snapshot_interval_P2:
                snapshot_path = f"snapshot_{formatted_datetime}_{snapshot_counter+1}.jpg"
                cv2.imwrite(output_mp4AndJpg_path + snapshot_path, frame)
                snapshot_counter += 1
                last_snapshot_time = current_time  # อัปเดตเวลาของ snapshot ล่าสุด
                print(f"Saved snapshot: {snapshot_path}")
    # print("LED : ", led_state)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Disconnect Camera")
        # subprocess.run(['gpio', '-g', 'mode', str(led_gpio_pin), 'in'])
        subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin_H), str(0)])
        subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin_D), str(0)])

        break

# คืนทรัพยากร
cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()