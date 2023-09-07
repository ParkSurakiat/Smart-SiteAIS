# import subprocess
# import time

# # Define the GPIO pin number (e.g., GPIO 123)
# gpio_pin = 150

# try:
#     while True:
#         # Turn the GPIO pin ON (HIGH)
#         subprocess.run(['gpio', '-g', 'write', str(gpio_pin), '1'])
#         print("GPIO is ON")
#         time.sleep(1)
#         subprocess.run(['gpio', '-g', 'write', str(gpio_pin), '0'])
#         print("GPIO is OFF")
#         time.sleep(1)

# except KeyboardInterrupt:
#     pass

import subprocess
import time

# กำหนดหมายเลขขา GPIO ที่ใช้
led_gpio_pin = 121  # กำหนดหมายเลขขา GPIO ที่เชื่อม LED
# button_gpio_pin = 123  # กำหนดหมายเลขขา GPIO ที่เชื่อม push-button switch

# กำหนดโหมดของขา GPIO
subprocess.run(['gpio', '-g', 'mode', str(led_gpio_pin), 'out'])
# subprocess.run(['gpio', '-g', 'mode', str(button_gpio_pin), 'in'])

led_state = 0  # กำหนดสถานะเริ่มต้นของ LED เป็นปิด

try:
    while True:
        # ตรวจสอบสถานะของ push-button
        # button_state = subprocess.run(['gpio', '-g', 'read', str(button_gpio_pin)], capture_output=True, text=True)
        # button_state = button_state.stdout.strip()

        # หากมีการกด push-button
        # if button_state == '0':
        #     led_state = 0  # สลับสถานะ LED
        #     print(led_state)
        
        # elif button_state == '1':
        #     led_state = 1
        # ตั้งค่าสถานะของ LED ตามผลลัพธ์
        subprocess.run(['gpio', '-g', 'write', str(led_gpio_pin), str(1)])

        # time.sleep(0.1)  # หน่วงเวลาเพื่อลดการกดซ้ำ

except KeyboardInterrupt:
    pass

# คืนค่า GPIO ให้สถานะปกติ
subprocess.run(['gpio', '-g', 'mode', str(led_gpio_pin), 'out'])
# subprocess.run(['gpio', '-g', 'mode', str(button_gpio_pin), 'in'])

