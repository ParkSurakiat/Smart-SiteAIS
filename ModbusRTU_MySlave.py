# from modbus_tk import modbus_rtu
# from modbus_tk.exceptions import ModbusError
# import serial

# # Configure the serial port (change port to '/dev/ttyS1' for UART 1)
# serial_port = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1)

# # Create a Modbus master instance
# master = modbus_rtu.RtuMaster(serial_port)
# master.set_timeout(1.0)  # Set a timeout for Modbus communication

# try:
#     # Modbus address of the register you want to read
#     register_address = 0x310C

#     # Read the register
#     response = master.execute(1, function_code=4, starting_address=register_address, quantity_of_x=1)  # Reading 1 register

#     # Extract the value from the response
#     value = response[0]

#     print("Value:", value)

# except ModbusError as e:
#     print("Modbus Error:", e)

# finally:
#     serial_port.close()




from modbus_tk import modbus_rtu
from modbus_tk.exceptions import ModbusError
import serial
import time

# Configure the serial port (change port to '/dev/ttyS1' for UART 1)
serial_port = serial.Serial(port='/dev/ttyUSB1', baudrate=115200, bytesize=8, parity='N', stopbits=1)

# Create a Modbus master instance
master = modbus_rtu.RtuMaster(serial_port)
master.set_timeout(1.0)  # Set a timeout for Modbus communication

try:
    # Modbus address of the slave device
    slave_address = 1

    # Modbus address of the register you want to write to
    register_address_5 = 5
    register_address_6 = 6

    # Values you want to write to the registers
    value_to_write_5 = 1
    value_to_write_6 = 1
    
    # Write the value to the register using execute function for address 5
    master.execute(slave=slave_address, function_code=6, starting_address=register_address_5, output_value=value_to_write_5)
    print("Value written to address 5:", value_to_write_5)

    time().sleep(1)
    
    # Write the value to the register using execute function for address 6
    master.execute(slave=slave_address, function_code=6, starting_address=register_address_6, output_value=value_to_write_6)
    print("Value written to address 6:", value_to_write_6)

except ModbusError as e:
    print("Modbus Error:", e)

finally:
    serial_port.close()

