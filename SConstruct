# Starter SConstruct for enscons

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

# full_tag = py2.py3-none-any # pure Python packages compatible with 2+3

env = Environment(tools=['default', 'packaging', enscons.generate, enscons.cpyext.distutool],
                  PACKAGE_METADATA=metadata,
                  WHEEL_TAG=full_tag,
                  ROOT_IS_PURELIB=False)

# ask distutils what the extension filename should be
from distutils import dist
from distutils.command.build_ext import build_ext
ext = build_ext(dist.Distribution(dict(name='cryptacular')))
ext_filename = ext.get_ext_filename('cryptacular.bcrypt._bcrypt')

extension = env.SharedLibrary(target=ext_filename,
        source=['crypt_blowfish-1.2/crypt_blowfish.c',
    'crypt_blowfish-1.2/crypt_gensalt.c',
    'crypt_blowfish-1.2/wrapper.c',
    'cryptacular/bcrypt/_bcrypt.c',], 
        LIBPREFIX='',
        CPPPATH=env['CPPPATH'] + ['crypt_blowfish-1.2'],
        parse_flags='-DNO_BF_ASM')

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
