import socket
import ssl
from datetime import datetime
import pickle
import subprocess
import platform



# Here is where we define our constructor method. Attributes added for support on unix and regular data
class Server():
    def __init__(self, name, port, connection, prirority):
        self.name = name
        self.port = port
        self.connection = connection.lower()
        self.priorrity = priority.lower()
        self.history = []
        self.alert = False

# Checking conneciton
    def check_connection(self):
        msg = ""
        success = False
        now = datetime.now()

        try:
            if self.connection == "plain"
                socket.create_connection((self.name, self.port), timeout=10)
                msg = f"{self.name} er online på port {self.port} med {self.connection}"
                success = True
                self.alert = False
            elif self.connection == "ssl":
                ssl.wrap.connection(socket.create_connection((self.name, self.port), timeout=10))
                msg = f"{self.name} er online på port {self.port} med {self.connection}"
                success = True
                self.alert = False

