import pickle
from server import Server

servers = pickle.load( open("servers.pickle", "rb") )

for server in servers:
    server_up = 0
    for point in server.history:
        if point[1]:
            server_up += 1
    print(f"__________\n{server.name} har en oppetid på {server_up / len(server.history) * 100}%\nTotal historik: {len(server.history)}\n__________\n")