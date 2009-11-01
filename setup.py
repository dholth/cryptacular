import os
import sys

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
from distutils.core import Extension

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [ ]

setup(name='cryptacular',
      version='0.1',
      description='A pbkdf2 and public-domain bcrypt password hashing framework.',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        ],
      author='Daniel Holth',
      author_email='dholth@fastmail.fm',
      url='http://bitbucket.org/dholth/cryptacular/',
      keywords='bcrypt password security pbkdf2 crypt hash',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      tests_require = requires,
      ext_modules=[
          Extension('cryptacular.bcrypt._bcrypt',
              sources = [
              'crypt_blowfish-1.0.3/crypt_blowfish.c',
              'crypt_blowfish-1.0.3/crypt_gensalt.c',
              'crypt_blowfish-1.0.3/wrapper.c',
              # how do I compile .S with distutils?
              # 'crypt_blowfish-1.0.3/x86.S', 
              ],
              include_dirs = [
              'crypt_blowfish-1.0.3/',
              ]
          )
      ]
      )

