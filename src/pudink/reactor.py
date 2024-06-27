# from twisted.internet.task import LoopingCall

# DESIRED_FPS = 30.0 # 30 frames per second

# def game_tick():
#    events = pygame.events.get()
#    for event in events:
#       # Process input events
#    redraw()

# # Set up a looping call every 1/30th of a second to run your game tick
# tick = LoopingCall(game_tick)
# tick.start(1.0 / DESIRED_FPS)

# # Set up anything else twisted here, like listening sockets

# reactor.run() # Omit this if this is a tap/tac file


from twisted.internet import endpoints, protocol, reactor


class Echo(protocol.Protocol):
    def dataReceived(self, data):
        self.transport.write(data)


class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()


endpoints.serverFromString(reactor, "tcp:1234").listen(EchoFactory())
reactor.run()
