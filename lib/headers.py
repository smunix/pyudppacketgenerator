import struct
from common import NotImplemented
import exceptions
import types

NAME = "FIELD"
VALUE = "VALUE"

########################################################################
class ByteOrder:
  """"""

  NATIVE_MACHINE = '@'
  NATIVE_STANDARD = '='
  LITTLE_ENDIAN = '<'
  BIG_ENDIAN = '>'
  NETWORK = '!'

########################################################################
class Type:
  """"""
  
  CHAR = 'c'
  INT8 = 'b'
  UINT8 = 'B'
  INT16 = 'h'
  UINT16 = 'H'
  INT32 = 'i'
  UINT32 = 'I'
  LONG = 'l'
  ULONG = 'L'
  QUAD = 'q'
  UQUAD = 'Q'
  FLOAT = 'f'
  DOUBLE = 'd'
  POINTER = 'p'
  
  #----------------------------------------------------------------------
  @staticmethod
  def STRING(size):
    """"""
    assert isinstance (size, types.IntType) and size > 0, "Parameter to STRING has to be an Integer"
    return '%ss' % size

  
########################################################################
class FieldNotFound (exceptions.Exception):
  """"""

  #----------------------------------------------------------------------
  def __init__(self, val):
    """Constructor"""
    
    self.name = val
  #----------------------------------------------------------------------
  def __str__(self):
    """"""
    return "FieldNotFound : %s" % self.name
    
  
########################################################################
class AccessorHelper:
  """"""
  #----------------------------------------------------------------------
  def __init__(self, obj):
    """Constructor"""
    self.__dict__["obj"] = obj
  #----------------------------------------------------------------------
  def __setattr__(self, k, v):
    """"""
    self.__dict__["obj"].SetField (k, v)
  #----------------------------------------------------------------------
  def __getattr__(self, k):
    """"""
    return self.__dict__["obj"].GetField (k)
  #----------------------------------------------------------------------
  def Get(self):
    """"""
    return self.obj
########################################################################

class HeaderBase:
  """"""
  #----------------------------------------------------------------------
  def __init__(self, cls, byteOrder):
    """Constructor"""
    self.name = cls.__name__
    self.formatter = struct.Struct (byteOrder + HeaderBase.Format (cls))
    self.fields_list = []
    self.fields = {}
    for f in HeaderBase.Fields (cls):
      t = {
        NAME  :f ,
        VALUE : 0
        }
      self.fields [f] = t
      self.fields_list.append (t)
  #----------------------------------------------------------------------
  def SetField (self, k, v):
    """"""
    if k not in self.fields: raise FieldNotFound (k)
    self.fields[k][VALUE] = v
  #----------------------------------------------------------------------
  def GetField (self, k):
    return self.fields[k][VALUE]
  #----------------------------------------------------------------------
  def IsEqual2(self, o):
    """"""
    e = lambda a: a[0][NAME] == a[1][NAME] and a[0][VALUE] == a[1][VALUE]
    f = lambda *a: a[0] and a[1]
    return reduce (f, map (e, zip (self.fields_list, o.fields_list)), True)
  #----------------------------------------------------------------------
  def IsEqual(self, o):
    """"""
    return self.Serialize () == o.Serialize ()
  #----------------------------------------------------------------------
  def __str__(self):
    """"""
    return "%s\n%s\n%s" % (self.name, '='*len (self.name), '\n'.join (["%s=%s" % (x[NAME], x[VALUE]) for x in self.fields_list]))
  #----------------------------------------------------------------------
  def __setitem__(self, k, v):
    """"""
    self.SetField (k, v)
  #----------------------------------------------------------------------
  def __getitem__(self, k):
    """"""
    return self.GetField (k)
  #----------------------------------------------------------------------
  def Size (self):
    """"""
    return self.formatter.size
  #----------------------------------------------------------------------
  def Serialize(self):
    """"""
    listTuple = self.__MakeTupleFromFieldsValue ()
    return self.formatter.pack (*listTuple), self.Size ()
  #----------------------------------------------------------------------
  def __MakeTupleFromFieldsValue(self):
    """"""
    return tuple ([x[VALUE] for x in self.fields_list])
  #----------------------------------------------------------------------
  @staticmethod
  def DeSerialize(cls, data, aByteOrder):
    """"""
    p = HeaderBase.Make (cls, withByteOrder = aByteOrder, withAccessor = False)
    data = p.formatter.unpack (data)
    for f, v in zip (HeaderBase.Fields (cls), data):
      p[f] = v
    return AccessorHelper (p)
  #----------------------------------------------------------------------
  @staticmethod
  def Format (cls):
    """"""
    return ''.join ([y for x, y in cls.FIELDS])
  #----------------------------------------------------------------------
  @staticmethod
  def Fields (cls):
    """"""
    return tuple ([x for x, y in cls.FIELDS])
  #----------------------------------------------------------------------
  @staticmethod
  def Make(cls, withByteOrder = ByteOrder.NATIVE_STANDARD, withAccessor = True):
    """
    Packet Header generator
    """
    if withAccessor:
      return AccessorHelper (cls (aByteOrder = withByteOrder))
    else:
      return cls (aByteOrder = withByteOrder)
