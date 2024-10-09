import dragon_cultists
import sand
import nomad

from tkinter import *
import dearpygui.dearpygui as dpg
import multiprocessing as mp
#IMPORTANT
#WARNING
#this must be imported at the top level or eventloop wont work because
# only the main thread can SIGNALTERM on the main module
import thread


mapping = {
        "fire inner": dragon_cultists.inner_ring,
        "fire outer": dragon_cultists.outer_ring,
        "sand": sand.main,
        "nomad": nomad.main
    }



def startgui():
    # Define the options for the dropdown
    options = ["Option 1", "Option 2", "Option 3", "Option 4"]

    options=[*mapping]



    # Callback function to handle selection
    def show_selected(sender, app_data):
        selected_value = app_data  # app_data contains the selected option value
        selected_index = options.index(selected_value)  # Get the index of the selected option
        print(f"Selected option: {selected_value} (Index: {selected_index})")

        import eventloop
        eventloop.wrap(mapping[selected_value])

        return


    # Create the DearPyGui context
    dpg.create_context()

    # Create a window
    with dpg.window(label="Dropdown Menu Example",width=500,height=500):
        dpg.add_text("Select an option:")

        # Add the dropdown (combo) menu
        dpg.add_combo(items=options, label="Dropdown", default_value=options[0], callback=show_selected)



    with dpg.font_registry():
        # Load a font from your system with a larger size (adjust the path accordingly)
        default_font = dpg.add_font("C:/Windows/Fonts/Arial.ttf", 50)  # Change to 25 to make things bigger

    dpg.bind_font(default_font)  # Apply the custom font to make elements larger


    # Create and show the DearPyGui viewport
    dpg.create_viewport(title="DearPyGui Dropdown Example", width=500, height=500)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    print("foo")
    dpg.start_dearpygui()
    print("bar")
    dpg.destroy_context()
    print("destroy")




def radiogroup():
    def print_selection(sender, app_data, user_data):
        print(f"Selected: {app_data}")

        import eventloop
        eventloop.wrap(mapping[app_data])




    dpg.create_context()

    # Create a window for the radio button group
    with dpg.window(label="Radio Button Group Example", width=600, height=600):
        # Create radio button group with no default selection
        with dpg.group():
            dpg.add_text("Choose an option:")
            dpg.add_radio_button(list(mapping.keys()), callback=print_selection)


    with dpg.font_registry():
        # Load a font from your system with a larger size (adjust the path accordingly)
        default_font = dpg.add_font("C:/Windows/Fonts/Arial.ttf", 50)  # Change to 25 to make things bigger

    dpg.bind_font(default_font)  # Apply the custom font to make elements larger


    # Show DearPyGui
    dpg.create_viewport(title="Radio Button Example", width=600, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()



if __name__ == '__main__':
    radiogroup()
