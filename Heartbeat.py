from periphery import GPIO
import time

# กำหนดหมายเลขขา GPIO ที่ต้องการใช้งาน
gpio_pin123 = 123

gpio123 = GPIO(gpio_pin123, "out")

# # try:
#     # เปิดขา GPIO
#     # gpio = periphery.GPIO(gpio_pin, "out")
#     # gpio.write(True)  # เปิด

#     # เปิด/ปิดขา GPIO แล้วหน่วงเวลา
# while True:
#     gpio123.write(True)  # เปิด
#     print("GPIO is ON")
#     # periphery.sleep_ms(3000)
#     time.sleep(60)

#     gpio123.write(False) # ปิด
#     print("GPIO is OFF")
#     # periphery.sleep_ms(5000)
#     time.sleep(60)

interval = 60  # 60 วินาที = 1 นาที
last_heartbeat_time = time.time()

while True:
    current_time = time.time()
    
    if current_time - last_heartbeat_time >= interval:
        # ทำงานที่ต้องการทำก่อนการส่งสัญญาณ heartbeat
        gpio123.write(True)  # เปิด
        print("Sending heartbeat...")
        
        last_heartbeat_time = current_time
    
    # ทำงานอื่น ๆ ที่คุณต้องการทำ
    