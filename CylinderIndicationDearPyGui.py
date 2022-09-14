import dearpygui.dearpygui as dpg
from math import sin

dpg.create_context()

# creating data
cylIdx = 0
sindatax = [1 , 2, 3, 4]
sindatay = [10.0, 20.0, 35.0, 40.0]
sindataxline = [i for i in range(6)]
sindatayline = [sindatay[0] for i in range(6)]

def buttonCyl_callback(sender, app_data, user_data):
    global cylIdx
    cylIdx = user_data
    return cylIdx

def update_series():
    global cylIdx
    sindatay[0] = sindatay[0] + 10
    dpg.set_value('series_tag', [sindatax, sindatay])
    dpg.set_item_label('row1col1', sindatay[0])
    print(cylIdx)
    sindatayline = [sindatay[cylIdx] for i in range(6)]
    dpg.set_value('ImportantCylinder',[sindataxline, sindatayline])

with dpg.window(label="Tutorial"):
    dpg.add_button(label="Update Series", callback=update_series)

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
    with dpg.plot(label="Cisnienie w cylindrach", height=400, width=400):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")

        # series belong to a y axis
        dpg.add_bar_series(sindatax, sindatay, parent="y_axis", tag="series_tag", weight=0.75)
        dpg.add_line_series(sindataxline, sindatayline, parent="y_axis", tag="ImportantCylinder")

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()