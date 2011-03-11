cryptacular
===========

Hash responsibly::

    from cryptacular.bcrypt import BCRYPTPasswordManager
    manager = BCRYPTPasswordManager()
    hashed = manager.encode('password')
    if manager.check(hashed, 'password'):
        pass # let them in

cryptacular is a collection of strong password hashing functions that
share a common interface, and a nice way to use bcrypt as a password
hash. It's designed to make it easy for you to migrate away from your
half-assed custom password scheme. Compared with popular choices like
plain text or single rounds of md5 or sha, strong password hashes greatly
increase the computational cost of obtaining users' passwords from a
leaked password database.

cryptacular's interface was inspired by zope.password but cryptacular does
not depend on zope and implements much stronger algorithms. cryptacular
also provides a convenient way to recognize and upgrade obsolete password
hashes on the fly when users log in with their correct password.

`z3c.bcrypt`_ integrates cryptacular into zope.password.

http://chargen.matasano.com/chargen/2007/9/7/enough-with-the-rainbow-tables-what-you-need-to-know-about-s.html
explains why bcrypt is a good idea. Computers are fast now. To protect
our users against a leaked password database, we should use password
hashes that take a little longer to check than sha1(salt + hash). bcrypt
and pbkdf2 have this property. They also have parametric complexity so
they can be made stronger as computers continue to get faster.

cryptacular ships with 100% test coverage.

.. _`z3c.bcrypt`: http://pypi.python.org/pypi/z3c.bcrypt

cryptacular.core
----------------

``cryptacular.core`` defines the ``DelegatingPasswordManager``
and the interfaces (abstract base classes) ``PasswordChecker`` and
``PasswordManager``.

``DelegatingPasswordManager`` is the recommended way to use
cryptacular. ``DelegatingPasswordManager`` holds a preferred
``cryptacular.core.PasswordManager`` instance that can
encode and check password hashes and a list of fallback
``cryptacular.core.PasswordChecker`` instances that are only
required to be able to check password hashes (no need to implement
``InsecurePasswordHash.encode()``). When asked to check a password hash
against a plaintext password, ``DelegatingPasswordManager`` finds the
first item in its list that understands the given hash format and uses
it to check the password. If the password was correct but not in the
preferred hash format, ``DelegatingPasswordManager`` will re-hash the given
password using its preferred ``PasswordManager``.

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

``cryptacular.bcrypt`` uses a C extension module to call the public-domain
crypt_blowfish (http://www.openwall.com/crypt/) which is bundled with
cryptacular. You should use this if you can.

cryptacular.pbkdf2
------------------

``cryptacular.pbkdf2`` applies the pbkdf2 key derivation algorithm
described in RFC 2898 as a password hash. It uses M2Crypto.EVP.pbkdf2
with a Python fallback when M2Crypto is not available. You can use this
even if you cannot run C extension modules in your Python.

cryptacular.crypt
-----------------

``cryptacular.crypt`` uses Python's builtin ``crypt`` module, available on
Unix, to hash passwords. It takes a string such as '$1$' as an argument
to determine which kind of hash the underlying ``crypt()`` function will
produce (see ``man crypt`` for details). ``crypt()`` can even provide
bcrypt hashes if you are lucky; the SHA hashes invented for RedHat are also
good.

On my Ubuntu system::

    from cryptacular.crypt import CRYPTPasswordManager, SHA256CRYPT
    manager = CRYPTPasswordManager(SHA256CRYPT)
    manager.encode('secret')
    >>> '$5$Ka9M/5GqJWMCnLI7$ZR0k9g2NlnXvgjjDYmobVUuLzfn/Tmo.vnW4WvW5Tx/'
    manager.encode('secret')
    >>> '$5$o4RUq2zuVWYWZpuq$35VyAVxfeL4sQ9//ODNw8jIDW7khJ5s0lUlXCHJ6WZ2'

