from twisted.internet import protocol


import random
import string


class PudinkClient(protocol.Protocol):
    def generate_random_name(self):
        length = random.randint(5, 10)
        name = "".join(random.choices(string.ascii_lowercase, k=length))
        return name

    def connectionMade(self):
        random_name = self.generate_random_name()
        self.transport.write(random_name.encode())

    def dataReceived(self, data):
        print("Server said:", data)

    def connectionLost(self, reason):
        print("connection lost")

    def sendMessage(self, msg):
        self.transport.write(msg.encode())
