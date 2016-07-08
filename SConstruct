# SConstruct for enscons

import sys
from distutils import sysconfig
import pytoml as toml
import enscons, enscons.cpyext

metadata = dict(toml.load(open('pyproject.toml')))['tool']['enscons']

# most specific binary, non-manylinux1 tag should be at the top of this list
import wheel.pep425tags
for tag in wheel.pep425tags.get_supported():
    full_tag = '-'.join(tag)
    if not 'manylinux' in tag:
        break

if sys.version_info[0] == 3:
    # This extension will work with Python 3.2+ using Py_LIMITED_API
    full_tag = "cp3-abi3-linux_x86_64"

env = Environment(tools=['default', 'packaging', enscons.generate, enscons.cpyext.generate],
                  PACKAGE_METADATA=metadata,
                  WHEEL_TAG=full_tag,
                  ROOT_IS_PURELIB=False,)

# ask distutils what the extension filename should be
from distutils import dist
from distutils.command.build_ext import build_ext
ext = build_ext(dist.Distribution(dict(name='cryptacular')))
# ext_filename = ext.get_ext_filename('cryptacular.bcrypt._bcrypt')
ext_filename = 'cryptacular/bcrypt/_bcrypt'

import imp
for (suffix, _, _) in imp.get_suffixes():
    if 'abi3' in suffix:
        ext_filename  += suffix # SCons doesn't like double-extensions .a.b in LIBSUFFIX

extension = env.SharedLibrary(target=ext_filename,
        source=['crypt_blowfish-1.2/crypt_blowfish.c',
    'crypt_blowfish-1.2/crypt_gensalt.c',
    'crypt_blowfish-1.2/wrapper.c',
    'cryptacular/bcrypt/_bcrypt.c',], 
        LIBPREFIX='',
        CPPPATH=['crypt_blowfish-1.2'] + env['CPPPATH'],
        parse_flags='-DNO_BF_ASM -DPy_LIMITED_API')

# Only *.py is included automatically by setup2toml.
# Add extra 'purelib' files or package_data here.
py_source = Glob('cryptacular/*.py') + Glob('cryptacular/bcrypt/*.py') + Glob('cryptacular/core/*.py') + Glob('cryptacular/crypt/*.py') + Glob('cryptacular/pbkdf2/*.py')

env.Whl('platlib', py_source + extension, root='')

# Add automatic source files, plus any other needed files.
sdist_source=FindSourceFiles() + ['PKG-INFO', 'setup.py']

sdist = env.Package(
        NAME=env['PACKAGE_NAME'],
        VERSION=env['PACKAGE_METADATA']['version'],
        PACKAGETYPE='src_targz',
        source=sdist_source,
        target=['/'.join(['dist', env['PACKAGE_NAME'] + '-' + env['PACKAGE_VERSION'] + '.tar.gz'])],
        )
