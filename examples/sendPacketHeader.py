import multicast
from headers import PacketHeader
from lib import Header
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
  p = Header.Make (PacketHeader)
  p.PacketLength = 1
  s = multicast.Sender (GROUP, PORT)
  counter = 0
  while True:
    p.PacketSeqNum = counter
    counter = counter + 1
    data = p.Get ().Serialize () [0]
    print "Sending : [", data, "] : to GROUP <", GROUP, ">, PORT <", PORT, ">."
    s.Send (data)
    # time.sleep (1)
    
if __name__ == '__main__':
  Main ()