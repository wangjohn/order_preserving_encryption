from threading import Thread
import time
import communication_channel, protocol, client, server

factory = communication_channel.CommunicationFactory()
server_channel = factory.build_for("server")
client_channel = factory.build_for("client")
client = client.Client(client_channel)
server = server.Server(server_channel)

def client_function(inputs):
    for current_input in inputs:
        print "Inserting input %s" % current_input
        client.insert_message(current_input)

def server_function():
    while True:
        server.run()


inputs = ["0001", "0010", "0100", "1000"]

client_thread = Thread(target=client_function, args=(inputs,))
server_thread = Thread(target=server_function)
client_thread.start()
server_thread.start()

