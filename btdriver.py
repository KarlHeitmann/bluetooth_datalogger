import threading
import time
from kivy.uix.boxlayout import BoxLayout

from jnius import autoclass

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


class Thread(BoxLayout):
    def __init__(self, datalogger_main, threadID, name, counter, inputStream):
        threading.Thread.__init__(self)
        print("Iniciando thread")
        self.datalogger_main = datalogger_main
        self.inputStream = inputStream
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("Starting " + self.name)
        counter = 5
        mensaje = ""
        while counter:
            if self.datalogger_main.condicion_salida:
                print("CONDICION DE SALIDA")
                return
            if (self.inputStream.available()):
                if self.datalogger_main.condicion_salida:
                    print("CONDICION DE SALIDA")
                    return
                input_chr = chr(self.inputStream.read())
                print(input_chr)
                mensaje = mensaje + input_chr
                if (input_chr == '\n'):
                    print(mensaje)
                    self.datalogger_main.callback_bluetooth_rx(mensaje)
                    mensaje = ""
            '''
            data_in = self.inputStream.available()
            buffer_array = []
            if (data_in):
                byte_string = self.inputStream.read(buffer_array)
                print(byte_string)
                print(buffer_array)
                data_in = 0
                #print(byte_string.decode())
            #print(self.inputStream)
            '''
        print_time(self.name, self.counter, 5)
        print ("Exiting " + self.name)

class Driver():
    def __init__(self, dsa):
        print(dsa)
    def conectar(self, datalogger_main):
        print("inicializando")
        if BLUETOOTH_MODULE:
            self.recv_stream, self.send_stream = get_socket_stream(BLUETOOTH_NAME)
            self.input_thread = Thread(datalogger_main, 1, "Thread-1", 1, self.recv_stream)
            self.input_thread.start()
    def enviar(self, send_data):
        print("ENVIANDO...")
        if BLUETOOTH_MODULE:
            self.send_stream.write(send_data.encode())
    def attach(self, datalogger_main):
        self.datalogger_main = datalogger_main
        print("ATTACHED")
        self.datalogger_main.callback_bluetooth_rx("!")
    def apagar_thread(self):
        self.input_thread.join()

