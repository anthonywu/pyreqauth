import unittest
from reqauth import RequireAuth


def get_mock_user():
    return {
        "first_name": "foo",
        "last_name": "bar"
        }


class UserNotFound(Exception):
    pass


def handle_user_not_found():
    raise UserNotFound("user is not authenticated in system")


class TestReqAuth(unittest.TestCase):

    def testUserFound(self):
        userop = RequireAuth(get_mock_user, handle_user_not_found)
        @userop
        def get_full_name_add_pargs(user, *pargs):
            return ("%s %s" % (user["first_name"], user["last_name"]), sum(pargs))
        full_name, arg_sum = get_full_name_add_pargs(1, 2, 3)
        self.assertEquals("foo bar", full_name)
        self.assertEquals(6, arg_sum)

    def testUserNotFound(self):
        userop = RequireAuth(lambda: None, handle_user_not_found)
        @userop
        def wont_be_called(user, x, y):
            self.assertFalse(True, "user op function should not be called if user not available")
        self.assertRaises(UserNotFound, wont_be_called, 1, 2)

    def testPargProxy(self):
        userop = RequireAuth(get_mock_user, handle_user_not_found)
        @userop
        def parg_test(user, *pargs):
            self.assertIsNotNone(user)
            self.assertEquals(3, len(pargs))
        parg_test(1, 2, 3)

    def testKwargsProxy(self):
        userop = RequireAuth(get_mock_user, handle_user_not_found)
        @userop
        def parg_test(user, *pargs, **kwargs):
            self.assertIsNotNone(user)
            self.assertEquals(2, len(pargs))
            self.assertEquals(3, len(kwargs))
            self.assertTrue('x' in kwargs)
            self.assertTrue('y' in kwargs)
            self.assertTrue('z' in kwargs)
        parg_test(1, 2, x=3, y=4, z=5)


if __name__ == '__main__':
    unittest.main()

