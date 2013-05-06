from threading import Thread
import time
import communication_channel, protocol, client, server

factory = communication_channel.CommunicationFactory()
server_channel = factory.build_for("server")
client_channel = factory.build_for("client")
client = client.Client(client_channel)
server = server.Server(server_channel)

print "initialized"

def client_function(inputs):
    while True:
        print "looping client function"
        if (inputs):
            print "sending", inputs[0], "to server"
            client.insert_message(inputs[0])
            inputs = inputs[1:]

def server_function():
    while True:
        print "looping server function"
        print server.communication_channel._send_queue.qsize()
        print server.communication_channel._receive_queue.qsize()
        server.run()


inputs = ["0001", "0010", "0100", "1000"]

client_thread = Thread(target=client_function, args=(inputs,))
server_thread = Thread(target=server_function)
client_thread.start()
server_thread.start()

