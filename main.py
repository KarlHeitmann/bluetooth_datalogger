from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty

import time

# modulos personales
from bluetooth_screen import BluetoothScreen
from setgraph import SetGraph

class Thread(Screen):
    counter = NumericProperty(0)
    def Counter_function(self):
        self.counter += 1
        self.ids.lbl.text = "{}".format(self.counter)

    def First_thread(self):
        threading.Thread(target = working).start()
        self.counter += 1
        self.ids.lbl.text = "{}".format(self.counter)

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

class BluetoothDataloggerApp(App):
    def on_connect(self):
        print("Conectando...")
    def build(self):
        sm = ScreenManager()
        self.disp = SetGraph()
        self.disp.update_graph()
        ms = MenuScreen(name='menu')
        sm.add_widget(ms)
        sm.add_widget(BluetoothScreen(name='bluetooth'))
        sm.add_widget(Thread(name='thread'))
        sm.add_widget(SettingsScreen(name='settings'))
        return sm

if __name__ == "__main__":
    app = BluetoothDataloggerApp()
    app.run()
