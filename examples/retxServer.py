import threading, SocketServer, socket, time
from headers import PacketHeader
from lib import Header, Endian
from retransmission import RequestHandler
import logging


########################################################################
class Client:
  """
  """
  cId = 0
  #----------------------------------------------------------------------
  def __init__(self, ip, port, *messages):
    """Constructor"""
    
    self.mIp = ip
    self.mPort = port
    self.mMessages = messages
    self.mId = Client.cId
    Client.cId += 1
    self.socket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect ((self.mIp, self.mPort))
    pass
  #----------------------------------------------------------------------
  def RunMessage (self, message):
    """"""
    print "Client ", self.mId, " sends ", message
    self.socket.send (message)
    time.sleep (1)
    try:
      response = self.socket.recv (9)
    except:
      print "exception occurred while receiving messages"
    else:
      print "Client %d receives %s" % (self.mId, response)
    pass
  #----------------------------------------------------------------------
  def Loop(self):
    """"""
    while True:
      pass
  #----------------------------------------------------------------------
  def Run (self):
    """"""
    self.Loop ()
    for m in self.mMessages: 
      self.RunMessage (m)
    pass
  #----------------------------------------------------------------------
  def Stop (self):
    """"""
    self.socket.close ()
  
#----------------------------------------------------------------------
def Main ():
  """"""
  HOST, PORT = '0.0.0.0', 8001
  server = SocketServer.ForkingTCPServer ((HOST, PORT), RetransmissionRequestHandler)
  serverThread = threading.Thread (target = server.serve_forever)
  serverThread.setDaemon (True)
  serverThread.start ()
  time.sleep (120)
  server.shutdown ()
  pass
  
if __name__ == '__main__':
  Main ()