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
BLUETOOTH_NAME = 'ESP32test'

if not('BLUETOOTH_OFF' in os.environ):
    from jnius import autoclass
    BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
    BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
    BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
    UUID = autoclass('java.util.UUID')

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
    def quit(self):
        print("quit")
        print(self.ids["wena_choro"])
        print(self.ids["MiGraf"])
        #plot = MeshLinePlot(color=[1, 0, 0, 1])
        #plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        #self.ids["MiGraf"].pintar()
        self.ids["MiGraf"].add_point(15.0, 43.4)

class SettingsScreen(Screen):
    pass


class SetGraph(BoxLayout):
    graph_test = ObjectProperty(None)
    def update_graph(self):
        pass
    def pintar(self):
        print("update_graph")
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.plot.points = [(x, sin(x / 10.)) for x in range(0, 20)]
        self.x = 20
        print(self.plot)
        print(self.plot.points)
        #self.graph_test.add_plot(plot)
        self.ids["graph_test"].add_plot(self.plot)
        print(self.graph_test)
        print("CLICK!!!")
    def add_point(self, _x, _y):
        #plot = MeshLinePlot()
        #plot.points = [(_x, _y)]
        #plot.points = [(0, 0.0), (1, 0.09983341664682815), (2, 0.19866933079506122), (3, 0.29552020666133955), (4, 0.3894183423086505), (5, 0.479425538604203), (6, 0.5646424733950354), (7, 0.644217687237691), (8, 0.7173560908995228), (9, 0.7833269096274834), (10, 0.8414709848078965), (11, 0.8912073600614354), (12, 0.9320390859672263), (13, 0.963558185417193), (14, 0.9854497299884601), (15, 0.9974949866040544), (16, 0.9995736030415051), (17, 0.9916648104524686), (18, 0.9738476308781951), (19, 0.9463000876874145), (20, 0.9092974268256817), (21, 0.8632093666488737), (22, 0.8084964038195901), (23, 0.7457052121767203), (24, 0.675463180551151), (25, 0.5984721441039565), (26, 0.5155013718214642), (27, 0.4273798802338298), (28, 0.3349881501559051), (29, 0.23924932921398243), (30, 0.1411200080598672), (31, 0.04158066243329049), (32, -0.058374143427580086), (33, -0.1577456941432482), (34, -0.2555411020268312), (35, -0.35078322768961984), (36, -0.44252044329485246), (37, -0.5298361409084934), (38, -0.6118578909427189), (39, -0.6877661591839738), (40, -0.7568024953079282), (41, -0.8182771110644103), (42, -0.8715757724135882), (43, -0.9161659367494549), (44, -0.951602073889516), (45, -0.977530117665097), (46, -0.9936910036334644), (47, -0.9999232575641008), (48, -0.9961646088358407), (49, -0.9824526126243325), (50, -0.9589242746631385), (51, -0.9258146823277325), (52, -0.8834546557201531), (53, -0.8322674422239013), (54, -0.7727644875559871), (55, -0.7055403255703919), (56, -0.6312666378723216), (57, -0.5506855425976376), (58, -0.46460217941375737), (59, -0.373876664830236), (60, -0.27941549819892586), (61, -0.18216250427209588), (62, -0.0830894028174964), (63, 0.016813900484349713), (64, 0.11654920485049364), (65, 0.21511998808781552), (66, 0.31154136351337786), (67, 0.4048499206165983), (68, 0.49411335113860816), (69, 0.5784397643882001), (70, 0.6569865987187891), (71, 0.7289690401258759), (72, 0.7936678638491531), (73, 0.8504366206285644), (74, 0.8987080958116269), (75, 0.9379999767747389), (76, 0.9679196720314863), (77, 0.9881682338770004), (78, 0.998543345374605), (79, 0.998941341839772), (80, 0.9893582466233818), (81, 0.9698898108450863), (82, 0.9407305566797731), (83, 0.9021718337562933), (84, 0.8545989080882804), (85, 0.7984871126234903), (86, 0.7343970978741133), (87, 0.6629692300821833), (88, 0.5849171928917617), (89, 0.5010208564578846), (90, 0.4121184852417566), (91, 0.3190983623493521), (92, 0.22288991410024764), (93, 0.1244544235070617), (94, 0.024775425453357765), (95, -0.0751511204618093), (96, -0.17432678122297965), (97, -0.27176062641094245), (98, -0.3664791292519284), (99, -0.45753589377532133), (100, -0.5440211108893698)]
        self.x = self.x + 1
        self.plot.points.append((self.x, 2))
        #self.ids["graph_test"].add_plot(plot)


class BluetoothDataloggerApp(App):
    def on_connect(self):
        print("Conectando...")
    def build(self):
        sm = ScreenManager()
        '''
        ms.add_widget(disp)
        '''
        self.disp = SetGraph()
        self.disp.update_graph()
        ms = MenuScreen(name='menu')
        sm.add_widget(ms)
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
