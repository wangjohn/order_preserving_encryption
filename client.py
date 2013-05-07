import encryption, protocol, random, dcs_preprocessing

class Client:
    def __init__(self, communication_channel, dcs=False):
        self.encryption_scheme = encryption.BasicEncryptionScheme()
        self.key = self.encryption_scheme.generate_key()
        self.communication_channel = communication_channel
        if dcs:
            self.dcs_scheme = dcs_preprocessing.DistributionConfidentialityScheme()
        else:
            self.dcs_scheme = False

    def query(self, message):
        if self.dcs_scheme:
            message = self.dcs_scheme.encrypt(message)
        ciphertext = self.encryption_scheme.encrypt(self.key, message)
        client_message = protocol.ClientMessage()
        client_message.query(ciphertext)
        return self._send_client_message(client_message)

    def range_query(self, min_message, max_message):
        if self.dcs_scheme:
            min_message = self.dcs_scheme.encrypt_min(min_message)
            max_message = self.dcs_scheme.encrypt_min(max_message)
        min_ciphertext = self.encryption_scheme.encrypt(self.key, min_message)
        max_ciphertext = self.encryption_scheme.encrypt(self.key, max_message)
        client_message = protocol.ClientMessage()
        client_message.range_query(ciphertext)
        return self._send_client_message(client_message)

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
                    return self._insert(None, original_ciphertext, None)
                else:
                    # Insert the original ciphertext, using the previous
                    # ciphertext and direction.
                    return self._insert(previous_ciphertext[0], original_ciphertext, previous_ciphertext[1])

            elif message < current_ciphertext:
                # Move left
                previous_ciphertext = (current_ciphertext, "left")
                current_ciphertext = self._move_left(current_ciphertext)

            elif message > current_ciphertext:
                # Move right
                previous_ciphertext = (current_ciphertext, "right")
                current_ciphertext = self._move_right(current_ciphertext)

            else:
                # Randomly choose which side to insert on, unless dcs is enabled
                if self.dcs_scheme:
                    return self._insert(current_ciphertext, original_ciphertext, "left")
                else:
                    if random.random() > .5:
                        return self._insert(current_ciphertext, original_ciphertext, "left")
                    else:
                        return self._insert(current_ciphertext, original_ciphertext, "right")


    def _get_root(self):
        client_message = protocol.ClientMessage()
        client_message.get_root()
        return self._send_client_message(client_message)

    def _move_left(self, ciphertext):
        if self.dcs_scheme:
            ciphertext = self.dcs_scheme.encrypt(ciphertext)
        client_message = protocol.ClientMessage()
        client_message.move_left(ciphertext)
        return self._send_client_message(client_message)

    def _move_right(self, ciphertext):
        if self.dcs_scheme:
            ciphertext = self.dcs_scheme.encrypt(ciphertext)
        client_message = protocol.ClientMessage()
        client_message.move_right(ciphertext)
        return self._send_client_message(client_message)

    def _insert(self, current_ciphertext, new_ciphertext, direction):
        if self.dcs_scheme:
            current_ciphertext = self.dcs_scheme.encrypt(current_ciphertext)
            new_ciphertext = self.dcs_scheme.encrypt(new_ciphertext)
        print "Client insert, current_ciphertext="+str(current_ciphertext)+", new_ciphertext:"+str(new_ciphertext)+", direction:"+str(direction)
        client_message = protocol.ClientMessage()
        client_message.insert(current_ciphertext, new_ciphertext, direction)
        return self._send_client_message(client_message)

    # Communicate with the server and get back the +ciphertext+ that the
    # server responds with
    def _send_client_message(self, client_message):
        self.communication_channel.put(client_message)
        server_message = self.communication_channel.get()
        root_ciphertext = server_message.ciphertext
        decrypted_text = self.encryption_scheme.decrypt(self.key, root_ciphertext)
        if self.dcs_scheme:
            decrypted_text = self.dcs_scheme.decrypt(decrypted_text)
        return decrypted_text
