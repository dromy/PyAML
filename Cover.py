#!/export/packages/bin/python

#
# Python code for wrapping AML code
#
import string
import AML 
from AML import mkvar
from AML import tempcov
from List import List
from Cursor import Cursor

# Generic cover class
class Cover:
   def __init__(self,name,file):
      self.name = name
      self.function = 'init'
      self.code = ''
      self.file = file
      self.exists()
      #self.hasnodes()
      self.features = {}
      self.items = {}

   def writecode(self,code):
      self.code = self.code + code
      f = open(self.file,'a')
      f.write(code)
      f.close()
      #self.code = self.code + code

   def getcode(self):
      return self.code
      #self.code = ''

   def exists(self):
      # Check that the cover does not exist
      code = '''
      /*
      /* Check if a requested cover exists
      /*
      &if not [exists %s -cover] &then
         &do
         &ty
         &ty
         &ty COVERAGE ERROR:
         &ty Cover %s does not exist
         directory cover 
         &return &error
         &end
      /*=============================================================
      ''' % (self.name,self.name)
      self.writecode(code)

   def outcovexists(self,outcov):
      # For many arc functions an output cover is generated
      # This section of code tests that the name chosen for 
      # the outcover is not the name of an existing cover
      code = '''
      /*
      /* Check that an output cover does not already exist 
      /*
      &if [exists %s -cover] &then
          &do
          &ty
          &ty
          &ty COVERAGE ERROR:
          &ty Coverage name %s already exists. Cannot create cover.
          directory cover
          &return &error

          &end
      /*============================================================
      ''' % (outcov,outcov)
      self.writecode(code)

   def buffer(self,dist,feat):
      self.function = 'buffer'
      if feat == 'arc':
         feat = 'line'
      outcov = tempcov()
      code = '''
      &do
      buffer %s %s # # %s 0.000000000001 %s
      &end
      ''' % (self.name,outcov,dist,feat)
      self.writecode(code)
      return Cover(outcov,self.file)

   def build(self,feat):
      self.function = 'build'
      code = '''
      &do
      build %s %s
      &end
      ''' % (self.name,feat)
      self.writecode(code)

   def checktopology(self,feat):
      # Many functions require that a cover is 
      # built for a certain feature. This code
      # asserts that  the cover is built for a 
      # given feature class
      code = '''
      /*
      /* Check that the cover has the required topology
      /*
      &if not [exists %s -%s] &then
         &do
         &ty 
         &ty 
         &ty FEATURE ERROR in %s:  
         &ty Cover does not have the required feature
         &ty Requested feature: %s
         &ty Existing features: 
         directory featureclass %s
         &return &error 
         &end
      /*===========================================================
      ''' % (self.name,feat,self.name,string.upper(feat),self.name)
      self.writecode(code)

   def checkextratopology(self,feat,features):
      # Checks that a cover is not  built for a certain feature
      # or has uneeded features
      self.function = 'checkextratopology'
      code = '''
      /*
      /* Check that the cover does not have unneeded topology
      /*
      &if [exists %s -%s] &then
         &do
         &ty
         &ty
         &ty FEATURE ERROR 
         &ty Cover %s has %s topology 
         &ty Legal features: %s
         &return &error
         &end
      /*===========================================================
      ''' % (self.name,feat,self.name,string.upper(feat),features)
      self.writecode(code)

   def checkextrafeatures(self,feat,features):
      # Checks that a the cover does not contain unwanted
      # feature types
      tests = {'point':'%dsc$points% > 0',
               'arc':'%dsc$arcs% > 0',
               'polygon':'%dsc$qtopology%'}

      self.function = 'checkextrafeatures'
      self.code = '''
      /*
      /* Checks that a the cover does not contain unwanted
      /* feature classes
      /*
      &describe %s
      &if %s &then
         &do
         &ty
         &ty
         &ty FEATURE ERROR 
         &ty Cover %s has %s features
         &ty Legal features %s
         &end
      /*===========================================================
      ''' % (self.name,tests[feat],self.name,feat,features)
      self.writecode(self.code)

   def checkclean(self):
      self.function = 'checkclean'
      self.code = '''
      /* 
      /* Check that cover is clean
      /*
      &if not [exists %s -clean] &then
         &do
         &ty 
         &ty
         &ty COVERAGE ERROR 
         &ty Cover %s in not clean.
         &ty
         &return &error
         &end
      /*============================================================
      ''' % (self.name,self.name)
      self.writecode(code)

   def checkproj(self):
      self.function = 'checkproj'
      self.code = '''
      /* 
      /* Check that a projection is defined
      /*
      &describe %s
      &if [null %prj$name%] &then
         &do
         &ty
         &ty
         &ty COVERAGE ERROR 
         &ty Cover %s has no projection defined.
         &ty
         &return &error
         &end
      /*============================================================
      ''' % (self.name,self.name)
      self.writecode(code)

      
   def hasnodes(self):
      # None of our data should be built for node
      # This code asserts that the cover does not
      # have node atributes.
      code = '''
      /*
      /* Check that the cover does not have node topology
      /*
      &if [exists %s -node] &then
         &do
         &ty
         &ty
         &ty FEATURE ERROR 
         &ty Cover %s should not have NODE attributes
         &ty Existing features:
         directory featureclass %s

         &return &error
         &end
      /*===========================================================
      ''' % (self.name,self.name,self.name)
      self.writecode(code)

   def checkitem(self,feat,item):
      code = '''
      /*
      /* Check that the cover has a required item
      /*
      &if not [iteminfo %s -%s %s -exists] &then
         &do
         &ty
         &ty 
         &ty ITEM ERROR 
         &ty Item %s does not exist for %s %ss 
         &ty 
         &return &error 
         &end
      /*============================================================
      ''' % (self.name,feat,item,item,self.name,feat)
      self.writecode(code)

   def checkitems(self):
      for f in self.features.keys():
         for i in self.items[f]:
            self.checkitem(f,i)

   def dropitem(self,feat,item):
      types = {'line':'.aat',
               'poly':'.pat',
               'point':'.pat'
              }
      self.checkitem(feat,item)
      code = '''
      /*
      /* Drop item
      /*
      dropitem %s%s %s%s %s
      ''' % (self.name,types[feat],self.name,types[feat], item)
      self.writecode(code)
      
   def validitems(self,feat):
      return List(string.join(self.items[feat]),self.file)

   def checkextraitems(self):
      for f in self.features.keys():
         current = self.validitems(f)
         valid = self.currentitems(f)
         result = valid.isequal(current)
         code = '''
         /*
         /* Check for unwanted items
         /*
         &s bool %s
         &if [calc %%bool%% = .FALSE.] &then
            &do
            &ty
            &ty COVERAGE ERROR
            &ty Cover %s has extra items
            &ty Legal items:
            &ty %s
            &ty Current items:
            &ty %s
            &end
         /* ==============================================================
         ''' % (result,self.name,valid,current)
         self.writecode(code)

   def checkfeatcodes(self):
      # Check current feat_codes against the valid feat_codes
      # for this cover.
      for f in self.features.keys():
         current = self.unique(f,'feat_code')
         valid = self.validitems(f)
         result = current.compareto(valid)
         code = '''
         &if %s = .FALSE. &then
            &do
            &ty ITEM ERROR
            &ty Cover %s has illegal feat_codes for feature %s
            &ty Current feat_codes:
            &ty %s
            &ty Legal feat_codes:
            &ty %s
            &end
         ''' % (result,self.name,f,current,valid) 
         self.writecode(code)
             
   def copy(self,newname):
      self.function = 'copy'
      self.outcovexists(newname)
      code = '''
      copy %s %s
      ''' % (self.name,newname)
      self.writecode(code)
      return Cover(newname,self.file)

   def rename(self,newname):
      self.function = 'rename'
      self.outcovexists(newname)
      code = '''
      rename %s %s
      ''' % (self.name,newname)
      self.writecode(code)
      return Cover(newname,self.file)
      
   def unique(self,feat,item):
      self.function = 'unique'
      self.checktopology(feat)
      self.checkitem(feat,item)
      func = '[listunique %s -%s %s]' % (self.name,feat,item)
      return List(func,self.file)

   def getitems(self,feat):
      self.function = 'getitems'
      self.checktopology(feat)
      func = '[listitem %s -%s]' % (self.name,feat)
      return List(func,self.file) 

   def currentitems(self,feat):
      return (self.getitems(feat))

   def arcpoint(self,item):
      self.function = 'arcpoint'
      outcov = tempcov()
      self.outcovexists(outcov)
      self.checktopology('arc')
      self.checkitem('arc',item)
      code = '''
      arcpoint %s %s line %s 
      ''' % (self.name,outcov,item)
      self.writecode(code)
      return Cover(outcov,self.file)

   def clip(self,ccov,feat):
      self.function = 'clip'
      outcov = tempcov()
      ccov.checktopology('polygon')
      self.outcovexists(outcov)
      self.checktopology(feat)
      code = '''
      clip %s %s %s %s 0.0000000000001
      ''' % (self.name,ccov.name,outcov,feat)
      self.writecode(code)
      return Cover(outcov,self.file)

   def erase(self,ercov,feat):
      self.function = 'erase'
      ercov.checktopology('polygon')
      outcov = tempcov()
      self.outcovexists(outcov)
      self.checktopology(feat)
      code = '''
      clip %s %s %s %s 0.0000000000001
      ''' % (self.name,ercov.name,outcov,feat)
      self.writecode(code)
      return Cover(outcov,self.file)

   def export(self):
      self.function = 'export'
      code = '''
      export cover %s %s
      ''' % (self.name,self.name)
      self.writecode(code)

   def reselect(self,feat,query):
      self.function = 'reselect'
      self.checktopology(feat)
      outcov = tempcov()
      self.outcovexists(outcov)
      code = '''
      reselect %s %s %s 
      res %s
      ~
      n
      n
      ''' % (self.name,outcov,feat,query)
      self.writecode(code)
      return Cover(outcov,self.file)

   def reduce(self,feat,query):
      self = self.reselect(feat,query)

   def identity(self,icov,feat):
      self.function = 'identity'
      icov.checktopology('polygon')
      outcov = tempcov()
      self.outcovexists(outcov)
      self.checktopology(feat)
      code = '''
      identity %s %s %s %s 0.00000000001 
      ''' % (self.name,icov.name,outcov,feat)
      self.writecode(code)
      return Cover(outcov,self.file)

   def intersect(self,icov,feat):
      self.function = 'intersect'
      icov.checktopology('polygon')
      outcov = tempcov()
      self.outcovexists(outcov)
      self.checktopology(feat)
      code = '''
      intersect %s %s %s %s 0.00000000001
      ''' % (self.name,icov.name,outcov,feat)
      self.writecode(code)
      return Cover(outcov,self.file)

   def near(self,ncov,feat,rad):
      self.function = 'near'
      if feat == 'point':
         ncov.checktopology('point')
      elif feat == 'arc':
         ncov.checktopology('arc')
      outcov = tempcov()
      self.outcovexists(outcov)
      code = '''
      near %s %s %s %s %s
      ''' % (self.name,ncov.name,feat,rad,outcov)
      self.writecode(code)
      return Cover(outcov,self.file)

   def union(self,ucov):
      self.function = 'union'
      self.checktopology('polygon')
      ucov.checktopology('polygon')
      outcov = tempcov()
      self.outcovexists(outcov)
      code = '''
      union %s %s %s 0.000000001
      ''' % (self.name,ucov.name,outcov)
      self.writecode(code)
      return Cover(outcov,self.file)
 
   def close(self):
      code = '''
      &if [show program] = ARCEDIT &then
         &do
         removeedit %s yes
         &end
      ''' % (self.name)
      self.writecode(code)

   def kill(self):
      self.function = 'kill'
      self.exists()
      code = '''
      kill %s all
      ''' % self.name
      self.writecode(code)

   def addxy(self):
      self.function = 'addxy'
      code = '''
      addxy %s point
      ''' % self.name
      self.writecode(code)

   def editfeature(self,feat):
      self.function = 'editfeature'
      # assert that we are in arcedit
      self.writecode(AML.ismodule(self.function,'ARCEDIT'))
      self.checktopology(feat)
      code = '''
      editfeature %s
      ''' % feat
      self.writecode(code)
      
      
      
