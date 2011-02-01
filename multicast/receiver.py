import sys
from socket import *
import lib

########################################################################
class Receiver (lib.Receiver):
  """
  Multicast listener API
  """

  #----------------------------------------------------------------------
  def __init__(self, group, port):
    """Constructor"""
    
    self.socket = self.__OpenMulticastSocket (group, port)
    
  #----------------------------------------------------------------------
  def __OpenMulticastSocket (self, group, port):
    """"""
    import string
    import struct
    
    s = socket (AF_INET, SOCK_DGRAM)
    s.setsockopt (SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind (('', port))
    group = gethostbyname (group)
    bytes = map (int, string.split (group, '.'))
    grpadd = 0
    for b in bytes:
      grpadd = (grpadd << 8) | b
    mreq = struct.pack ('ll', htonl (grpadd), htonl (INADDR_ANY))
    s.setsockopt (IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)
    
    return s
    
  #----------------------------------------------------------------------
  def Receive (self, dataSize = lib.DEFAULT_RECV_SIZE):
    """"""
    data, sender = self.socket.recvfrom (dataSize)
    return data, sender
    
#----------------------------------------------------------------------
def Test():
  """
  Test the Receiver API
  """
  r = Receiver(lib.Sender.DEFAULT_GROUP, lib.Sender.DEFAULT_PORT)
  while 1:
    data, sender = r.Receive ()
    print sender, ':', bytes (data)
    
if __name__ == '__main__':
  Test ()