import threading   
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.properties import StringProperty

import time

gbl_force_close = False

def working(socket_in, conectando_str):
    print(socket_in)
    print("WORKING")
    for i in range(10):
        print("EN LOOP")
        if gbl_force_close:
            print("condicion_salida")
            break
        if (socket_in.available()):
            input_chr = chr(socket_in.read())
            #conectando_str = input_chr
            conectando_str(input_chr)
            print(input_chr)
        print("i = %d" % i)
        time.sleep(1)
    print("va a cerrar socket")
    socket_in.close()
    print("BYE BYE Thread")

from jnius import autoclass

BLUETOOTH_NAME = 'ESP32test'
BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
UUID = autoclass('java.util.UUID')

def get_socket_stream(name):
    paired_devices = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
    print("========================")
    print([ x.getName() for x in paired_devices ])
    print(paired_devices)
    socket = None
    for device in paired_devices:
        print(device.getName())
        if device.getName() == name:
            socket = device.createRfcommSocketToServiceRecord(
                UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
            recv_stream = socket.getInputStream()
            send_stream = socket.getOutputStream()
            break
    socket.connect()
    print("FIN SOCKET CONNECT")
    return recv_stream, send_stream

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
class BluetoothScreen(Screen):
    conectando_text = StringProperty("Noc")
    #conectando_text = "Con"
    def on_enter(self):
        print("Bienvenido!")
        gbl_force_close = False
        recv_stream, send_stream = get_socket_stream(BLUETOOTH_NAME)
        self.send_stream = send_stream
        #threading.Thread(target=working, args=(recv_stream, self.conectando_text, )).start()
        threading.Thread(target=working, args=(recv_stream, self.actualizar, )).start()
    def cambiar(self):
        print("CAMBIAR!!!!!!!!!!!!!!!")
        print(self.conectando_text)
        self.conectando_text = "asdsda"
        print(self.conectando_text)
    def actualizar(self, caracter):
        print("JKHGDFHJKGDFJHGKJDFHGJKDFHGDJFKHGKDFHGKFDJHGDFKJHGKJDFHGKFJHGDFJKHGDF")
        print(self.conectando_text)
        self.conectando_text = caracter
        print(caracter)
        print(self.conectando_text)
        print("dsfsdfsdfs ================ %s", caracter)
        print("JKHGDFHJKGDFJHGKJDFHGJKDFHGDJFKHGKDFHGKFDJHGDFKJHGKJDFHGKFJHGDFJKHGDF")
    def on_leave(self):
        self.send_stream.close()
        gbl_force_close = True
        print("Cerrando salida")


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
        sm.add_widget(BluetoothScreen(name='bluetooth'))
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