# An example to show how to usr the Cover and Cursor objects
# This example takes the junction features out of two covers
# buffers them and compares the buffer polygons to check that they
# are coincident in both covers.
if (__name__ == '__main__'):
   import sys
   import EditSession
   file = string.lower(tempcov()) + '.aml'

   f = Cover('i5308fm',file)
   w = Cover('i5308wm',file)
   fjunc = f.reselect('arc',"feat_code = 'junction'")
   wjunc = w.reselect('arc',"lpoly# = 1 | rpoly# = 1")
   wjunc2 = wjunc.reselect('arc',"feat_code = 'junction'")
   fjbuf = fjunc.buffer(1,'line')
   wjbuf = wjunc2.buffer(1,'line')
   wfunion = fjbuf.union(wjbuf)
   wfunion.addxy()

   cur = Cursor(wfunion,'polygon','ro','%s-id = 0 & area > 0'% fjbuf.name)
   proc = '''
          &ty
          &ty Waterbody junction does not have corresponding framework junction
          &ty at [truncate %s],[truncate %s]
          &ty
          ''' % (cur.getitem('x-coord'),cur.getitem('y-coord'))

   cur.iterate(proc)
   cur.remove()

   cur = Cursor(wfunion,'polygon','ro','%s-id = 0 & area > 0' % wjbuf.name)
   proc = '''
          &ty
          &ty Framework junction does not have corresponding waterbody junction
          &ty at [truncate %s],[truncate %s]
          &ty
          ''' % (cur.getitem('x-coord'),cur.getitem('y-coord'))

   cur.iterate(proc)
   cur.remove()

   wjunc.kill()
   fjunc.kill()
   wjunc2.kill()
   fjbuf.kill()
   wjbuf.kill()
   #wfunion.kill()
   es = EditSession.EditSession(file)
   cov = es.edit(wfunion.name)
   cov.editfeature('poly')
   
   sys.stderr.write('%s\n' % file)
