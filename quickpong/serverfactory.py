# Developed by Roman Arkharov, arkharov@gmail.com. 04.2013

"""
    This factory runs on kece.ru:10080 (by default) and creates QuickpongProtocol() instances for every
    connected users. If number of connected users reach the value max_clients then this factory creates instance
    of ErrorQuickpongProtocol() for new users.

    Also this class, on own initialization, creates instance of the class Quickpong which is a game main loop.

    See method buildProtocol() in current class and method initClient() in class Quickpong().
"""
from twisted.internet.protocol import ServerFactory

from protocol import QuickpongProtocol
from quickpong import Quickpong
from errorprotocol import ErrorQuickpongProtocol

from twisted.python import log


class QuickpongServerFactory(ServerFactory):
    """
      Quickpong server factory. Process incoming client requests
      
      Protocol logic:
      
      1. user press "connect" button in client-application and connecting to server
      2. server creates new connection (method self.buildProtocol create object client) and set this client to wating list (in client user see message: 'connecting...')
      3. server send to client his client_id (in client user see message: 'waiting opponent...')
      4. when two users connect to server method self.checkWaitingList (which calling by LoopingCall) create new game and remove client from wating list
      5. method self.sendPrestartMessage send message 'prestart' to both gamers. Client-application show button "start"
      6. when user click "start" button, then client-application send message 'ready' to server. Client showing to user message 'waiting second player'
      7. when server receive 'ready' message from both client its send 'start' message ti clients.
      8. Client s start sending data to server and server start send data to clients
    """

    protocol = QuickpongProtocol

    def __init__(self, max_clients, service):
        """
          Quickpong server factory constructor
        """
        log.msg('Quickpong server initialized')
        
        # parameters
        self.quickpong_service = Quickpong(max_clients)
        self.service = service

    def buildProtocol(self, addr):
        """
          This method is calling when new client connected
          
          Clone of method buildProtocol from class Factory (protocol.py)
          
          create new protocol QuickpongProtocol if clients < max_clients
          OR
          send error to client, if clients >= max_clients
        """
        if len(self.quickpong_service.clients) < self.quickpong_service.max_clients:
            p = self.protocol()
            p.factory = self

            p = self.quickpong_service.initClient(p, addr)
            
            log.msg('class QuickpongServerFactory, method buildProtocol: protocol was built')

            return p
        else:
            """
              If count of gamers more then self.max_clients then close connections for all new clients
            """
            p = ErrorQuickpongProtocol()
            p.factory = self
            return p