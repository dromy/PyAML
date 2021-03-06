# Aml code fragments that can be used as a library
import sys,string
from keygen import rtimekey

# Make some precompiled code to search the error messages for the
# current function name
global findfunc  
findfunc = compile('function = sys.exc_traceback.tb_frame.f_code.co_name',
                   '<string>','exec')

# Make some precompiled code that will force an error
global raiserror
raiserror = compile("1 + ''",'<string>','exec')

def tempcov():
   scratchname = rtimekey()
   return 'TMP' + scratchname[:10]

def mkvar():
   var = 'var' + rtimekey() 
   return var


def header():
   # Generates a call to a main routine
   headercode = '''
   &severity &error &routine bailout

   &call main

   &return
   
   /*==========================================================
   &routine main

   '''
   return headercode

# Maybe this should be in a String class
def getslice(list,result):
   # Takes a list and extracts a substring
   
   code = '''
   &s l1 %s /* list
   &s low [unquote [after [quote %%l1%%] [extract %%i%% %%l1%%]]]
   &if not [null %%j%%] &then
        &do
        &s high [before [quote %%low%%] [extract [calc %%j%% - %%i%%] [unquote %%low%%]]]
        &end
   &else
        &do
        &s high %%low%%
        &end
   &s %s %%high%% /* result
   &dv high low l1 i j
   /*==============================================================
   ''' % (list,result)
   return code

def isequal(list1,list2,result):
   # Force an error so that we can find out the name of this
   # function. We do this in case we need to report it in the
   # aml.
   try:
      exec(raiserror)
   except TypeError:
      exec(findfunc)
   errorcode = '''
   /*
   /* This code was generated by function %s in file %s
   /*
   &s file %s
   &s function %s

   ''' % (function,__file__,__file__,function)
  
   code = '''
   &severity &error &routine bailout
   /*
   /* Test lists have identical elements
   /*
   &s list1 %s
   &s list2 %s
   &s %s .FALSE.
   &if [token %%list1%% -count] = [token %%list2%% -count] &then
      &do
      &do i = 1 &to [token %%list1%% -count]
         &s item1 [upcase [quote[extract %%i%% %%list1%%]]]
         &s item2 [upcase [quote[extract %%i%% %%list2%%]]]
         &ty [value item1] [value item2]
         &s %s [calc %%item1%% = %%item2%%]
         &end
      &end
   ''' % (list1,list2,result,result)
   return errorcode + code

def bailout():
   bailcode = '''
   &return
   /* ==============================================================

   &routine bailout
     &severity &error &ignore
     
     &if [calc [upcase [quote %:program%]] = 'TABLES'] &then quit
     &if [calc [upcase [quote %:program%]] = 'ARCPLOT'] &then quit
     &if [calc [upcase [quote %:program%]] = 'ARCEDIT'] &then quit
     &if [calc [upcase [quote %:program%]] = 'GENERATE'] &then
        &do
        ~
        quit
        &end
     &ty An Error has occurred with the code
     &ty generated by %file% in function %function% 
     &ty [date -cal] [date -AMPM]
     &return &error
   ''' 
   return bailcode

def ismodule(function,module):
   code = '''
   &if not [show program] = %s &then
      &do
      &ty
      &ty MODULE ERROR:
      &ty Cannot run %s from [show program]
      &ty
      &return &error
      &end   
   ''' % (string.upper(module),function)
   return code

