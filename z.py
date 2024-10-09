import dragon_cultists
import sand

import multiprocessing as mp
from pynput import keyboard
import time
import threading
import dearpygui.dearpygui as dpg
import thread



def info():
    t = threading.current_thread()
    print(t.name, t.native_id)



def loop():
    while True:
        print('Looping')
        time.sleep(1)




def onpress(key):
    import threading
    info()

    if key == keyboard.Key.esc:
        global side
        side.kill()
        print('terminating')
    else:
        print(f'Pressed: {key}')


def listen():
    listener = keyboard.Listener(on_press=onpress,daemon=True)
    listener.start()
    print('listening')
    listener.join()
    print("done")



def gui():
    print('GUI')


    mapping = {
        "fire inner": dragon_cultists.inner_ring,
        "fire outer": dragon_cultists.outer_ring,
        "sand": sand.main
    }


    # Define the options for the dropdown
    options = ["Option 1", "Option 2", "Option 3", "Option 4"]

    options=[*mapping]



    # Callback function to handle selection
    def show_selected(sender, app_data):
        selected_value = app_data  # app_data contains the selected option value
        selected_index = options.index(selected_value)  # Get the index of the selected option
        print(f"Selected option: {selected_value} (Index: {selected_index})")

        info()
        print(__name__)
        import eventloop
        eventloop.wrap(loop)
        return

        listener = keyboard.Listener(on_press=onpress)
        listener.start()

        p = mp.Process(target=eventloop.wrap,args=(loop,))
        global side
        side=p
        p.start()


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


    print('Exiting GUI')
    return


side:mp.Process

if __name__ == '__main__':
    import eventloop
    eventloop.wrap(loop)
    print("finished")
    exit()

    info()
    gui()
    exit()
    side = mp.Process(target=loop)

    import thread
    side = thread.Thread(target=loop)

    listener = keyboard.Listener(on_press=onpress, daemon=True)
    listener.start()

    # listen_p = mp.Process(target=listen)
    # listen_p.start()
    # listen_p.join()
    print("after")


    side.start()
    side.join()
    listener.stop()
    # listen.close()
    print("joined")
else:
    print('new process')
    info    ()