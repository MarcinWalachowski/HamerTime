from pymodbus.client.sync, import ModbusSerialClient as ModbusClient
import pymodbus.register_read_message as ResponseClass

#client = ModbusClient(method='rtu', port='/dev/ttyUSB0', timeout=4, baudrate=9600, stopbits=1, bytesize=8, parity='N')
client = ModbusClient(method='rtu', port='COM6', timeout=4, baudrate=9600, stopbits=1, bytesize=8, parity='N')
print(f"Modbus client parameters: {client}")
connection = client.connect()
print(f"Do we have connection: {connection}")

for i in range(1, 256):
    cur_address = client.read_holding_registers(253, unit=i)
    if isinstance(cur_address, ResponseClass.ReadHoldingRegistersResponse):
        print(f"Modbus address of connected device: {i}")
        cur_module_address = i
        break
    else:
        pass

address = int(input(f"New modbus address for connected device: "))
if input(f"Do you want to change the address (y/n): ") == 'y':
    respond = client.write_register(unit=cur_module_address, value=address, address=253)
    print(respond)
else:
    pass
