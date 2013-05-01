import protocol

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

        def __init__(self):
            self.count = 0

        # updates state based on message
        def process_message(self, client_message):
            self.count += 1 

        # possibilities: NONE, INCREASING, DECREASING, RANDOM
        def get_recommendation(self):
            if (self.count == 0):
                return "NONE"
            else:
                return "INCREASING"

    def __init__(self):
        self.ope_table = {} 
        # use fake ope table for now -- instead of storing the OPE path, 
        # we store pointers to the node directly 
        self.fake_ope_table = {} 
        self.root = Server.OPE_Node(None)
        self.learner = Server.MachineLearner()

    '''
    Server response to a client message.
    '''
    def receive(self, client_message):
        self.learner.process_message(client_message)

        if (client_message.message_type == protocol.MessageType("move_left")):
            left_child = self.fake_ope_table[client_message.ciphertext].left
            if left_child:
                return ServerMessage(ciphertext=left_child.ciphertext, client_message=client_message)
            else:
                return ServerMessage(ciphertext=None, client_message=client_message)

        elif (client_message.message_type == protocol.MessageType("move_right")):
            right_child = self.fake_ope_table[client_message.ciphertext].right
            if right_child:
                return ServerMessage(ciphertext=right_child.ciphertext, client_message=client_message)
            else:
                return ServerMessage(ciphertext=None, client_message=client_message)

        elif (client_message.message_type == protocol.MessageType("get_root")):
            if not self.root:
                return ServerMessage(ciphertext=None, client_message=client_message)
            return ServerMessage(ciphertext=self.root.ciphertext, client_message=client_message)

        elif (client_message.message_type == protocol.MessageType("insert")):
            new_node = OPE_Node(client_message.new_ciphertext)
            # root case
            if client_message.ciphertext == None:
                self.root = new_node
                self.fake_ope_table[client_message.new_ciphertext] = self.root
            else:
                node = self.fake_ope_table[client_message.ciphertext]
                new_node.parent = node
                if (client_message.insert_direction == "left"):
                    node.left = new_node
                elif (client_message.insert_direction == "right"):
                    node.right = new_node
                self.fake_ope_table[client_message.new_ciphertext] = new_node
                # AVL rebalance
                while (node.parent != None):
                    self.rebalance(node.parent)
                    node = node.parent 
            return ServerMessage(ciphertext=new_node.new_ciphertext, client_message=client_message)

        elif (client_message.message_type == protocol.MessageType("query")):
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

    def subtree_size(self, node):
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return 1
        elif node.left is None:
            return 1 + self.subtree_size(node.right)
        elif node.right is None:
            return 1 + self.subtree_size(node.left)
        else:
            return 1 + sum[self.subtree_size(node.left), self.subtree_size(node.right)] 

    def counter(fn):
        def wrapper(*args, **kwargs):
            for arg in args:
                subtree_sizes += [subtree_size(node)]
            return fn(*args, **kwargs)
        wrapper.subtree_sizes = []
        wrapper.__name__ = fn.__name__
        return wrapper

    def height(self,node):
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return 1
        elif node.left is None:
            return 1 + self.height(node.right)
        elif node.right is None:
            return 1 + self.height(node.left)
        else:
            return 1 + max(self.height(node.left), self.height(node.right))

    def balance_factor(self, node):
        return self.height(node.left) - self.height(node.right)

    def left_rotate(self, node):
        A = node
        B = node.right
        B.parent = A.parent
        A.parent = B
        A.right = B.left
        B.left = A

    def right_rotate(self, node):
        A = node
        B = node.left
        B.parent = A.parent
        A.parent = B
        A.left = B.right
        B.right = A

    '''
    rebalance.heights will return the subtree_sizes of every rebalance,
    allowing us to figure out the speed of our insertion procedure.
    len(rebalance.heights) is the number of rebalances.
    '''
    @counter 
    def rebalance(self, node):
        if self.balance_factor(node) == -2:
            if self.balance_factor(node.right) == -1: # right-right case
                self.left_rotate(node)
            elif self.balance_factor(node.right) == 1: # right-left case
                self.right_rotate(node.right)
                self.left_rotate(node)
        elif self.balance_factor(node) == 2:
            if self.balance_factor(node.left) == 1: # left-left case
                self.right_rotate(node)
            elif self.balance_factor(node.left) == -1: # left-right case
                self.left_rotate(node.left)
                self.right_rotate(node)







