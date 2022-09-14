import dearpygui.dearpygui as dpg
import time, threading
from math import sin

dpg.create_context()

# creating data
cylIdx = 0
sindatax = [1 , 2, 3, 4]
sindatay = [0.1, 0.1, 0.1, 0.1]
sindataxline = [i for i in range(6)]
sindatayline = [sindatay[0] for i in range(6)]

def buttonCyl_callback(sender, app_data, user_data):
    global cylIdx
    cylIdx = user_data
    return cylIdx

def update_series():
    global cylIdx
    sindatay[0] = sindatay[0] + 0.05
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


dpg.create_viewport(title='Custom Title', width=800, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
