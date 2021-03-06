import socket
import ssl
from datetime import datetime
import pickle
import subprocess
import platform
from gmail import email_alert


# Here is where we define our constructor method. Attributes added for support on unix and regular data
class Server():
    def __init__(self, name, port, connection, priority):
        self.name = name
        self.port = port
        self.connection = connection.lower()
        self.priority = priority.lower()
        self.history = []
        self.alert = False

# Defining our check_conneciton
    def check_connection(self):
        msg = ""
        success = False
        now = datetime.now()

# Here we define our test methods. Via our socket, we create a connection to {self.name} with the defined port {self.port} If connection is not established later than 10 seconds, the connection will timeout.
        try:
            if self.connection == "plain":
                socket.create_connection((self.name, self.port), timeout=10)
# If the connection is successfully established, it will print out msg, and tell us the service is running without issues.
                msg = f"{self.name} er online på port {self.port} med {self.connection}"
                success = True
                self.alert = False
# If test value is not set to plain, the use a else if, or elif to run our second part of our code. In this part we check if there is the possibility to create a SSL connection.
# In this instance, due to SSL connections being encrypted, we first need to wrap our connection in a SSL packet, to make sure the responding server will receive and respond to the request.
            elif self.connection == "ssl":
                ssl.wrap_connection(socket.create_connection((self.name, self.port), timeout=10))
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

            if success == False and self.alert == False:
            # Send alert
                self.alert = True
            email_alert(self.name,f"{msg}\n{now}","tron.999@hotmail.com")
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
        servers = pickle.load( open("servers.pickle", "rb") )
    except:
        servers = [
            Server("dette_er_en_test_hjemmeside_der_skal_vise_systemet_virker.dk", 80, "plain", "high"),
            Server("r159.dk", 80, "plain", "high")
        ]
    for server in servers:
        server.check_connection()
        print(len(server.history))
        print(server.history[-1])

    pickle.dump(servers, open("servers.pickle", "wb"))