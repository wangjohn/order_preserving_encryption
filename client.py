import encryption
import protocol

class Client:
    def __init__(self, communication_channel):
        self.encryption_scheme = encyption.BasicEncryptionScheme()
        self.key = self.encryption_scheme.generate_key()
        self.communication_channel = communication_channel

    # Stores a plaintext message +message+ in the database by communicating and
    # interacting with the server. The plaintext will be encrypted into a
    # ciphertext, and this ciphertext will be stored at the server in an order
    # preserving manner.
    def insert_message(self, message):
        original_ciphertext = self.encryption_scheme.encrypt(self.key, message)
        previous_ciphertext = None
        current_ciphertext = self._get_root()

        # Move down the binary search tree, moving right, left, and inserting
        # as appropriate.
        while True:
            if current_ciphertext == None:
                if previous_ciphertext == None:
                    # Create a new root since there was no previous root.
                    return self._insert(None, current_ciphertext, None)
                else:
                    # Insert the original ciphertext, using the previous
                    # ciphertext and direction.
                    return self._insert(previous_ciphertext[0], original_ciphertext, previous_ciphertext[1])
            elif message < current_ciphertext:
                previous_ciphertext = (current_ciphertext, "left")
                current_ciphertext = self._move_left(current_ciphertext)
            elif message > current_ciphertext:
                previous_ciphertext = (current_ciphertext, "right")
                current_ciphertext = self._move_right(current_ciphertext)
            else:
                # Arbitrarily choose to insert in the right direction since the
                # node values are actually the same.
                return self._insert(current_node, original_ciphertext, "right")


    def _get_root(self):
        client_message = protocol.ClientMessage().get_root()
        self._send_client_message(client_message)

    def _move_left(self, ciphertext):
        client_message = protocol.ClientMessage().move_left(ciphertext)
        self._send_client_message(client_message)

    def _move_right(self, ciphertext):
        client_message = protocol.ClientMessage().move_right(ciphertext)
        self._send_client_message(client_message)

    def _insert(self, current_ciphertext, new_ciphertext, direction):
        client_message = protocol.ClientMessage().insert(current_ciphertext, new_ciphertext, direction)
        self._send_client_message(client_message)

    # Communicate with the server and get back the +ciphertext+ that the
    # server responds with
    def _send_client_message(self, client_message):
        self.communication_channel.put(client_message)
        server_message = self.communication_channel.get(client_message.uuid)
        root_ciphertext = server_message.ciphertext

        return self.encryption_scheme.decrypt(self.key, root_ciphertext)

