# Copyright (c) 2009 Daniel Holth <dholth@fastmail.fm>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__all__ = ['BCRYPTPasswordManager']

import os
import re
from ctypes import cdll
from ctypes import c_char_p, c_void_p, c_int, c_ulong, create_string_buffer

_bcrypt = cdll.LoadLibrary(
        os.path.join(os.path.dirname(__file__), '_bcrypt.so')
        )

# char *crypt_rn(const char *key, const char *setting, void *data, int size);
_bcrypt.crypt_rn.restype = c_char_p
_bcrypt.crypt_rn.argtypes = [c_char_p, c_char_p, c_void_p, c_int]

# char *crypt_gensalt_rn(const char * prefix, unsigned long count,
#                        const char *input, int size,
#                        char *output, int output_size);
_bcrypt.crypt_gensalt_rn.restype = c_char_p
_bcrypt.crypt_gensalt_rn.argtypes = [c_char_p, c_ulong, c_char_p, c_int, c_char_p, c_int]

class BCRYPTPasswordManager(object):

    SCHEME = "BCRYPT"
    PREFIX = "$2a$"

    _bcrypt_syntax = re.compile('\$2a\$[0-9]{2}\$[./A-Za-z0-9]{53}')

    def encode(self, password):
        """Hash a password using bcrypt.

        Note: only the first 72 characters of password are significant.
        """
        settings = create_string_buffer(30)
        data = create_string_buffer(61)
        salt = os.urandom(16)
        rc = _bcrypt.crypt_gensalt_rn('$2a$', 10, salt, len(salt), settings, len(settings))
        if rc is None:
            raise ValueError("_bcrypt.crypt_gensalt_rn returned None") # pragma NO COVERAGE
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        if not isinstance(password, str):
            raise TypeError("password must be a str")
        rc = _bcrypt.crypt_rn(password, settings, data, len(data))
        if rc is None: 
            raise ValueError("_bcrypt.crypt_rn returned None") # pragma NO COVERAGE
        return rc

    def check(self, encoded, password):
        """Check a bcrypt password hash against a password."""
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        if isinstance(encoded, unicode):
            encoded = encoded.encode('utf-8')
        if not isinstance(password, str):
            raise TypeError("password must be a str")
        if not isinstance(encoded, str):
            raise TypeError("encoded must be a str")
        if not self.match(encoded):
            return False
        data = create_string_buffer(61)
        rc = _bcrypt.crypt_rn(password, encoded, data, len(data))
        if rc is None:
            raise ValueError("_bcrypt.crypt_rn returned None")
        return rc == encoded

    def match(self, hash):
        """Return True if hash looks like a BCRYPT password hash."""
        return self._bcrypt_syntax.match(hash) is not None

