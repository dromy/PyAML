# A List class
import AML
from AML import mkvar
class List:
   def __init__(self,list,file):
      self.name = mkvar()
      self.list = list
      self.file = file
      self.code = ''
      code = '''
      &s %s %s
      ''' % (self.name,self.list)
      self.writecode(code)

   def __repr__(self):
      # Returns an AML % quoted variable.This really cleans
      # up the string formatting code. 
      return '%%%s%%' % self.name

   def writecode(self,code):
      self.code = self.code + code
      f = open(self.file,'a')
      f.write(code)
      f.close()

   def find(self,item):
      result = mkvar()
      code = '''
      &s %s [token %s -find %s]
      ''' % (result,self,item)
      self.writecode(code)
      return '[ value %s]' % result

   def length(self):
      result = mkvar()
      code = '''
      &s %s [token %s -count]
      ''' % (result,self)
      self.writecode(code)
      return '[value %s]' % result

   def __getitem__(self,i):
      result = mkvar()
      code = '''
      &s %s [extract %s %s]
      ''' % (result,str(i),self)
      self.writecode(code)
      return '[value %s]' % result

   def iterate(self,proc):
      # Do 'proc' to each element
      code = '''
      &do i &list %s
         %s
         &end
      ''' % (self,proc)
      self.writecode(code)

   def compareto(self,validlist):
      # Compare a this list against another known correct list.
      # If an unknown value is found return false, else true  
      result = mkvar()
      code = '''
      &s %s .TRUE.
      &do i &list %s  
         &s found [calc  [token %s -find %%i%%] > 0]
         &if ^ %%found%% &then
            &do
            &s %s .FALSE.
            &end
         &end
      ''' % (result,self,validlist,result)
      self.writecode(code)
      return '[value %s]' % result
      
   def __getslice__(self,i=1,j=0):
      result = mkvar()
      code = '''
      /*
      /* Extracting a slice from a list
      /*
      '''
      self.writecode(code)
      if i != 1:
         code = '&s i %d\n' % i
         self.writecode(code)
      else:
         code = '&s i 1\n'
         self.writecode(code)
      if j != 0:
         code = '&s j %d\n' % j
         self.writecode(code)
      else:
         code = '&s j\n'
         self.writecode(code)

      # Generate code to extract a sublist. The sublist is stored in result
      code = AML.getslice(self.list,result)
      self.writecode(code)
      return List('[value %s]'% result,self.file)

   def isequal(self,other):
      result = mkvar()
      code = AML.isequal(self.list,other.list,result)
      self.writecode(code)
      return '[value %s]' % result

