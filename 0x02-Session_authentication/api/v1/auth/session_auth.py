#!/usr/bin/env python3
"""Representation of session authentication class
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Session auth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session id for user
        """
        if user_id and isinstance(user_id, str):
            self.session_id = str(uuid.uuid4())
            self.user_id_by_session_id[self.session_id] = user_id
            return self.session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieve user_id based on session ID
        """
        if session_id and isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value:
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """Destroy session
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        try:
            del self.user_id_by_session_id[session_id]
        except Exception:
            pass

        return True
