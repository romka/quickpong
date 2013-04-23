# Developed by Roman Arkharov, arkharov@gmail.com. 04.2013

"""
    This class creates a web-server (by default on kece.ru:10082), which returns current number of gamers and games.
     This data might be used in Zabbix.
"""
from twisted.web.resource import Resource


class StatsWebserver(Resource):
    isLeaf = True

    def __init__(self, game):
        self.game = game

    def render_GET(self, request):
        return "%d,%d" % (len(self.game.quickpong_service.clients), len(self.game.quickpong_service.games))

