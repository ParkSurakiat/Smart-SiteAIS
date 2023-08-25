import smbus
import time

bus = smbus.SMBus(1)  # I2C-1

sensor1_address = 0x48
sensor2_address = 0x49

def read_temperature(sensor_address):
    data = bus.read_word_data(sensor_address, 0)
    temperature = ((data << 8) & 0xFF00) + (data >> 8)
    temperature = (temperature / 32.0) / 8.0
    return temperature

try:
    while True:
        try:
            temperature1 = read_temperature(sensor1_address)
            print(f"Sensor 1 Temperature: {temperature1:.2f} °C")
        except:
            print("Error reading from Sensor 1")

        try:
            temperature2 = read_temperature(sensor2_address)
            print(f"Sensor 2 Temperature: {temperature2:.2f} °C")
        except:
            print("Error reading from Sensor 2")
        
        time.sleep(1)

except KeyboardInterrupt:
    pass
