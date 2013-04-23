# Developed by Roman Arkharov, arkharov@gmail.com. 04.2013

"""
    Instance of this class creates for every connected user by the QuickpongServerFactory().

    This class has methods for send and receive data from remote client (gamer).
"""

from twisted.internet.protocol import Protocol
import time
import simplejson as json
from twisted.python import log

class QuickpongProtocol(Protocol):
    """
      This protocol using for ordinary clients
    """
    def connectionLost(self, reason):
        log.msg('QuickpongProtocol.connectionLost. Connection lost for client %s' % (self.client_id))
        self.factory.quickpong_service.connectionClosedByClient(self.client_id)
        
    def connectionMade(self):
        log.msg('QuickpongProtocol.connectionMade. New connection %s, sending client_id to new client' % (self.client_id,))
        self.data = '[1] init data'

        tmp = []
        
        tmp.append(self.client_id)
        tmp.append(int(time.time()))

        self.writeData(str(tmp))

    def dataReceived(self, raw_data):
        """
            Sometimes, I don't know why, server received two merged data frames from client.
            Here I check if server received several data packets, split them and summarize data
        """
        if '\x00[' in raw_data:
            data = []
            data_array = raw_data.split('\x00')

            first = True
            for data_item in data_array:
                if data_item != '':
                    data_item_array = json.loads(data_item)
                    if isinstance(data_item_array, list):
                        if first:
                            data = data_item_array
                            first = False
                        else:
                            data[0] = data_item_array[0]
                            data[1] += data_item_array[1]
                            #data[1] = data_item_array[1]
                            data[2] = data_item_array[2]
        else:
            data = raw_data.replace('\x00', '')

        if len(data):
            if isinstance(data, list):
                received_data = data
            elif isinstance(data, str):
                received_data = json.loads(data)
            else:
                pass

            #if len(received_data) > 1 and received_data[1] != 0:
            #    log.msg('%d) %d' % (received_data[2], received_data[1]))


            self.factory.quickpong_service.aggregateClientsData(self.client_id, received_data)

    def writeData(self, data):
        self.transport.write(data + '\x00')
