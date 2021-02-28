#!/usr/bin/env python3

from distutils.core import setup
import platform
import sys

if platform.python_version() < '3':
    sys.exit("Sorry, only python3.6 or > are supported (yet)")

setup(
      name='lzw_compressor',
      version='1.0.0',
      description='Lempel-Ziv-Welch compressor and decompressor',
      author='Andrea Magnani e Lorenzo Stefanelli',
      license='MIT',
      packages=['src'],
      scripts= ['script/compress','script/uncompress', 'script/Compress.sh'],

	  install_requires=['bitstring >= 3', 'bitarray >= 0.9.3', "PyPDF2 >= 1.26.0"]
     )
