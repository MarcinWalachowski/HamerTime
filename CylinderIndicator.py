from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from itertools import count
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

cylidx = 0
minPress = 0.0
maxPress = -0.7
x = [1, 2, 3, 4]
y = [0, 0, 0, 0]
xline = [0, 1, 2, 3, 4, 5]
yline = [0, 0, 0, 0, 0, 0]
xlimit1 = [0, 1, 2, 3, 4, 5]
ylimit1 = [0.4 for i in range(6)]
ylimit2 = [0.5 for i in range(6)]
ylimit3 = [0.7 for i in range(6)]
ani = None

fig, ax = plt.subplots()
fig.suptitle('Cisnienie w cylindrach')
plt.style.use('fivethirtyeight')

client = ModbusClient(method='rtu', port='/dev/ttyUSB0', timeout=4, baudrate=9600, stopbits=1, bytesize=8, parity='N')
print(client)

connection = client.connect()
print(connection)

def addCyl1(k):
    global cylidx
    cylidx = 0
    return cylidx

def addCyl2(k):
    global cylidx
    cylidx = 1
    return cylidx

def addCyl3(k):
    global cylidx
    cylidx = 2
    return cylidx

def addCyl4(k):
    global cylidx
    cylidx = 3
    return cylidx

def animate(i):
    value = client.read_holding_registers(1, unit=0x01)
    y1 = ((value.registers[0] - 400)/16000) * (0.7)
    print(y1)
    y = [0.1, 0.1, 0.2, 0.25]
    print(y)
    for n in range(len(xline)):
        yline[n] = y[cylidx]
    ax.clear()
    
    ax.plot(xline, yline, color='darkcyan')
    ax.fill_between(xlimit1, ylimit1, ylimit2, color = 'lime')
    ax.fill_between(xlimit1, ylimit2, ylimit3, color = 'red')
    ax.bar(x,y,
            color= ['peachpuff', 'cyan', 'violet', 'wheat'])
    #ax.legend(loc='lower center')
    

#value = client.read_holding_registers(0, 4, unit=0x01)
#print(value.registers[0])

axCyl_1 = plt.axes([0.25, 0, 0.1, 0.1])
axCyl_2 = plt.axes([0.39, 0, 0.1, 0.1])
axCyl_3 = plt.axes([0.53, 0, 0.1, 0.1])
axCyl_4 = plt.axes([0.67, 0, 0.1, 0.1])
btnCyl_1 = Button(axCyl_1, 'Cyl 1')
btnCyl_2 = Button(axCyl_2, 'Cyl 2')
btnCyl_3 = Button(axCyl_3, 'Cyl 3')
btnCyl_4 = Button(axCyl_4, 'Cyl 4')
btnCyl_1.on_clicked(addCyl1)
btnCyl_2.on_clicked(addCyl2)
btnCyl_3.on_clicked(addCyl3)
btnCyl_4.on_clicked(addCyl4)

ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.show()