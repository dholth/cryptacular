# Tests for the pbkdf2 module.
# Copyright 2004 Matt Johnston <matt @ ucc asn au>
# Copyright 2009 Daniel Holth <dholth@fastmail.fm>
# This code may be freely used and modified for any purpose.
from nose.tools import eq_, raises, assert_not_equal
from cryptacular.pbkdf2 import PBKDF2PasswordManager
from binascii import hexlify, unhexlify
from pbkdf2 import *

def test():
    # test vector from rfc3211
    password = 'password'
    salt = unhexlify( '1234567878563412' )
    password = 'All n-entities must communicate with other n-entities via n-1 entiteeheehees'
    itercount = 500
    keylen = 16
    ret = pbkdf2( password, salt, itercount, keylen )
    hexret = ' '.join(map(lambda c: '%02x' % ord(c), ret)).upper()
    eq_(hexret, "6A 89 70 BF 68 C9 2C AE A8 4A 8D F2 85 10 85 86")

    # from botan
    password = unhexlify('6561696D72627A70636F706275736171746B6D77')
    expect = 'C9A0B2622F13916036E29E7462E206E8BA5B50CE9212752EB8EA2A4AA7B40A4CC1BF'
    salt = unhexlify('45248F9D0CEBCB86A18243E76C972A1F3B36772A')
    keylen = 34
    itercount = 100
    ret = pbkdf2( password, salt, itercount, keylen )
    hexret = hexlify(ret).upper()
    eq_(hexret, expect)

    eq_(xorstr('foo', 'foo'), '\x00\x00\x00')

def test_passwordmanager():
    from base64 import urlsafe_b64decode
    manager = PBKDF2PasswordManager()
    # Never call .encode with a salt.
    salt = urlsafe_b64decode('ZxK4ZBJCfQg=')
    text = u"hashy the \N{SNOWMAN}"
    hash = manager.encode(text, salt)
    eq_(hash, '$p5k2$1000$ZxK4ZBJCfQg=$jJZVscWtO--p1-xIZl6jhO2LKR0=')
    password = "xyzzy"
    hash = manager.encode(password)
    assert manager.check(hash, password)
    assert manager.check(unicode(hash), password)
    assert not manager.check(password, password)
    assert_not_equal(manager.encode(password), manager.encode(password))
    hash = manager.encode(text, salt, rounds=1)
    eq_(hash, "$p5k2$1$ZxK4ZBJCfQg=$Kexp0NAVgxlDwoA-TS34o8o2Okg=")
    assert manager.check(hash, text)

@raises(ValueError)
def test_xorstr():
    xorstr('foo', 'quux')

if __name__ == "__main__":
    test() # pragma: NO COVERAGE
