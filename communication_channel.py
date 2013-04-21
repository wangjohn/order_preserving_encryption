import Queue

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
