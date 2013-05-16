# Developed by Roman Arkharov, arkharov@gmail.com. 04.2013

"""
    This file is a test client for Quickpong server. Main client is written on ActionScript 3.0 for
    humans gamers.

    The goal of this client is a performance test of Quickpong server. This client emulates actions of
    main AS client.

    Don't forget to set correct value for max_clients variable.
    If set 1 and no other users online, then you can play game against the simple AI :))
"""


from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet.task import LoopingCall

import simplejson as json

host = 'kece.ru'
port = 10080
max_clients = 500
#max_clients = 1


class QuickpongTestClient():
    def __init__(self):
        print 'QuickpongTestClient init'

    def init_client(self, client, addr):
        # client is an instance of class QuickpongTestProtocol()
        client.port = addr.port
        client.host = addr.host
        client.type = addr.type
        client.addr = addr
        client.data = []
        client.status = 'waiting'
        client.position = ''  # left or right board
        client.frame = 0

        self.client = client
        print 'added client %s' % (addr)

    def work_with_server(self):
        ball_y_id = 2

        if self.client.position == 'left':
            board_y_id = 7
        else:
            board_y_id = 8

        if self.data[board_y_id] + 50 > self.data[ball_y_id]:
            delta_y = -20
        else:
            delta_y = 20


        data_for_send = [self.client.position, delta_y, self.client.frame]
        #print data_for_send
        self.client.writeData(data_for_send)
        self.client.frame += 1

    def on_data_received(self, raw_data):
        local_data = raw_data.replace('\x00', '')

        if 'Your game is stopped' in local_data:
            local_data = 'Your game is stopped'
        elif '][' in local_data:
            # Take last item if received several items in one data packet
            local_data = local_data.replace('][', ']+++[')
            local_data = local_data.split('+++')
            local_data = local_data[len(local_data) - 1]

        if self.client.status == 'waiting' and local_data != 'prestart':
            self.client.client_id = local_data
            print 'client_id %s' % (local_data,)
        elif self.client.status == 'waiting' and local_data == 'prestart':
            self.client.status = 'ready'
            self.client.writeData(['ready'])
        elif self.client.status == 'ready':
            self.client.status = 'working'
            self.data = json.loads(local_data)
            if self.data[0] == 'start-1':
                self.client.position = 'left'
            else:
                self.client.position = 'right'

            self.lc = LoopingCall(self.work_with_server)
            self.lc.start(0.2)
        elif self.client.status == 'working' and local_data != 'Your game is stopped':
            #print local_data
            self.data = json.loads(local_data)
        elif self.client.status == 'working' and local_data == 'Your game is stopped':
            print 'client %s disabled' % (self.client.client_id)
            # recreate tester
            del self
            reactor.connectTCP(host, port, QuickpongTestClientFactory())
        else:
            # here client receives from server data array with ball and boards coordinates
            pass
            #print 'unhandled data %s, current status %s' % (data, self.client.status)


class QuickpongTestProtocol(Protocol):
    """
        Object of this class is an item of dictionary clients in QuickpongTestClient()
    """
    def dataReceived(self, data):
        self.test_client.on_data_received(data)

    def writeData(self, data):
        self.transport.write(json.dumps(data))


class QuickpongTestClientFactory(ClientFactory):
    protocol = QuickpongTestProtocol

    def buildProtocol(self, addr):
        print 'Test client %s connected to server.' % (addr,)

        p = self.protocol()
        p.test_client = QuickpongTestClient()
        p.test_client.init_client(p, addr)

        return p

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason


# Run QuickpongTestClientFactory() N times. This factory creates N instances of class QuickpongTestProtocol()
# with name "protocol" and  attaches instance of QuickpongTestClient() to protocol object
#
# Every instance of QuickpongTestClient() emulates user actions: receives data from server, process it and send
# responses to server. Data sends to server evey 0,2 seconds through the LoopingCall.
for i in range(0, max_clients):
    reactor.connectTCP(host, port, QuickpongTestClientFactory())

reactor.run()
