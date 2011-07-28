# -*- coding: utf-8 -*-
"""
Cryptacular password manager based on builtin ``crypt`` module (available
on Unix). Available crypt functions will vary by system. See ``man crypt``.

Usage::

    try:
        manager = CRYPTPasswordManager(cryptacular.crypt.SHA256CRYPT)
        hashed = manager.encode('secret')
        assert manager.check(hashed, 'secret') == True
    except NotImplementedError:
        print "SHA256CRYPT is not implemented on your system."
"""
# Copyright (c) 2011 Daniel Holth <dholth@fastmail.fm>
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

__all__ = ['CRYPTPasswordManager', 'OLDCRYPT', 'MD5CRYPT', 'SHA256CRYPT',
    'SHA512CRYPT', 'BCRYPT', 'available']

import os
import re
import crypt
import base64

import cryptacular.core

OLDCRYPT = ""
BCRYPT = "$2a$"
MD5CRYPT = "$1$"
SHA256CRYPT = "$5$"
SHA512CRYPT = "$6$"

def available(prefix, _crypt=crypt.crypt):
    # Lame 'is implemented' check.
    l = len(_crypt('implemented?', prefix + 'xyzzy'))
    if prefix == OLDCRYPT:
        if l != 13:
           return False
    elif l < 26:
        return False
    return True

class CRYPTPasswordManager(object):
    _crypt = crypt.crypt
    def __init__(self, prefix):
        """prefix: $1$ etc. indicating hashing scheme."""
        self.PREFIX = prefix
        if not available(prefix, self._crypt):
            raise NotImplementedError

    def encode(self, password):
        """Hash a password using the builtin crypt module."""
        salt = self.PREFIX + base64.b64encode(os.urandom(12), altchars='./')
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        if not isinstance(password, str):
            raise TypeError("password must be a str")
        rc = self._crypt(password, salt)
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
        rc = self._crypt(password, encoded)
        return cryptacular.core._cmp(rc, encoded)

    def match(self, hash):
        """Return True if hash starts with our prefix."""
        return hash.startswith(self.PREFIX)

