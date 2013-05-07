from threading import Thread
import time, random
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

NUM_INPUTS = 5
LEN_INPUTS = 4
inputs = []
for i in range(NUM_INPUTS):
    inp = ""
    for j in range(LEN_INPUTS):
        inp += str(int(random.random()*2))
    inputs.append(inp)

#inputs = ["0001"]
print "Program inputs:", inputs

client_thread = Thread(target=client_function, args=(inputs,))
server_thread = Thread(target=server_function)
client_thread.start()
server_thread.start()

