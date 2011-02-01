import sys
from socket import *
import lib

########################################################################
class  Sender(lib.Sender):
  """
  Multicast sender API
  """
  MCST_TTL = 30
  #----------------------------------------------------------------------
  def __init__(self, group, port):
    """Constructor"""
    import struct
    self.group = group
    self.port = port
    self.socket = socket (AF_INET, SOCK_DGRAM)
    ttl = struct.pack ('b', Sender.MCST_TTL)
    self.socket.setsockopt (IPPROTO_IP, IP_MULTICAST_TTL, ttl)
  #----------------------------------------------------------------------
  def Send(self, data):
    """
    Sends data to an endpoint peer
    """
    size = self.socket.sendto (data, (self.group, self.port))
    print "Sending :", data, " -[", size, "] bytes..."
    
  
#----------------------------------------------------------------------
def Test():
  """
  Test the Sender API
  """
  import time
  s = Sender(lib.Sender.DEFAULT_GROUP, lib.Sender.DEFAULT_PORT)
  while 1:
    import struct
    ## (PacketType (uint32), PacketLength (uint16), Password (20-char))
    f = struct.Struct ('=LH20s')
    data = f.pack (2, 16, 'Providence')
    s.Send (data)
    time.sleep (1)
    
if __name__ == '__main__':
  Test ()