class Server:
    ENC_LEN = 32 # for padding

    '''
    A node in the OPE Tree
    '''
    class OPE_Node:
        def __init__(v):
            value = v
            left = None
            right = None

    '''
    A dumb ML algo that learns something from a message and is able to 
    give recommendations to the server on how to encode a value
    '''
    class MachineLearner:

        # maintains the state
        class State:
            def __init__():
                count = 0

        def __init__():
            state = State()

        # updates state based on message
        def process_message(message):
            state.count += 1 

        # possibilities: NONE, INCREASING, DECREASING, RANDOM
        def get_recommendation():
            if (state.count == 0):
                return "NONE"
            else:
                return "INCREASING"

    def __init__():
        OPE_table = {}
        learner = MachineLearner()

    def receive(message):
        learner.process_message(message)

    def pad(value):
        if (len(value) < ENC_LEN):
            value += "1"
        while (len(value) < ENC_LEN):
            value += "0"
        return value

    def unpad(value):
        r = value.rfind("1")
        return value[:r]

