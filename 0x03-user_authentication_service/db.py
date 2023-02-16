#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """
    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine(
            "sqlite:///a.db",
            echo=False,
            connect_args={"check_same_thread": False})
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Add user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ Find user by key_pairs arguements
        """
        if not kwargs or not self.valid_query_args(**kwargs):
            raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()

        if not user:
            raise NoResultFound
        else:
            return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user based on user ID
        """
        if not self.valid_query_args(**kwargs):
            raise ValueError

        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            setattr(user, k, v)

        self._session.commit()

    def valid_query_args(self, **kwargs):
        """Get users table columns
        """
        columns = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in columns:
                return False
        return True
