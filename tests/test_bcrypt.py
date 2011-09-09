import unittest
from cryptacular.bcrypt import BCRYPTPasswordManager


try:
    unicode
except NameError:
    unicode = str


class TestBcrypt(unittest.TestCase):

    snowpass = unicode('hashy the \N{SNOWMAN}')

    def setUp(self):
        self.bcrypt = BCRYPTPasswordManager()

    def test_none_1(self):
        self.assertRaises(TypeError, self.bcrypt.encode, None)

    def test_none_2(self):
        self.assertRaises(TypeError, self.bcrypt.check, None, 'xyzzy')

    def test_none_3(self):
        hash = self.bcrypt.encode('xyzzy')
        self.assertRaises(TypeError, self.bcrypt.check, hash, None)

    def test_badhash(self):
        self.assertFalse(
            self.bcrypt.check(
                '$p5k2$400$ZxK4ZBJCfQg=$kBpklVI9kA13kP32HMZL0rloQ1M=',
            self.snowpass))

    def test_shorthash(self):
        def match(hash):
            return True
        bcrypt = BCRYPTPasswordManager()
        bcrypt.match = match
        short_hash = bcrypt.encode(self.snowpass)[:28]
        self.assertRaises(ValueError, bcrypt.check, short_hash, self.snowpass)

    def test_too_few_rounds(self):
        self.assertRaises(ValueError, self.bcrypt.encode, self.snowpass, rounds=1)

    def test_too_many_rounds(self):
        self.assertRaises(ValueError, self.bcrypt.encode,
            self.snowpass, rounds=100)

    def test_emptypass(self):
        self.bcrypt.encode('')

    def test_valid_hash_1(self):
        hash = self.bcrypt.encode(self.snowpass)
        self.assertTrue(self.bcrypt.match(hash))
        self.assertTrue(self.bcrypt.check(hash, self.snowpass))
        self.assertEqual(len(hash), 60)

    def test_valid_hash_2(self):
        password = "xyzzy"
        hash = self.bcrypt.encode(password)
        self.assertTrue(self.bcrypt.check(hash, password))
        self.assertTrue(self.bcrypt.check(unicode(hash), password))
        self.assertFalse(self.bcrypt.check(password, password))
        self.assertNotEqual(self.bcrypt.encode(password),
            self.bcrypt.encode(password))
        hash = self.bcrypt.encode(password, rounds=4)
        self.assertTrue(self.bcrypt.check(hash, password))


if __name__ == '__main__':
    unittest.main()
