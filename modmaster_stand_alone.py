import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import time
import threading
import json
import serial


with open('DataFromCombineMod.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)

json_Data_to_WD1 = json_object['json_Data_to_WD1']
cabinet_serf = json_Data_to_WD1["cabinet_serf"]
cabinet_sers = json_Data_to_WD1["cabinet_sers"]
cabinet_serc = json_Data_to_WD1["cabinet_serc"]
wacthdog_serf = json_Data_to_WD1["wacthdog_serf"]
wacthdog_sers = json_Data_to_WD1["wacthdog_sers"]
otp_serf = json_Data_to_WD1["otp_serf"]
otp_sers = json_Data_to_WD1["otp_sers"]
t_day = json_Data_to_WD1["t_day"]
t_month = json_Data_to_WD1["t_month"]
t_years = json_Data_to_WD1["t_years"]
t_hour = json_Data_to_WD1["t_hour"]
t_min = json_Data_to_WD1["t_min"]
t_sec = json_Data_to_WD1["t_sec"]

#timeMod
last_time_Mod = 0
Time_interval_Mod = 3


logger = modbus_tk.utils.create_logger("console")

PORT = '/dev/ttyUSB0'
master = modbus_rtu.RtuMaster(
    serial.Serial(port=PORT, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=0)
)

def thread_RTU():
    #Connect to the slave
    master.set_timeout(1)
    master.set_verbose(True)
    logger.info("connected")

thr = threading.Thread(target=thread_RTU)
thr.start()

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
while True:        
    current_time_Mod = time.time()
    if current_time_Mod - last_time_Mod >= Time_interval_Mod:
        last_time_Mod = current_time_Mod
        Mod()
