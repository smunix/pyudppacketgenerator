from twisted.internet import reactor
from retransmission import RetransmissionClientFactory
#----------------------------------------------------------------------
def TwistedRetxClient ():
  """"""
  reactor.connectTCP ('localhost', 9090, RetransmissionClientFactory ())
  reactor.run ()
  pass
  
if __name__ == '__main__':
  TwistedRetxClient ()
  pass
