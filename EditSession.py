from Cover import Cover
class EditSession:
   def __init__(self,file):
      self.file = file
      self.code = ''
      self.module = 'ARCEDIT'
      self.covers = []
      self.backcovers = []
      self.currentcov = None
      self.startup()
      
   def writecode(self,code):
      self.code = self.code + code
      f = open(self.file,'a')
      f.write(code)
      f.close()

   def startup(self):
      code = '''
      /*
      /* Check that the user is starting the module from
      /* the correct place
      /*
      &if not [show program] = ARC &then
         &do
         &ty MODULE ERROR:
         &ty Cannot start %s from [show program]
         &return &error
         &end
      &else
         &do
         %s
         &end
      /* ==================================================
      ''' % (self.module,self.module)
      self.writecode(code)
         
   def edit(self,name,feature='' ):
      self.currentcov = Cover(name,self.file)
      if feature == '':
         code = '''
            edit %s
            ''' % self.currentcov.name
      else:
         if feat == 'poly':
            feat = 'polygon'
         self.currentcov.checktopology(feat)
         code = '''
            edit %s %s
            ''' % (self.currentcov.name,feat)
      self.writecode(code)
      if self.currentcov.name not in self.covers:
         self.covers.append(self.currentcov.name)         
      return self.currentcov

    
            
      

      
