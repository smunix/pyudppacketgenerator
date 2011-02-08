import SocketServer, socket
from headers import PacketHeader
from lib import Header, Endian
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )

########################################################################
class RequestHandler (SocketServer.BaseRequestHandler):
  """"""
  counter = 0
  
  #----------------------------------------------------------------------
  def __init__(self, request, client_address, server):
    """Constructor"""
    self.counter = RequestHandler.counter
    RequestHandler.counter += 1
    self.logger = logging.getLogger('retransmission.RequestHandler{%d}' % self.counter)
    self.logger.debug ("__init__")
    SocketServer.BaseRequestHandler.__init__ (self, request, client_address, server)
    pass
  #----------------------------------------------------------------------
  def handle (self):
    """"""
    self.logger.debug ("handle")
    while True:
      data = self.request.recv (PacketHeader.SIZE)
      self.logger.debug ('data recv = %s (%d)' % (str(data), len (data)))
      if not len (data) == PacketHeader.SIZE:
        continue
      p = Header.DeSerialize (PacketHeader, data, Endian.NETWORK)
      self.logger.debug ("\nPacket received\n%s" % p.Get ())
    #self.request.send ("Counter<%d> : Thread<%s> : Data<%s>" % (self.counter, 
                                                                #threading.currentThread ().getName (), 
                                                                #data))
