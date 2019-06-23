from math import sin

from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager

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
        self.ids["graph_test"].add_plot(self.plot)
        print(self.graph_test)
        print("CLICK!!!")
    def add_point(self, _x, _y):
        self.x = self.x + 1
        self.plot.points.append((self.x, 2))

if __name__ == '__main__':
    from kivy.app import App
    class SetGraphApp(App):
        def on_connect(self):
            print("Conectando...")
        def build(self):
            sm = ScreenManager()
            screen = Screen(name='set_graph')
            sm.add_widget(screen)
            return sm
            #return SetGraph()
    SetGraphApp().run()


