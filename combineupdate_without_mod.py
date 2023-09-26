import cv2
import time
import datetime
import serial
import subprocess
import smbus2 as smbus
import json 

# import modbus_tk
# import modbus_tk.defines as cst
# from modbus_tk import modbus_rtu

import threading
import os
import psutil

# cvlc v4l2:///dev/video5 --sout '#transcode{vcodec=h264,acodec=none}:rtp{sdp=rtsp://:8554/}'

# กำหนด URL ของกล้องผ่าน RTSP
rtsp_url = "rtsp://192.168.11.104:8554/"

# เปิดการเชื่อมต่อกับกล้อง
cap = cv2.VideoCapture(rtsp_url)

# กำหนดขนาดของวิดีโอ
frame_width = 640
frame_height = 480
frame_rate = 15

#ที่อยู่ของ mp4 และ video ที่ถูกบันทึก
output_mp4AndJpg_path = '/home/linaro/ASI_SS/Photo_and_Video/'

# กำหนดระยะเวลาหน่วงระหว่างการบันทึก snapshot (วินาที)
snapshot_interval_P1 = 1 #ทุกๆ 1 วิ
snapshot_interval_P2 = 180 #ทุกๆ 3 นาที
last_snapshot_time = 0
#หัวใจ
last_time_H = 0
Time_interval_H = 8
#GY
last_time_GY = 0
Time_interval_GY = 10
#Time2Print
last_time_print = 0
Time_interval_print = 2
last_time_print2 = 0
Time_interval_print2 = 2
# #timeMod
# last_time_Mod = 0
# Time_interval_Mod = 3

### GPIO ###
# Define the GPIO pin number (e.g., GPIO 123)
led_gpio_pin_D = 149
led_gpio_pin_H = 125
led_gpio_pin_GYRO = 146
led_gpio_pin_TCPIP = 123
PIR_gpio_pin = 41
subprocess.run(['gpio', '-g', 'mode', str(led_gpio_pin_D), 'out'])
subprocess.run(['gpio', '-g', 'mode', str(led_gpio_pin_H), 'out'])
subprocess.run(['gpio', '-g', 'mode', str(led_gpio_pin_GYRO), 'out'])
subprocess.run(['gpio', '-g', 'mode', str(led_gpio_pin_TCPIP), 'out'])
subprocess.run(['gpio', '-g', 'mode', str(PIR_gpio_pin), 'in'])

led_state = 0  # กำหนดสถานะเริ่มต้นของ LED เป็นปิด
subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin_D), str(led_state)])

### I2C ###
# กำหนดหมายเลขของ I2C Bus
bus_number = 7
# กำหนดที่อยู่ของ GY-521
device_address = 0x68  # ที่อยู่เริ่มต้นของ GY-521
i2c_address = 0x40  # ที่อยู่ I2C ของ SHT20

# สร้างออบเจกต์สำหรับ I2C Bus
busGY = smbus.SMBus(bus_number)
busSHT = smbus.SMBus(bus_number)

# configure from Interface
site_code = "BKKTM"
count_of_slave = 3
cabinet_numbers =[]
num_cabinets = count_of_slave
IP_address = "192.168.11.104"
deviceName = 'SmartSite_' + site_code 

# ระบุโฟลเดอร์ที่คุณต้องการลบข้อมูลภาพและวิดีโอ
target_folder = '/home/linaro/ASI_SS/Photo_and_Video/'

# ตรวจสอบพื้นที่ที่ใช้งานของ SD card
# sd_card_usage = psutil.disk_usage('/')

# ส่งคำสั่งให้ GY-521 เปิดใช้งานการวัด
busGY.write_byte_data(device_address, 0x6B, 0)
# อ่านข้อมูลจากเซ็นเซอร์ SHT20
data = busSHT.read_i2c_block_data(i2c_address, 0xE3, 4) 
#OTP
serial_port = serial.Serial('/dev/ttyS0', 115200) 

# logger = modbus_tk.utils.create_logger("console")

# PORT = '/dev/ttyUSB0'
# master = modbus_rtu.RtuMaster(
#     serial.Serial(port=PORT, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=0)
# )

# def thread_RTU():
#     #Connect to the slave
#     master.set_timeout(1)
#     master.set_verbose(True)
#     logger.info("connected")

