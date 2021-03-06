import uuid

# This is the baseline protocol for communication between the client and the
# server. The MessageProtocol object itself is abstract and should never be
# initialized.
class MessageProtocol:
    def __init__(self):
        self.uuid = uuid.uuid4() # generates a random universally unique ID.

    def __str__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

# Message which the server sends to the client. Must contain a ciphertext.
class ServerMessage(MessageProtocol):
    def __init__(self, ciphertext, client_message):
        MessageProtocol.__init__(self)
        self.ciphertext = ciphertext
        self.client_message = client_message
        self.message_type = MessageType("query")

# Message which the client sends to the server.
#
# Once the +ClientMessage+ has been created, you can configure it to send the
# correct message by calling one of its methods. The following API is allowed:
#
#   move_left
#   move_right
#   get_root
#   insert
#   query
#   None
#
# Once one of these messages is called, the message will be automatically
# configured with the correct +MessageType+
class ClientMessage(MessageProtocol):
    def __init__(self):
        MessageProtocol.__init__(self)
        self.message_type = None
        self.ciphertext = None
        self.new_ciphertext = None
        self.insert_direction = None
        #self.min_ciphertext = None
        #self.max_ciphertext = None

    def move_left(self, ciphertext):
        self.message_type = MessageType("move_left")
        self.ciphertext = ciphertext

    def move_right(self, ciphertext):
        self.message_type = MessageType("move_right")
        self.ciphertext = ciphertext

    def get_root(self):
        self.message_type = MessageType("get_root")

    def insert(self, ciphertext, new_ciphertext, insert_direction):
        self.message_type = MessageType("insert")
        self.ciphertext = ciphertext
        self.new_ciphertext = new_ciphertext
        self.insert_direction = insert_direction
        self._check_insert_direction()

    def query(self, ciphertext):
        self.message_type = MessageType("query")
        self.ciphertext = ciphertext

    def range_query(self, min_ciphertext, max_ciphertext):
        self.message_type = MessageType("range_query")
        self.min_ciphertext = min_ciphertext
        self.max_ciphertext = max_ciphertext

    def _check_insert_direction(self):
        if not (self.insert_direction == 'left' or self.insert_direction == 'right' or self.insert_direction == None):
           raise Exception("'%s' is not a valid insert direction" % self.insert_direction)

# Class that wraps valid message types that are passed from the client to the
# server. It contains a whitelist of valid message types. Checking the type of
# the object is as easy as checking +type+ on the object.
class MessageType:

    def __init__(self, message_type):
        self._message_type = message_type
        self._check_valid_message_type()

    def type(self):
        self._message_type

    def __repr__(self):
        return self._message_type        

    def _check_valid_message_type(self):
        if self._message_type not in ["move_left", "move_right", "get_root", "insert", "query", "range_query"]:
            raise Exception("'%s' is not a valid message type" % message_type)
