from threading import Thread
import time, random
import communication_channel, protocol, client, server

factory = communication_channel.CommunicationFactory()
server_channel = factory.build_for("server")
client_channel = factory.build_for("client")
client = client.Client(client_channel, dcs=False)
server = server.Server(server_channel)

def client_function(inputs):
    for index, current_input in enumerate(inputs):
        print "\nInserting input %s (%s)" % (current_input, index)
        client.insert_message(current_input)

def server_function():
    while True:
        server.run()

def monitor_queue():
    while True:
        time.sleep(1)
        for element in client_channel._send_queue:
            print element
        #print client_channel._receive_queue

NUM_INPUTS = 50
LEN_INPUTS = 4
inputs = []
for i in range(NUM_INPUTS):
    inp = ""
    for j in range(LEN_INPUTS):
        inp += str(int(random.random()*2))
    inputs.append(inp)

inputs = ['1100', '1001', '0110', '0000', '0101', '0111', '0010', '1001', '1100', '0011', '0110', '1011', '1111', '1111', '0001', '0101', '0111', '1011', '1111', '1110', '0111', '1001', '1101', '0110', '0000', '0001', '0010', '0000', '0000', '1000', '0111', '1011', '1100', '0111', '1001', '0001', '1100', '0000', '1011', '0001', '1100', '1111', '0110', '1000', '0101', '0010', '1110', '1100', '0101', '0011']
print "Program inputs:", inputs

client_thread = Thread(target=client_function, args=(inputs,))
server_thread = Thread(target=server_function)
queue_thread = Thread(target=monitor_queue)

client_thread.start()
server_thread.start()
queue_thread.start()



