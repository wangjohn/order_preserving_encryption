import Queue

# A class for building a communication channel. This class will output a channel
# for the server and the client. This should be used like so:
#
#  factory = CommunicationFactory()
#
#  # server should get the server_channel
#  server_channel = factory.build_for("server")
#
#  # client should get the client_channel
#  client_channel = factory.build_for("client")
#
# The channels that you receive will be of type +CommunicationChannel+.
class CommunicationFactory:
    def __init__(self):
        self.client_to_server = Queue.Queue()
        self.server_to_client = Queue.Queue()

    def build_for(self, build_type):
        if build_type == "client":
            return CommunicationChannel(self.client_to_server, self.server_to_client)
        elif build_type == "server":
            return CommunicationChannel(self.server_to_client, self.client_to_server)
        else:
            raise Exception("Cannot build communication channel for %s." % build_type)

# Queue that acts as the port between the client and the server, or the server
# and the client.
#
# You can put/get messages from the queue whenever you are ready for them.
class CommunicationChannel:
    def __init__(self, send_queue, receive_queue):
        self._send_queue = send_queue
        self._receive_queue = receive_queue

    def put(self, message):
        message.message_type._check_valid_message_type()
        self._send_queue.put(message)

    def get(self):
        self._receive_queue.get()
