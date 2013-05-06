import communication_channel, protocol, client, server

factory = communication_channel.CommunicationFactory()
server_channel = factory.build_for("server")
client_channel = factory.build_for("client")
client = client.Client(client_channel)
server = server.Server(server_channel)

server.run()
client_message = "010101"
server_response = client.query(client_message)
print server_response