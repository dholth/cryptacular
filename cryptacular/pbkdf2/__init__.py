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

__all__ = ['PBKDF2PasswordManager']

import os
from base64 import urlsafe_b64encode, urlsafe_b64decode
import cryptacular.core
try: # pragma NO COVERAGE
    import M2Crypto.EVP
    _pbkdf2 = M2Crypto.EVP.pbkdf2
except (ImportError, AttributeError): # pragma NO COVERAGE
    from . import pbkdf2
    _pbkdf2 = pbkdf2.pbkdf2

class PBKDF2PasswordManager(object):

    SCHEME = "PBKDF2"
    PREFIX = "$p5k2$"
    ROUNDS = 1<<12

    def encode(self, password, salt=None, rounds=None, keylen=20):
        if salt is None:
            salt = os.urandom(16)
        rounds = rounds or self.ROUNDS
        if isinstance(password, unicode):
            password = password.encode("utf-8")
        key = _pbkdf2(password, salt, rounds, keylen)
        hash = "%s%x$%s$%s" % (
                self.PREFIX,
                rounds,
                urlsafe_b64encode(salt),
                urlsafe_b64encode(key))
        return hash

    def check(self, encoded, password):
        if isinstance(encoded, unicode):
            encoded = encoded.encode("utf-8")
        if not self.match(encoded):
            return False
        iter, salt, key = encoded[len(self.PREFIX):].split('$')
        iter = int(iter, 16)
        salt = urlsafe_b64decode(salt)
        keylen = len(urlsafe_b64decode(key))
        hash = self.encode(password, salt, iter, keylen)
        return cryptacular.core._cmp(hash, encoded)

    def match(self, encoded):
        """True if encoded appears to match this scheme."""
        return encoded.startswith(self.PREFIX)

