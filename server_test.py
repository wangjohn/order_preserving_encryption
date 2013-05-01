import unittest
import server
import protocol

class TestServer(unittest.TestCase):

	def setUp(self):
		self.s = server.Server()

	#TODO ope table is not being updated
	def test_recieve_root(self):
		root_message = protocol.ClientMessage()
		root_message.insert(None, 5, 'left')
		self.s.receive(root_message)
		self.assertEqual(1, self.s.subtree_size(self.s.root))
		self.assertEqual(root_message.message_type.__repr__(), protocol.MessageType('insert').__repr__())
		self.assertEqual(5, root_message.new_ciphertext)
		self.assertEqual(None, root_message.ciphertext)
		self.assertEqual(self.s.fake_ope_table,{root_message.new_ciphertext: self.s.root})

if __name__ == '__main__':
	unittest.main()