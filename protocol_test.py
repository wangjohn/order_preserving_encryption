import unittest, protocol, encryption

class TestProtocol(unittest.TestCase):

	def setUp(self):
		self.encryption_scheme = encryption.BasicEncryptionScheme()
		self.key = self.encryption_scheme.generate_key()
		self.message = 1010101

	''' Creates all possible message types and assert that the 
	type is correct
	'''
	def test_move_left(self):
		ciphertext = self.encryption_scheme.encrypt(self.key, self.message)
		client_message = protocol.ClientMessage()
		client_message.move_left(ciphertext)
		#TODO protocol.ClientMessage().move_left(ciphertext) doesn't work
		self.assertIsInstance(client_message, protocol.ClientMessage)
		self.assertEqual(client_message.message_type.__repr__(), protocol.MessageType("move_left").__repr__())

	def test_move_right(self):
		ciphertext = self.encryption_scheme.encrypt(self.key, self.message)
		client_message = protocol.ClientMessage()
		client_message.move_right(ciphertext)
		self.assertIsInstance(client_message, protocol.ClientMessage)
		self.assertEqual(client_message.message_type.__repr__(), protocol.MessageType("move_right").__repr__())

	def test_get_root(self):
		client_message = protocol.ClientMessage()
		client_message.get_root()
		self.assertIsInstance(client_message, protocol.ClientMessage)
		self.assertEqual(client_message.message_type.__repr__(), protocol.MessageType("get_root").__repr__())

	def test_insert(self):
		ciphertext = self.encryption_scheme.encrypt(self.key, self.message)
		client_message = protocol.ClientMessage()
		client_message.insert(ciphertext, None, "left")
		self.assertIsInstance(client_message, protocol.ClientMessage)
		self.assertIsNone(client_message.new_ciphertext)
		self.assertEqual(client_message.insert_direction, "left")
		self.assertEqual(client_message.message_type.__repr__(), protocol.MessageType("insert").__repr__())

	def test_query(self):
		ciphertext = self.encryption_scheme.encrypt(self.key, self.message)
		client_message = protocol.ClientMessage()
		client_message.query(ciphertext)
		self.assertIsInstance(client_message, protocol.ClientMessage)
		self.assertEqual(client_message.message_type.__repr__(), protocol.MessageType("query").__repr__())

if __name__ == '__main__':
	unittest.main()