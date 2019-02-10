class Cursor:
   def __init__(self,cover,feat,access,query):
      self.name = 'ptr'
      self.cover = cover
      code = '''
      cursor %s declare %s %s %s %s
      ''' % (self.name,self.cover.name,feat,access,query)
      self.cover.writecode(code)

   def open(self):
      code = '''
      cursor % open
      ''' % self.name
      self.cover.writecode(code)

   def close(self):
      code = '''
      cursor %s close
      ''' % self.name
      self.cover.writecode(code)

   def remove(self):
      code = '''
      cursor %s remove
      ''' % self.name
      self.cover.writecode(code)

   def first(self):
      code = '''
      cursor %s first
      ''' % self.name
      self.cover.writecode(code)

   def next(self):
      code = '''
      cursor %s next
      ''' % self.name
      self.cover.writecode(code)

   def previous(self):
      code = '''
      cursor %s previous
      ''' % self.name
      self.cover.writecode(code)

   def iterate(self,procedure):
      code = '''
      cursor %s open
      &if %%:%s.aml$nsel%% > 0 &then
         &do
         &do &while %%:%s.aml$next%%
            %s
            cursor %s next
            &end
         &end
      ''' % (self.name,self.name,self.name,procedure,self.name)
      self.cover.writecode(code)

   def getitem(self,item):
      return "%%:%s.%s%%" % (self.name,item)

