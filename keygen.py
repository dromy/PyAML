#!/usr/local/bin/python
#
'''\
generate unique key strings
mocons.lib.persist.keygen.py
jjk  10/02/98  001  
jjk  04/28/99  002  add UniqueKeyObject and UniqueKeyDictionary
jjk  05/03/99  003  
jjk  11/05/99  004  add some addl docs and disclaimers

There are several extras in this, but the
keygen.rtimekey() has been the most useful 
to me in general.

rtimekey() is not optimized for speed, and 
make no claims for it being theoretically 
correct. But it works pretty well for me
for generating universally unique keys
for database-type objects.

*** USE AT YOUR OWN RISK ***
Jeff Kunce <kuncej@mail.conservation.state.mo.us>
'''

import time, whrandom, string, UserDict

def timekey():
	'''answer a (hopefully unique) string key (18 or more characters).
	The key is based on the time and tends to increase in value with
	time (though keys generated quickly may not increase). The first
	characters of all keys will be very similar, so there may
	be problems indexing or hashing these values. see rtimekey().
	jjk  10/02/98'''
	keyval = time.time()	# start with the current time
	keyval = keyval+(whrandom.random()/1000)   #randomize sub-milliseconds
	keystr = str(long(keyval*1000000000))[:-1]  #make 18+ character string
	return(keystr)

def rtimekey():
	'''answer a (hopefully unique) string key (18 or more characters).
	Simply answers the reverse of call to timekey() - making the beginning
	of each key random.
	jjk  10/02/98'''
	keylst = list(timekey())
	keylst.reverse()
	keystr = string.join(keylst,'')
	return(keystr)

SeqKeyLast = {}

def seqkey(seqid='', base=0, incr=1):
	'''answer an integer key that increase with each call
	jjk  10/02/98'''
	try: keyval = SeqKeyLast[seqid]+incr
	except KeyError: keyval = base
	SeqKeyLast[seqid] = keyval
	return(keyval)

class UniqueKeyObject:
	'''a superclass for objects having a unique key
	jjk  04/28/99'''

	def __init__(self, uniqueKey='', uniqueKeyMethod=rtimekey):
		'''initialize an instance of the receiver
		jjk  04/28/99'''
		if (uniqueKey):
			self._uniqueKey = uniqueKey
		else:
			self._uniqueKey = apply(uniqueKeyMethod)

	def uniqueKey(self):
		'''answer the receiver's unique key
		jjk  04/28/99'''
		return(self._uniqueKey)

	def __cmp__(self, aUniqueKeyObject):
		'''Public: compare the receiver to UniqueKeyObject
		jjk  05/03/99'''
		return(cmp(self._uniqueKey, UniqueKeyObject._uniqueKey))

class UniqueKeyDictionary(UserDict.UserDict):
	'''a dictionary of UniqueKeyObjects
	jjk  04/28/99'''

	def add(self, aUniqueKeyObject): 
		'''add aUniqueKeyObject to the receiver
		jjk  04/28/99'''
		UserDict.UserDict.__setitem__(self, aUniqueKeyObject.uniqueKey(), aUniqueKeyObject)

	def remove(self, aUniqueKeyObject): 
		'''remove aUniqueKeyObject from the receiver
		jjk  04/28/99'''
		UserDict.UserDict.__delitem__(self, aUniqueKeyObject.uniqueKey())

	def __setitem__(self, key, item): 
		'''not applicable for this class, use add() instead
		jjk  04/28/99'''
		raise NameError, 'use add() method to add values to UniqueKeyDictionary'

	def __delitem__(self, key): 
		'''not applicable for this class, use remove() instead
		jjk  04/28/99'''
		raise NameError, 'use remove() method to remove values from UniqueKeyDictionary'

	def includes(self, aUniqueKeyObject): 
		'''answer true if aUniqueKeyObject is in the receiver
		jjk  05/03/99'''
		return(self.has_key(aUniqueKeyObject.uniqueKey()))

def demo():
	'''jjk  10/02/98'''
	print 'Here are five increasing keys [timekey()]:'
	for i in range(5):
		print timekey()
	print 'Here are five random keys [rtimekey()]:'
	for i in range(5):
		print rtimekey()
	print 'Here are five sequential keys [seqkey("test",0,5)]:'
	for i in range(5):
		print seqkey('test',0,5)

if (__name__=='__main__'):
	demo()
