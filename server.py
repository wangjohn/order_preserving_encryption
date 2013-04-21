class Server:

    '''
    A node in the OPE tree
    '''
    class OPE_Node:
        def __init__(self, v):
            self.value = v
            self.left = None
            self.right = None

    '''
    A dumb ML algo that learns something from a message and is able to 
    give recommendations to the server on how to encode a value
    '''
    class MachineLearner:

        # maintains the state
        class State:
            def __init__(self):
                self.count = 0

        def __init__(self):
            self.state = State()

        # updates state based on message
        def process_message(self, client_message):
            self.state.count += 1 

        # possibilities: NONE, INCREASING, DECREASING, RANDOM
        def get_recommendation(self):
            if (self.state.count == 0):
                return "NONE"
            else:
                return "INCREASING"

    def __init__(self):
        self.ope_table = {} 
        # use fake ope table for now -- instead of storing the OPE path, 
        # we store pointers to the node directly 
        self.fake_ope_table = {} 
        self.root = OPE_Node()
        self.learner = MachineLearner()

    '''
    Server response to a client message.
    '''
    def receive(self, client_message):
        self.learner.process_message(client_message)

        if (client_message.message_type == "move_left"):
            left_child = self.fake_ope_table[client_message.ciphertext]
            return ServerMessage(ciphertext=left_child.ciphertext, client_message=client_message)

        elif (client_message.message_type == "move_right"):
            right_child = self.fake_ope_table[client_message.ciphertext]
            return ServerMessage(ciphertext=right_child.ciphertext, client_message=client_message)

        elif (client_message.message_type == "get_root"):
            return ServerMessage(ciphertext=self.root.ciphertext, client_message=client_message)

        elif (client_message.message_type == "insert"):
            node = self.fake_ope_table[client_message.ciphertext]
            new_node = OPE_Node(client_message.new_ciphertext)
            if (client_message.insert_direction == "left"):
                node.left = new_node
            elif (client_message.insert_direction == "right"):
                node.right = new_node
            self.fake_ope_table[client_message.new_ciphertext] = new_node
            return ServerMessage(ciphertext=new_node.new_ciphertext, client_message=client_message)

        elif (client_message.message_type == "query"):
            # trivial implementation since there is no data associated with a ciphertext besides itself
            return ServerMessage(ciphertext=client_message.ciphertext, client_message=client_message)

    '''
    ENC_LEN = 32 # for padding

    def pad(self, value):
        if (len(value) < ENC_LEN):
            value += "1"
        while (len(value) < ENC_LEN):
            value += "0"
        return value

    def unpad(self, value):
        r = value.rfind("1")
        return value[:r]
    '''
