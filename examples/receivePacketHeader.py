import multicast
from headers import PacketHeader
from lib import Header, Endian

#----------------------------------------------------------------------
def Main ():
  """
  - Creates a Packet containing a dummy PacketHeader as data
  - Creates a multicast Sender
  - Uses the Sender to emit the packet data
  
  Easy, huh?
  """
  GROUP, PORT = '225.0.0.250', 8383
  r = multicast.Receiver (GROUP, PORT)
  while True:   
    data, sender = r.Receive ()
    p = Header.DeSerialize (PacketHeader, data, Endian.NETWORK)
    print sender, ':\n', p.Get ()
    
if __name__ == '__main__':
  Main ()