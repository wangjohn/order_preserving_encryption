import unittest, client, communication_channel, protocol, server

class TestClient(unittest.TestCase):

	def setUp(self):
		factory = communication_channel.CommunicationFactory()
		self.server_channel = factory.build_for("server")
		self.client_channel = factory.build_for("client")
		self.client = client.Client(self.client_channel)
		self.server = server.Server(self.server_channel)

	def test_initialization(self):
		self.assertEqual(self.client_channel, self.client.communication_channel)
		self.assertEqual(self.server_channel, self.server.communication_channel)

	def root_test(self):
		message = self.client._get_root()
		test_message = protocol.ClientMessage()
		test_message.get_root()
		self.assertEqual(message, test_message)

	def right_test(self):
		message = self.client._move_right(10)
		test_message = protocol.ClientMessage()
		test_message._move_right(10)
		self.assertEqual(message, test_message)

	def left_test(self):
		message = self.client._move_left(10)
		test_message = protocol.ClientMessage()
		test_message.move_left(10)
		self.assertEqual(message, test_message)

	def insert_test(self):
		message = self.client._insert(1, 10, 'left')
		test_message = protocol.ClientMessage()
		test_message.insert(1, 10, 'left')
		self.assertEqual(message, test_message)

	# TODO test failing
	# def test_query(self):
	# 	self.server.run()
	# 	client_message = 010101
	# 	server_response = self.client.query(client_message)
	# 	self.assertEqual(None, server_response)

if __name__ == '__main__':
	unittest.main()