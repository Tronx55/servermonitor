import pickle
from server import Server


print("Tilføj din server")

servername = input("Indtast server adresse")
port = int(input("Indtast portnummer som en integer"))
connection = input("Indtast målingsværdi ping/plain/ssl")
priority = input("Indtast priority high/low")

new_server = Server(servername, port, connection, priority)
servers.append(new_server)

pickle.dump(servers, open("servers.pickle", "wb" ))