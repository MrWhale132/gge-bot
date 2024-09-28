from thread import Thread
from pynput import keyboard


class EventLoop():
    def __init__(self, event):
        self.event = event
        self.loop = Thread(event)



    def run(self):
        self.loop.start()

        listener = keyboard.Listener(on_press=self.handle)
        listener.start()

        self.loop.join()

        listener.stop()


    def handle(self,key):
        if (key == keyboard.Key.esc) or (key == keyboard.Key.space):
            self.loop.kill()
            print("killed t")
        else:
            if isinstance(key, keyboard.KeyCode): print(key.char)
            if isinstance(key, keyboard.Key): print(key.value)



def wrap(func):
    EventLoop(func).run()
