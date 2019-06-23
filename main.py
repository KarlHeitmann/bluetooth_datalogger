import threading   
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen


import time

def working():
    for i in range(10):
        print("i = %d" % i)
        time.sleep(5)


class Thread(Screen):
    counter = NumericProperty(0)

    def Counter_function(self):
        self.counter += 1
        self.ids.lbl.text = "{}".format(self.counter)

    def First_thread(self):
        threading.Thread(target = working).start()
        self.counter += 1
        self.ids.lbl.text = "{}".format(self.counter)

# Declare both screens
class MenuScreen(Screen):
    def start_bluetooth(self):
        print("starting")

class SettingsScreen(Screen):
    pass

class BluetoothDataloggerApp(App):
    def on_connect(self):
        print("Conectando...")
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(Thread(name='thread'))
        sm.add_widget(SettingsScreen(name='settings'))
        #self.load_kv('thread.kv')
        #return Thread() 
        #return Widget()
        return sm
if __name__ == "__main__":
    # Create the screen manager
    #TestApp().run()

    app = BluetoothDataloggerApp()
    app.run()
