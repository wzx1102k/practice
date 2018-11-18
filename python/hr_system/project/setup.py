from distutils.core import setup
import py2exe

import sys
from glob import glob

data_files = [
        ("Stuff", glob(r'C:\Users\yq\Desktop\demo\dist\Stuff\*.*')) 
        ,("dlls", glob(r'C:\Users\yq\Desktop\demo\dist\dlls\*.dll'))                  
        ,("pyds", glob(r'C:\Users\yq\Desktop\demo\dist\pyds\*.pyd'))  
         ]

options = { "py2exe": {
            "bundle_files": 1,
            "dll_excludes": ["MSVCP90.dll","w9xpopen.exe"]
            } 
          }

setup(
name='test'
,options = options
,zipfile = None
,data_files=data_files
,console=['frame.py']
)