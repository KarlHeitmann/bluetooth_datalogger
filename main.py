import os

import threading   
from math import sin

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.garden.graph import Graph, MeshLinePlot

from kivy.properties import StringProperty

import time

gbl_force_close = False

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
                print(mensaje)
                conectando_str(mensaje)
                mensaje = ""
            print(input_chr)
    print("va a cerrar socket")
    socket_in.close()
    print("BYE BYE Thread")

if 'BLUETOOTH_OFF' in os.environ:
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
    raw_txt_str = ""
    raw_txt = StringProperty(str(raw_txt_str))
    def on_enter(self):
        print("Bienvenido!")
        gbl_force_close = False
        recv_stream, send_stream = get_socket_stream(BLUETOOTH_NAME)
        self.send_stream = send_stream
        #threading.Thread(target=working, args=(recv_stream, self.conectando_text, )).start()
        threading.Thread(target=working, args=(recv_stream, self.actualizar, self.raw_log)).start()
    def raw_log(self, caracter):
        self.raw_txt_str = self.raw_txt_str + caracter
        print(self.raw_txt_str)
        print(type(self.raw_txt_str))
        print(type(str(self.raw_txt_str)))
        self.raw_txt = StringProperty(str(self.raw_txt_str))
    def actualizar(self, mensaje):
        self.conectando_text = mensaje
    def on_leave(self):
        self.send_stream.close()
        gbl_force_close = True
        print("Cerrando salida")


class MenuScreen(Screen):
    def on_start(self):
        self.graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
            x_ticks_major=25, y_ticks_major=1,
            y_grid_label=True, x_grid_label=True, padding=5,
            x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1
        )
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        self.graph.add_plot(self.plot)

    def start_bluetooth(self):
        print("starting")

class SettingsScreen(Screen):
    pass


class SetGraph(Widget):
    graph_test = ObjectProperty(None)
    def update_graph(self):
        print("update_graph")
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        print(plot)
        print(plot.points)
        #self.graph_test.add_plot(plot)
        self.ids["graph_test"].add_plot(plot)
        print(self.graph_test)

class BluetoothDataloggerApp(App):
    def on_connect(self):
        print("Conectando...")
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(BluetoothScreen(name='bluetooth'))
        sm.add_widget(Thread(name='thread'))
        sm.add_widget(SettingsScreen(name='settings'))
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        self.graph = Graph(
            _with_stencilbuffer= False,
            xlabel='X',
            ylabel='Y',
            x_ticks_minor=5,
            x_tics_major=25,
            y_ticks_major=1,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            x_grid=True,
            y_grid=True,
            xmin=-0,
            xmax=100,
            ymin=-10,
            ymax=10,
            pos= 0, root.height / 6,
        )
        self.graph.add_plot(self.plot)

        #disp.update_graph()
        #self.load_kv('thread.kv')
        #return Thread() 
        #return Widget()
        return sm
if __name__ == "__main__":
    # Create the screen manager
    #TestApp().run()

    app = BluetoothDataloggerApp()
    app.run()
