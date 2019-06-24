import os

import threading   

from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.graph import Graph, MeshLinePlot

from setgraph import SetGraph

BLUETOOTH_NAME = 'ESP32test'

if not('BLUETOOTH_OFF' in os.environ):
    from jnius import autoclass
    BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
    BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
    BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
    UUID = autoclass('java.util.UUID')

gbl_force_close = False


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

def working(socket_in, conectando_str, raw_log):
    print(socket_in)
    print("WORKING")
    mensaje = ""
    while(not(gbl_force_close)):
        if (socket_in.available()):
            input_chr = chr(socket_in.read())
            raw_log(input_chr)
            #conectando_str = input_chr
            mensaje = mensaje + input_chr
            if (input_chr == '\n'):
                conectando_str(mensaje)
                mensaje = ""
            print(input_chr)
    print("va a cerrar socket")
    socket_in.close()
    print("BYE BYE Thread")

# Declare both screens
class BluetoothScreen(Screen):
    conectando_text = StringProperty("Noc")
    raw_txt_str = ""
    raw_txt = StringProperty(str(raw_txt_str))
    def on_enter(self):
        print("Bienvenido!")
        gbl_force_close = False
        if not('BLUETOOTH_OFF' in os.environ):
            recv_stream, send_stream = get_socket_stream(BLUETOOTH_NAME)
            self.send_stream = send_stream
            threading.Thread(target=working, args=(recv_stream, self.actualizar, self.raw_log, )).start()
            self.ids["MiGraf"].inicializar()
        else:
            print("NO BLUETOOTH")
    def raw_log(self, caracter):
        self.raw_txt_str = (self.raw_txt_str + caracter).replace('\n', ' ')
        self.raw_txt = self.raw_txt_str
    def actualizar(self, mensaje):
        try:
            val = int(mensaje)
            print("Agregar punto")
            self.ids["MiGraf"].add_point(_y = val)
        except ValueError:
            print("That's not an int!")
            self.conectando_text = mensaje
    def on_leave(self):
        self.send_stream.close()
        gbl_force_close = True
        print("Cerrando salida")

if __name__ == '__main__':
    from kivy.app import App
    class BluetoothScreenApp(App):
        def on_connect(self):
            print("Conectando...")
        def build(self):
            sm = ScreenManager()
            sm.add_widget(BluetoothScreen(name='bluetooth'))
            return sm
    BluetoothScreenApp().run()

