import sys,string
import Items
import ItemDefs
import PointFeatcodes
import ArcFeatcodes

class Item:
   def __init__(self,name):
      
      if ItemDefs.values.has_key(string.lower(name)):
         self.name = string.lower(name)
         self.width = ItemDefs.values[self.name][0]
         self.output =  ItemDefs.values[self.name][1]
         self.type =  ItemDefs.values[self.name][2]
         self.ndec =  ItemDefs.values[self.name][3]
         
      else:
         sys.stderr.write('Invalid item: %s\n' % name)
         sys.exit(0)
      
class Feature:
   def __init__(self,name,file,type):
      self.name = name      
      self.type = type
      self.file = file
      self.items = []
      self.code = ''
      try:
         for i in Items.items[name]:
            self.items.append(Item(i))
      except KeyError:
         sys.stderr.write("Invalid name: %s\n" % name)
         sys.exit(0)

      self.checkname(name)
   
   def checkname(self,name):
      if name not in self.names:
         sys.stderr.write("Invalid name: %s\n" % name)
         sys.exit(0)

   def writecode(self,code):
      self.code = self.code + code
      f = open(self.file,'a')
      f.write(code)
      f.close()



class PointFeature(Feature):
   def __init__(self,name,file):
      self.names = PointFeatcodes.names
      self.id = None
      Feature.__init__(self,name,file,'point')

class LineFeature(Feature):
   def __init__(self,name,file):
      self.names = ArcFeatcodes.names
      Feature.__init__(self,name,file,'line')

class PolyFeature(Feature):
   def __init__(self,name,file):
      Feature.__init__(self,name,file,'polygon')   

class AnnoFeature(Feature):
   def __init__(self,name,file):
      Feature.__init__(self,name,file,'anno')


