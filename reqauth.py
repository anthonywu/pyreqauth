"""
Copyright (c) 2012 Anthony Wu

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

class RequireAuth(object):
    """
    A decorator that attempts to fetch an authenticated user object for a function that assumes user is authenticated.
    If the user is logged in, this decorator automagically inserts a valid user object argument as the first arg of the function.
    If the user is not logged in, this decorator will call a failure handler.

    Example:

    >> def get_user():
           return {"first_name": "Anthony", "last_name": "Wu"}

    >> def handle_auth_fail():
           raise Exception("Cannot retrieve user!")

    >> require_user = RequireAuth(get_user, handle_auth_fail)

    >> @require_user
    >> def handle_user(user, foo, bar, **kwargs):
           # do something with user, foo, bar, and kwargs
           ......
           ......

    Now you can invoke handle_user without explicitly providing user object. It'll be automatically provided:
    >> handle_user(1, 2)
    """
    def __init__(self, user_getter, failure_handler):
        """Instantiates a decorator that modifies user operation functions

        Arguments:
        user_getter -- a user retrieval function that takes no arguments
        failure_handler -- a function to be called if user cannot be retrieved
        """
        self.user_getter = user_getter
        self.failure_handler = failure_handler

    def __call__(self, user_handler_fn):
        """Returns a wrapped function around user_handler_fn.

        Arguments:
        user_handler_fn -- a function that assumes existence of an user object

        Returns: wrapper function around user_handler_fn that behaves as follows:
        - if the user is available, insert user object as first positional argument for user_handler_fn 
        - if the user is not available, call the failure_handler
        """
        import functools
        @functools.wraps(user_handler_fn)
        def wrapper(*args, **kwargs):
            user_obj = self.user_getter()
            if user_obj:
                return user_handler_fn(user_obj, *args, **kwargs)
            else:
                self.failure_handler()
        return wrapper
