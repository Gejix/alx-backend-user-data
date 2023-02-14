#!/usr/bin/env python3
"""Representation of Authentication class
"""
from flask import request
from typing import List, TypeVar
import re
import os


class Auth:
    """Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require authentication
        """
        if path is not None and excluded_paths is not None:
            for exc_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exc_path[-1] == "*":
                    pattern = "{}.*".format(exc_path[0:-1])
                elif exc_path[-1] == "/":
                    pattern = "{}/*".format(exc_path[0:-1])
                else:
                    pattern = "{}/*".format(exc_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Get current user
        """
        return None

    def session_cookie(self, request=None):
        """Retrieve cookie value from  a request
        """
        if request is None:
            return None

        return request.cookies.get(os.getenv('SESSION_NAME'))
