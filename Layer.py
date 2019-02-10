import string
import AML
from AML import mkvar
from AML import tempcov
from List import List
from Cursor import Cursor
from Cover import Cover

class SDELayer

  def __init__(self,name,file):
      self.database = "TOPO250K"
      self.dataset = ""
      self.feature = ""
      self.geometryitem = "SHAPE"
      self.name = name
      self.file = file
      self.code = ''

      code = ''' layer define %s SDE %s %s.%s %s %s
      ''' % (self.name ,self.database,self.database,self.dataset,self.geometryitem,self.feature)
      self.writecode(code)


  def writecode(self,code):
     self.code = self.code + code
     f = open(self.file,'a')
     f.write(code)
     f.close()

   def exists(self):
      # Check that the cover does not exist
      code = '''
      /*
      /* Check if a defined layer exists
      /*
      &if not [exists %s -deflayer] &then
         &do
         &ty
         &ty
         &ty LAYER ERROR:
         &ty Layer %s does not exist
         &return &error
         &end
      /*=============================================================
      ''' % (self.name,self.name)
      self.writecode(code)

  def remove(self):
     code = ''' layer remove %s''' % self.name
     self.writecode(code)

  def query(self,q):
     code = ''' layer %s query %s ''' (self.name,q)
     self.writecode(code)

  def load(self,cover):

     code = '''
          &s cols [show layercolumns %s]

          layerimport %s COVERAGE %s %s define
          FEATURERELIABILI FEATURERELIABILITY
          ATTRIBUTERELIABI ATTRIBUTERELIABILITY
          PLANIMETRICACCUR PLANIMETRICACCURACY
          ELEVATIONACCURAC ELEVATIONACCURACY
          &do col &list %%cols%%
             %%col%% %%col%%
          &end'''
          self.writecode(code)

  def columns(self):
     func = '[show layercolumns %s]' % self.name
     return List(func,self.file)

  def count(self):
     num = mkvar()
     code = ''' &s %s = [show definedlayer %s count] ''' % (num,self.name)
     self.writecode(code)
     return num




