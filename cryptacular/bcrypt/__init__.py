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

from cryptacular.bcrypt._bcrypt import crypt_rn, crypt_gensalt_rn
import cryptacular.core

class BCRYPTPasswordManager(object):

    SCHEME = "BCRYPT"
    PREFIX = "$2a$"
    ROUNDS = 10

    _bcrypt_syntax = re.compile('\$2a\$[0-9]{2}\$[./A-Za-z0-9]{53}')

    def encode(self, password, rounds=None):
        """Hash a password using bcrypt.

        Note: only the first 72 characters of password are significant.
        """
        work_factor = rounds or self.ROUNDS
        settings = crypt_gensalt_rn('$2a$', work_factor, os.urandom(16))
        if settings is None:
            raise ValueError("_bcrypt.crypt_gensalt_rn returned None") # pragma NO COVERAGE
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        if not isinstance(password, str):
            raise TypeError("password must be a str")
        rc = crypt_rn(password, settings)
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
        rc = crypt_rn(password, encoded)
        if rc is None:
            raise ValueError("_bcrypt.crypt_rn returned None")
        return cryptacular.core._cmp(rc, encoded)

    def match(self, hash):
        """Return True if hash looks like a BCRYPT password hash."""
        return self._bcrypt_syntax.match(hash) is not None

