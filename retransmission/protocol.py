from twisted.internet.protocol import Protocol, ServerFactory, ClientFactory
from twisted.internet.defer import Deferred
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
import logging, time
from headers import PacketHeader, TYPE_FIELD, LENG_FIELD
from lib import Header, Endian
from threading import Thread

########################################################################
class RetransmissionProtocol (Protocol):
  """"""
  COUNTER = 0
  #----------------------------------------------------------------------
  def __init__(self):
    """"""
    self.COUNTER  = RetransmissionProtocol.COUNTER
    RetransmissionProtocol.COUNTER += 1
    self.LOGGER = logging.getLogger ("RetransmissionProtocol<%d>" % self.COUNTER)
    self.__disconnected = True
    self.mHeartbeatDeferred = Deferred ()
    self.mHeartbeatDeferred.addCallback (self.Service, lambda x, t: self.HeartbeatService (x, t), 3)
    pass
  #----------------------------------------------------------------------
  def Service (self, result, aTarget, aArgs = None):
    """"""
    self.LOGGER.debug ('Starting service [%s]' % result[0])
    if aArgs is not None:
      aTarget (aArgs, result[1])
    else:
      aTarget ()
    pass
  #----------------------------------------------------------------------
  def StopAllServices (self):
    """"""
    self.LOGGER.debug ('StopAllServices')
    pass
  #----------------------------------------------------------------------
  def SendResponse (self):
    """"""
    self.LOGGER.debug ('Sending response ...')
    p = Header.Make (PacketHeader, withByteOrder = Endian.NETWORK)
    p.PacketLength = 16
    p.PacketType = 37
    self.LOGGER.debug (p.Get ())
    self.transport.write (p.Get ().Serialize () [0])
    pass
  #----------------------------------------------------------------------
  def dataReceived (self, data):
    """"""
    if self.__disconnected:
      return
    self.LOGGER.debug ('Recv <%s> (%d)' % (data, len(data)))
    p = Header.DeSerialize (PacketHeader, data[:16], Endian.NETWORK)
    if p.PacketType == PacketHeader.TYPE['RETX_REQUEST'][TYPE_FIELD]:
      self.LOGGER.debug ("RETRANSMISSION REQUEST")
      reactor.callLater (1, self.SendResponse)
      pass
    if p.PacketType == PacketHeader.TYPE['HEARTBEAT_RESPONSE'][TYPE_FIELD]:
      self.LOGGER.debug ("HEARTBEAT RESPONSE")
      pass
    self.LOGGER.debug ("%s" % p.Get ())
    pass
  #----------------------------------------------------------------------
  def connectionMade (self):
    """"""
    self.LOGGER.debug ('Connection made')
    self.__disconnected = False
    self.mHeartbeatDeferred.callback (('HEARTBEAT', self.transport))
    pass
  #----------------------------------------------------------------------
  def connectionLost (self, reason):
    """"""
    self.LOGGER.debug ('Connection lost')
    self.__disconnected = True
    self.StopAllServices ()
    pass
  #----------------------------------------------------------------------
  def HeartbeatService (self, aDelay, aTransport):
    """"""
    self.LOGGER.debug ('Heartbeat will be sent every %d sec' % aDelay)
    self.mDelay = aDelay
    self.DoHeartbeat ()
    pass
  #----------------------------------------------------------------------
  def DoHeartbeat (self):
    """"""
    if not self.__disconnected:
      self.LOGGER.debug ('Sending heartbeat ...')
      p = Header.Make (PacketHeader, withByteOrder = Endian.NETWORK)
      p.PacketLength = 16
      p.PacketType = 2
      self.transport.write (p.Get ().Serialize () [0])
      reactor.callLater (self.mDelay, self.DoHeartbeat)
    pass
  pass


########################################################################
class RetransmissionFactory (ServerFactory):
  """"""
  protocol = RetransmissionProtocol
  pass
  
########################################################################
class RetransmissionClientProtocol (Protocol, LineReceiver):
  """"""
  COUNTER = 0
  #----------------------------------------------------------------------
  def __init__(self):
    """Constructor"""
    self.COUNTER  = RetransmissionClientProtocol.COUNTER
    RetransmissionClientProtocol.COUNTER += 1
    self.LOGGER = logging.getLogger ("RetransmissionClientProtocol<%d>" % self.COUNTER)
    self.LOGGER.debug ('__init__')
    self.data = b''
    pass
  #----------------------------------------------------------------------
  def connectionMade(self):
    """"""
    self.LOGGER.debug ('Connection made')
    self.SendRequest ()
    pass
  #----------------------------------------------------------------------
  def dataReceived (self, data):
    """"""
    self.data += data
    self.LOGGER.debug ('dataReceived, total len = %d' % len (data))
    while len (self.data) >= 16:
      self.DoDataReceived (data[:16])
      self.data = self.data[16:]
    pass
  #----------------------------------------------------------------------
  #----------------------------------------------------------------------
  def DoDataReceived(self, data):
    """"""
    self.LOGGER.debug ('dataReceived <%s> (%d)' % (data, len(data)))
    p = Header.DeSerialize (PacketHeader, data, Endian.NETWORK)
    self.LOGGER.debug ("Packet received\n%s" % p.Get ())
    
  def SendRequest(self):
    """"""
    p = Header.Make (PacketHeader, withByteOrder = Endian.NETWORK)
    p.PacketLength = 44
    p.PacketType = 36
    self.transport.write (p.Get ().Serialize () [0])
  pass

########################################################################
class RetransmissionClientFactory (ClientFactory):
  """"""
  protocol = RetransmissionClientProtocol
  #----------------------------------------------------------------------
  def startedConnecting (self, connector):
    """"""
    print "startedConnection %s" % connector
    pass
  pass
  
  