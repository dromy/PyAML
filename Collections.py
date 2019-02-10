from Cover import Cover

class Buildings(Cover):
   def __init__(self,cover,file):
      Cover.__init__(self,cover.name,file)
      self = cover.reselect('point',"feat_code = 'building'" )

   def __getitem__(self,offset):
      id = self.name + '#'
      value = offset + 1

      return self.reselect('point',"%s = %s" %(id,value))

      

      


c = Cover('f5513gm','test')
x = Buildings(c,'test')
z = x[0]

