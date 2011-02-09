import multicast
from headers import PacketHeader
from lib import Header, Endian
import time

#----------------------------------------------------------------------
def Main ():
  """
  - Creates a Packet containing a dummy PacketHeader as data
  - Creates a multicast Sender
  - Uses the Sender to emit the packet data
  
  Easy, huh?
  """
  GROUP, PORT = '225.0.0.250', 8383
  p = Header.Make (PacketHeader, withByteOrder = Endian.NETWORK
                   )
  p.PacketLength = 16
  p.PacketType = 2
  s = multicast.Sender (GROUP, PORT)
  counter = 0
  while True:
    p.PacketSeqNum = counter
    counter = counter + 1
    data = p.Get ().Serialize () [0]
    print "Sending : [", data, "] : to GROUP <", GROUP, ">, PORT <", PORT, ">."
    s.Send (data)
    time.sleep (1)
    
    f = 3
    print "ssss%s" % f
    
if __name__ == '__main__':
  Main ()