# thr = threading.Thread(target=thread_RTU)
# thr.start()
cabinet_code = {}
cabinet_code[1] = 'not found cabinet'
cabinet_code[2] = 'not found cabinet'
cabinet_code[3] = 'not found cabinet'
cabinet_code[4] = 'not found cabinet'
cabinet_code[5] = 'not found cabinet'

for i in range(1, num_cabinets + 1):
    cabinet_code[i] = site_code + '-' + str(i)
    print(cabinet_code[i])
    cabinet_numbers.append(i)
# print(cabinet_numbers)


cap_not_Connect = False

# ตรวจสอบว่าเชื่อมต่อกล้องสำเร็จหรือไม่
if not cap.isOpened():
    print("ไม่สามารถเชื่อมต่อกล้องได้")
    cap_not_Connect = True
    subprocess.run("sudo init 6", shell=True)
    exit()

recording = False
out = None


while True:
    if cap_not_Connect == True:
        subprocess.run("sudo init 6", shell=True)

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
        subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin_GYRO), str(1)])
        # สร้างเหตุการณ์แจ้งเตือนที่นี่ (เช่น ส่งอีเมล์ หรือแจ้งเตือนผ่านแอพพลิเคชัน)
    else:
        current_time_GY = time.time()
        if current_time_GY - last_time_GY >= Time_interval_GY:
            last_time_GY = current_time_GY  # อัปเดตเวลาของ snapshot ล่าสุด
            subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin_GYRO), str(0)])

    if abs(gyro_x) > threshold_gyro or abs(gyro_y) > threshold_gyro or abs(gyro_z) > threshold_gyro:
        subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin_GYRO), str(1)])
        print("มีการหมุนเซ็นเซอร์ในแกนอัตราความเร็ว")
        # สร้างเหตุการณ์แจ้งเตือนที่นี่ (เช่น ส่งอีเมล์ หรือแจ้งเตือนผ่านแอพพลิเคชัน)
    else:
        current_time_GY = time.time()
        if current_time_GY - last_time_GY >= Time_interval_GY:
            last_time_GY = current_time_GY 
            subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin_GYRO), str(0)])

    # แสดงผลค่า
    current_time_print2 = time.time()
    if current_time_print2 - last_time_print2 >= Time_interval_print2:
        last_time_print2 = current_time_print2
        print("ความเร็วในแกน X (g): {:.2f}".format(accel_x))
        print("ความเร็วในแกน Y (g): {:.2f}".format(accel_y))
        print("ความเร็วในแกน Z (g): {:.2f}".format(accel_z))
        accel_x_rtu = round(accel_x, 2)*100
        accel_y_rtu = round(accel_y, 2)*100
        accel_z_rtu = round(accel_z, 2)*100

        print("อัตราความเร็วในแกน X (deg/s): {:.2f}".format(gyro_x))
        print("อัตราความเร็วในแกน Y (deg/s): {:.2f}".format(gyro_y))
        print("อัตราความเร็วในแกน Z (deg/s): {:.2f}".format(gyro_z))
        gyro_x_rtu = round(gyro_x, 2)*100
        gyro_y_rtu = round(gyro_y, 2)*100
        gyro_z_rtu = round(gyro_z, 2)*100

        print("-" * 20)

    # แปลงข้อมูลเป็นค่าอุณหภูมิ
    raw_temp = (data[0] << 8) + data[1]
    temperature = -46.85 + (175.72 * raw_temp / 65536.0)
    temp_rtu = round(temperature, 2)*100
    # อ่านข้อมูลความชื้นจากเซ็นเซอร์ SHT20
    data_humidity = busSHT.read_i2c_block_data(i2c_address, 0xE5, 2)

    # แปลงข้อมูลเป็นค่าความชื้น
    raw_humidity = (data_humidity[0] << 8) + data_humidity[1]
    humidity = -6.0 + (125.0 * raw_humidity / 65536.0)
    hum_rtu = round(humidity, 2)*100
   
    #PIR_sensor
    # ตรวจสอบสถานะของ push-button
    PIR_state = subprocess.run(['gpio', '-g', 'read', str(PIR_gpio_pin)], capture_output=True, text=True)
    PIR_state = PIR_state.stdout.strip()
    # แสดงผลค่า
    current_time_print = time.time()
    if current_time_print - last_time_print >= Time_interval_print:
        last_time_print = current_time_print
        print("Temperature:", temperature, "°C")
        print("Humidity:", humidity, "%")
        print("PIR_state : ",PIR_state)
    # หากมีการกด push-button


    # อ่านเฟรมภาพจากกล้อง
    ret, frame = cap.read()

    # รับวันที่และเวลาปัจจุบัน
    current_datetime = datetime.datetime.now()
    # แปลงวันที่และเวลาเป็นสตริงแบบกำหนดรูปแบบ
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    #ตัวแปรที่ส่งไป rtu
    cabinet_serf = 21
    cabinet_sers = 188
    cabinet_serc = 2422
    wacthdog_serf = 134
    wacthdog_sers = 557
    otp_serf = 987
    otp_sers = 567
    t_day = current_datetime.strftime("%d")
    t_month = current_datetime.strftime("%m")
    t_years = current_datetime.strftime("%Y")
    t_hour = current_datetime.strftime("%H")
    t_min = current_datetime.strftime("%M")
    t_sec = current_datetime.strftime("%S")
    
    #OTP
    data_to_send = current_datetime.strftime("OTPi"+"123456"+"D"+"%d"+"M"+"%m"+"Y"+"%Y"+"H"+"%H"+"Mi"+"%M"+"S"+"%S"+"A"+"12"+"B"+"345"+"C"+"6789"+"WA"+"134"+"WB"+"557"+"END\n") 
    serial_port.write(data_to_send.encode()) 
    
    if not ret:
        print("เกิดข้อผิดพลาดในการอ่านเฟรมภาพ")
        subprocess.run("sudo init 6", shell=True)
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


    #BLUETOOTH
    def check_internet_connection():
        try:
            subprocess.check_output(["sudo", "ping", "-c", "1", "192.168.11.57"])
            return True
        except subprocess.CalledProcessError:
            return False

        if check_internet_connection() == True:
            # print("Internet is connected.")
            subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin_TCPIP), str(1)])

        else:
            # print("Internet is not connected.")
            subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin_TCPIP), str(0)])
    
    
    def Mod():
        current_time_Mod = time.time()
        
        try:
            # Define the register values you want to write
            # register_values = [int(temp_rtu), int(hum_rtu), int(accel_x_rtu), int(accel_y_rtu), int(accel_z_rtu), int(gyro_x_rtu), int(gyro_y_rtu), int(gyro_z_rtu)]
            register_values_cabinetf = [cabinet_serf, cabinet_sers, cabinet_serc, wacthdog_serf, wacthdog_sers, otp_serf, otp_sers]
            register_values_cabinets = [int(t_day), int(t_month), int(t_years), int(t_hour), int(t_min), int(t_sec)]
            # Write multiple registers starting at address 0
            master.execute(10, cst.WRITE_MULTIPLE_REGISTERS, 1, output_value=register_values_cabinetf)
            master.execute(10, cst.WRITE_MULTIPLE_REGISTERS, 10, output_value=register_values_cabinets)
            read_rtu = master.execute(10, cst.READ_HOLDING_REGISTERS, 16, 17)
            # รับจากESP main
            G_door_sensor = read_rtu[0]
            G_door_status = read_rtu[1]
            G_Acce_X = read_rtu[2]
            G_Acce_Y = read_rtu[3]
            G_Acce_Z = read_rtu[4]
            G_Gyro_X = read_rtu[5]
            G_Gyro_Y = read_rtu[6]
            G_Gyro_Z = read_rtu[7]
            G_Temperature6050 = read_rtu[8]
            G_TemperatureSHT20 = read_rtu[9]
            G_humidtySHT20 = read_rtu[10]
            G_PIR = read_rtu[11]
            G_Buzzer_B = read_rtu[12]
            G_WD_HeartBeat_B = read_rtu[13]
            G_Steal_Acce = read_rtu[14]
            G_Steal_Gyro = read_rtu[15]
            G_Steal_Condition = read_rtu[16]

            print(f"ค่า G_door_sensor จากตู้ JB21-1882422: {G_door_sensor}")
            print(f"ค่า G_door_status จากตู้ JB21-1882422: {G_door_status}")
            print(f"ค่า G_Acce_X จากตู้ JB21-1882422: {G_Acce_X}")
            print(f"ค่า G_Acce_Y จากตู้ JB21-1882422: {G_Acce_Y}")
            print(f"ค่า G_Acce_Z จากตู้ JB21-1882422: {G_Acce_Z}")
            print(f"ค่า G_Gyro_X จากตู้ JB21-1882422: {G_Gyro_X}")
            print(f"ค่า G_Gyro_Y จากตู้ JB21-1882422: {G_Gyro_Y}")
            print(f"ค่า G_Gyro_Z จากตู้ JB21-1882422: {G_Gyro_Z}")
            print(f"ค่า G_Temperature6050 จากตู้ JB21-1882422: {G_Temperature6050}")
            print(f"ค่า G_TemperatureSHT20 จากตู้ JB21-1882422: {G_TemperatureSHT20}")
            print(f"ค่า G_humidtySHT20 จากตู้ JB21-1882422: {G_humidtySHT20}")
            print(f"ค่า G_PIR จากตู้ JB21-1882422: {G_PIR}")
            print(f"ค่า G_Buzzer_B จากตู้ JB21-1882422: {G_Buzzer_B}")
            print(f"ค่า G_WD_HeartBeat_B จากตู้ JB21-1882422: {G_WD_HeartBeat_B}")
            print(f"ค่า G_Steal_Acce จากตู้ JB21-1882422: {G_Steal_Acce}")
            print(f"ค่า G_Steal_Gyro จากตู้ JB21-1882422: {G_Steal_Gyro}")
            print(f"ค่า G_Steal_Condition จากตู้ JB21-1882422: {G_Steal_Condition}")

        except modbus_tk.modbus.ModbusError as exc:
            logger.error("%s- Code=%d", exc, exc.get_exception_code())
        
    # current_time_Mod = time.time()
    # if current_time_Mod - last_time_Mod >= Time_interval_Mod:
        # last_time_Mod = current_time_Mod
        # Mod()
    
    # # ถ้าพื้นที่ใช้งานของ SD card เกินค่าที่กำหนดให้ลบข้อมูลภาพและวิดีโอ
    # if sd_card_usage.percent >= threshold_percent:
    #     try:
    #         # ลบข้อมูลภาพและวิดีโอทั้งหมดในโฟลเดอร์
    #         for root, dirs, files in os.walk(target_folder):
    #             for file in files:
    #                 file_path = os.path.join(root, file)
    #                 os.remove(file_path)
    #                 print(f"ลบไฟล์ {file_path} สำเร็จ")
    #         print("ลบข้อมูลภาพและวิดีโอทั้งหมดในโฟลเดอร์เรียบร้อยแล้ว")
    #     except Exception as e:
    #         print(f"เกิดข้อผิดพลาดในการลบข้อมูลภาพและวิดีโอ: {e}")
    # else:
    #     # print(f"พื้นที่ใช้งานของ SD card ยังไม่เกิน {threshold_percent}%")
    #     pass
    json_Data_to_WD1 = {
        
        "cabinet_serf" : cabinet_serf,
        "cabinet_sers" : cabinet_sers,
        "cabinet_serc" : cabinet_serc,
        "wacthdog_serf" : wacthdog_serf,
        "wacthdog_sers" : wacthdog_sers,
        "otp_serf" : otp_serf,
        "otp_sers" : otp_sers,
        "t_day" : t_day,
        "t_month" : t_month,
        "t_years" : t_years,
        "t_hour" : t_hour,
        "t_min" : t_min,
        "t_sec" : t_sec
        
    }

    Update_Master_Data = {
    "cabinetList": [
        {
            "isCabinetActive": "True",
            "cabinetCode": cabinet_code[1]
        },
        {
            "isCabinetActive": "True",
            "cabinetCode": cabinet_code[2]
        },
        {
            "isCabinetActive": "True",
            "cabinetCode": cabinet_code[3]
        }
    ],
    "siteCode": site_code,
    "isSiteActive": "True"  #if cabinet A online or B online 
    }

    Update_emergency_key =  {
        "siteCode": site_code,
        "cabinetList": [
            {
                "emergencyKey": "[B@72a3ec3d",
                "isCabinetActive": "True",
                "cabinetCode": cabinet_code[1],
                "deviceName": deviceName
            },
            {
                "emergencyKey": "[B@72a3ec3d",
                "isCabinetActive": "True",
                "cabinetCode": cabinet_code[2],
                "deviceName": deviceName
            }
        ],
        "isSiteActive": "True"
    }

    Get_cabinet_status = {
        "cabinets" : [ 
            {
                "site_code" : site_code,
                "cabinet_code" : cabinet_code[1],
                "locked" : "True",
                "is_emergency" : "No",
                "last_updated" : "2021-08-24T16:42:59.014",
                "emerg_key" : "null",
                "mac_address" : "NO_DATA",
                "device_name" : deviceName
                }, {

                "site_code" : site_code,
                "cabinet_code" : cabinet_code[2],
                "locked" : "True",
                "is_emergency" : "No",
                "last_updated" : "2021-08-24T16:42:59.237",
                "emerg_key" : "null",
                "mac_address" : "NO_DATA",
                "device_name" : deviceName
            } 
        ]
    }

    Lock_cabinet = {
        "success" : "true",
        "message" : "Lock successful"
    }

    Unlock_cabinet = {
        "success" : "true",
        "message" : "Unlock successful"
    }

    Device_API = {
        "success" : "true",
        "message" : "Lock successful"
    }

    Device_status_report_API = {
        "site_code": "100CP",
        "devices": [
            { 
                "serial": "", "cabinet_code": "100CP-1", "device_status_id": 1, "device_type_id": 1,
                "event_type_id": 2, "dt": "2019-07-16 17:29:00"},
            { 
                "serial": "", "cabinet_code": "100CP-1", "device_status_id": 1, "device_type_id": 2,
                "event_type_id": 5, "dt": "2019-07-16 17:29:00"},
            { 
                "serial": "", "cabinet_code": "100CP-1", "device_status_id": 1, "device_type_id": 10,
                "event_type_id": 11, "dt": "2019-07-16 17:29:00"},
            { 
                "serial": "", "cabinet_code": "100CP-1", "device_status_id": 1, "device_type_id": 7,
                "event_type_id": 6, "dt": "2019-07-16 17:29:00"},
            { 
                "serial": "", "cabinet_code": "E131M-2", "device_status_id": 0, "device_type_id": 6,
                "event_type_id": 0, "dt": "2019-07-16 17:29:00"},
            { 
                "serial": "", "cabinet_code": "E131M-2", "device_status_id": 1, "device_type_id": 1,
                "event_type_id": 0, "dt": "2019-07-16 17:29:00"},
            { 
                "serial": "", "cabinet_code": "E131M-2", "device_status_id": 0, "device_type_id": 10, 
                "event_type_id": 7, "dt": "2019-07-16 17:29:00"},
            { 
                "serial": "", "cabinet_code": "E131M-2", "device_status_id": 0, "device_type_id": 7,
                "event_type_id": 10, "dt": "2019-07-16 17:29:00"}
        ]
    }

    Send_emergency_API = {
        "emerg_key": "AAAAAAAAAA"
    }

    # Device_send_image = {
    #     "site_code": "",
    #     "cabinet_code": "BKKYM-1",
    #     "dt": "2019-03-27 12:00:11",
    #     "img": "IMAGE_URL_GENERATE_BY_DEVICE"
    # }

    Device_alarm_on_off =  {
        "site_code": site_code,
        "cabinet_code": cabinet_code[1],
        "alarm_timer": Time_interval_GY #Alarm time in second unit
    }



    # รวมข้อมูลจากทั้งสองตัวแปร
    combined_data = {
        "Update_Master_Data": Update_Master_Data,
        "Update_emergency_key": Update_emergency_key,
        "Get_cabinet_status": Get_cabinet_status,
        "Lock_cabinet": Lock_cabinet,
        "Unlock_cabinet": Unlock_cabinet,
        "Device_API": Device_API,
        "Device_status_report_API": Device_status_report_API,
        "Send_emergency_API": Send_emergency_API,
        # "Device_send_image": Device_send_image,
        "Device_alarm_on_off": Device_alarm_on_off,
        "json_Data_to_WD1" : json_Data_to_WD1
    }



    with open("DataFromCombineMod.json", "w") as outfile:
        json.dump(combined_data, outfile, indent=4)

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
