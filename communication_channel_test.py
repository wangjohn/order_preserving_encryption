import unittest, communication_channel, protocol

class TestProtocol(unittest.TestCase):

	def setUp(self):
		self.factory = communication_channel.CommunicationFactory()
		self.server_channel = self.factory.build_for("server")
		self.client_channel = self.factory.build_for("client")
		#self.client = client.Client(self.client_channel)
		self.client_message = protocol.ClientMessage()
		self.client_message.get_root()

	# def test_put(self):
	# 	self.channel.put(self.client_message)
		# self.assertEqual(self.channel._send_queue.get(), self.client_message)

	# TODO this test is failing
	# def test_get(self):
	# 	self.client_channel.put(self.client_message)
	# 	message = self.client_channel.get()
	# 	self.assertEqual(message, self.client_message)		

if __name__ == '__main__':
	unittest.main()