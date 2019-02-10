from Cover import Cover
from List import List
import AML
from AML import mkvar
import string

# Aeronautical Cover inherits from the Generic Cover class
# Here we specialise the class by adding the info that this cover should
# know about about itself such as its feature types, items etc.
class ACover(Cover):
   def __init__(self,name,filename):
      Cover.__init__(self,name,filename)
      # A features table showing feature classes and
      # related feat_codes
      self.features = {'point':  ['aircrft_flty']}
      self.items = {'point': ['area',
                              'perimeter',
                              '%s#' % self.name,
                              '%s-id' % self.name,
                              'feat_code',
                              'name',
                              'facility',
                              'q_info',
                              'ufi',
                              'symbol',
                              'feat_wid',
                              'orientation',
                              'old_ufi']
                   }
                             

   def checktopology(self,feat):
      # Check that DOES have point topology
      Cover.checktopology(self,'point')

      # Check that it DOESNT have other topology or features.
      feats = string.join(self.features.keys())
      allfeats = ['point','arc','polygon']
      for f in allfeats:
         if f not in self.features.keys():
            Cover.checkextratopology(self,f,feats)
            Cover.checkextrafeatures(self,f,feats)



         
class AMCover(ACover):
   def __init__(self,name,filename):
      self.suf = 'am'
      self.name = name+self.suf
      ACover.__init__(self,self.name,filename)
      # For conversion of units from meters to geo
      # in this case it is 1.
      self.sfactor = 1.0
      

class AADCover(ACover):
   def __init__(self,name,filename):
      self.suf = 'aad'
      self.name = name+self.suf
      ACover.__init__(self,self.name,filename)
      # For conversion of units from meters to geo
      # in this case it is 1.
      self.sfactor = 1.0

class ALDCover(ACover):
   def __init__(self,name,filename):
      self.suf = 'ald'
      self.name = name + self.suf
      ACover.__init__(self,self.name,filename)
      # For conversion of units from meters to geo
      # in this case it is 100000.
      self.sfactor = 100000.0


code = AML.header()
f = open('test.aml','a')
f.write(code)
f.close()

c = AMCover('e5108','test.aml')
#c.checkfeatcodes()

#c.checktopology('point')
#c.checkitems()
c.checkextraitems()

code = AML.bailout()
f = open('test.aml','a')
f.write(code)
f.close()

