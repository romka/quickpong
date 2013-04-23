# Developed by Roman Arkharov, arkharov@gmail.com. 04.2013

"""
    Instance of this class sends policy xml-file to flash-client. This protocol doesn't used in
    python test-client (quickpong_test_client.py) and also it is no necessary, for example, for
    htnl5 client (if it will be created some day).
"""
from twisted.internet.protocol import Protocol
from twisted.python import log

class SendPolicyProtocol(Protocol):
    def connectionMade(self):
        """
          This methos send domain policy to client. Its nececary for flash-client
          
          TODO: move var policy to external file crossdomain.xml
        """
        log.msg('SendPolicyProtocol. Policy was sent to client')
        policy = "<cross-domain-policy><allow-access-from domain='*' to-ports='*' /></cross-domain-policy>"
        self.transport.write(policy + '\x00')
        #self.transport.loseConnection()