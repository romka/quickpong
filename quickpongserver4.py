# Developed by Roman Arkharov, arkharov@gmail.com. 04.2013

"""
    Quickpong is a server of online version of classic game Pong. Users can play with other users,
    but not with computer (for test purposes you can use quickpong_test_client.py to emulate opponent).

    Code of this project based on framework Twisted (v. 13) http://twistedmatrix.com/trac/ and several
    external libraries like simplejson https://pypi.python.org/pypi/simplejson/ .

    This file is a start point for the game. Run this file from command line something like this:

        twistd --python quickpongserver4.py

    or like this:

        twistd --python --reactor=poll quickpongserver4.py

    or like this (for debug purposes):
        twistd --nodaemon --python quickpongserver4.py

    This file:
    * run main server factory QuickpongServerFactory() on kece.ru:10080
    * run policy-server factory SendPolicyFactory() on kece.ru:10081
    * run simple web-server StatsWebserver() on kece.ru:10082. This server returns comma separated amount of
      online users and current amount of games.
"""

import optparse

from quickpong.serverfactory import QuickpongServerFactory
from quickpong.sendpolicyfactory import SendPolicyFactory

from twisted.application import internet, service


host = 'kece.ru'
port = 10080
policy_port = 10081
stats_port = 10082
max_clients = 10000

top_service = service.MultiService()

quickpong_service = service.Service()
quickpong_service.setServiceParent(top_service)

factory = QuickpongServerFactory(max_clients, quickpong_service)
tcp_service = internet.TCPServer(port, factory, interface=host)
tcp_service.setServiceParent(top_service)

policy_factory = SendPolicyFactory(quickpong_service)
tcp_policy_service = internet.TCPServer(policy_port, policy_factory, interface=host)
tcp_policy_service.setServiceParent(top_service)

# StatsFactory should be imported after factory object creation
from quickpong.statswebserver import StatsWebserver
from twisted.web.server import Site

stats = StatsWebserver(factory)
stats_factory = Site(stats)
tcp_stats_service = internet.TCPServer(stats_port, stats_factory, interface=host)
tcp_stats_service.setServiceParent(top_service)


application = service.Application("quickpongserver4")

# this hooks the collection we made to the application
top_service.setServiceParent(application)



"""
# This commented code earlier was used for run server in console, without making daemon. Now it is deprecated.
from twisted.internet import reactor

factory = QuickpongServerFactory(opts.max_clients)
server = reactor.listenTCP(opts.port, factory)

f = ServerFactory()
f.protocol = SendPolicyProtocol
reactor.listenTCP(opts.policy_port, f)

log.msg('Listening started on %s:%d' % (opts.host, opts.port))
log.msg('Policy server started on %s:%d' % (opts.host, opts.policy_port))

reactor.run()
#"""
