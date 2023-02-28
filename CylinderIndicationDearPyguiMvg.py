import dearpygui.dearpygui as dpg
import threading, sys, random
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import pymodbus.register_read_message as ResponseClass

dpg.create_context()

# creating data
cylIdx = 0
cyldata = 0
lentab = 15
maxPress = 0.7
sindatax = [1 , 2, 3, 4]
sindatay = [0.0, 0.0, 0.0, 0.0]
sindatay1 = [0 for i in range(lentab)]
sindatay2 = [0 for i in range(lentab)]
sindatay3 = [0 for i in range(lentab)]
sindatay4 = [0 for i in range(lentab)]
sindataxline = [i for i in range(6)]
sindatayline = [sindatay[0] for i in range(6)]

# Modbus connection initialization
#client = ModbusClient(method='rtu', port='/dev/ttyUSB0', timeout=4, baudrate=9600, stopbits=1, bytesize=8, parity='N')
client = ModbusClient(method='rtu', port='COM3', timeout=4, baudrate=9600, stopbits=1, bytesize=8, parity='N')
print(f"Modbus client parameters: {client}")
connection = client.connect()
print(f"Do we have connection: {connection}")


def button_cyl_callback(sender, app_data, user_data):
    global cylIdx
    cylIdx = user_data
    return cylIdx

def update_series_sim():
    global cylIdx
    global cyldata
    mvg_thr_value = dpg.get_value("mvg_thr")
    #Simulation
    value1 = random.uniform(0.45, 0.65)
    value2 = random.uniform(0.45, 0.65)
    value3 = random.uniform(0.45, 0.65)
    value4 = random.uniform(0.45, 0.65)
    cyl1 = 0
    cyl2 = 0
    cyl3 = 0
    cyl4 = 0
    for i in range(lentab):
        cyl1 = sindatay1[i] + cyl1
        cyl2 = sindatay2[i] + cyl2
        cyl3 = sindatay3[i] + cyl3
        cyl4 = sindatay4[i] + cyl4
    sindatay[0] = cyl1/lentab
    sindatay[1] = cyl2/lentab
    sindatay[2] = cyl3/lentab
    sindatay[3] = cyl4/lentab
    if value1 > sindatay[0] * mvg_thr_value:
        sindatay1[cyldata] = value1
    else:
        sindatay1[cyldata] = sindatay[0]
        print("Cyl 1 wart odrzucona")
    if value2 > sindatay[1] * mvg_thr_value:
        sindatay2[cyldata] = value2
    else:
        sindatay2[cyldata] = sindatay[1]
    if value3 > sindatay[2] * mvg_thr_value:
        sindatay3[cyldata] = value3
    else:
        sindatay3[cyldata] = sindatay[2]
    if value4 > cyl4 * mvg_thr_value:
        sindatay4[cyldata] = value4
    else:
        sindatay4[cyldata] = sindatay[3]
    cyldata = cyldata + 1
    print("sindatay", sindatay)
    print("cyldata", cyldata)
    if cyldata == lentab:
        cyldata = 0
        print("zeruje")
    print("sindatay1", sindatay1)


