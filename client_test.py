import unittest
import client
import communication_channel

class TestClient(unittest.TestCase):

	def setUp(self):
		self.factory = CommunicationFactory()
		self.server_channel = factory.build_for("server")
		self.client_channel = factory.build_for("client")
		self.communication_channel = CommunicationChannel(server_channel,client_channel)
		self.client = Client(self.communication_channel)

	def test(self):
		self.assertEqual(1,1)

if __name__ == '__main__':
	unittest.main()