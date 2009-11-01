cryptacular
===========

cryptacular is a collection of password hashing functions that share a
common interface. It's designed to make it easy for you to migrate away
from your half-assed custom password scheme. Use bcrypt if you are able
to run C code in your Python and pbkdf2 if you are not.

cryptacular's interface was inspired by zope.password. Unlike
zope.password it includes schemes that are strong enough for modern use
and it does not depend on zope.

http://chargen.matasano.com/chargen/2007/9/7/enough-with-the-rainbow-tables-what-you-need-to-know-about-s.html
explains why bcrypt is a good idea. Computers are fast now. To protect
our users against a leaked password database, we should use password hashes
that take a little longer to check than sha1(salt + hash). bcrypt
and pbkdf2 have parametric complexity so they can be made stronger as
computers continue to get faster.

cryptacular ships with 100% test coverage.

cryptacular.core
----------------

``cryptacular.core`` defines the DelegatingPasswordManager and the
interfaces PasswordChecker and PasswordManager. DelegatingPasswordManager
fallbacks are PasswordChecker instances that need not implement password
encoding, e.g. do not implement InsecurePasswordScheme().encode()

>>> import cryptacular.core
>>> import cryptacular.bcrypt
>>> import cryptacular.pbkdf2
>>> bcrypt = cryptacular.bcrypt.BCRYPTPasswordManager()
>>> pbkdf2 = cryptacular.pbkdf2.PBKDF2PasswordManager()
>>> delegator = cryptacular.core.DelegatingPasswordManager(preferred=bcrypt, fallbacks=(pbkdf2,))
>>> users = {'one':{'password':'xyzzy'}, 'two':{'password':u'hashy the \N{SNOWMAN}'}}
>>> for key in users: users[key]['hash'] = pbkdf2.encode(users[key]['password'])
>>> bcrypt.match(users['one']['password'])
False
>>> def set_hash(hash): users['one']['hash'] = hash
>>> delegator.check(users['one']['hash'], users['one']['password'], setter=set_hash)
True
>>> bcrypt.match(users['one']['hash'])
True
>>> def set_hash(hash): raise Exception("Should not re-set a preferred hash")
>>> delegator.check(users['one']['hash'], users['one']['password'], setter=set_hash)
True
>>> bcrypt.match(users['two']['hash'])
False
>>> pbkdf2.match(users['two']['hash'])
True
>>> delegator.check(users['two']['hash'], users['two']['password'])
True
>>> bcrypt.match(users['two']['hash'])
False
>>> pbkdf2.match(users['two']['hash'])
True

cryptacular.bcrypt
------------------

``cryptacular.bcrypt`` uses ctypes to access the public-domain
crypt_blowfish (http://www.openwall.com/crypt/) which is bundled with
cryptacular. You should use this if you can.

cryptacular.pbkdf2
------------------

``cryptacular.pbkdf2`` applies the pbkdf2 key derivation algorithm
described in RFC 2898 as a password hash. It uses M2Crypto.EVP.pbkdf2
with a Python fallback when M2Crypto is not available.

