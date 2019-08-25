import socket

import threading
from multiprocessing import Queue

from functools import partial


print = partial(print, flush=True)

class PibbleJoystick:
    def __init__(self, brain, params=None):
        self.brain = brain
        self.inited = False

        self.running = False

        if params:
            self.params = params
        else:
            self.params = {
                'joystick_host' : '0.0.0.0',
                'joystick_port' : '42666'
            }

        self.listenning_socket = None

        self.connection_lock = threading.Lock()
        self.connection_socket = None
        self.connection_infos = None

        self.manager_thread = None
        self.connection_thread = None

    def init(self):
        if not self.brain.inited:
            self.inited = False
            self.running = False
            return False
        else:
            try:
                self.listenning_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.listenning_socket.bind((self.params["joystick_host"], self.params["joystick_port"]))
                self.listenning_socket.listen(1)

                self.running = True
                self.manager_thread = threading.Thread(target=self.connectionManager, daemon=True)
                self.manager_thread.start()
                return True
            except(Exception) as err:
                print(err)
                self.inited = False
                return {"error" : str(err)}


    def connectionManager(self):
        if self.inited:
            try:
                while self.running:
                    conn, addr = self.listenning_socket.accept()
                    if self.connection_infos == None and self.connection_socket == None:
                        self.connection_lock.acquire()
                        self.connection_socket = conn
                        self.connection_infos = {"ip" : addr[0], "port" : addr[1]}
                        self.connection_thread = threading.Thread(target=self.listener, daemon=True)
                        self.connection_thread.start()
                        self.connection_lock.release()
                    else:
                        conn.close()
            except(Exception) as err:
                print(err)
                return {"error" : str(err)}
        else:
            return {"inited" : False}

    def listener(self):
        if self.inited:
            try:
                while self.running:
                    if self.connection_socket != None:
                        try:
                            msg = self.connection_socket.recv().decode('utf-8')
                            print(msg)
                        except(ConnectionError) as err:
                            self.closeConnection()
            except(Exception) as err:
                print(err)
                return {"error" : str(err)}
        else:
            return {"inited" : False}

    def closeConnection(self):
        self.connection_lock.acquire()
        self.connection_socket.close()
        self.connection_socket = None
        self.connection_infos = None
        self.connection_lock.release()