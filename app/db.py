"""
db.py interfaces with an in-memory SQLite database using SQLAlchemy
I chose to use SQLAlchemy with Marshmallow since it is very good at
enforcing sanitized inputs and marshalling on serialization and
deserialization.
"""

import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import table, column, select, asc

from logger import logger

engine = sa.create_engine("sqlite:///:memory:")
session = scoped_session(sessionmaker(bind=engine))


def insert_user(user):
    """
    Method for interfacing with web services
  
    Parameters: 
    user (User): The user object to add to the database
  
    Returns:
    None on success. On failure, logs error output
    """

    try:
        session.add(user)
        session.commit()
    except Exception as e:
        logger.error(e)


def get_youngest_five():
    """
    Method for capturing five youngest users from our running SQLLite session
  
    Parameters:
    None, queries session object
  
    Returns:
    juser_list: On success, returns five youngest users sorted by name.
    On failure, logs error output
    """

    try:
        from models import User

        users = session.query(User).order_by(asc(User.age)).limit(5)
        user_list = []
        for user in users:
            user_list.append(user)

        return sorted(user_list, key=lambda u: u.name)
    except Exception as e:
        logger.error(e)
