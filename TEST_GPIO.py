from periphery import GPIO
import time

# กำหนดหมายเลขขา GPIO ที่ต้องการใช้งาน
gpio_pin = 123 #ขา123 ใช้เป็น heartbeat แล้ว

gpio = GPIO(gpio_pin, "out")

# try:
    # เปิดขา GPIO
    # gpio = periphery.GPIO(gpio_pin, "out")
    # gpio.write(True)  # เปิด

    # เปิด/ปิดขา GPIO แล้วหน่วงเวลา
while True:
    gpio.write(True)  # เปิด
    print("GPIO is ON")
    # periphery.sleep_ms(3000)
    time.sleep(3)

    # gpio.write(False) # ปิด
    # print("GPIO is OFF")
    # # periphery.sleep_ms(5000)
    # time.sleep(3)

# except KeyboardInterrupt:
    # หยุดการทำงานเมื่อกด Ctrl+C
    # gpio.close()
