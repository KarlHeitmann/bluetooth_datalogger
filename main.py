import threading   
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty

class Thread(BoxLayout):
    counter = NumericProperty(0)

    def Counter_function(self):
        self.counter += 1
        self.ids.lbl.text = "{}".format(self.counter)

    def First_thread(self):
        threading.Thread(target = self.Counter_function).start()
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
