import threading   
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty

import time

def working():
    for i in range(10):
        print("i = %d" % i)
        time.sleep(5)


class Thread(BoxLayout):
    counter = NumericProperty(0)

    def Counter_function(self):
        self.counter += 1
        self.ids.lbl.text = "{}".format(self.counter)

    def First_thread(self):
        threading.Thread(target = working).start()
        self.counter += 1
        self.ids.lbl.text = "{}".format(self.counter)

class BluetoothDataloggerApp(App):
    def on_connect(self):
        print("Conectando...")
    def build(self):
        #self.load_kv('thread.kv')
        #return Thread() 
        #return Widget()
        pass

if __name__ == "__main__":
    app = BluetoothDataloggerApp()
    app.run()
