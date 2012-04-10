import os
import sys

from setuptools import setup, find_packages
from distutils.core import Extension

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

tests_require = ["nose", "coverage"]

setup(name='cryptacular',
      version='1.4.1',
      description='A password hashing framework with bcrypt and pbkdf2.',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: C",
        "Topic :: Security :: Cryptography",
        ],
      author='Daniel Holth',
      author_email='dholth@fastmail.fm',
      url='http://bitbucket.org/dholth/cryptacular/',
      keywords='bcrypt password security pbkdf2 crypt hash',
      license='MIT',
      packages=find_packages(),
      namespace_packages = ['cryptacular'],
      include_package_data=True,
      zip_safe=False,
      install_requires = ['pbkdf2', 'setuptools'],
      tests_require = tests_require,
      extras_require = dict(test=tests_require),
      test_suite = 'nose.collector',
      ext_modules=[
          Extension('cryptacular.bcrypt._bcrypt',
              sources = [
              'crypt_blowfish-1.2/crypt_blowfish.c',
              'crypt_blowfish-1.2/crypt_gensalt.c',
              'crypt_blowfish-1.2/wrapper.c',
              'cryptacular/bcrypt/_bcrypt.c',
              # how do I compile .S with distutils?
              # 'crypt_blowfish-1.0.3/x86.S', 
              ],
              define_macros = [ ('NO_BF_ASM', None) ],
              include_dirs = [
              'crypt_blowfish-1.2/',
              ]
          )
      ]
      )

