# Developed by Roman Arkharov, arkharov@gmail.com. 04.2013

"""
    This version of protocol is called in case if current number of gamers exceeded max_clients limit.

    This class sends to client error message and closes connection.
"""

from twisted.internet.protocol import Protocol

class ErrorQuickpongProtocol(Protocol):
    """
      This protocol using, if too much connection to server
    """
    def connectionMade(self):
        print 'new error connection (too much connections)'
        self.writeData('connection failed, too much connections')
        self.transport.loseConnection()

    def writeData(self, data):
        self.transport.write(data + '\x00')
