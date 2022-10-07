import dearpygui.dearpygui as dpg
import time, threading, sys
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import pymodbus.register_read_message as ResponseClass

dpg.create_context()

# creating data
cylIdx = 0
maxPress = 0.7
sindatax = [1 , 2, 3, 4]
sindatay = [0.1, 0.4, 0.1, 0.8]
sindataxline = [i for i in range(6)]
sindatayline = [sindatay[0] for i in range(6)]

#Modbus connection initialization
#client = ModbusClient(method='rtu', port='/dev/ttyUSB0', timeout=4, baudrate=9600, stopbits=1, bytesize=8, parity='N')
client = ModbusClient(method='rtu', port='COM6', timeout=4, baudrate=9600, stopbits=1, bytesize=8, parity='N')
print(f"Modbus client parameters: {client}")
connection = client.connect()
print(f"Do we have connection: {connection}")

def buttonCyl_callback(sender, app_data, user_data):
    global cylIdx
    cylIdx = user_data
    return cylIdx

def update_series():
    global cylIdx
    #Simulation
    #for i in range(len(sindatay)):
     #   ytemp = random.uniform(0.2, 0.65)
      #  if ytemp > 0.6:
       #     sindatay[i] = random.uniform(0.55, 0.65)
    #Modbus read values
    for i in range(1, 5):
        value = client.read_holding_registers(1, unit=i)
        if isinstance(value, ResponseClass.ReadHoldingRegistersResponse):
            sindatay[i-1] = ((value.registers[0] - 400) / 16000) * (maxPress)
        else:
            sys.exit(f"Error when reading register on module {i}")
    #sindatay = [y1, 0.1, 0.2, 0.25]
    print(sindatay)

    #Update Cylinder pressure
    dpg.set_value('series_tag', [sindatax, sindatay])
    #Update value on the button in the table
    dpg.set_item_label('row1col1', sindatay[0])
    dpg.set_item_label('row1col2', sindatay[1])
    dpg.set_item_label('row1col3', sindatay[2])
    dpg.set_item_label('row1col4', sindatay[3])
    #Update line depends which cylinder is leading
    sindatayline = [sindatay[cylIdx] for i in range(6)]
    dpg.set_value('ImportantCylinder',[sindataxline, sindatayline])
    #Cyclic operation
    threading.Timer(0.5, update_series).start()

with dpg.window(label="Tutorial", width=790, height=800):

    with dpg.theme(tag="plot_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (242, 27, 106), category=dpg.mvThemeCat_Plots)

    dpg.add_button(label="Start", callback=update_series)

    with dpg.table(header_row=True, row_background=True, borders_outerV=True, resizable=True, delay_search=True,
                            hideable=True, reorderable=True, borders_innerH=True):
        dpg.add_table_column(label="Cylinder 1")
        dpg.add_table_column(label="Cylinder 2")
        dpg.add_table_column(label="Cylinder 3")
        dpg.add_table_column(label="Cylinder 4")

        with dpg.table_row():
            dpg.add_button(label=sindatay[0], tag="row1col1", width=-1, callback=buttonCyl_callback, user_data=0)
            dpg.add_button(label=sindatay[1], tag="row1col2", width=-1, callback=buttonCyl_callback, user_data=1)
            dpg.add_button(label=sindatay[2], tag="row1col3", width=-1, callback=buttonCyl_callback, user_data=2)
            dpg.add_button(label=sindatay[3], tag="row1col4", width=-1, callback=buttonCyl_callback, user_data=3)
    # create plot
    with dpg.plot(label="Cisnienie w cylindrach",  width=790, height=650):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="x", no_gridlines=True)
        dpg.add_plot_axis(dpg.mvYAxis, label="Pressure", tag="y_axis")
        dpg.set_axis_limits("y_axis", ymin=0, ymax=0.8)

        # series belong to a y axis
        dpg.add_bar_series(sindatax, sindatay, parent="y_axis", tag="series_tag", weight=0.75)
        dpg.add_line_series(sindataxline, sindatayline, parent="y_axis", tag="ImportantCylinder")
        dpg.add_line_series(sindataxline, [0.5 for i in range(6)], parent="y_axis", tag="LL_band" )
        dpg.add_line_series(sindataxline, [0.6 for i in range(6)], parent="y_axis", tag="ML_band")
        dpg.add_line_series(sindataxline, [0.7 for i in range(6)], parent="y_axis", tag="HL_band")

        # apply theme to series
        dpg.bind_item_theme("LL_band", "plot_theme")
        dpg.bind_item_theme("ML_band", "plot_theme")

dpg.create_viewport(title='Custom Title', width=800, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
