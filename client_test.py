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

	# TODO test failing
	def test_query(self):
		self.server.run()
		client_message = 010101
		server_response = self.client.query(client_message)
		self.assertEqual(None, server_response)

if __name__ == '__main__':
	unittest.main()