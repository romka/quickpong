# Developed by Roman Arkharov, arkharov@gmail.com. 04.2013

"""
    Flash requires to request policy file from server. This factory precess policy requests.

    This faactory by default runs on kece.kru:10081.
"""
from twisted.internet.protocol import ServerFactory
from sendpolicyprotocol import SendPolicyProtocol
from twisted.python import log

class SendPolicyFactory(ServerFactory):
    log.msg("SendPolicyFctory")
    protocol = SendPolicyProtocol

    def __init__(self, service):
        log.msg("SendPolicyFctory constructor")
        self.service = service

