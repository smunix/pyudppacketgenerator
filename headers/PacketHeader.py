from lib import Header, Accessor, Endian, Type

########################################################################
class PacketHeader (Header):
  """"""
  FIELDS = (
    ("PacketLength", Type.UINT16),
    ("PacketType", Type.UINT16),
    ("PacketSeqNum", Type.UINT32),
    ("SendTime", Type.UINT32),
    ("ServiceID", Type.UINT16),
    ("DeliveryFlag", Type.UINT8),
    ("NumberMsgEntries", Type.UINT8),
    ("OutOfBand", Type.STRING (4))
  )
  #----------------------------------------------------------------------
  def __init__(self):
    """Constructor"""
    Header.__init__ (self, 
                     PacketHeader,
                     byteOrder = Endian.NATIVE_STANDARD)

#----------------------------------------------------------------------
def MakePacketHeader():
  """"""
  p = Header.Make (PacketHeader)
  p.PacketLength = 1
  p.PacketType = 2
  p.PacketSeqNum = 3
  p.SendTime = 4
  p.ServiceID = 5
  p.DeliveryFlag = 6
  p.NumberMsgEntries = 7
  p.OutOfBand = "Providence is the Lawyer"
  return p

#----------------------------------------------------------------------
def FormatTest():
  """"""
  print "Format = ", Header.Format (PacketHeader)
  print "Fields = ", Header.Fields (PacketHeader)
#----------------------------------------------------------------------
def SerializeTest():
  """"""
  p1 = MakePacketHeader ()
  packed = p1.Get ().Serialize () [0]
  p2 = Header.DeSerialize (PacketHeader, packed)
  sourceLabel = 'PACKET SOURCE'
  destinatLabel = 'PACKET DESTINATION'
  print "%s\n%s\n%s\n" % (sourceLabel, '=' * len (sourceLabel), p1.Get ())
  print "%s\n%s\n%s\n" % (destinatLabel, '=' * len (destinatLabel), p2.Get ())
  print "IsEqual (source, destination) ==>", p1.Get ().IsEqual (p2.Get ())
  p1.PacketLength = 2
  print "IsEqual (source, destination) ==>", p1.Get ().IsEqual (p2.Get ())
  
if __name__ == '__main__':
  # FormatTest ()
  SerializeTest ()