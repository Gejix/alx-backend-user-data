#!/usr/bin/env python3
"""Representation of BasicAuth class
"""
import base64
from api.v1.auth.auth import Auth
from typing import TypeVar, Tuple
from models.user import User
import re


class BasicAuth(Auth):
    """Basic authentication
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """Extract based64 authorization header
        """
        if isinstance(authorization_header, str):
            pattern = r'Basic (?P<token>.+)'
            match = re.fullmatch(pattern, authorization_header.strip())
            if match is not None:
                return match.group('token')
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """ decode base64 authorization header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf8')
        except Exception as e:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header:
            str) -> Tuple[str, str]:
        """ Extract user credentials
        """
        if isinstance(decoded_base64_authorization_header, str):
            pattern = r'(?P<email>.[^:]+):(?P<password>.+)'
            match = re.fullmatch(
                pattern,
                decoded_base64_authorization_header.strip())
            if match is not None:
                email = match.group('email')
                password = match.group('password')
                return (email, password)
        return (None, None)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Get user Object based on user's email and password
        """
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        credentials = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(*credentials)
