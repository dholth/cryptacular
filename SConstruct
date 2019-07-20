#
# Build cryptacular.
# `scons` or run setup.py
#

import sys, os, os.path
import distutils.sysconfig
import pytoml as toml
import enscons, enscons.cpyext

metadata = dict(toml.load(open("pyproject.toml")))["tool"]["enscons"]

full_tag = enscons.get_abi3_tag()

MSVC_VERSION = None
SHLIBSUFFIX = None
TARGET_ARCH = None  # only set for win32
if sys.platform == "win32":
    import distutils.msvccompiler

    MSVC_VERSION = str(distutils.msvccompiler.get_build_version())  # it is a float
    SHLIBSUFFIX = ".pyd"
    TARGET_ARCH = "x86_64" if sys.maxsize.bit_length() == 63 else "x86"

env = Environment(
    tools=["default", "packaging", enscons.generate, enscons.cpyext.generate],
    PACKAGE_METADATA=metadata,
    WHEEL_TAG=full_tag,
    MSVC_VERSION=MSVC_VERSION,
    TARGET_ARCH=TARGET_ARCH,
)

use_py_limited = "abi3" in full_tag

ext_filename = enscons.cpyext.extension_filename(
    "cryptacular.bcrypt._bcrypt", abi3=use_py_limited
)

extension = env.SharedLibrary(
    target=ext_filename,
    source=[
        "crypt_blowfish-1.2/crypt_blowfish.c",
        "crypt_blowfish-1.2/crypt_gensalt.c",
        "crypt_blowfish-1.2/wrapper.c",
        "cryptacular/bcrypt/_bcrypt.c",
    ],
    LIBPREFIX="",
    SHLIBSUFFIX=SHLIBSUFFIX,
    CPPPATH=["crypt_blowfish-1.2"] + env["CPPPATH"],
    CPPFLAGS=["-D__SKIP_GNU"],
    parse_flags="-DNO_BF_ASM" + " -DPy_LIMITED_API=0x03030000"
    if use_py_limited
    else "",
)

# Only *.py is included automatically by setup2toml.
# Add extra 'purelib' files or package_data here.
py_source = (
    Glob("cryptacular/*.py")
    + Glob("cryptacular/bcrypt/*.py")
    + Glob("cryptacular/core/*.py")
    + Glob("cryptacular/crypt/*.py")
    + Glob("cryptacular/pbkdf2/*.py")
)

platlib = env.Whl("platlib", py_source + extension, root="")
whl = env.WhlFile(source=platlib)

# Add automatic source files, plus any other needed files.
sdist_source = list(
    set(
        FindSourceFiles()
        + ["PKG-INFO", "setup.py"]
        + Glob("crypt_blowfish-1.2/*", exclude=["crypt_blowfish-1.2/*.os"])
    )
)

sdist = env.SDist(source=sdist_source)
env.Alias("sdist", sdist)

env.Default(whl, sdist)
