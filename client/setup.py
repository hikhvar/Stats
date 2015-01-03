#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from distutils.core import setup
import py2exe
from glob import glob
#import numpy
import sys
import matplotlib
#import scipy.stats
opts={"py2exe":{"bundle_files"}}
sys.argv.append('py2exe')
opts = {'py2exe': 
	{"bundle_files" : 3,
	"includes" : [ "matplotlib.backends", "pylab","numpy"],#, 'scipy.sparse.csgraph._validation', 'scipy.special._ufuncs_cxx'], 
	'excludes':['_gtkagg', '_tkagg', '_agg2', '_cairo', '_cocoaagg', '_fltkagg', '_gtk', '_gtkcairo', 'scipy'], 
	'dll_excludes': ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll']}}

data_files = [("Microsoft.VC90.CRT", 
    glob(r'C:\Windows\winsxs\x86_microsoft.vc90\*.*'))]
packages=[
    'pandas',
    'matplotlib',
    'numpy'
]

setup(windows=['schiessdb.py'],zipfile="library.zip",options=opts,data_files=matplotlib.get_py2exe_datafiles())