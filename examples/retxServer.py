
from twisted.internet import reactor
from retransmission import RetransmissionFactory
#----------------------------------------------------------------------
def TwistedRetxServer ():
  """"""
  reactor.listenTCP (9090, RetransmissionFactory ())
  reactor.run ()
  pass
  
if __name__ == '__main__':
  TwistedRetxServer ()
  pass
