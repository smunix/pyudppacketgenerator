from lib.common import NotImplemented

########################################################################
class  Receiver:
  """
  """
  
  DEFAULT_PORT = 8282
  DEFAULT_GROUP = '225.0.0.250'
  
  #----------------------------------------------------------------------
  def __init__(self):
    """Constructor"""
    
    
  #----------------------------------------------------------------------
  def  Receive(self, dataSize):
    """
    Reads up to dataSize from ending peer
    """
    raise NotImplemented 
  
  