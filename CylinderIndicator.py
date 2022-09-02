from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from itertools import count
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

cylidx = 0
x = [1, 2, 3, 4]
y = [0, 0, 0, 0]
xline = [0, 1, 2, 3, 4, 5]
yline = [0, 0, 0, 0, 0, 0]
xlimit1 = [0, 1, 2, 3, 4, 5]
ylimit1 = [45 for i in range(6)]
ylimit2 = [65 for i in range(6)]
ylimit3 = [85 for i in range(6)]
ani = None

fig, ax = plt.subplots()
fig.suptitle('Cisnienie w cylindrach')
plt.style.use('fivethirtyeight')

client = ModbusClient(method='rtu', port='/dev/ttyUSB0', timeout=4, baudrate=9600, stopbits=1, bytesize=8, parity='N')
print(client)

connection = client.connect()
print(connection)

def addCyl(cylSel):
    global cylidx
    cylidx = cylSel
    return cylidx

def addCyl_1(k):
    global cylidx
    cylidx = 0
    return cylidx

def addCyl_2(k):
    global cylidx
    cylidx = 1
    return cylidx

def addCyl_3(k):
    global cylidx
    cylidx = 2
    return cylidx

def addCyl_4(k):
    global cylidx
    cylidx = 3
    return cylidx

def animate(i):
    value = client.read_holding_registers(1, unit=0x01)
    y = [value, 1000, 1300, 1500]
    #for n in range(len(x)):
     #   y[n] = value.registers[n]
      #  print(f"{i}: {value.registers[n]}")
    for n in range(len(xline)):
        yline[n] = y[cylidx]
    #plt.cla()
    #print(f"x {x}")
    #print(f"y {y}")
    #print(f"xline {xline}")
    #print(f"yline {yline}")
    ax.clear()
    
    ax.plot(xline, yline, color='darkcyan')
    ax.fill_between(xlimit1, ylimit1, ylimit2, color = 'lime')
    ax.fill_between(xlimit1, ylimit2, ylimit3, color = 'red')
    ax.bar(x,y,
            label=['Cylinder 1', 'Cylinder 2', 'Cylinder 3', 'Cylinder 4'],
            color= ['peachpuff', 'cyan', 'violet', 'wheat'])
    ax.legend(loc='lower center')
    

#value = client.read_holding_registers(0, 4, unit=0x01)
#print(value.registers[0])

axCyl_1 = plt.axes([0.18, 0, 0.1, 0.1])
axCyl_2 = plt.axes([0.37, 0, 0.1, 0.1])
axCyl_3 = plt.axes([0.55, 0, 0.1, 0.1])
axCyl_4 = plt.axes([0.75, 0, 0.1, 0.1])
btnCyl_1 = Button(axCyl_1, addCyl(1))
btnCyl_2 = Button(axCyl_2, addCyl(2))
btnCyl_3 = Button(axCyl_3, addCyl(3))
btnCyl_4 = Button(axCyl_4, addCyl(4))
btnCyl_1.on_clicked(addCyl_1)
btnCyl_2.on_clicked(addCyl_2)
btnCyl_3.on_clicked(addCyl_3)
btnCyl_4.on_clicked(addCyl_4)

ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.show()