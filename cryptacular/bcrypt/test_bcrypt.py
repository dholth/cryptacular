from nose.tools import eq_, raises, assert_false, assert_true, assert_not_equal
import cryptacular.bcrypt
from cryptacular.bcrypt import BCRYPTPasswordManager

class TestBCRYPTPasswordManager(object):
    snowpass = u"hashy the \N{SNOWMAN}"

    def setup(self):
        self.manager = BCRYPTPasswordManager()

    @raises(TypeError)
    def test_None1(self):    
        self.manager.encode(None)

    @raises(TypeError)
    def test_None2(self):    
        self.manager.check(None, 'xyzzy')

    @raises(TypeError)
    def test_None3(self):
        hash = self.manager.encode('xyzzy')
        self.manager.check(hash, None)

    def test_badhash(self):
        eq_(self.manager.check('$p5k2$400$ZxK4ZBJCfQg=$kBpklVI9kA13kP32HMZL0rloQ1M=', self.snowpass), False)

    @raises(ValueError)
    def test_shorthash(self):
        manager = BCRYPTPasswordManager()
        def match(hash):
            return True
        manager.match = match
        short_hash = manager.encode(self.snowpass)[:28]
        assert_true(manager.match(short_hash))
        manager.check(short_hash, self.snowpass)

    def test_emptypass(self):
        self.manager.encode('')

    def test_general(self):
        manager = self.manager
        hash = manager.encode(self.snowpass)
        eq_(manager.match(hash), True)
        eq_(len(hash), 60)
        assert_true(manager.check(hash, self.snowpass))
        password = "xyzzy"
        hash = manager.encode(password)
        assert_true(manager.check(hash, password))
        assert_true(manager.check(unicode(hash), password))
        assert_false(manager.check(password, password))
        assert_not_equal(manager.encode(password), manager.encode(password))
