# Developed by Roman Arkharov, arkharov@gmail.com. 04.2013

"""
    This is a "main loop" of the game. It is created on QuickpongServerFactory() start and has
    several LoopingCall's which prepare and send data to clients (gamers).
"""

import simplejson as json
from quickponggame import QuickpongGame
import time
from twisted.python import log

class Quickpong:
    """
      Main game class.
    """
    def __init__(self, max_clients):
        self.clients = {}
        self.max_clients = max_clients

        """
            Two debug variables
        """
        self.debug_counter = 0
        self.debug_max_counter = 30

        """
          Game is a block, which contains two clients. This clients sends data to each other.
        """
        self.games = {}
        self.clients_waiting_list = []

        from twisted.internet import reactor
        from twisted.internet.task import LoopingCall

        """
          Prepare data to clients in active games.
        """
        self.lc = LoopingCall(self.prepareDataToClients)
        #self.lc.start(.1)
        self.lc.start(.05)

        """
          Send data to clients in active games.
        """
        self.lc = LoopingCall(self.sendDataToClients)
        #self.lc.start(.1)
        self.lc.start(.05)

        """
          Check wating list, Create a new game if two not active clients exists
        """
        self.waiting_list_lc = LoopingCall(self.checkWaitingList)
        #self.waiting_list_lc.start(0.5)
        self.waiting_list_lc.start(3)


    def initClient(self, client, addr):
        """
            Save connected user data.
        """
        client.client_id = addr.port
        client.data = ['', 0]
        client.status = 'waiting'
        client.game_id = ''
        self.clients[addr.port] = client
        self.clients_waiting_list.append(addr.port)

        log_msg = 'class Quickpong, method initClient: %s, %s:%s' % (addr.type, addr.host, addr.port,)
        log.msg(log_msg)
        
        return client

    def checkWaitingList(self):
        """
          This method is calling by LoopingCall every N seconds (see constructor of this class).
          
          This method creates new games, if list contains pair of not active clients.
        """
        while len(self.clients_waiting_list) > 1:
            log.msg(self.clients_waiting_list)
            log.msg(self.clients[self.clients_waiting_list[0]])
            gamer1 = self.clients[self.clients_waiting_list[0]].client_id
            gamer2 = self.clients[self.clients_waiting_list[1]].client_id

            game_id = str(gamer1) + '-' + str(gamer2)
            
            self.clients[self.clients_waiting_list[0]].game_id = game_id
            self.clients[self.clients_waiting_list[1]].game_id = game_id

            self.games[game_id] = QuickpongGame(self.clients[self.clients_waiting_list[0]], self.clients[self.clients_waiting_list[1]])

            self.clients_waiting_list.pop(0)
            self.clients_waiting_list.pop(0)
            
            self.sendPrestartMessage(gamer1)
            self.sendPrestartMessage(gamer2)
            
            log.msg('Quickpong.checkWaitingList: created new game %s with gamers %s and %s' % (game_id, gamer1, gamer2))

    def sendPrestartMessage(self, client_id):
        """
          This methos called from method self.checkWaitingList when new game is created
          
          This method send 'prestart' message to client
        """
        self.clients[client_id].status = 'prestart'
        self.clients[client_id].writeData('prestart')
      
    def connectionClosedByClient(self, client_id):
        """
          This method is calling from connectionLost method of class QuickpongProtocol.
          
          This method calls when client closes the connection.
          
          This method stops the game and set second user to the waiting lists
        """
        if self.clients[client_id].status == 'waiting':
            """remove from waiting list
            """
            self.clients_waiting_list.remove(client_id)

        del self.clients[client_id]
        self.stopGame(client_id)

    def checkStartGame(self, game_id):
        """
            This method checks if both gamers in game pressed "start button" or not.
        """
        gamer1, gamer2 = self.games[game_id].gamers_list()
        
        if self.clients[gamer1].status == 'ready' and self.clients[gamer2].status == 'ready':
            self.startGame(game_id)
    
    def startGame(self, game_id):
        gamer1, gamer2 = self.games[game_id].gamers_list()
        self.clients[gamer1].status = 'working'
        self.clients[gamer2].status = 'working'

        data1 = []
        data2 = []

        # http://ku.kece.ru/projects/quickpong/wiki/%D0%A4%D0%BE%D1%80%D0%BC%D0%B0%D1%82_%D0%BE%D0%B1%D0%BC%D0%B5%D0%BD%D0%B0_%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8_V31#%D0%98%D0%BD%D0%B8%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F
        data1.append('start-1') # 0
        data1.append(self.games[game_id].ball['x'])  # 1
        data1.append(self.games[game_id].ball['y'])  # 2
        data1.append(0)  # 3
        data1.append(0)  # 4
        data1.append(self.games[game_id].score_left)  # 5
        data1.append(self.games[game_id].score_right)  # 6
        data1.append(self.games[game_id].left_y)  # 7
        data1.append(self.games[game_id].right_y)  # 8
        data1.append(0)  # 9
        data1.append(0)  # 10
        data1.append(self.games[game_id].data_frame)  # 11

        # http://ku.kece.ru/projects/quickpong/wiki/%D0%A4%D0%BE%D1%80%D0%BC%D0%B0%D1%82_%D0%BE%D0%B1%D0%BC%D0%B5%D0%BD%D0%B0_%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8_V31#%D0%98%D0%BD%D0%B8%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F
        data2.append('start-2') # 0
        data2.append(self.games[game_id].ball['x'])  # 1
        data2.append(self.games[game_id].ball['y'])  # 2
        data2.append(0)  # 3
        data2.append(0)  # 4
        data2.append(self.games[game_id].score_left)  # 5
        data2.append(self.games[game_id].score_right)  # 6
        data2.append(self.games[game_id].left_y)  # 7
        data2.append(self.games[game_id].right_y)  # 8
        data2.append(0)  # 9
        data2.append(0)  # 10
        data2.append(self.games[game_id].data_frame)  # 11

        log.msg('Quickpong.startGame == GAME STARTED == both gamers pressed Start button')
        log.msg('prestart data1 %s' % (json.dumps(data1), ))
        log.msg('prestart data2 %s' % (json.dumps(data2), ))

        self.clients[gamer1].data = ['', 0, 0]
        self.clients[gamer2].data = ['', 0, 0]

        self.clients[gamer1].writeData(json.dumps(data1))
        self.clients[gamer2].writeData(json.dumps(data2))
    
    def stopGame(self, client_id):
        """
          This is a helper function for method self.connectionClosedByClient
        """
        stop = False
        for game in self.games:
            gamers = self.games[game].gamers_list()
            if gamers[0] == client_id:
                second_gamer = gamers[1]
                delete_game = game
                stop = True
            elif gamers[1] == client_id:
                second_gamer = gamers[0]
                delete_game = game
                stop = True

        if stop:
            #self.clients_waiting_list.append(second_gamer)
            del self.games[delete_game]
            log.msg('stopped game %s, client %s is waiting' % (delete_game, second_gamer))
            self.clients[second_gamer].writeData('Your game is stopped')
            self.clients[second_gamer].status = 'stopped'

    def aggregateClientsData(self, client_id, data):
        """
          This method called from method dataReceived of class QuickpongProtocol.

          Method receive data from all clients, prepare data to sending and save data in list.

          Method self.sendDataToClients sending to clients data prepared by this method
        """
        if self.clients[client_id].status == 'prestart':
            """
                game created, user should press 'start'  button
            """
            self.clients[client_id].status = 'ready'
            self.checkStartGame(self.clients[client_id].game_id)
        elif self.clients[client_id].status == 'working':
            """
              prepare data for gaming players
            """
            self.clients[client_id].data = data

    def prepareDataToClients(self):
        """
          This method calling by LoopingCall (see constructor of this class)
          
          This method prepare data to all active gamers. Method using data prepared by method self.aggregateClientsData
        """
        for game in self.games:
            gamers = self.games[game].gamers_list()
            if self.clients[gamers[0]].status == 'working' and self.clients[gamers[1]].status == 'working':
                # Send data about all clients in game to all clients in game
                # See protocol description wiki http://ku.kece.ru/projects/quickpong/wiki

                # Calculate boards position
                # self.clients[gamers[0]].data[1] and self.clients[gamers[1]].data[1] is a board_y deltas from
                # left and right players
                if self.games[game].left_last_processed_frame != self.clients[gamers[0]].data[2]:
                    self.games[game].left_last_processed_frame = self.clients[gamers[0]].data[2]
                    self.games[game].left_y += self.clients[gamers[0]].data[1]

                    if self.games[game].left_y < 0:
                        self.games[game].left_y = 0
                        self.clients[gamers[0]].data[1] = 0
                    elif self.games[game].left_y + self.games[game].board_height > self.games[game].field_height:
                        self.games[game].left_y = self.games[game].field_height - self.games[game].board_height
                        self.clients[gamers[0]].data[1] = 0
                else:
                    pass

                if self.games[game].right_last_processed_frame != self.clients[gamers[1]].data[2]:
                    self.games[game].right_last_processed_frame = self.clients[gamers[1]].data[2]
                    self.games[game].right_y += self.clients[gamers[1]].data[1]
                    if self.games[game].right_y < 0:
                        self.games[game].right_y = 0
                        self.clients[gamers[1]].data[1] = 0
                    elif self.games[game].right_y + self.games[game].board_height > self.games[game].field_height:
                        self.games[game].right_y = self.games[game].field_height - self.games[game].board_height
                        self.clients[gamers[1]].data[1] = 0


                ball = self.games[game].update_ball()

                """
                    To understand format watch this:
                    # http://ku.kece.ru/projects/quickpong/wiki/%D0%A4%D0%BE%D1%80%D0%BC%D0%B0%D1%82_%D0%BE%D0%B1%D0%BC%D0%B5%D0%BD%D0%B0_%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8_V31#%D0%98%D0%B3%D1%80%D0%BE%D0%B2%D0%BE%D0%B9-%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81
                """
                data = []
                data.append('')  # 0
                data.append(ball['x'])  # 1
                data.append(ball['y'])  # 2
                data.append(ball['delta_x'])  # 3
                data.append(ball['delta_y'])  # 4
                data.append(ball['score_left'])  # 5
                data.append(ball['score_right'])  # 6
                data.append(self.games[game].left_y)  # 7
                data.append(self.games[game].right_y)  # 8
                data.append(self.clients[gamers[0]].data[1])  # 9
                data.append(self.clients[gamers[1]].data[1])  # 10
                data.append(self.games[game].data_frame)  # 11

                self.games[game].data_frame += 1
                self.games[game].game_data.append(data)


                #log.msg('=== ' * 5)
                """
                if len(ball['x_client']):
                    #log.msg('len %d' % (len(ball['x_client'])))
                    
                    for i in range(0, len(ball['x_client'])):
                        local_data = []
                        local_data.append('')  # 0
                        local_data.append(ball['x_client'][i])  # 1
                        local_data.append(ball['y_client'][i])  # 2
                        #data.append(ball['x'])  # 1
                        #data.append(ball['y'])  # 2
                        local_data.append(ball['score_left'])  # 3
                        local_data.append(ball['score_right'])  # 4
                        local_data.append(self.games[game].left_y)  # 5
                        local_data.append(self.games[game].right_y)  # 6
                        local_data.append(self.games[game].data_frame)  # 7

                        self.games[game].data_frame += 1
                        #log.msg('piece of data:')
                        #log.msg(local_data)

                        #data.append(local_data)
                        self.games[game].game_data.append(local_data)
                #"""


                    #log.msg('prepared data %s' % (json.dumps(data)))
                    #self.games[game].game_data.append(data)

                    #log.msg('-' * 5)
                    #for data in self.games[game].game_data:
                    #    log.msg(data)

    def sendDataToClients(self):
        """
          This method calling by LoopingCall (see constructor of this class).
          
          This method sends data to all active gamers. Method using data ptrepared by methods self.aggregateClientsData
          and self.prepareDataToClients.
        """
        for game in self.games:
            gamers = self.games[game].gamers_list()
            if self.clients[gamers[0]].status == 'working' and self.clients[gamers[1]].status == 'working':
                if len(self.games[game].game_data):
                    #log.msg('game_data len %d' % len(self.games[game].game_data))
                    #log.msg('game_data[0] %s' % self.games[game].game_data[0])
                    local_game_data = self.games[game].game_data
                    sent_counter = 0
                    for data in local_game_data:
                        data_to_send = json.dumps(data)

                        self.clients[gamers[0]].writeData(data_to_send)
                        self.clients[gamers[1]].writeData(data_to_send)
                        #log.msg(data_to_send)

                        sent_counter += 1

                    """
                        I should remove from game_data list items which were sent to clients to avoid sending
                        one data packet twice. But I can't do smth like self.games[game].game_data = [] because method
                        prepareDataToClients could add new items while sendDataToClients working. In this reason
                        I count amount of sent items and remove this number of elements from the beginning of
                        game_data list.
                    """
                    #log.msg('send %d packets' % (sent_counter))
                    self.games[game].game_data = self.games[game].game_data[sent_counter:]