def update_series():
    global cylIdx
    global cyldata
    mvg_thr_value = dpg.get_value("mvg_thr")
    # Modbus read values
    value1 = client.read_holding_registers(1, unit=1)
    value2 = client.read_holding_registers(1, unit=2)
    value3 = client.read_holding_registers(1, unit=3)
    value4 = client.read_holding_registers(1, unit=4)
    cyl1 = 0
    cyl2 = 0
    cyl3 = 0
    cyl4 = 0
    for i in range(lentab):
        cyl1 = sindatay1[i] + cyl1
        cyl2 = sindatay2[i] + cyl2
        cyl3 = sindatay3[i] + cyl3
        cyl4 = sindatay4[i] + cyl4
    sindatay[0] = cyl1 / lentab
    sindatay[1] = cyl2 / lentab
    sindatay[2] = cyl3 / lentab
    sindatay[3] = cyl4 / lentab
    if isinstance(value1, ResponseClass.ReadHoldingRegistersResponse):
        if ((value1.registers[0] - 400) / 16000) * (maxPress) * 10 > sindatay[0] * mvg_thr_value:
            sindatay1[cyldata] = ((value1.registers[0] - 400) / 16000) * (maxPress) * 10
        else:
            sindatay1[cyldata] = sindatay[0]
    else:
        sys.exit(f"Error when reading register on module 1")
    if isinstance(value2, ResponseClass.ReadHoldingRegistersResponse):
        if ((value2.registers[0] - 400) / 16000) * (maxPress) * 10 > sindatay[1] * mvg_thr_value:
            sindatay2[cyldata] = ((value2.registers[0] - 400) / 16000) * (maxPress) * 10
        else:
            sindatay2[cyldata] = sindatay[1]
    else:
        sys.exit(f"Error when reading register on module 2")
    if isinstance(value3, ResponseClass.ReadHoldingRegistersResponse):
        if ((value3.registers[0] - 400) / 16000) * (maxPress) * 10 > sindatay[2] * mvg_thr_value:
            sindatay3[cyldata] = ((value3.registers[0] - 400) / 16000) * (maxPress) * 10
        else:
            sindatay3[cyldata] = sindatay[2]
    else:
        sys.exit(f"Error when reading register on module 3")

    if isinstance(value4, ResponseClass.ReadHoldingRegistersResponse):
        if ((value4.registers[0] - 400) / 16000) * (maxPress) * 10 > sindatay[3] * mvg_thr_value:
            sindatay4[cyldata] = ((value4.registers[0] - 400) / 16000) * (maxPress) * 10
        else:
            sindatay4[cyldata] = sindatay[3]
    else:
        sys.exit(f"Error when reading register on module 4")

    cyldata = cyldata + 1
    if cyldata == lentab:
        cyldata = 0
        print("zeruje")
    #print(sindatay)
    #print("sindatay1",sindatay1)

    # Update Cylinder pressure
    dpg.set_value('series_tag', [sindatax, sindatay])
    # Update value on the button in the table
    dpg.set_item_label('row1col1', sindatay[0])
    dpg.set_item_label('row1col2', sindatay[1])
    dpg.set_item_label('row1col3', sindatay[2])
    dpg.set_item_label('row1col4', sindatay[3])
    # Update line depends which cylinder is leading
    sindatayline = [sindatay[cylIdx] for i in range(6)]
    dpg.set_value('ImportantCylinder', [sindataxline, sindatayline])
    # Cyclic operation
    threading.Timer(0.01, update_series).start()
    # Use when simulation active
    # threading.Timer(0.01, update_series_sim).start()


with dpg.window(label="Tutorial", width=690, height=700):

    with dpg.theme(tag="plot_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (242, 27, 106), category=dpg.mvThemeCat_Plots)

    dpg.add_button(label="Start", callback=update_series)
    # Use when simulation active
    # dpg.add_button(label="Start", callback=update_series_sim)

    dpg.add_input_float(label="Threshold for average value", default_value=0.7, min_value=0.1,
                        max_value=1.0, step=0.05, tag="mvg_thr")

    with dpg.table(header_row=True, row_background=True, borders_outerV=True, resizable=True, delay_search=True,
                            hideable=True, reorderable=True, borders_innerH=True):
        dpg.add_table_column(label="Cylinder 1")
        dpg.add_table_column(label="Cylinder 2")
        dpg.add_table_column(label="Cylinder 3")
        dpg.add_table_column(label="Cylinder 4")

        with dpg.table_row():
            dpg.add_button(label=sindatay[0], tag="row1col1", width=-1, callback=button_cyl_callback, user_data=0)
            dpg.add_button(label=sindatay[1], tag="row1col2", width=-1, callback=button_cyl_callback, user_data=1)
            dpg.add_button(label=sindatay[2], tag="row1col3", width=-1, callback=button_cyl_callback, user_data=2)
            dpg.add_button(label=sindatay[3], tag="row1col4", width=-1, callback=button_cyl_callback, user_data=3)
    # create plot
    with dpg.plot(label="Cisnienie w cylindrach",  width=690, height=550):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="x", no_gridlines=True)
        dpg.add_plot_axis(dpg.mvYAxis, label="Pressure", tag="y_axis")
        dpg.set_axis_limits("y_axis", ymin=0, ymax=0.5)

         # series belong to a y axis
        dpg.add_bar_series(sindatax, sindatay, parent="y_axis", tag="series_tag", weight=0.75)
        dpg.add_line_series(sindataxline, sindatayline, parent="y_axis", tag="ImportantCylinder")
        dpg.add_line_series(sindataxline, [0.5 for i in range(6)], parent="y_axis", tag="LL_band" )
        dpg.add_line_series(sindataxline, [0.6 for i in range(6)], parent="y_axis", tag="ML_band")
        dpg.add_line_series(sindataxline, [0.7 for i in range(6)], parent="y_axis", tag="HL_band")

        # apply theme to series
        dpg.bind_item_theme("LL_band", "plot_theme")
        dpg.bind_item_theme("ML_band", "plot_theme")


dpg.create_viewport(title='Custom Title', width=700, height=700)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
