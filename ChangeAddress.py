from pymodbus.client.sync import ModbusSerialClient as ModbusClient

client = ModbusClient(method='rtu', port='/dev/ttyUSB0', timeout=4, baudrate=9600, stopbits=1, bytesize=8, parity='N')
print(client)
connection = client.connect()
print(connection)

cur_address = client.read_holding_registers(255, unit=0x01)
print(f"Aktualny adres: {cur_address}")

address = int(input(f"Podaj adres modulu modbus: "))

if input(f"Czy zmienic adres (t/n): ") == 't':
    respond = client.write_register(slave=0x01, value=address, address=253)
    print(respond)
else:
    pass