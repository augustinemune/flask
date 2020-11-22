import socket
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person
#socket.getaddrinfo('localhost', 8080)
#Global constants
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZ = 512


#Global variables
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def broadcast(msg, name):
    """
    send new message to all clients
    :param msg: bytes ("utf8")
    :param name: str
    :return:
    """
    for person in persons:
        client = person.client
        client.send(bytes(name, "utf8") + msg)


def client_communication(person):
    """
    Tread to handle all messages from client
    : param person: person
    : return: None
    """
    client = person.client

    #get persons name
    name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)
    msg = bytes(f"{name} has joined the chat!!", "utf8")
    broadcast(msg, name) #broadcast welcome message
    while True:
        try:
            msg = client.recv(BUFSIZ)


            if msg == bytes("{quit}", "utf8"):
                #client.send(bytes("{quit}", "utf8"))
                client.close()
                persons.remove(person)
                broadcast(f"{name} has left the chat.....", "")
                print(f"[DISCONNECTED] {name} disconnected")
                break
            else:
                broadcast(msg, name + ": ")
                print(f"{name}: ", msg.decode("utf8"))
                
        except Exception as e:
            print("[EXCEPTION]", e)
            break

def wait_for_connection():
    """
    wait for communication from new clients, start new thread once connected
    :param SERVER: socket
    :return: none
    """
    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)
            persons.append(person)
            print(f"[CONNECTED] {addr} connected to the server at {time.time()}")
            Thread(target=client, args=(person)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            run = False

    print("SERVER CRASHED")




if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS) #LISTENING FOR CONNECTION
    print("[STARTED] waiting for connection ...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()










