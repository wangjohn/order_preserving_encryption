import Queue

# Queue that acts as the port between the client and the server, or the server
# and the client.
#
# You can put/get messages from the queue whenever you are ready for them.
class CommunicationQueue:
    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver
        self.messages = Queue.Queue()

    def put(self, message):
        message.message_type._check_valid_message_type()
        self.messages.put(message)

    def get(self):
        self.messages.get()
