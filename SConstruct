#
# Build cryptacular.
# 'python -m SCons' or run setup.py
#

import sys, os
from distutils import sysconfig
import pytoml as toml
import enscons, enscons.cpyext

metadata = dict(toml.load(open('pyproject.toml')))['tool']['enscons']

# most specific binary, non-manylinux1 tag should be at the top of this list
import wheel.pep425tags
full_tag = '-'.join(next(tag for tag in wheel.pep425tags.get_supported() if not 'manylinux' in tag))
print(full_tag)

if sys.version_info[0] == 3:
    full_tag = '-'.join(next(tag for tag in wheel.pep425tags.get_supported() if 'abi3' in tag))

MSVC_VERSION = None
SHLIBSUFFIX = None
TARGET_ARCH = None  # only set for win32
if sys.platform == 'win32':
    import distutils.msvccompiler
    MSVC_VERSION = str(distutils.msvccompiler.get_build_version()) # it is a float
    SHLIBSUFFIX = '.pyd'    
    TARGET_ARCH = 'x86_64' if sys.maxsize.bit_length() == 63 else 'x86'

env = Environment(tools=['default', 'packaging', enscons.generate, enscons.cpyext.generate],
                  PACKAGE_METADATA=metadata,
                  WHEEL_TAG=full_tag,
                  ROOT_IS_PURELIB=False,
                  MSVC_VERSION=MSVC_VERSION,
                  TARGET_ARCH=TARGET_ARCH)

import pprint
print("distutils compiler invocation:")
pprint.pprint(enscons.cpyext.no_build_ext.output)

# ask distutils what the extension filename should be
from distutils import dist
from distutils.command.build_ext import build_ext
ext = build_ext(dist.Distribution(dict(name='cryptacular')))
# ext_filename = ext.get_ext_filename('cryptacular.bcrypt._bcrypt')
ext_filename = os.path.join('cryptacular', 'bcrypt', '_bcrypt')

import imp
for (suffix, _, _) in imp.get_suffixes():
    if 'abi3' in suffix:
        ext_filename  += suffix # SCons doesn't like double-extensions .a.b in LIBSUFFIX/SHLIBSUFFIX

use_py_limited = 'abi3' in full_tag

extension = env.SharedLibrary(target=ext_filename,
        source=['crypt_blowfish-1.2/crypt_blowfish.c',
    'crypt_blowfish-1.2/crypt_gensalt.c',
    'crypt_blowfish-1.2/wrapper.c',
    'cryptacular/bcrypt/_bcrypt.c',], 
        LIBPREFIX='',
        SHLIBSUFFIX=SHLIBSUFFIX,
        CPPPATH=['crypt_blowfish-1.2'] + env['CPPPATH'],
        parse_flags='-DNO_BF_ASM' + ' -DPy_LIMITED_API' if use_py_limited else '')

# Only *.py is included automatically by setup2toml.
# Add extra 'purelib' files or package_data here.
py_source = Glob('cryptacular/*.py') + Glob('cryptacular/bcrypt/*.py') + Glob('cryptacular/core/*.py') + Glob('cryptacular/crypt/*.py') + Glob('cryptacular/pbkdf2/*.py')

env.Whl('platlib', py_source + extension, root='')

# Add automatic source files, plus any other needed files.
sdist_source=FindSourceFiles() + ['PKG-INFO', 'setup.py']

sdist = env.Package(
        NAME=env['PACKAGE_NAME'],
        VERSION=env['PACKAGE_METADATA']['version'],
        PACKAGETYPE='src_zip',
        source=sdist_source,
        target=['/'.join(['dist', env['PACKAGE_NAME'] + '-' + env['PACKAGE_VERSION'] + '.zip'])],
        )
