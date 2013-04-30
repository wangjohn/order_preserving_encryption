class Server:

    '''
    A node in the OPE tree
    '''
    class OPE_Node:
        def __init__(self, v):
            self.value = v
            self.left = None
            self.right = None
            self.count = 1
            self.parent = None

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
            left_child = self.fake_ope_table[client_message.ciphertext].left
            if left_child:
                return ServerMessage(ciphertext=left_child.ciphertext, client_message=client_message)
            else:
                return ServerMessage(ciphertext=None, client_message=client_message)

        elif (client_message.message_type == "move_right"):
            right_child = self.fake_ope_table[client_message.ciphertext].right
            if right_child:
                return ServerMessage(ciphertext=right_child.ciphertext, client_message=client_message)
            else:
                return ServerMessage(ciphertext=None, client_message=client_message)

        elif (client_message.message_type == "get_root"):
            if not self.root:
                return ServerMessage(ciphertext=None, client_message=client_message)
            return ServerMessage(ciphertext=self.root.ciphertext, client_message=client_message)

        elif (client_message.message_type == "insert"):
            new_node = OPE_Node(client_message.new_ciphertext)
            # root case
            if client_message.ciphertext == None:
                root = new_node
                self.fake_ope_table[client_message.new_ciphertext] = root
            else:
                node = self.fake_ope_table[client_message.ciphertext]
                new_node.parent = node
                if (client_message.insert_direction == "left"):
                    node.left = new_node
                elif (client_message.insert_direction == "right"):
                    node.right = new_node
                self.fake_ope_table[client_message.new_ciphertext] = new_node
            # AVL rebalance
            while (node.parent != None)
                rebalance(node.parent)
                node = node.parent 
            return ServerMessage(ciphertext=new_node.new_ciphertext, client_message=client_message)

        elif (client_message.message_type == "query"):
            # trivial implementation since there is no data associated with a ciphertext besides itself
            return ServerMessage(ciphertext=client_message.ciphertext, client_message=client_message)

    '''
    These functions handle a rebalance of the tree upon insertion of a node. 
    In our implementation, because we use a fake_ope_table with pointers to 
    the nodes, this procedure doesn't take very long. However, in CryptDB, 
    this procedure is the very time-consuming.

    Specifically, we count two things: 1) the number of rebalance operations
    and 2) the subtree size at each rebalanced node. This is because in CryptDB,
    the time taken for each rebalance is proportional to the height of the subtree
    rooted at that node.
    '''
    def height(node):
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return 1
        elif node.left is None:
            return 1 + height(node.right)
        elif node.right is None:
            return 1 + height(node.left)
        else:
            return 1 + max(height(node.left), height(node.right))

    def balance_factor(node):
        return height(node.left) - height(node.right)

    def left_rotate(node):
        A = node
        B = node.right
        B.parent = A.parent
        A.parent = B
        A.right = B.left
        B.left = A

    def right_rotate(node):
        A = node
        B = node.left
        B.parent = A.parent
        A.parent = B
        A.left = B.right
        B.right = A

    def rebalance(node):
        if balance_factor(node) == -2:
            if balance_factor(node.right) == -1: # right-right case
                left_rotate(node)
            elif balance_factor(node.right) == 1: # right-left case
                right_rotate(node.right)
                left_rotate(node)
        elif balance_factor(node) == 2:
            if balance_factor(node.left) == 1: # left-left case
                right_rotate(node)
            elif balance_factor(node.left) == -1: # left-right case
                left_rotate(node.left)
                right_rotate(node)







