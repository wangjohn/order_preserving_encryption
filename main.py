from threading import Thread
import time, random
import communication_channel, protocol, client, server

factory = communication_channel.CommunicationFactory()
server_channel = factory.build_for("server")
client_channel = factory.build_for("client")
client = client.Client(client_channel, dcs=True)
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

NUM_INPUTS = 200
REPEAT_INPUTS = 0
LEN_INPUTS = 10 # assuming negligible repeats

inputs = []
#random inputs
for i in range(NUM_INPUTS - REPEAT_INPUTS):
    inp = ""
    for j in range(LEN_INPUTS):
        inp += str(int(random.random()*2))
    inputs.append(inp)

#repeat inputs
for j in range(LEN_INPUTS):
    inp += str(int(random.random()*2))
for i in range(REPEAT_INPUTS):
    inputs.append(inp)

random.shuffle(inputs)

print "Program inputs:", inputs

client_thread = Thread(target=client_function, args=(inputs,))
server_thread = Thread(target=server_function)
queue_thread = Thread(target=monitor_queue)

client_thread.start()
server_thread.start()
#queue_thread.start()



