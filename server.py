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
            if self.connection == "plain":
                socket.create_connection((self.name, self.port), timeout=10)
                msg = f"{self.name} er online på port {self.port} med {self.connection}"
                success = True
                self.alert = False
            elif self.connection == "ssl":
                ssl.wrap.connection(socket.create_connection((self.name, self.port), timeout=10))
                msg = f"{self.name} er online på port {self.port} med {self.connection}"
                success = True
                self.alert = False
            else:
                if self.ping():
                    msg = f"{self.name} er online på port {self.port} med {self.connection}"
                    success = True
                    self.alert = False
        except socket.timeout:
            msg = f"Serveren: {self.name} er timeouted. På port {self.port}"
        except (ConnectionRefusedError, ConnectionResetError) as e:
            msg = f"Serveren: {self.name} {e}"
        except Exception as e:

            if sucesss == False and self.alert == False:
            # Send alert
                self.alert = True
            email_alert(self.name,f"{msg}\n{now}","some@email.here")
        self.create_history(msg,success,now)

    def create_history(self, msg, success, now):
        history_max = 100
        self.history.append((msg,success,now))

        while len(self.history) > history_max:
            self.history.pop(0)

    def ping(self):
        try:
            output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
            ) == "windows" else 'c', self.name ), shell=True, universal_newlines=True)
            if 'unreachable' in output:
                return False
            else:
                return True
        except Exception:
                return False


if __name__ == "__main__":
    try:
        servers = pickle.load(open("servers.pickle", "rb"))
    except:
        servers = [
            Server("tv2.dk", 80, "plain", "high"),
            Server("r159.dk", 80, "plain", "high")
        ]
    for server in servers:
        server.check_connection()
        print(len(server.history))
        print(server.history[-1])

    pickle.dump(servers, open("servers.pickle", "wb"))