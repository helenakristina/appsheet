"""
models.py is stores our SQLAlchemy model for sanitizing/validation
of inputs prior to inserting into database.
If the phone number is not valid US number, the User object will not
be created.
"""
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import PhoneNumberType
from sqlalchemy.orm import validates

from db import engine
from errors import NonUSPhoneNumberException
from logger import logger

Base = declarative_base()


class User(Base):
    """
    Class for generating valid user and ensuring types are correct
  
    Parameters: 
    id (integer): The id of the user
    name (string): The name of the user
    age (integer): Current age
    number(string): String representation of a US phone number
    photo(string): The URL location of the photo
    bio(string): Text describing the user
    Returns:
    User object
    """

    __tablename__ = "user"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    age = sa.Column(sa.Integer)
    number = sa.Column(PhoneNumberType())
    photo = sa.Column(sa.String)
    bio = sa.Column(sa.String)

    @validates("number")
    def validate_phone(self, key, number):
        if not number:
            raise NonUSPhoneNumberException("Missing Phone Number")
        number = "".join(c for c in number if c.isdigit())
        if len(number) != 10:
            raise NonUSPhoneNumberException(f"Invalid phone length {number}")
        return number

    def __repr__(self):
        return f"<User(name={self.name!r} age={self.age})>"


Base.metadata.create_all(engine)
