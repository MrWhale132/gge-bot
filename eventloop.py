import time

from thread import Thread
from pynput import keyboard


class EventLoop():
    def __init__(self, event):
        self.event = event
        self.loop = Thread(event)
        self.loop.add_hook(lambda result: self.oncomplete(result))
        self.listener=keyboard.Listener(on_press=self.handle)


    def oncomplete(self, result):
        self.listener.stop()
        print("completed")


    def run(self):
        def loop():
            while True:
                print("looping")
                time.sleep(1)

        # self.event=loop
        # self.loop = Thread(self.event,daemon=False)
        self.loop.start()

        self.listener.start()

        # self.loop.join()
        #
        # listener.stop()


    def wait(self):
        self.loop.join()
        #todo: implement
        # listener.stop()


    def handle(self,key):
        if (key == keyboard.Key.esc) or (key == keyboard.Key.space):
            self.loop.kill()
            self.listener.stop()
            print("killed t")
        # else:
        #     if isinstance(key, keyboard.KeyCode): print(key.char)
        #     if isinstance(key, keyboard.Key): print(key.value)



def wrap(func)->EventLoop:
    loop = EventLoop(func)
    loop.run()
    return loop

